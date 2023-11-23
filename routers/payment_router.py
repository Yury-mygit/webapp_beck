from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from peewee import DoesNotExist, fn
from models.db_model import Payment

router = APIRouter(tags=["payment"])

class PaymentIn(BaseModel):
    student_id: int
    subscription_type: int

class PaymentOut(PaymentIn):
    id: int
    status: str

# Create new payment
@router.put("/payments", response_model=PaymentOut)
def create_payment(payment: PaymentIn):
    # print(payment)
    payment_data = payment.model_dump()
    payment_data['status'] = 'new'
    payment_obj = Payment.create(**payment_data)
    return PaymentOut(**payment_obj.__data__)

#return all payments
@router.get("/payments", response_model=List[PaymentOut])
def read_payments(limit: int = 20, offset: int = 0):
    payments = Payment.select().offset(offset).limit(limit)
    return [PaymentOut(**payment.__data__) for payment in payments]


@router.get("/payments/{student_id}", response_model=List[PaymentOut])
def read_payments_by_student(student_id: int):
    payments = Payment.select().where(Payment.student_id == student_id)
    return [PaymentOut(**payment.__data__) for payment in payments]

@router.get("/payments/payment/{payment_id}", response_model=PaymentOut)
def read_payment_by_id(payment_id: int):
    try:
        payment = Payment.get(Payment.id == payment_id)
        return PaymentOut(**payment.__data__)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Payment not found")


@router.post("/payments/use/{payment_id}")
def use_payment(payment_id: int):
    # Logic to use the payment goes here
    pass
