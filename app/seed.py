from app import app, db
from models import Employee, Review, Leave  

with app.app_context():

    Employee.query.delete()
    Review.query.delete()
    Leave.query.delete()

    
    employees_data = [
        Employee(name='John Doe', email='john@example.com', department='Engineering', role='employee'),
        Employee(name='Jane Smith', email='jane@example.com', department='Finance', role='employee'),
        Employee(name='Alice Johnson', email='alice@example.com', department='HR', role='admin')
    ]

    db.session.add_all(employees_data)

    review_data = [
        Review(description='Annual review'),
        Review(description='Performance evaluation'),
        Review(description='Quarterly review')
    ]

    db.session.add_all(review_data)

    leave_data = [
        Leave(leaveType='sick', startDate='2024-04-18', endDate='2024-04-19', status='accepted'),
        Leave(leaveType='casual', startDate='2024-04-20', endDate='2024-04-21', status='rejected'),
        Leave(leaveType='vacation', startDate='2024-04-22', endDate='2024-04-23', status='accepted')
    ]

    db.session.add_all(leave_data)

    db.session.commit()
