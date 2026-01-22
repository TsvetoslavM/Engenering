from datetime import datetime
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

app = FastAPI(title="File Storage API", version="1.0.0")

STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)


def get_file_count() -> int:
    return len([f for f in STORAGE_DIR.iterdir() if f.is_file()])


files_stored_counter = get_file_count()


@app.get("/")
async def root():
    return {
        "message": "File Storage API",
        "endpoints": [
            "GET /files/{filename}",
            "POST /files",
            "GET /files",
            "GET /health",
            "GET /metrics",
        ],
    }


@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = STORAGE_DIR / filename

    if not file_path.resolve().is_relative_to(STORAGE_DIR.resolve()):
        raise HTTPException(status_code=400, detail="Invalid filename")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )


@app.post("/files")
async def store_file(file: UploadFile = File(...)):
    filename = os.path.basename(file.filename or "")
    if not filename or filename in (".", ".."):
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_path = STORAGE_DIR / filename
    content = await file.read()

    file_exists = file_path.exists()
    try:
        with open(file_path, "wb") as f:
            f.write(content)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to store file: {str(e)}")

    global files_stored_counter
    if not file_exists:
        files_stored_counter += 1

    return {
        "message": "File stored successfully",
        "filename": filename,
        "size": len(content),
        "content_type": file.content_type,
    }


@app.get("/files")
async def list_files():
    files = [f.name for f in STORAGE_DIR.iterdir() if f.is_file()]
    return {"files": files, "count": len(files)}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "File Storage API",
    }


@app.get("/metrics")
async def metrics():
    files = [f for f in STORAGE_DIR.iterdir() if f.is_file()]
    total_size = sum(f.stat().st_size for f in files)

    return {
        "files_stored_total": files_stored_counter,
        "files_current": len(files),
        "total_storage_bytes": total_size,
        "total_storage_mb": round(total_size / (1024 * 1024), 2),
        "timestamp": datetime.utcnow().isoformat(),
    }
