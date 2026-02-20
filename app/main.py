from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

origins = [
    "http://localhost:3000", 
    "https://health-techfrontend-qnkz.vercel.app/" # Next.js dev server
]

app = FastAPI(
    title="PharmaGuard",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "PharmaGuard API running"}
