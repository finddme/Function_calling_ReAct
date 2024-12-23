import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
import asyncio
# from motor.motor_asyncio import AsyncIOMotorClient
import streamlit as st
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from graph.graph import Graph
from fastapi.responses import StreamingResponse
import io
from io import BytesIO
from PIL import Image
from utils.formats import UserInput
from pyngrok import conf, ngrok

class ConnectionManager:
    """Web socket connection manager."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

# uvicorn.run(fast_api_app, host="0.0.0.0", port=7808)
async def app(args):
    app=Graph(args).graph()
    
    # FastAPI
    fast_api_app = FastAPI(
        title="CHAT"
    )

    origins = ["*"]

    conn_mgr = ConnectionManager()

    fast_api_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @fast_api_app.get("/")
    def home():
        return {"message": "CHAT"}

    @fast_api_app.post("/chat")
    async def api(user_input: UserInput):
        nonlocal app
        user_input=user_input.user_input
        inputs = {"query": user_input}
        res= await app.ainvoke(inputs)
        if "image_generation" in res["action"]:
            image = Image.open(io.BytesIO(res["generate"][0]))
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            return StreamingResponse(img_byte_arr, media_type="image/png")
        else:
            result = {
                "output": res["generate"],
                "agent": res["action"],
                "observation":res["observation"],
                "log":res["log"]
            }
            return result

    conf.get_default().region = "eu"
    http_tunnel = ngrok.connect(7808) 
    tunnels = ngrok.get_tunnels() 
    for kk in tunnels: 
        print(kk)

    config = uvicorn.Config(fast_api_app, host="0.0.0.0", port=7808)
    server = uvicorn.Server(config)
    await asyncio.to_thread(server.run)



