# Campus Desk

Campus Desk is a beginner-friendly Django Student Management System for managing students, departments, courses, and enrollments from one responsive dashboard.

## Features

- Dashboard statistics and recent activity
- Authenticated student CRUD with search, department filtering, and pagination
- Department and course management
- Enrollment management with duplicate prevention
- Django admin configuration for all models
- Responsive Tailwind CSS interface
- Idempotent demo data command and focused test suite

## Tech Stack

Python 3.12, Django 5, SQLite, Tailwind CSS via CDN, Django ORM, Django Authentication, and Django Admin.

## Installation

```text
git clone <repository-url>
cd student_management
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Then run:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/login/` and sign in with your superuser.

## Project Structure

- `config/`: project settings, root URLs, and WSGI/ASGI configuration
- `students/`: models, forms, views, routes, admin, tests, and seed command
- `templates/`: shared layout, authentication, and feature templates
- `static/`: project-level static assets
- `db.sqlite3`: local development database created by migrations

## Screenshots

Add dashboard, student list, and admin screenshots here for a portfolio presentation.

## Future Improvements

Attendance management, grade management, a REST API, PostgreSQL support, email notifications, and cloud deployment.