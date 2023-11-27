
import random
from models.db_model import Payment, Employee, Session, ServiceType, Status, Student, Office, PaymentStatus, \
    SubscriptionType
from datetime import datetime, timedelta, time, date
from models.db_model import Student
from typing import List
from faker import Faker


import random

fake = Faker()

def create_payment(id):
    return Payment(
        student_id=id,
        # status=random.choice(list(PaymentStatus)).value,
        status='new',
        subscription_type=random.choice(list(SubscriptionType)).value
    )



class Session_item:
    def __init__(self, id=None, student_id=None, employee_ig=None, office_id=None ,first_name=None):
        self.id = id
        self.first_name = first_name
        self.day = None
        self.time = None
        self.student_id = student_id
        self.employee_id = employee_ig
        self.office_id = office_id


class Period:
    def __init__(self, start=None, end=None, session=None):
        today = datetime.today()
        self.start = start if start else today - timedelta(days=30)
        self.end = end if end else today + timedelta(days=60)
        self.session = session if session else Session_item(id=1, first_name='default_name')

        self.sessionList: List[Session] = []


    def add_session(self, session):
        self.sessionList.append(session)


    def find_session(self, s_day, s_time):
        for item in self.sessionList:
            # print(item.day == s_day)
            if item.day == s_day and item.time == s_time:
                return True
        return False


    def make_model(self, session:Session_item):

        day_of_week_number = session.day
        now = datetime.now()
        diff = day_of_week_number - now.weekday()
        target_date = now + timedelta(days=diff)

        print(target_date)
        pass
        session = Session(
            startDateTime= target_date,
            duration=40,
            week_first_day=now,
            online=random.choice([True, False]),
            paid=True,
            confirmed=random.choice([True, False]),
            student_id=session.student_id,
            employee_id=session.employee_id,
            repeatable=True,
            notes=fake.text(),
            office_id=session.office_id,
            performed=target_date < datetime.now(),
            serviceType=random.choice(list(ServiceType)),
            status=random.choice(list(Status)),
        )
        return session

    def create_session_list(self):
        # 1 step: query to database
        queryStu = Student.select()
        queryEmp = Employee.select()
        queryOfi = Office.select()

        # 2 step: make a list of sessions
        for stud in queryStu:
            for i in range(random.randint(2, 3)):
                session = Session_item(first_name=stud.first_name, student_id=stud.id)  # Create a new Session object
                self.add_session(session)


        empList = []
        for emp in queryEmp:
           empList.append(emp.id)

        ar = {}
        for sess in self.sessionList:
            if sess.student_id not in ar:
                employee = random.choice(empList)
                ar[sess.student_id] = employee
                sess.employee_id = employee
            else:
                 sess.employee_id = ar[sess.student_id]


        ofiList = []
        for ofi in queryOfi:
            ofiList.append(ofi.id)

        of = {}
        for sess in self.sessionList:
            if sess.student_id not in of:
                office = random.choice(ofiList)
                of[sess.office_id] = office
                sess.office_id = office
            else:
                sess.office_id = of[sess.office_id]


        self.sessionList = [setattr(session, 'id', i) or session for i, session in enumerate(self.sessionList, start=1)]


        for session in self.sessionList:

            for i in range(1000):

                day = random.randint(0, 6)  # Randomly choose a day of the week (0-6)
                hour = random.randint(8, 20)  # Randomly choose an hour between 8 a.m. and 8 p.m.
                session_time = time(hour=hour)

                # print('i=', i, '__',day, session_time)

                if not self.find_session(day, session_time):
                    session.day = day
                    session.time = session_time
                    break

                else:
                    continue


        listSes = [self.make_model(session) for session in self.sessionList]


        print(listSes)





