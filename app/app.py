from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
import os

from models import db, Employee, Review, Leave

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
load_dotenv()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')


migrate = Migrate(app, db)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)
# CORS(app, origins=["https://alex-m-kimeu.github.io", "http://localhost:5173", "http://127.0.0.1:5500"])
CORS(app, resources={r"/*": {"origins": "*"}})

# Restful Routes
class SignIn(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        email = data.get('email')
        password = data.get('password')
        
        employee = Employee.query.filter_by(email=email).first()
        
        if not employee:
            return {"error": "User does not exist"}, 401
        if not bcrypt.check_password_hash(employee.password, password):
            return {"error": "Incorrect password"}, 401
        
        access_token = create_access_token(identity={'id': employee.id, 'role': employee.role})
        refresh_token = create_refresh_token(identity={'id': employee.id, 'role': employee.role})
        return {"access_token": access_token, "refresh_token": refresh_token}, 200

api.add_resource(SignIn, '/signin')

class TokenRefresh(Resource):
    @jwt_required('refresh')
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 200

api.add_resource(TokenRefresh, '/refresh-token')
        
class Employees(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt_identity()
        employee_id = claims['id']
        employee_role = claims['role']
        employees = [employee.to_dict() for employee in Employee.query.all()]
        return make_response(employees, 200)
    
    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {"error": "Only admins can create new employees"}, 403
        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
        
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        employee = Employee(
            name=data['name'], 
            email=data['email'],
            role=data['role'],
            password=hashed_password,
            department=data['department'],
            image=data['image']
            )
        
        db.session.add(employee)
        db.session.commit()
        return make_response(employee.to_dict(), 201)
    
api.add_resource(Employees, '/employees')

class EmployeeByID(Resource):
    @jwt_required()
    def get(self, id):
        employee = Employee.query.filter_by(id=id).first()
        if employee is None:
            return {"error": "Employee not found"}, 404
        response_dict = employee.to_dict()
        return make_response(response_dict, 200)
    
    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        employee = Employee.query.filter_by(id=id).first()
        if employee is None:
            return {"error": "Employee not found"}, 404

        data = request.get_json()
        if claims['role'] == 'admin':
            if all(key in data for key in ['name', 'email', 'password']):
                try:   
                    employee.name = data['name']
                    employee.email = data['email']
                    employee.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                    db.session.commit()
                    return make_response(employee.to_dict(), 200)

                except AssertionError:
                    return {"errors": ["validation errors"]}, 400
            else:
                return {"errors": ["validation errors"]}, 400
        elif claims['role'] == 'employee' and any(key in data for key in ['password', 'name', 'image']):
            try:
                if 'password' in data:
                    employee.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                if 'name' in data:
                    employee.name = data['name']
                if 'image' in data:
                    employee.image = data['image']
                db.session.commit()
                return make_response(employee.to_dict(), 200)
            except AssertionError:
                return {"errors": ["validation errors"]}, 400
        else:
            return {"error": "Unauthorized"}, 403

    @jwt_required()
    def delete(self, id):        
        employee = Employee.query.filter_by(id=id).first()
        if employee is None:
            return {"error": "Employee not found"}, 404
        
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'})
 
api.add_resource(EmployeeByID, '/employee/<int:id>')  

class Reviews(Resource):
    @jwt_required()
    def get(self):      
        reviews = Review.query.all()
        return jsonify([{'id': review.id, 'description': review.description, 'employee_id': review.employee_id} for review in reviews])

    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {'error': 'Only admins can add reviews'}, 403
        
        data = request.json
        if 'description' not in data or 'employee_id' not in data:
            return {'error': 'Description and employee_id are required'}, 400
        review = Review(description=data['description'], employee_id=data['employee_id'])

        db.session.add(review)
        db.session.commit()
        return {'message': 'Review added successfully'}, 201

api.add_resource(Reviews, '/reviews')

class ReviewByID(Resource):
    @jwt_required()
    def get(self, review_id):
        review = Review.query.get_or_404(review_id)
        return {'id': review.id, 'description': review.description, 'employee_id': review.employee_id}

    @jwt_required()
    def patch(self, review_id):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {'error': 'Only admins can add reviews'}, 403
        
        review = Review.query.get_or_404(review_id)
        data = request.json
        if 'description' in data:
            review.description = data['description']
        if 'employee_id' in data:
            review.employee_id = data['employee_id']
        db.session.commit()
        return {'message': 'Review updated successfully'}
    
    @jwt_required()
    def delete(self, review_id):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {'error': 'Only admins can add reviews'}, 403
        
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return {'message': 'Review deleted successfully'}

api.add_resource(ReviewByID, '/reviews/<int:review_id>')

class Leave(Resource):
    @jwt_required()
    def get(self):
        leaves = Leave.query.all()
        return {'leaves': [leave.to_dict() for leave in leaves]}
    # def get(self):      
    #     leaves = Leave.query.all()
    #     return jsonify([{'id': leave.id, 'leaveType': leave.leaveType, 'startDate': leave.startDate, 'endDate': leave.endDate, 'employee_id': leave.employee_id}  for leave in leaves])
    
    @jwt_required()
    def post(self):        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
        
        new_leave = Leave(
            leaveType=data['leaveType'],
            startDate=data['startDate'],
            endDate=data['endDate'],
            employee_id=get_jwt_identity()['id'],
            )
        
        db.session.add(new_leave)
        db.session.commit()
        return make_response(new_leave.to_dict(), 201)
    
api.add_resource(Leave, '/leave')
    
class LeaveById(Resource):
    @jwt_required()
    def get(self, id):
        leave = Leave.query.filter_by(id=id).first()
        if leave is None:
            return {"error": "Not found"}, 404
        response_dict = leave.to_dict()
        return make_response(response_dict, 200)

    # @jwt_required()
    # def patch(self, id):
    #     leave = Leave.query.get_or_404(id)
    #     data = request.json
    #     if 'leavetype' not in data or 'startdate' not in data or 'enddate' not in data:
    #         return jsonify({'error': 'Leave type, start date, end date are required'}), 400
    
    #     leave.leavetype = data['leavetype']
    #     leave.startdate = data['startdate']
    #     leave.enddate = data['enddate']
    #     db.session.commit()
    
    #     return jsonify({'message': 'Leave updated successfully!', 'id': leave.id}), 200

api.add_resource(LeaveById, '/leave/<int:id>')

class LeaveApproval(Resource):
    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {'error': 'Only admins can approve leaves'}, 403
    
        leave = Leave.query.get_or_404(id)
        data = request.json
        if 'status' not in data or data['status'] not in ['accepted', 'rejected']:
            return {'error': 'Status is required and must be either "approved" or "rejected"'}, 400
    
        leave.status = data['status']
        db.session.commit()
        return {'message': 'Leave status updated successfully'}

api.add_resource(LeaveApproval, '/leave-approval/<int:id>')

    
if __name__ == '__main__':
    app.run(debug=True, port=5500)