from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from pydantic import BaseModel
from peewee import DoesNotExist
from models.db_model import Payment
from auth.login import get_current_user
from fastapi.security import OAuth2PasswordBearer
import jwt
router = APIRouter(tags=["payment"])

class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

class PaymentIn(BaseModel):
    student_id: int
    subscription_type: int


class PaymentOut(PaymentIn):
    id: int
    status: str

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# return all payments
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/refresh")

def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(str)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Replace this with actual user lookup in your database
        user = UserOut(username=username, id=1, is_active=True)
        return user
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/paymentsss", response_model=List[PaymentOut])
# def read_payments(user: UserOut = Depends(get_current_user), limit: int = 20, offset: int = 0):
def read_payments(limit: int = 20, offset: int = 0):
    payments = Payment.select().offset(offset).limit(limit)
    return [PaymentOut(**payment.__data__) for payment in payments]



# Create new payment
@router.put("/payments", response_model=PaymentOut)
def create_payment(payment: PaymentIn):
    # print(payment)
    payment_data = payment.model_dump()
    payment_data['status'] = 'new'
    payment_obj = Payment.create(**payment_data)
    return PaymentOut(**payment_obj.__data__)


# return all payments for student
@router.get("/payments/{student_id}", response_model=List[PaymentOut])
def read_payments_by_student(student_id: int):
    payments = Payment.select().where(Payment.student_id == student_id)
    return [PaymentOut(**payment.__data__) for payment in payments]


# return payment by id
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
