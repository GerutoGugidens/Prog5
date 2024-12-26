import requests
from datetime import date, timedelta
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Tuple
import threading
import time
import matplotlib.pyplot as plt


class Singleton(type):
    """
    Метакласс для реализации паттерна "Одиночка".
    Ограничивает создание более одного экземпляра класса.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Currency(metaclass=Singleton):
    """
    Класс для получения курсов валют с сайта ЦБ РФ.
    """

    def __init__(self):
        self.url = "https://www.cbr.ru/scripts/XML_daily.asp"
        self.date = date.today().strftime("%d/%m/%Y")
        self.lock = threading.Lock()
        self.last_request_time = None
        self.rate_limit_interval = 1  # По умолчанию 1 секунда
        self.__id_list = []
        self.__currencies_lst = []

    def get_currencies(self) -> List[Dict]:
        """
        Получение курсов валют по списку идентификаторов.
        :param currencies_ids_lst: список идентификаторов валют
        :return: список словарей с информацией о валюте
        """
        from xml.etree import ElementTree as ET
        if self.is_rate_limit_exceeded():
            return []

        response = requests.get(self.url, params={"date_req": self.date})
        rates = []
        if response.status_code == 200:
            root = ET.fromstring(response.content.decode("windows-1251"))
            for child in root.findall("Valute"):
                char_code = child.find("CharCode").text
                name = child.find("Name").text
                value = child.find("Value").text.split(',')
                nominal = int(child.find("Nominal").text)
                if char_code in self.__id_list:
                    rates.append({
                        char_code: (
                            name,
                            f"{(float(f'{value[0]}.{value[1]}') / nominal)}".replace('.', ','))
                    })
        self.update_last_request_time()
        self.__currencies_lst = rates
        return rates

    def is_rate_limit_exceeded(self) -> bool:
        """
        Проверка, не превышен ли лимит запросов.
        :return: True, если лимит превышен, иначе False
        """
        current_time = time.time()
        if self.last_request_time is None:
            return False
        elapsed_time = current_time - self.last_request_time
        return elapsed_time < self.rate_limit_interval

    def update_last_request_time(self):
        """
        Обновление времени последнего запроса.
        """
        self.last_request_time = time.time()

    def plot_currencies(self):
        """
        Отображение графиков курсов валют.
        """
        rates = self.__currencies_lst if self.__currencies_lst is not None else self.get_currencies()
        if not rates:
            return False
        fig, ax = plt.subplots()
        currencies = []
        names, values = [], []
        for rate in rates:
            x = tuple(rate.values())[0]
            names.append(list(rate.keys())[0])
            values.append(float(x[1].replace(',', '.')))
        ax.bar(names, values)
        ax.set_title("Курсы валют")
        plt.savefig("currencies.jpg")
        plt.close(fig)
        return True

    def set_rate_limit_interval(self, interval: float):
        """
        Установка интервала лимита запросов.
        :param interval: интервал в секундах
        """
        self.rate_limit_interval = interval

    def set_valutes(self, valutes):
        """
        Задаёт валюты.
        :param valutes: список идентификаторов валют
        """
        self.__id_list = valutes

    def __del__(self):
        """
        Деструктор класса.
        """
        del self.url
        del self.date
        del self.lock
        del self.last_request_time
        del self.rate_limit_interval
        del self.__id_list
        del self.__currencies_lst

# currency = Currency()
# currency.set_valutes(["GBP", "KZT", "TRY", "USD"])
# print(currency.get_currencies())
# currency.plot_currencies()
