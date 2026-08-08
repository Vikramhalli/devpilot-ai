from fastapi import FastAPI

app = FastAPI(
    title="DevPilot AI API",
    description="Backend API for DevPilot AI",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "message": "Welcome to DevPilot AI 🚀"
    }