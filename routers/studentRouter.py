from fastapi import HTTPException
from pydantic import BaseModel
from peewee import DoesNotExist
from typing import List
from faker import Faker
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from models.db_model import Student

fake = Faker()

router = APIRouter(tags=["student"])


class StudentIn(BaseModel):
    first_name: str
    last_name: str
    parents_name: str
    age: int
    status: str
    session_transfer_rate: float
    percentage_of_absences: float
    contact_email: str
    contact_telephone: str
    allow_telegram_notification: bool
    telegram_id: int
    issue: str
    date_of_initial_diagnosis: str
    address: str
    found_us_through: str
    online: bool
    notes: str


class StudentOut(StudentIn):
    id: int


@router.get("/students", response_model=List[StudentOut])
def read_students():
    students = Student.select()
    # for student in students:
    #     student.date_of_initial_diagnosis = student.date_of_initial_diagnosis.isoformat()
    return list(students)


@router.post("/students/", response_model=StudentOut)
def create_student(student: StudentIn):
    student_obj = Student.create(**student.dict())
    return student_obj


@router.get("/students/{student_id}", response_model=StudentOut)
def read_student(student_id: int):
    try:
        student = Student.get(Student.id == student_id)
        student.date_of_initial_diagnosis = student.date_of_initial_diagnosis.isoformat()
        return student
    except:
        return JSONResponse(content={'status': "not found"}, status_code=404)


@router.patch("/students/{student_id}", response_model=StudentOut)
def update_student(student_id: int, student: StudentIn):
    try:
        student_obj = Student.get(Student.id == student_id)
        student_obj.update(**student.dict()).execute()
        return JSONResponse(content={'status': "updated"}, status_code=200)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Student not found")


def create_random_student() -> StudentIn:
    return StudentIn(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        parents_name=fake.name(),
        age=fake.random_int(min=5, max=20),
        status=fake.random_element(elements=('active', 'inactive')),
        session_transfer_rate=fake.random_number(digits=2),
        percentage_of_absences=fake.random_number(digits=2),
        contact_email=fake.email(),
        contact_telephone=fake.phone_number(),
        allow_telegram_notification=fake.boolean(),
        telegram_id=fake.random_int(),
        issue=fake.sentence(),
        date_of_initial_diagnosis=fake.date_time().isoformat(),
        address=fake.address(),
        found_us_through=fake.sentence(),
        online=fake.boolean(),
        notes=fake.text(),
    )


@router.post("/students/fill", response_model=List[StudentOut])
def fill_students():
    students = []
    for _ in range(20):
        student_in = create_random_student()
        student_out = create_student(student_in)
        students.append(student_out)
    return JSONResponse(content={'status': "ok"})

@router.delete("/students/{student_id}")
def delete_student(student_id: int):
    try:
        student = Student.get(Student.id == student_id)
        student.delete_instance()
        return {"message": "Student deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Student not found")

