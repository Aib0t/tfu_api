from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    pass

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/files", StaticFiles(directory="/files"), name="files")

@app.get('/{folder_id}/{file_name}')
async def client(file_name:str,folder_id:int):

    if os.path.exists(f"/gamecdn/{folder_id}/{file_name}"):
        return FileResponse(f"/gamecdn/{folder_id}/{file_name}")
    else:
        print(f"Look like file {folder_id}/{file_name} doesn't exists!")
        return Response(status_code=404)

@app.get("/game/public/availablegames/")
def read_root():
    return JSONResponse({"lobbies":[{"name":"main","lobbyName":"main","lobbyUrl":"127.0.0.1"}]}) #"name":"main", {"lobbies": [{"lobbyUrl":"127.0.0.1"}]}

@app.put("/crashes/{uuid}")
def read_root(uuid: str):
    print(f"Client tried to submit a crash report. We don't care")
    return Response()

@app.get("/update/{player_platform}/{version}")
def read_root(player_platform:str,version: int):

    print(f"Got connection from {player_platform} {version}")
    data = open("patch.xml","r").read()

    if version == 102409: #bypass, since it stuck if there is a proper response
        return Response(status_code=404)
    else:
        return Response(data,media_type = "text/xml")

@app.get("/crossdomain.xml")
def read_root():
    data = open("crossdomain.xml","r").read()

    return Response(data,media_type = "text/xml")


