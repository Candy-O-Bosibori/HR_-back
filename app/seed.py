from random import choice as rc

from app import app
from models import db, Employee

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Employee.query.delete()


        print("Seeding powers...")
        powers = [

            Employee(name="Lindey Stroud", email="lindseystroud@gmail.com", password="lindsey123", department="Technology Department", role="emloyee"),
            Employee(name="John Doe", email="johndoe@gmail.com", password="johndoe123", department="Communications Department", role="emloyee"),
            Employee(name="Peter paker", email="peterpaker@gamil.com", password="peterpaker123", department="Research Department", role="emloyee"),
            

        ]



