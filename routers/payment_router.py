from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from peewee import DoesNotExist, fn
from models.db_model import Payment

router = APIRouter(tags=["payment"])

class PaymentIn(BaseModel):
    student_id: int
    status: str
    subscription_type: int

class PaymentOut(PaymentIn):
    id: int

@router.post("/payments", response_model=PaymentOut)
def create_payment(payment: PaymentIn):
    payment_obj = Payment.create(**payment.dict())
    return payment_obj

@router.get("/payments", response_model=List[PaymentOut])
def read_payments():
    payments = Payment.select()
    return [PaymentOut(**payment.__data__) for payment in payments]


@router.get("/payments/{student_id}", response_model=List[PaymentOut])
def read_payments_by_student(student_id: int):
    payments = Payment.select().where(Payment.student_id == student_id)
    return list(payments)

@router.get("/payments/payment/{payment_id}", response_model=PaymentOut)
def read_payment_by_id(payment_id: int):
    try:
        payment = Payment.get(Payment.id == payment_id)
        return payment
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Payment not found")

@router.post("/payments/use/{payment_id}")
def use_payment(payment_id: int):
    # Logic to use the payment goes here
    pass
