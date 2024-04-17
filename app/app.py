from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Employee, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
CORS(app)

# Restful Routes
class Employees(Resource):
    def get(self):
        employees = [employee.to_dict() for employee in Employee.query.all()]
        return make_response(employees, 200)
    

    def post(self):
        data = request.get_json()
        employee = Employee(
            name=data['name'], 
            email=data['email'],
            role=data['role'],
            password=data['password'],
            department=data['department']
            )
        
        db.session.add(employee)
        db.session.commit()
        return make_response(employee.to_dict(), 201)
    
api.add_resource(Employees, '/employees')

class EmployeeByID(Resource):
    def get(self, id):
        employee = Employee.query.filter_by(id=id).first()
        if employee is None:
            return {"error": "Hero not found"}, 404
        response_dict = employee.to_dict()
        return make_response(response_dict, 200)
    
    # edit an employee
    def patch(self, id):
        # check if id excist in data base 
        employee = Employee.query.filter_by(id=id).first()
        if employee is None:
            return {"error": "Employee not found"}, 404
        
        # if it does then retrieve the updated part
        data = request.get_json()

        if all(key in data for key in ['name', 'email', 'password']):
            try:   
                employee.name = data['name']
                employee.email = data['email']
                employee.password = data['password']
                db.session.commit()
                return make_response(employee.to_dict(), 200)

            except AssertionError:
                return {"errors": ["validation errors"]}, 400
        else:
            return {"errors": ["validation errors"]}, 400

    def delete(self, employee_id):
        employee = Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'})
 
api.add_resource(EmployeeByID, '/employees/<int:employee_id>')  

class Reviews(Resource):
    def get(self):
        reviews = Review.query.all()
        return jsonify([{'id': review.id, 'description': review.description, 'employee_id': review.employee_id} for review in reviews])

    def post(self):
        data = request.json
        if 'description' not in data or 'employee_id' not in data:
            return {'error': 'Description and employee_id are required'}, 400
        review = Review(description=data['description'], employee_id=data['employee_id'])

        db.session.add(review)
        db.session.commit()
        return {'message': 'Review added successfully'}, 201

api.add_resource(Reviews, '/reviews')

class ReviewByID(Resource):
    def get(self, review_id):
        review = Review.query.get_or_404(review_id)
        return {'id': review.id, 'description': review.description, 'employee_id': review.employee_id}

    def patch(self, review_id):
        review = Review.query.get_or_404(review_id)
        data = request.json
        if 'description' in data:
            review.description = data['description']
        if 'employee_id' in data:
            review.employee_id = data['employee_id']
        db.session.commit()
        return {'message': 'Review updated successfully'}

    def delete(self, review_id):
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return {'message': 'Review deleted successfully'}

api.add_resource(ReviewByID, '/reviews/<int:review_id>')

if __name__ == '__main__':
    app.run(debug=True, port=5500)