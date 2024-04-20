from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import os

from models import db, Employee, Review, Leave

app = Flask(__name__)
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
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            return {'access_token': access_token}, 200
        except Exception as e:
            return jsonify(error=str(e)), 500

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
    def get(self, id):
        review = Review.query.filter_by(id=id).first()
        if review is None:
            return {"error": "Review not found"}, 404
        response_dict = review.to_dict()
        return make_response(response_dict, 200)

    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {'error': 'Only admins can add reviews'}, 403
        
        review = Review.query.get_or_404(id)
        data = request.json
        if 'description' in data:
            review.description = data['description']
        if 'employee_id' in data:
            review.employee_id = data['employee_id']
        db.session.commit()
        return {'message': 'Review updated successfully'}
    
    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {'error': 'Only admins can add reviews'}, 403
        
        review = Review.query.get_or_404(id)
        db.session.delete(review)
        db.session.commit()
        return {'message': 'Review deleted successfully'}

api.add_resource(ReviewByID, '/review/<int:id>')

class LeaveResource(Resource):
    @jwt_required()
    def get(self):
        leaves = [leave.to_dict() for leave in Leave.query.all()]
        return make_response(leaves, 200)
    
    @jwt_required()
    def post(self):        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        if 'leaveType' not in data or 'startDate' not in data or 'endDate' not in data:
            return {"error": "Missing necessary fields in request"}, 400

        try:
            new_leave = Leave(
                leaveType=data['leaveType'],
                startDate=datetime.strptime(data['startDate'], '%Y-%m-%d').date(),
                endDate=datetime.strptime(data['endDate'], '%Y-%m-%d').date(),
                employee_id=get_jwt_identity()['id'],
            )

            db.session.add(new_leave)
            db.session.commit()
        except Exception as e:
            return {"error": str(e)}, 500

        return make_response(new_leave.to_dict(), 201)
    
api.add_resource(LeaveResource, '/leaves')
    
class LeaveById(Resource):
    @jwt_required()
    def get(self, id):
        leave = Leave.query.filter_by(id=id).first()
        if leave is None:
            return {"error": "Not found"}, 404
        response_dict = leave.to_dict()
        return make_response(response_dict, 200)

    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {'error': 'Only admins approve leaves'}, 403

        leave = Leave.query.get_or_404(id)
        data = request.json
        new_status = data['status']

        if new_status not in ['accepted', 'rejected']:
            return {'error': 'Invalid status value'}, 400

        leave.status = new_status
        db.session.commit()

        return {'message': 'status updated successfully!', 'id': leave.id}, 200

api.add_resource(LeaveById, '/leave/<int:id>')
    
if __name__ == '__main__':
    app.run(debug=True, port=5500)