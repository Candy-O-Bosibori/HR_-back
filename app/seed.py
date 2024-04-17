from random import choice as rc

from app import app
from models import db, Employee , Review

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Employee.query.delete()


        print("Seeding powers...")
        employees = []

        db.session.add_all(employees)
        db.session.commit()

    



