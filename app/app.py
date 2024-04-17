from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Employee

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
CORS(app)

# Restful Routes
@app.routes('/emloyees', methods=['GET', 'POST'])
def employees():
    if request.method == 'GET':
        employees = Employee.query.all()
        return jsonify([{'id': employee.id, 'name': employee.name, 'status': employee.status} for employee in employees])
    
    if request.method == 'POST':
        data = request.json
        if 'name' not in data or 'status' not in data:
            return jsonify({'error': 'Name and status are require'}), 400
        employee = Employee(name=data['name'], status=data['status'])

        db.session.add(employee)
        db.session.commit()
        return jsonify({'message': 'Employee added successfully'}), 201

@app.route('/employee/<init:employee_id>', methods=['GET', 'PATCH', 'DELETE'])
def employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    if request.method == 'GET':
        return jsonify({'id': employee.id, 'name': employee.name, 'status': employee.status})
    
    if request.method == 'PATCH':
        data = request.json
        if 'name' in data:
            employee.name = data['name']

        if 'status' in data:
            employee.status = data['status']

        db.session.commit()
        return jsonify({'message': 'Employee updated successfully'})
    if request.method == 'DELETE':
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)