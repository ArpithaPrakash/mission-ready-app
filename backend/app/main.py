from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.routes import conops

app = FastAPI(title="Mission Ready In 20 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
UPLOAD_ROOT = Path("uploaded_conops")
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

DRAW_OUTPUT_ROOT = Path("generated_draws")
DRAW_OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_ROOT)), name="uploads")
app.mount("/generated_draws", StaticFiles(directory=str(DRAW_OUTPUT_ROOT)), name="generated_draws")

# Include routers
app.include_router(conops.router)
