from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from peewee import DoesNotExist
from typing import List
from models.db_model import Session, ServiceType
from faker import Faker

router = APIRouter(tags=["session"])
fake = Faker()


class SessionModel(BaseModel):

    startDateTime: str
    duration: int
    week_first_day: str
    online: bool
    paid: bool
    confirmed: bool
    student_id: int
    employee_id: int
    repeatable: bool
    notes: str
    office_id: int
    performed: bool
    serviceType: str
    status: str




class SessionModel_OUT(SessionModel):
    id: int


@router.get(
    "/sessions",
    response_model=List[SessionModel_OUT]
)
def read_sessions():
    sessions = Session.select()
    response = []
    for session in sessions:
        # print(session.serviceType)
        response.append(
            SessionModel_OUT(
                id=session.id,
                startDateTime=session.startDateTime,
                duration=session.duration,
                week_first_day=session.week_first_day,
                online=session.online,
                paid=session.paid,
                confirmed=session.confirmed,
                student_id=session.student_id.id,
                employee_id=session.employee_id.id,  # Use the ID directly
                repeatable=session.repeatable,
                notes=session.notes,
                office_id=session.office_id.id,  # Use the ID directly
                performed=session.performed,
                serviceType=session.serviceType,  # Use the integer value of the enum member
                status=session.status,
            )

        )
    return response

@router.get("/sessions/{session_id}", response_model=SessionModel_OUT)
def get_session_by_id(session_id: int):
    try:
        session = Session.get(Session.id == session_id)
        return SessionModel_OUT(
            id=session.id,
            startDateTime=session.startDateTime,
            duration=session.duration,
            week_first_day=session.week_first_day,
            online=session.online,
            paid=session.paid,
            confirmed=session.confirmed,
            student_id=session.student_id.id,
            employee_id=session.employee_id.id,
            repeatable=session.repeatable,
            notes=session.notes,
            office_id=session.office_id.id,
            performed=session.performed,
            serviceType=session.serviceType,
            status=session.status,
        )
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Session not found")


class SessionModelCreate(BaseModel):

    startDateTime: str
    duration: int
    week_first_day: str
    online: bool
    paid: bool
    confirmed: bool
    student_id: int
    employee_id: int
    repeatable: bool
    notes: str
    office_id: int
    performed: bool
    serviceType: int
    status: str

class SessionModelUpdate(BaseModel):
    id: int
    startDateTime: str
    duration: int
    week_first_day: str
    online: bool
    paid: bool
    confirmed: bool
    student_id: int
    employee_id: int
    repeatable: bool
    notes: str
    office_id: int
    performed: bool
    serviceType: int
    status: str

# CREATE
@router.put( "/sessions",     response_model=SessionModelUpdate
)
def create_session(session: SessionModelCreate):
    try:
        session_obj = Session.create(**session.model_dump())
        print(session_obj)  # contain an id of new record
        # return {'status': 'ok'}
        return JSONResponse(content={'status': "updated"}, status_code=200)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Session not found")

def create_random_session():
    # Fill with your random data generator logic
    pass


@router.post("/sessions/fill")
def fill_sessions():
    for _ in range(10):
        session = create_random_session()
        create_session(session)
    return JSONResponse(content={'status': "ok"})


# UPDATE
@router.patch("/sessions", response_model=SessionModelUpdate)
def update_session(session: SessionModelUpdate):
    try:
        # Verify the session exists
        session_obj = Session.get(Session.id == session.id)

        # Create a copy of the session dictionary without the 'id' field
        session_dict = {key: value for key, value in session.model_dump().items() if key != 'id'}

        # Update the session
        Session.update(**session_dict).where(Session.id == session.id).execute()

        return JSONResponse(content={'status': "updated"}, status_code=200)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Session not found")
