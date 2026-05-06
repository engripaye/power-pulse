from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, location_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.setdefault(location_id, []).append(websocket)

    def disconnect(self, location_id: int, websocket: WebSocket) -> None:
        connections = self.active_connections.get(location_id, [])
        if websocket in connections:
            connections.remove(websocket)

    async def broadcast_to_location(self, location_id: int, message: dict) -> None:
        for connection in self.active_connections.get(location_id, []):
            await connection.send_json(message)

