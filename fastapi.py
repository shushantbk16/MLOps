
import os
from dotenv import load_dotenv
import threading
import queue
import asyncio
from resume_parser import generate_followup_question
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions
from deepgram.core.events import EventType

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

MOCK_RESUME = "Candidate is a Python Developer with 3 years of experience in FastAPI and AI."
api_key = os.getenv("DEEPGRAM_API_KEY")
if not api_key:
    print("error in api_key")
@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    audio_queue = queue.Queue()
    def deepgram_worker():
        try:
            deepgram = DeepgramClient(api_key)
            options = LiveOptions(
                model="nova-2",
                language="en-US",
                smart_format=True,
                encoding="linear16",
                channels=1,
                sample_rate=16000,
            )
            with deepgram.listen.live.v("1").connect(options) as dg_connection:
                def on_message(self, result, **kwargs):
                    sentence = result.channel.alternatives[0].transcript
                    if len(sentence) > 0:
                    print(sentence)
                dg_connection.on(EventType.transcript, on_message)
            while True:
                data = audio_queue.get()
                if data is None:
                    break
                dg_connection.send(data)
        except Exception as e:
            print(f"Deepgram error: {e}")

    worker_thread = threading.Thread(target=deepgram_worker)
    worker_thread.start()
    try:
        while True:
            audio_from_tab = await websocket.receive_bytes()
            audio_queue.put(audio_from_tab)
    finally:
        audio_queue.put(None)
        worker_thread.join()
   
@app.get("/")
def check():
    return "hello"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)