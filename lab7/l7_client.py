import asyncio
import websockets

async def receive_updates():
    uri = "ws://127.0.0.1:8000/ws/client_123"
    async with websockets.connect(uri) as websocket:
        print("Connected to the server. Waiting for updates...")
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

asyncio.run(receive_updates())