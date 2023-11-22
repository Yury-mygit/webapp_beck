import random
from models.db_model import Payment, Employee, Session, ServiceType, Status, Student, Office, PaymentStatus, SubscriptionType


def create_payment(id):
    return Payment(
        student_id=id,
        # status=random.choice(list(PaymentStatus)).value,
        status='new',
        subscription_type=random.choice(list(SubscriptionType)).value
    )
