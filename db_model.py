import datetime
from peewee import *

# Create a PostgreSQL database connection
db = PostgresqlDatabase('users', user='postgres', password='321', host='localhost', port=5400)
d = datetime.datetime(2022, 12, 25, 17, 23, 22)


# Create a BaseModel representing a table in the database
class BaseModel(Model):
    class Meta:
        database = db


# Create a current model
class User(BaseModel):
    name = CharField()
    age = IntegerField()
    gender = CharField()
    created_date = DateTimeField(default=d)


class Rights(BaseModel):
    right = CharField(max_length=3)


class UserRights(BaseModel):
    user = ForeignKeyField(User, backref='rights')
    right = ForeignKeyField(Rights, backref='users')


class Student(BaseModel):
    id = AutoField()
    first_name = CharField()
    last_name = CharField()
    parents_name = CharField()
    age = IntegerField()
    status = CharField()
    session_transfer_rate = FloatField()
    percentage_of_absences = FloatField()
    contact_email = CharField()
    contact_telephone = CharField()
    allow_telegram_notification = BooleanField()
    telegram_id = BigIntegerField()
    issue = TextField()
    date_of_initial_diagnosis = DateTimeField()
    address = TextField()
    found_us_through = TextField()
    online = BooleanField()
    notes = TextField()


# Create table if it does not exist
Student.create_table(fail_silently=True)

# Create tables if they do not exist
User.create_table(fail_silently=True)
Rights.create_table(fail_silently=True)
UserRights.create_table(fail_silently=True)
