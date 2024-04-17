from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy

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
    review = db.relationship('Review', back_populates= 'employee', cascade="all, delete-orphan")
    leave = db.relationship('Leave', back_populates= 'employee', cascade="all, delete-orphan")

    # validation
    @validates('role')
    def validate_role(self, key, role):
        if role != 'Employee' and role != 'Admin':
            raise ValueError("Category must be either Employee or Admin.")
        return role









    def __repr__(self):
        return f"<Employee {self.name}, {self.email}>"

class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

class Leave(db.Model, SerializerMixin):
    __tablename__ = "Leave"

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
        if status != 'accepted' and status != 'rejected':
            raise ValueError("Category must be either accepted or rejected")
        return status
    
    @validates('leavetype')
    def validate_leavetype(self, key, leavetype):
        if leavetype not in ('sick', 'casual', 'vacation'):
            raise ValueError("Invalid Leave Type")
        return leavetype
    
    def __repr__(self):
        return f"<Leave {self.leaveType}, {self.startDate}, {self.endDate}, {self.status}>"
