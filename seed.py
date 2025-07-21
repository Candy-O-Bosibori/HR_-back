from flask_bcrypt import Bcrypt
from app import app
from models import db, Employee, Review, Leave
from sqlalchemy import text
import random
from datetime import date, timedelta

bcrypt = Bcrypt(app)

def execute_sql(sql):
    """Execute raw SQL."""
    with db.engine.begin() as connection:
        connection.execute(text(sql))


if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Review.query.delete()
        Leave.query.delete()
        Employee.query.delete()
        db.session.commit()

        print("Seeding employees...")
        # employees = [
        #     Employee(name="Alex Mambo", email="alex@gmail.com", password=bcrypt.generate_password_hash("Alex123!").decode('utf-8'), department='Administrative', role='admin', image='https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600'),
        #     Employee(name="Hamdi Adan", email="hamdi@gmail.com", password=bcrypt.generate_password_hash("Hamdi123!").decode('utf-8'), department='HR', role='employee', image='https://images.pexels.com/photos/764529/pexels-photo-764529.jpeg?auto=compress&cs=tinysrgb&w=600'),
        #     Employee(name="Anna Kioko", email="anna@gmail.com", password=bcrypt.generate_password_hash("Anna123!").decode('utf-8'), department='IT', role='employee', image='https://images.pexels.com/photos/11506216/pexels-photo-11506216.jpeg?auto=compress&cs=tinysrgb&w=600'),
        #     Employee(name="Sharon Mwende", email="sharon@gmail.com", password=bcrypt.generate_password_hash("Sharon123!").decode('utf-8'), department='Finance', role='employee', image='https://images.pexels.com/photos/20434986/pexels-photo-20434986/free-photo-of-jasmine-bajwa-model-shoot.jpeg?auto=compress&cs=tinysrgb&w=600'),
        #     Employee(name="Candy Bosibori", email="candy@gmail.com", password=bcrypt.generate_password_hash("Candy123!").decode('utf-8'), department='Operations', role='employee', image='https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600')
        # ]

        employees = [
            # Auto-generated employee instances

            Employee(name="Liam Bennett", email="liam@gmail.com", password=bcrypt.generate_password_hash("liam.123!").decode('utf-8'), department="Sales", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Olivia Martinez", email="olivia@gmail.com", password=bcrypt.generate_password_hash("olivia.123!").decode('utf-8'), department="Marketing", role="admin", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Noah Carter", email="noah@gmail.com", password=bcrypt.generate_password_hash("noah.123!").decode('utf-8'), department="Operations", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Emma Hughes", email="emma@gmail.com", password=bcrypt.generate_password_hash("emma.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Mason Rivera", email="mason@gmail.com", password=bcrypt.generate_password_hash("mason.123!").decode('utf-8'), department="Administrative", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Ava Collins", email="ava@gmail.com", password=bcrypt.generate_password_hash("ava.123!").decode('utf-8'), department="Sales", role="admin", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Ethan Reed", email="ethan@gmail.com", password=bcrypt.generate_password_hash("ethan.123!").decode('utf-8'), department="Operations", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Sophia Brooks", email="sophia@gmail.com", password=bcrypt.generate_password_hash("sophia.123!").decode('utf-8'), department="Marketing", role="admin", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Logan Morgan", email="logan@gmail.com", password=bcrypt.generate_password_hash("logan.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Isabella Perry", email="isabella@gmail.com", password=bcrypt.generate_password_hash("isabella.123!").decode('utf-8'), department="Administrative", role="admin", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="James Scott", email="james@gmail.com", password=bcrypt.generate_password_hash("james.123!").decode('utf-8'), department="Sales", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Mia Sanders", email="mia@gmail.com", password=bcrypt.generate_password_hash("mia.123!").decode('utf-8'), department="Operations", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Benjamin Price", email="benjamin@gmail.com", password=bcrypt.generate_password_hash("benjamin.123!").decode('utf-8'), department="Marketing", role="admin", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Charlotte Foster", email="charlotte@gmail.com", password=bcrypt.generate_password_hash("charlotte.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Alexander Bennett", email="alexander@gmail.com", password=bcrypt.generate_password_hash("alexander.123!").decode('utf-8'), department="Administrative", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Amelia Howard", email="amelia@gmail.com", password=bcrypt.generate_password_hash("amelia.123!").decode('utf-8'), department="Sales", role="admin", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Daniel James", email="daniel@gmail.com", password=bcrypt.generate_password_hash("daniel.123!").decode('utf-8'), department="Operations", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Harper Bryant", email="harper@gmail.com", password=bcrypt.generate_password_hash("harper.123!").decode('utf-8'), department="Marketing", role="admin", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Matthew Kelly", email="matthew@gmail.com", password=bcrypt.generate_password_hash("matthew.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Ella Cooper", email="ella@gmail.com", password=bcrypt.generate_password_hash("ella.123!").decode('utf-8'), department="Administrative", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Joseph Ward", email="joseph@gmail.com", password=bcrypt.generate_password_hash("joseph.123!").decode('utf-8'), department="Sales", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Abigail Brooks", email="abigail@gmail.com", password=bcrypt.generate_password_hash("abigail.123!").decode('utf-8'), department="Operations", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Samuel Ward", email="samuel@gmail.com", password=bcrypt.generate_password_hash("samuel.123!").decode('utf-8'), department="Marketing", role="admin", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Emily Reed", email="emily@gmail.com", password=bcrypt.generate_password_hash("emily.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="David Hughes", email="david@gmail.com", password=bcrypt.generate_password_hash("david.123!").decode('utf-8'), department="Administrative", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Elizabeth Foster", email="elizabeth@gmail.com", password=bcrypt.generate_password_hash("elizabeth.123!").decode('utf-8'), department="Sales", role="admin", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Andrew Diaz", email="andrew@gmail.com", password=bcrypt.generate_password_hash("andrew.123!").decode('utf-8'), department="Operations", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Grace Morgan", email="grace@gmail.com", password=bcrypt.generate_password_hash("grace.123!").decode('utf-8'), department="Marketing", role="admin", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Christopher Bailey", email="christopher@gmail.com", password=bcrypt.generate_password_hash("christopher.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Victoria Hughes", email="victoria@gmail.com", password=bcrypt.generate_password_hash("victoria.123!").decode('utf-8'), department="Administrative", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),
            Employee(name="Nathaniel Brooks", email="nathaniel@gmail.com", password=bcrypt.generate_password_hash("nathaniel.123!").decode('utf-8'), department="Sales", role="employee", image="https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600"),

        ]

        db.session.add_all(employees)
        db.session.commit()  

        print("Seeding reviews and leaves...")

        # Select 20% of employees (around 6)
        sample_employees = random.sample(employees, k=max(1, len(employees)//5))

        leave_types = ['sick', 'casual', 'vacation']
        leave_statuses = ['pending', 'approved', 'rejected']
        review_descriptions = [
            "Excellent work ethic and dedication.",
            "Needs improvement in communication skills.",
            "Outstanding teamwork and leadership.",
            "Punctual and reliable employee.",
            "Shows initiative and creativity.",
            "Could be more proactive in tasks."
        ]

        leaves = []
        reviews = []

        for emp in sample_employees:
            # Add 1-2 reviews per employee
            for _ in range(random.randint(1, 2)):
                desc = random.choice(review_descriptions)
                reviews.append(Review(description=desc, employee_id=emp.id))

            # Add 1 leave per employee with random valid data
            start = date.today() - timedelta(days=random.randint(30, 60))
            end = start + timedelta(days=random.randint(1, 10))
            leaves.append(Leave(
                leaveType=random.choice(leave_types),
                startDate=start,
                endDate=end,
                status=random.choice(leave_statuses),
                employee_id=emp.id
            ))

        db.session.add_all(reviews)
        db.session.add_all(leaves)
        db.session.commit()

        print("Done seeding!")