# HR-Hub

## Project Description

HR-Hub is a comprehensive HR Management System designed to streamline human resources processes, enhance data security, and improve employee engagement. It addresses common challenges faced by organizations, such as tedious data management, complex leave management, inefficient employee reports, security concerns, and lack of employee engagement. Built with modern technologies and user-centric design principles, HR-Hub offers user authentication, employee and admin dashboards, database management, and more.

## Installation Guide

### Prerequisites

Before proceeding with the installation, make sure you have the following prerequisites installed on your system:

- Python (>=3.6)
- pip package manager
- virtualenv (optional, but recommended)

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/hr-hub.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd hr-hub
   ```

3. **Create a virtual environment (optional, but recommended):**

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment (skip this step if you didn't create a virtual environment):**

5. **Install the project dependencies:**

   ```bash
   pip install -r requirements.txt


   ```

#### Backend Endpoints

##### Authentication
- **POST /signin**: Sign in with email and password. Returns access and refresh tokens.

##### Employees
- **GET /employees**: Retrieve all employees (admin only).
- **POST /employees**: Create a new employee (admin only).

##### Employee by ID
- **GET /employee/{id}**: Retrieve an employee by ID.
- **PATCH /employee/{id}**: Update an employee by ID (admin or employee only).
- **DELETE /employee/{id}**: Delete an employee by ID (admin only).

##### Reviews
- **GET /reviews**: Retrieve all reviews.
- **POST /reviews**: Add a new review (admin only).

##### Review by ID
- **GET /reviews/{review_id}**: Retrieve a review by ID.
- **PATCH /reviews/{review_id}**: Update a review by ID (admin only).
- **DELETE /reviews/{review_id}**: Delete a review by ID (admin only).

##### Leave
- **GET /leave**: Retrieve all leaves.
- **POST /leave**: Add a new leave.

##### Leave by ID
- **GET /leave/{leave_id}**: Retrieve a leave by ID.
- **PATCH /leave/{leave_id}**: Update a leave by ID.
- **DELETE /leave/{leave_id}**: Delete a leave by ID.

##### Leave Approval
- **PATCH /leave-approval/{leave_id}**: Approve or reject a leave (admin only)..
