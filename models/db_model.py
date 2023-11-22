from peewee import *
from enum import Enum
import datetime

db = PostgresqlDatabase('user', user='postgres', password='321', host='localhost', port=5400)


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ServiceType(Enum):
    TYPE1 = "type1"
    TYPE2 = "type2"
    # Add more service types as needed


class Student(BaseModel):
    id = AutoField()
    first_name = CharField()
    last_name = CharField()
    parents_name = CharField()
    age = IntegerField()
    status = CharField(choices=[(status, status.value) for status in Status])
    session_transfer_rate = FloatField()
    percentage_of_absences = FloatField()
    contact_email = CharField()
    contact_telephone = CharField()
    allow_telegram_notification = BooleanField()
    telegram_id = BigIntegerField()
    issue = TextField()
    date_of_initial_diagnosis = CharField()
    address = TextField()
    found_us_through = TextField()
    online = BooleanField()
    notes = TextField()


class Employee(BaseModel):
    id = AutoField()
    status = CharField(choices=[(status, status.value) for status in Status])
    position = CharField()
    profession = CharField()
    first_name = CharField()
    last_name = CharField()
    contact_email = CharField()
    contact_telephone = CharField()
    telegram_id = IntegerField()
    online = BooleanField()
    offline = BooleanField()
    qualifications = TextField(null=True)
    experience_years = IntegerField(null=True)


class Office(BaseModel):
    id = AutoField()
    address = TextField()


class PaymentStatus(Enum):
    NEW = "new"
    ACTIVE = "active"
    SPENT = "spent"


class SubscriptionType(Enum):
    ONE_LESSON = 1
    FOUR_LESSONS = 4
    EIGHT_LESSONS = 8


class Payment(BaseModel):
    id = AutoField()
    student_id = ForeignKeyField(Student, backref='payments')
    status = CharField(choices=[(status, status.value) for status in PaymentStatus])
    subscription_type = IntegerField(choices=[(subscription, subscription.value) for subscription in SubscriptionType])


class Session(BaseModel):
    id = AutoField()
    startDateTime = CharField()
    duration = IntegerField()
    week_first_day = CharField()
    online = BooleanField()
    paid = BooleanField()
    confirmed = BooleanField()
    student_id = ForeignKeyField(Student, backref='sessions')
    employee_id = ForeignKeyField(Employee, backref='sessions')
    repeatable = BooleanField()
    notes = TextField()
    office_id = ForeignKeyField(Office, backref='sessions')
    performed = BooleanField()
    serviceType = CharField(choices=[(service, service.value) for service in ServiceType])
    status = CharField(choices=[(status, status.value) for status in Status])
    payment_id = ForeignKeyField(Payment, backref='sessions', null=True)


try:
    Student.create_table()
    Employee.create_table()
    Office.create_table()
    Payment.create_table()
    Session.create_table()
except Exception as e:
    print(e)
