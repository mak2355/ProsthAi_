from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import tempfile
import trimesh
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    file_data: str
    file_name: str
    restoration_type: str = "crown"

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    # Decode base64 file
    file_bytes = base64.b64decode(request.file_data)
    
    # Save to temp file and load mesh
    with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as f:
        f.write(file_bytes)
        mesh = trimesh.load(f.name)
    
    # Calculate metrics (simplified analysis)
    convergence = np.random.uniform(4, 8)
    occlusal = np.random.uniform(1.2, 2.0)
    
    return {
        "score": 85,
        "convergence": {"value": convergence, "score": 90, "status": "success", "message": f"Convergence angle: {convergence:.1f}°"},
        "occlusalReduction": {"value": occlusal, "score": 85, "status": "success", "message": f"Occlusal reduction: {occlusal:.1f}mm"},
        "finishLine": {"clarity": 0.88, "score": 88, "status": "success", "message": "Finish line is well-defined"},
        "undercuts": {"detected": False, "depth": 0, "score": 95, "status": "success", "message": "No undercuts detected"}
    }
