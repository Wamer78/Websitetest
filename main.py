from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid
import asyncio
import edge_tts

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/tts", response_class=FileResponse)
async def text_to_speech(text: str = Form(...), voice: str = Form("fr-FR-DeniseNeural")):
    filename = f"output_{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(filename)
    return FileResponse(filename, media_type="audio/mpeg", filename="voix.mp3")
