from flask_bcrypt import Bcrypt
from app import app
from models import db, Employee, Review, Leave
from sqlalchemy import text

bcrypt = Bcrypt(app)

def execute_sql(sql):
    """Execute raw SQL."""
    with db.engine.begin() as connection:
        connection.execute(text(sql))


if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        execute_sql("TRUNCATE TABLE leaves, reviews, employees RESTART IDENTITY CASCADE")
        
        print("Seeding employees...")
        employees = [
            Employee(name="Alex Mambo", email="alex@gmail.com", password=bcrypt.generate_password_hash("Alex123!").decode('utf-8'), department='Administrative', role='admin', image='https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600'),
            Employee(name="Hamdi Adan", email="hamdi@gmail.com", password=bcrypt.generate_password_hash("Hamdi123!").decode('utf-8'), department='HR', role='admin', image='https://images.pexels.com/photos/764529/pexels-photo-764529.jpeg?auto=compress&cs=tinysrgb&w=600'),
            Employee(name="Anna Kioko", email="anna@gmail.com", password=bcrypt.generate_password_hash("Anna123!").decode('utf-8'), department='IT', role='employee', image='https://images.pexels.com/photos/11506216/pexels-photo-11506216.jpeg?auto=compress&cs=tinysrgb&w=600'),
            Employee(name="Sharon Mwende", email="sharon@gmail.com", password=bcrypt.generate_password_hash("Sharon123!").decode('utf-8'), department='Finance', role='employee', image='https://images.pexels.com/photos/20434986/pexels-photo-20434986/free-photo-of-jasmine-bajwa-model-shoot.jpeg?auto=compress&cs=tinysrgb&w=600'),
            Employee(name="Candy Bosibori", email="candy@gmail.com", password=bcrypt.generate_password_hash("Candy123!").decode('utf-8'), department='Operations', role='employee', image='https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600')
        ]

        db.session.add_all(employees)
        db.session.commit()    
        print("Done seeding!")