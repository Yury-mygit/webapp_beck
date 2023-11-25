from main import app
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost:3000",  # React
    "http://localhost:8000",  # Angular
    "http://localhost:8080",  # Vue.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

