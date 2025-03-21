# Django Student Report Management System

## Overview
This Django project provides a complete system for managing students, schools, and reports. The system includes the following features:

- User Authentication
- School Management (Add, View, Update School Info)
- Student Management (Add New Student, Update Student Details)
- Class Management (Upgrade Student Class)
- Report Management (Add and Manage Student Reports)

## Features

### 1. User Authentication
- **Signup**: Users can create an account.
- **Sign In**: Users can log in based on roles.
- **OTP Verification**: Email OTP verification for security.
- **Forgot Password**: Users can request a password reset.
- **Reset Password**: Users can reset their password using a token.

### 2. School Management
- **View All Schools**: Users can retrieve a list of all registered schools.
- **Get School Info**: Fetch detailed information about a school.
- **Update School Info**: Admins can update school details.

### 3. Student Management
- **View All Students**: List all students in a school.
- **Get Student Info**: Retrieve detailed student information.
- **Add New Student**: Admins can add new students.
- **Update Student Details**: Modify student information.

### 4. Class Management
- **Upgrade Student Class**: Change a student’s class level.

### 5. Report Management
- **Add Student Report**: Users can create new reports for students.

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- Django (>=5.1.5)
- PostgreSQL/MySQL/SQLite (Choose based on preference)

### Step 1: Clone the Repository
```bash
git https://github.com/ashiques-dev/students-progress.git
cd students-progress
```

### Step 2: Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file and set the following environment variables:
```env
SECRET_KEY='your_secret_key'
DEBUG=True  # Change to False in production
ALLOWED_HOSTS=127.0.0.1

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
```

### Step 5: Apply Migrations
```bash
python manage.py migrate
```

### Step 6: Run the Server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication Endpoints
| Method | Endpoint                              | Description                |
|--------|--------------------------------------|----------------------------|
| POST   | /auth/sign-up/                      | User Signup               |
| POST   | /auth/sign-in/<str:role>/           | User Sign In               |
| POST   | /auth/verify-otp/<str:uid>/<str:token>/ | OTP Verification          |
| POST   | /auth/resend-otp/<str:uid>/<str:token>/ | Resend OTP                |
| POST   | /auth/forgot-password/             | Forgot Password           |
| POST   | /auth/reset-password/<str:uid>/<str:token>/ | Reset Password |

### Admin Endpoints
| Method | Endpoint                      | Description                 |
|--------|--------------------------------|-----------------------------|
| GET    | /super-user/schools/          | Get all schools            |
| GET    | /super-user/school/<int:id>/  | Get school details         |
| GET    | /super-user/school/<int:id>/students/ | Get all students in a school |
| GET    | /super-user/student/<int:id>/ | Get student details        |

### User Endpoints
| Method | Endpoint                                | Description               |
|--------|----------------------------------------|---------------------------|
| GET    | /user/schools/                        | Get all schools           |
| GET    | /user/school/<int:id>/                | Get school details        |
| GET    | /user/school/<int:id>/students/       | Get all students in a school |
| GET    | /user/school/<int:school_id>/student/<int:id>/ | Get student details |
| POST   | /user/reports/<int:id>/               | Add a new student report  |
| PUT    | /user/upgrade-class/<int:id>/         | Upgrade student class     |

## Technologies Used
- Django & Django REST Framework (DRF)
- PostgreSQL/MySQL/SQLite
