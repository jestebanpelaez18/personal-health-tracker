from fastapi import FastAPI

app = FastAPI(
    title="Personal Health Tracker",
    description="AI-powered health analytics for hybrid athletes",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Personal Health Tracker API running"}