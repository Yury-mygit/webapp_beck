from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from peewee import DoesNotExist
from typing import List
from models.db_model import Employee
from faker import Faker

router = APIRouter(tags=["employee"])
fake = Faker()


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

class EmployeeModel_OUT(EmployeeModel):
    id: int

@router.get("/employees", response_model=List[EmployeeModel_OUT])
def read_employees():
    employees = Employee.select()

    return list(employees)

@router.post("/employees/")
def create_employee(employee: EmployeeModel):
    Employee.create(**employee.model_dump())
    return {'status':'ok'}

def create_random_employee():
    return EmployeeModel(
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

@router.post("/employees/fill")
def fill_employees():

    for _ in range(10):
        employee = create_random_employee()
        create_employee(employee)

    return JSONResponse(content={'status': "ok"})



@router.patch("/employees/{employee_id}", response_model=EmployeeModel_OUT)
def update_employee(employee_id: int, employee: EmployeeModel):
    try:
        employee_obj = Employee.get(Employee.id == employee_id)
        employee_obj.update(**employee.model_dump()).execute()
        return JSONResponse(content={'status': "updated"}, status_code=200)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Student not found")

