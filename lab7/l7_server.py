from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import requests
import threading
import time
from datetime import date
from xml.etree import ElementTree as ET


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CurrencyRates(metaclass=SingletonMeta):
    def __init__(self):
        self.url = "https://www.cbr.ru/scripts/XML_daily.asp"
        self.date = date.today().strftime("%d/%m/%Y")
        self.lock = threading.Lock()
        self.last_request_time = None
        self.rate_limit_interval = 1
        self.currency_ids = []
        self.cached_rates = []

    def get_currencies(self) -> List[Dict]:
        with self.lock:
            if self._is_rate_limited():
                return self.cached_rates

            response = requests.get(self.url, params={"date_req": self.date})
            if response.status_code != 200:
                return []

            root = ET.fromstring(response.content.decode("windows-1251"))
            rates = []
            for child in root.findall("Valute"):
                char_code = child.find("CharCode").text
                if char_code in self.currency_ids:
                    name = child.find("Name").text
                    value = float(child.find("Value").text.replace(',', '.'))
                    nominal = int(child.find("Nominal").text)
                    rates.append({"code": char_code, "name": name, "rate": value / nominal})

            self.cached_rates = rates
            self.last_request_time = time.time()
            return rates

    def set_currency_ids(self, ids: List[str]):
        self.currency_ids = ids

    def _is_rate_limited(self) -> bool:
        if self.last_request_time is None:
            return False
        return (time.time() - self.last_request_time) < self.rate_limit_interval


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)


app = FastAPI()
manager = ConnectionManager()
currency_rates = CurrencyRates()
currency_rates.set_currency_ids(["USD", "EUR", "GBP"])


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            rates = currency_rates.get_currencies()
            await manager.broadcast(f"Client {client_id}: {rates}")
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


def update_currency_rates():
    while True:
        currency_rates.get_currencies()
        time.sleep(60)


update_thread = threading.Thread(target=update_currency_rates, daemon=True)
update_thread.start()
