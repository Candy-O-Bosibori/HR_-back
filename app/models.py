from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
import re

db = SQLAlchemy()

# Define Models
class Employee(db.Model, SerializerMixin):
    __tablename__= 'employees'
    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    

    # relationships with review and leave
    reviews = db.relationship('Review', back_populates= 'employee', cascade="all, delete-orphan")
    leave = db.relationship('Leave', back_populates= 'employee', cascade="all, delete-orphan")

    # validation
    @validates('role')
    def validate_role(self, key, role):
        if role != 'employee' and role != 'admin':
            raise ValueError("Category must be either employee or admin.")
        return role

     # serialization rules
    serialize_rules= ('-reviews.employee', '-leaves.employee')
    
    # first and last name
    @validates('first_name')
    def validate_name(self, key, name):
        assert len(name) > 2
        assert name.isalpha(), "first name should only contain alphabetic characters"
        return name
    
    @validates('last_name')
    def validate_name(self, key, name):
        assert len(name) > 3
        assert name.isalpha(), "last name should only contain alphabetic characters"
        return name
    
    # email
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Invalid email format"
        return email
    
    # password
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 8
        assert re.search(r"[A-Z]", password), "Password should contain at least one uppercase letter"
        assert re.search(r"[a-z]", password), "Password should contain at least one lowercase letter"
        assert re.search(r"[0-9]", password), "Password should contain at least one digit"
        assert re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Password should contain at least one special character"
        return password

    def __repr__(self):
        return f"<User {self.id}, {self.name}, {self.department},{self.role}, {self.email}, {self.password}>"
    

# Review Table
class Review(db.Model, SerializerMixin):
    __tablename__= 'reviews' 
   
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    
    # Foreign Key
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
   
    # Relationship with employee
    employee = db.relationship('Employee', back_populates='reviews')

    @validates('description')
    def validate_description(self, key, description):
         if not 5 <= len(description) <= 100:
             raise ValueError("Description must be between 5 and 100 characters.")
         return description
    
    def __repr__(self):
         return f"<Review {self.id}, {self.description}>"


    
class Leave(db.Model, SerializerMixin):
    __tablename__ = "leave"

    id = db.Column(db.Integer,primary_key=True)
    leaveType = db.Column(db.String, nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')


    # relationship with employee
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    employee = db.relationship('Employee', back_populates='leave')
   

    #validation
    @validates('status')
    def validate_status(self, key, status):
        if status not in ('accepted', 'rejected', 'pending'):
            raise ValueError("Status must be either 'accepted', 'rejected', or 'pending'")
        return status

    @validates('leaveType')
    def validate_leaveType(self, key, leaveType):
        if leaveType not in ('sick', 'casual', 'vacation'):
            raise ValueError("Invalid Leave Type")
        return leaveType
    
    def __repr__(self):
        return f"<Leave {self.leaveType}, {self.startDate}, {self.endDate}, {self.status}>"
