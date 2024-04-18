from random import choice as rc
from flask_bcrypt import Bcrypt

from app import app
from models import db, Employee

bcrypt = Bcrypt(app)

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Employee.query.delete()

        print("Seeding Reviews...")
        employees = [
            Employee(name="Alex Mambo", email="alex@gmail.com", password=bcrypt.generate_password_hash("Alexmambo.123").decode('utf-8'), department='Administration department', role='admin', image='https://i.pinimg.com/736x/3f/e9/fe/3fe9fe7f0573b76d84f1bc313e43c98d.jpg'),
            Employee(name="Hamdi Adan", email="hamdi@gmail.com", password=bcrypt.generate_password_hash("Hamdiadan.123").decode('utf-8'), department='Finance department', role='admin', image='https://t4.ftcdn.net/jpg/06/74/23/85/360_F_674238560_CDDAIEhTRwdQRY88blPRJMcvTlA8DlKP.jpg'),
            Employee(name="Anna Kioko", email="anna@gmail.com", password=bcrypt.generate_password_hash("Annakioko.123").decode('utf-8'), department='Communications department', role='employee', image='https://expertphotography.b-cdn.net/wp-content/uploads/2020/08/social-media-profile-photos.jpg'),
            Employee(name="Sharon Mwende", email="sharon@gmail.com", password=bcrypt.generate_password_hash("Sharonmwende.123").decode('utf-8'), department='IT', role='employee', image='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYoPYV54xCwyVA5oatGxPAoStsuPH4jvG_kA&s'),
            Employee(name="Candy Bosibori", email="candy@gmail.com", password=bcrypt.generate_password_hash("Candybosibori.123").decode('utf-8'), department='HR', role='employee', image='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSSQmK39rkQ5MgPornwNbwD561ZzpZ16zVCrQO9EH5Hw&s')
        ]

        db.session.add_all(employees)
        db.session.commit()    
        print("Done seeding!")