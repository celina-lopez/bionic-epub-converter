import os
import mistune
import uvicorn
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from services import bionic
from starlette.background import BackgroundTasks

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/favicon.ico", include_in_schema=False)
async def favicon(): return FileResponse('./static/favicon.ico')

templates = Jinja2Templates(directory="templates")

@app.get("/", include_in_schema=False)
async def index(request: Request):
    with open('README.md', 'r') as readme:
        readme_content = readme.read()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "readme": mistune.html(readme_content)
        })


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
  book_file_path = await bionic.convert(file)
  print(book_file_path)
  return FileResponse(
    book_file_path
  )
   

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', "8000")))