import webbrowser
from fastapi import FastAPI
from routes.tasks import router as tasks_router
import uvicorn
import threading

app = FastAPI()

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

from auth.jwt import app as auth_app
app.mount("/", auth_app)

def open_browser():
    webbrowser.open("http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    threading.Timer(1.25, open_browser).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)