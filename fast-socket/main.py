from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


@app.get("/")
async def index(requst: Request):
    return templates.TemplateResponse("index.html", {"request": requst})

manager = ConnectionManager()


@app.get("/get_user")
async def users():
    return {"user": [str(ws.client.port) + " " for ws in manager.active_connections]}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # 메시지 수신
            # 클라이언트들에게 전송
            await manager.broadcast(f"{websocket.client.port}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
