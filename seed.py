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
            Employee(name="Olivia Martinez", email="olivia@gmail.com", password=bcrypt.generate_password_hash("olivia.123!").decode('utf-8'), department="Marketing", role="admin", image="https://plus.unsplash.com/premium_photo-1723568425978-81ef0ab51252?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZmVtYWxlJTIwcHJvZmlsZSUyMHBpY3R1cmVzfGVufDB8fDB8fHww"),
            Employee(name="Noah Carter", email="noah@gmail.com", password=bcrypt.generate_password_hash("noah.123!").decode('utf-8'), department="Operations", role="employee", image="https://plus.unsplash.com/premium_photo-1669703777663-a45e924bcda0?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8bWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlc3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Emma Hughes", email="emma@gmail.com", password=bcrypt.generate_password_hash("emma.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.unsplash.com/photo-1549351236-caca0f174515?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8ZmVtYWxlJTIwcHJvZmlsZSUyMHBpY3R1cmVzfGVufDB8fDB8fHww"),
            Employee(name="Mason Rivera", email="mason@gmail.com", password=bcrypt.generate_password_hash("mason.123!").decode('utf-8'), department="Administrative", role="employee", image="https://images.unsplash.com/photo-1658766801737-2f1e4e9a51a1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlc3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Ava Collins", email="ava@gmail.com", password=bcrypt.generate_password_hash("ava.123!").decode('utf-8'), department="Sales", role="admin", image="https://images.unsplash.com/photo-1617729819134-13c79630d2db?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8ZmVtYWxlJTIwcHJvZmlsZSUyMHBpY3R1cmVzfGVufDB8fDB8fHww"),
            Employee(name="Ethan Reed", email="ethan@gmail.com", password=bcrypt.generate_password_hash("ethan.123!").decode('utf-8'), department="Operations", role="employee", image="https://unsplash.com/photos/man-in-white-crew-neck-t-shirt-a6PMA5JEmWE"),
            Employee(name="Sophia Brooks", email="sophia@gmail.com", password=bcrypt.generate_password_hash("sophia.123!").decode('utf-8'), department="Marketing", role="admin", image="https://images.unsplash.com/photo-1618593167496-24fed8abacd3?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8ZmVtYWxlJTIwcHJvZmlsZSUyMHBpY3R1cmVzfGVufDB8fDB8fHww"),
            Employee(name="Logan Morgan", email="logan@gmail.com", password=bcrypt.generate_password_hash("logan.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.unsplash.com/photo-1717241325274-8a5d10592f2a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8bWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlc3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Isabella Perry", email="isabella@gmail.com", password=bcrypt.generate_password_hash("isabella.123!").decode('utf-8'), department="Administrative", role="admin", image="https://images.unsplash.com/photo-1605515223642-fd67abd879ab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGZlbWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlc3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="James Scott", email="james@gmail.com", password=bcrypt.generate_password_hash("james.123!").decode('utf-8'), department="Sales", role="employee", image="https://images.unsplash.com/photo-1714331251780-db56109a9887?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fG1hbGUlMjBwcm9maWxlJTIwcGljdHVyZXN8ZW58MHx8MHx8fDA%3D"),
            Employee(name="Mia Sanders", email="mia@gmail.com", password=bcrypt.generate_password_hash("mia.123!").decode('utf-8'), department="Operations", role="employee", image="https://images.unsplash.com/photo-1612307770126-f318cb35b542?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjB8fGZlbWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlc3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Benjamin Price", email="benjamin@gmail.com", password=bcrypt.generate_password_hash("benjamin.123!").decode('utf-8'), department="Marketing", role="admin", image="https://images.unsplash.com/photo-1590403461695-d1627462bb0c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjJ8fG1hbGUlMjBwcm9maWxlJTIwcGljdHVyZXN8ZW58MHx8MHx8fDA%3D"),
            Employee(name="Charlotte Foster", email="charlotte@gmail.com", password=bcrypt.generate_password_hash("charlotte.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.unsplash.com/photo-1557855765-c61eaa53c3ee?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjR8fGZlbWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlc3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Alexander Bennett", email="alexander@gmail.com", password=bcrypt.generate_password_hash("alexander.123!").decode('utf-8'), department="Administrative", role="employee", image="https://images.unsplash.com/photo-1557855765-c61eaa53c3ee?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjR8fGZlbWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlc3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Amelia Howard", email="amelia@gmail.com", password=bcrypt.generate_password_hash("amelia.123!").decode('utf-8'), department="Sales", role="admin", image="https://images.unsplash.com/photo-1557855765-c61eaa53c3ee?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjR8fGZlbWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlc3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Daniel James", email="daniel@gmail.com", password=bcrypt.generate_password_hash("daniel.123!").decode('utf-8'), department="Operations", role="employee", image="https://plus.unsplash.com/premium_photo-1664874603108-2c248e432f8f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjF8fG1hbGUlMjBwcm9maWxlJTIwcGljdHVyZXMlMjBibGFja3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Harper Bryant", email="harper@gmail.com", password=bcrypt.generate_password_hash("harper.123!").decode('utf-8'), department="Marketing", role="admin", image="https://images.unsplash.com/photo-1650050594038-55b4c4a86cc2?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8ZmVtYWxlJTIwcHJvZmlsZSUyMHBpY3R1cmVzJTIwYmxhY2t8ZW58MHx8MHx8fDA%3D"),
            Employee(name="Matthew Kelly", email="matthew@gmail.com", password=bcrypt.generate_password_hash("matthew.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.unsplash.com/photo-1625999984550-ef318c3a4648?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzJ8fG1hbGUlMjBwcm9maWxlJTIwcGljdHVyZXMlMjBibGFja3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Ella Cooper", email="ella@gmail.com", password=bcrypt.generate_password_hash("ella.123!").decode('utf-8'), department="Administrative", role="employee", image="https://images.unsplash.com/photo-1645092708550-2632c574bbfd?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGZlbWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlcyUyMGJsYWNrfGVufDB8fDB8fHww"),
            Employee(name="Joseph Ward", email="joseph@gmail.com", password=bcrypt.generate_password_hash("joseph.123!").decode('utf-8'), department="Sales", role="employee", image="https://images.unsplash.com/photo-1625708203905-ca6c5fcd0878?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDR8fG1hbGUlMjBwcm9maWxlJTIwcGljdHVyZXMlMjBibGFja3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Abigail Brooks", email="abigail@gmail.com", password=bcrypt.generate_password_hash("abigail.123!").decode('utf-8'), department="Operations", role="employee", image="https://plus.unsplash.com/premium_photo-1734603747105-ee6cfcf5d4b8?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjV8fGZlbWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlcyUyMGJsYWNrfGVufDB8fDB8fHww"),
            Employee(name="Samuel Ward", email="samuel@gmail.com", password=bcrypt.generate_password_hash("samuel.123!").decode('utf-8'), department="Marketing", role="admin", image="https://images.unsplash.com/photo-1625708203905-ca6c5fcd0878?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDR8fG1hbGUlMjBwcm9maWxlJTIwcGljdHVyZXMlMjBibGFja3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Emily Reed", email="emily@gmail.com", password=bcrypt.generate_password_hash("emily.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.unsplash.com/photo-1588479843425-2f1c68899617?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mjh8fGZlbWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlcyUyMGJsYWNrfGVufDB8fDB8fHww"),
            Employee(name="David Hughes", email="david@gmail.com", password=bcrypt.generate_password_hash("david.123!").decode('utf-8'), department="Administrative", role="employee", image="https://images.unsplash.com/photo-1630574320404-a7cdb7e5cab2?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTJ8fG1hbGUlMjBwcm9maWxlJTIwcGljdHVyZXMlMjBibGFja3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Elizabeth Foster", email="elizabeth@gmail.com", password=bcrypt.generate_password_hash("elizabeth.123!").decode('utf-8'), department="Sales", role="admin", image="https://images.unsplash.com/photo-1675469675830-11d9a6099ef4?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDB8fGZlbWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlcyUyMGJsYWNrfGVufDB8fDB8fHww"),
            Employee(name="Andrew Diaz", email="andrew@gmail.com", password=bcrypt.generate_password_hash("andrew.123!").decode('utf-8'), department="Operations", role="employee", image="https://images.unsplash.com/photo-1688990983011-38a71f213ec3?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTh8fG1hbGUlMjBwcm9maWxlJTIwcGljdHVyZXMlMjBibGFja3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Grace Morgan", email="grace@gmail.com", password=bcrypt.generate_password_hash("grace.123!").decode('utf-8'), department="Marketing", role="admin", image="https://plus.unsplash.com/premium_photo-1690820317063-d06300734a8b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDl8fGZlbWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlcyUyMGJsYWNrfGVufDB8fDB8fHww"),
            Employee(name="Christopher Bailey", email="christopher@gmail.com", password=bcrypt.generate_password_hash("christopher.123!").decode('utf-8'), department="Accounting", role="employee", image="https://images.unsplash.com/photo-1688990983011-38a71f213ec3?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTh8fG1hbGUlMjBwcm9maWxlJTIwcGljdHVyZXMlMjBibGFja3xlbnwwfHwwfHx8MA%3D%3D"),
            Employee(name="Victoria Hughes", email="victoria@gmail.com", password=bcrypt.generate_password_hash("victoria.123!").decode('utf-8'), department="Administrative", role="employee", image="https://plus.unsplash.com/premium_photo-1700932723489-dcbfd3e5db1f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTN8fGZlbWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlcyUyMGJsYWNrfGVufDB8fDB8fHww"),
            Employee(name="Nathaniel Brooks", email="nathaniel@gmail.com", password=bcrypt.generate_password_hash("nathaniel.123!").decode('utf-8'), department="Sales", role="employee", image="https://plus.unsplash.com/premium_photo-1692439050899-52203d012069?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),

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