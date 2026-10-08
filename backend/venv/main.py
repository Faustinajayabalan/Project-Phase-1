from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Neuro-Fuzzy Security Framework")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Neuro-Fuzzy Security Backend is running"
    }


@app.post("/upload-project")
async def upload_project(file: UploadFile = File(...)):
    upload_folder = Path("uploads")
    upload_folder.mkdir(exist_ok=True)

    file_path = upload_folder / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "message": "Project uploaded successfully",
        "filename": file.filename,
        "path": str(file_path)
    }