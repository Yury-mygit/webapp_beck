from datetime import datetime, timedelta, time
from models.db_model import Payment, Employee, Session, ServiceType, Status, Student, Office
from fastapi import APIRouter
from pydantic import BaseModel
from faker import Faker
import random

fake = Faker()
router = APIRouter(tags=["fake_data"])


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


class EmployeeModel(BaseModel):
    status: str
    position: str
    profession: str
    first_name: str
    last_name: str
    contact_email: str
    contact_telephone: str
    telegram_id: int
    online: bool
    offline: bool


def create_random_student():
    return Student(
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

def create_random_employee():
    return Employee(
        status=fake.random_element(elements=('active', 'inactive')),
        position=fake.random_element(elements=('massagist', 'speech therapist')),
        profession=fake.random_element(elements=('massagist', 'speech therapist')),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        contact_email=fake.email(),
        contact_telephone=fake.phone_number(),
        telegram_id=fake.random_int(),
        online=fake.boolean(),
        offline=fake.boolean(),
    )

def create_random_session(date, students, employees):
    # Select a random student and employee
    student = random.choice(students)
    employee = random.choice(employees)

    # Generate a random office_id that exists in your Office tabl
    # office_id = random.randint(1, Office.select().count())
    # Generate a random number of sessions (2 or 3)
    num_sessions = random.choice([2, 3])

    # Generate random start times for the sessions
    start_times = random.sample(range(10, 20), num_sessions)  # Hours from 10 to 19

    sessions = []
    for start_time in start_times:
        # Create a datetime object for the session start time
        startDateTime = datetime.combine(date, time(start_time, 0))

        # Create a new session
        session = Session(
            startDateTime=startDateTime,
            duration=40,
            week_first_day=date - timedelta(days=date.weekday()),
            online=random.choice([True, False]),
            paid=startDateTime < datetime.now(),
            confirmed=random.choice([True, False]),
            student_id=student.id,
            employee_id=employee.id,
            repeatable=random.choice([True, False]),
            notes=fake.text(),
            office_id=1,
            performed=startDateTime < datetime.now(),
            serviceType=random.choice(list(ServiceType)),
            status=random.choice(list(Status)),
        )
        sessions.append(session)

    return sessions

def create_random_office():
    return Office(
        address=fake.address(),
        # Add any other fields as needed
    )


@router.post("/filldb")
def fill_db():
    # Create 20 students and 5 employees
    students = [create_random_student() for _ in range(20)]
    for student in students:
        student.save()

    employees = [create_random_employee() for _ in range(5)]
    for employee in employees:
        employee.save()

    offices = [create_random_office() for _ in range(3)]
    for office in offices:
        office.save()

    # Create sessions for the past 10 days and the next 5 days
    for i in range(-10, 6):
        date = datetime.now().date() + timedelta(days=i)
        sessions = create_random_session(date, students, employees)
        for session in sessions:
            session.save()

    return {"detail": "Database filled with test data"}
