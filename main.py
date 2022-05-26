import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random
import mistune
from dotenv import load_dotenv
from services import converter
from starlette.background import BackgroundTasks

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/favicon.ico")
async def favicon(): return FileResponse('./static/favicon.ico')

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    with open('README.md', 'r') as readme:
        readme_content = readme.read()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "readme": mistune.html(readme_content)
        })


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
  file_name = f"files/{uploaded_file.filename}"
  file = converter.create_bionic_book(file_name)
  return FileResponse(
    file,
    background=BackgroundTask(converter.remove_file(file)),
  )
   

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', "8000")))