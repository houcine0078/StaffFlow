
<img src="https://github.com/user-attachments/assets/d3d5e714-28aa-44c9-8fa2-42fefb94dc46" width="175" alt="logo_python"> 
<img src="https://github.com/user-attachments/assets/19508975-46aa-42aa-b95c-7ef90125bf10" width="175" alt="logo_mysql"> 





# StaffFlow - Employee Management System

A comprehensive Django-based HR management system with role-based access control and MySQL database integration.  

## Features

### Role-Based Access Control
- **ADMIN**: Full system administration
- **RH (HR)**: Employee management and leave notifications 
- **MANAGER**: Team management, task assignment, and leave approval  
- **EMPLOYE**: Task management and leave requests 

### Core Functionality
- **User Management**: Complete employee profiles with contact information and hiring dates
- **Task Assignment**: Managers can assign and track tasks for their team members 
- **Leave Management**: Employee leave requests with manager approval workflow 
- **Internal Messaging**: Communication system between users 
- **Contract Management**: Employee contract tracking with salary information 
- **Employee Evaluation**: Performance assessment system

## Technology Stack

- **Backend**: Django (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Authentication**: Django's built-in authentication system

## Database Schema

The system uses five main models:

1. **Utilisateur**: Extended Django user model with role-based permissions
2. **Tache**: Task management with assignment tracking 
3. **Message**: Internal communication system
4. **Demande**: Leave and request management
5. **Contrat**: Employment contract information

## Installation

### Prerequisites
- Python 3.x
- MySQL Server
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/houcine0078/StaffFlow.git
cd StaffFlow
```

2. **Install dependencies**
```bash
pip install django mysqlclient
```

3. **Database Configuration**
Create a MySQL database named `Gestion_employe` and update the database settings in `projet_python/settings.py` if needed.

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Start the development server**
```bash
python manage.py runserver
```

## Usage

### User Roles and Permissions

**HR Dashboard**: 
- View all users
- Manage leave notifications
- Employee evaluation

**Manager Dashboard**: 
- Assign tasks to team members
- Track task progress
- Approve/reject leave requests

**Employee Dashboard**: 
- View assigned tasks
- Submit leave requests
- Receive and send messages

## Key Features Implementation

### Task Management
- Managers can assign tasks with deadlines
- Employees can mark tasks as completed
- Real-time task status tracking

### Leave Management Workflow
1. Employee submits leave request
2. Manager reviews and approves/rejects
3. HR receives notification for approved leaves
4. System tracks leave history

## Database Configuration

The system is configured to use MySQL with the following default settings:
- Database: `Gestion_employe`
- Host: `localhost`
- Port: `3306`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is developed for educational and business purposes.

## Support

For support and questions, please contact the development team.

## Notes

This README provides a comprehensive overview of the StaffFlow system based on the actual codebase structure. The system implements a complete HR workflow with proper role separation and database relationships. Security considerations should be reviewed before production deployment, particularly regarding database credentials and user authentication.
