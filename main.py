from fastapi import FastAPI
from faker import Faker
from routers.studentRouter import router as student_router
from routers.employee_router import router as employee_router
from routers.session_router import router as session_router
from routers.fake_data import router as fake_router
from routers.payment_router import router as payment_router
from routers.login_router import router as login_router
from fastapi.middleware.cors import CORSMiddleware
fake = Faker()

tags_metadata = [
    {
        "name": "student",
        "description": "Students of the center",
    },
    {
        "name": "employee",
        "description": "Employees if center",
        "externalDocs": {
            "description": "forward to site",
            "url": "https://goldenspeak.ru/",
        },
    },
    {
        "name": "session",
        "description": "Sessions",
    },
    {
        "name": "fake_data",
        "description": "fake_data",
    },
    {
        "name": "payment",
        "description": "Payments api",
    },
    {
        "name": "login",
        "description": "Login api",
    },
]

app = FastAPI(
    title="My Super Project",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="2.5.0",
    openapi_tags=tags_metadata,
)


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



app.include_router(student_router)
app.include_router(employee_router)
app.include_router(session_router)
app.include_router(fake_router)
app.include_router(payment_router)
app.include_router(login_router)


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('PyCharm')
