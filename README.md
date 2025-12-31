# Mini Assessment Engine

A Django-based REST API system that simulates the core functionality of an assessment platform. It enables students to take exams, submit answers securely, and receive automated grading feedback.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Security Features](#security-features)
- [License](#license)

## Overview

The Mini Assessment Engine is designed to demonstrate professional backend development skills through the implementation of a secure, scalable assessment system. The system handles exam management, student submissions, and automated grading with comprehensive validation and security measures.

### Target Users

- **Students**: Take exams and submit answers, view their submissions and grades
- **System Administrators**: Manage exams, questions, and monitor submissions
- **Frontend Developers**: Consume the API to build user interfaces

## Features

### Core Functionality

- **Exam Management**: Create and manage exams with metadata (duration, course, timing, instructions)
- **Question Bank**: Support for multiple question types (multiple choice, true/false, short answer, essay, fill-in-the-blank)
- **Secure Submissions**: Student exam submissions with comprehensive validation
- **Automated Grading**: Modular grading service supporting multiple grading strategies
- **Result Retrieval**: Students can view their submissions and detailed feedback

### Advanced Features

- **Authentication & Authorization**: Token-based or session-based authentication
- **Query Optimization**: Database indexes and optimized queries for performance
- **Detailed Feedback**: Per-question grading with individual scores and feedback
- **Time Tracking**: Automatic calculation of time taken for submissions
- **Data Integrity**: Unique constraints to prevent duplicate submissions

## Technology Stack

- **Framework**: Django 6.0
- **REST Framework**: Django REST Framework (DRF)
- **Database**: MySQL (configurable for PostgreSQL or SQLite)
- **Python**: Python 3.8+
- **Authentication**: Token/Session Authentication

## Database Schema

The system consists of four main models:

### 1. Exam Model
Stores exam information including title, duration, course, timing, and status.

### 2. Question Model
Stores questions with type, expected answer, marks, and metadata. Linked to exams via foreign key.

### 3. Answer Model
Stores individual student answers with marks awarded and feedback. Links submissions to questions.

### 4. Submission Model
Stores student exam submissions with grading status, total score, and metadata (IP address, user agent, attempt number).

**Key Relationships:**
- One Exam → Many Questions
- One Submission → Many Answers
- One Question → Many Answers
- One Student (User) → Many Submissions

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL database server
- pip package manager

### Setup Steps

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd justice
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django mysqlclient djangorestframework
   ```

   Optional dependencies for advanced grading:
   ```bash
   pip install scikit-learn  # For TF-IDF and text similarity
   ```

4. **Create the database**:
   ```bash
   mysql -u root -p
   ```
   ```sql
   CREATE DATABASE mini_assessment_engine CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'assessment_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON mini_assessment_engine.* TO 'assessment_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

5. **Configure database connection**:
   Copy the example configuration file:
   ```bash
   cp my.cnf.example my.cnf
   ```

   Edit `my.cnf` with your database credentials:
   ```ini
   [client]
   database = mini_assessment_engine
   user = assessment_user
   password = your_password
   default-character-set = utf8mb4
   ```

6. **Run migrations**:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

7. **Create a superuser** (for admin access):
   ```bash
   python3 manage.py createsuperuser
   ```

8. **Run the development server**:
   ```bash
   python3 manage.py runserver
   ```

   The API will be available at `http://localhost:8000/`

## Configuration

### Environment Settings

Key settings are located in `miniassessmentengine/settings.py`:

- **TIME_ZONE**: Set to `'Africa/Lagos'` (adjust as needed)
- **DEBUG**: Set to `False` in production
- **SECRET_KEY**: Change this in production
- **ALLOWED_HOSTS**: Configure for production deployment

### Security Considerations for Production

1. Set `DEBUG = False`
2. Update `SECRET_KEY` with a secure random value
3. Configure `ALLOWED_HOSTS` with your domain
4. Use HTTPS (configure SSL/TLS)
5. Set up proper database user permissions
6. Enable CSRF protection
7. Configure CORS if needed (install `django-cors-headers`)

## Usage

### Running the Server

```bash
python3 manage.py runserver
```

### Accessing the Admin Interface

Navigate to `http://localhost:8000/admin/` and log in with your superuser credentials to:
- Create and manage exams
- Add questions to exams
- View student submissions
- Monitor grading status

### Creating Sample Data

You can use the Django shell to create sample data:

```bash
python3 manage.py shell
```

```python
from api.models import Exam, Question
from django.contrib.auth import get_user_model

User = get_user_model()

# Create an exam
exam = Exam.objects.create(
    title="Python Programming 101 - Final Exam",
    duration=120,
    course="Computer Science",
    total_marks=100,
    passing_score=60,
    status='published'
)

# Create a question
question = Question.objects.create(
    exam=exam,
    question_text="What is the output of print(2 ** 3)?",
    question_type='multiple_choice',
    expected_answer={'correct': '8', 'options': ['6', '8', '9', '12']},
    marks=10,
    order=1
)
```

## API Endpoints

The following REST API endpoints are available (or will be implemented):

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/register/` - User registration

### Exams
- `GET /api/exams/` - List available exams
- `GET /api/exams/{id}/` - Get exam details
- `POST /api/exams/` - Create new exam (admin only)
- `PUT /api/exams/{id}/` - Update exam (admin only)
- `DELETE /api/exams/{id}/` - Delete exam (admin only)

### Submissions
- `POST /api/submissions/` - Submit exam answers
- `GET /api/submissions/` - List student's submissions
- `GET /api/submissions/{id}/` - Get submission details

### Expected Request/Response Formats

**Submit Exam (POST /api/submissions/)**
```json
{
  "exam_id": 1,
  "answers": [
    {
      "question_id": 1,
      "answer": "8"
    }
  ],
  "start_time": "2025-12-31T14:00:00Z",
  "submit_time": "2025-12-31T15:30:00Z"
}
```

**Response (201 Created)**
```json
{
  "submission_id": 1,
  "message": "Submission received successfully",
  "status": "pending",
  "submitted_at": "2025-12-31T15:30:00Z"
}
```

## Project Structure

```
justice/
├── api/                          # Main application
│   ├── migrations/              # Database migrations
│   ├── __init__.py
│   ├── admin.py                 # Admin interface configuration
│   ├── apps.py                  # App configuration
│   ├── models.py                # Data models (Exam, Question, Answer, Submission)
│   ├── serializers.py           # DRF serializers (to be implemented)
│   ├── views.py                 # API views (to be implemented)
│   ├── urls.py                  # API URL routes
│   └── tests.py                 # Unit tests
├── miniassessmentengine/        # Project settings
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
├── manage.py                    # Django management script
├── my.cnf                       # Database configuration (gitignored)
├── my.cnf.example              # Database configuration template
├── db.sqlite3                   # SQLite database (if using SQLite)
└── README.md                    # This file
```

## Security Features

### Implemented Security Measures

1. **Authentication Required**: All protected endpoints require authentication
2. **Authorization Checks**: Students can only access their own submissions
3. **Input Validation**: Comprehensive validation using Django's built-in validators
4. **SQL Injection Protection**: Using Django ORM's parameterized queries
5. **Password Security**: Django's built-in password hashing and validation
6. **CSRF Protection**: Enabled by default for state-changing operations
7. **Data Integrity**: Database constraints prevent duplicate submissions

### Additional Security Recommendations

- Enable HTTPS in production
- Implement rate limiting to prevent spam submissions
- Add XSS protection headers
- Configure CORS properly
- Implement request size limits
- Add logging and monitoring
- Regular security audits

## Development Roadmap

### Phase 1: Core API
- [x] Database models
- [x] Migrations
- [ ] Serializers
- [ ] API views and endpoints
- [ ] Authentication setup

### Phase 2: Grading System
- [ ] Mock grading service (keyword matching, text similarity)
- [ ] LLM integration (optional)
- [ ] Grading feedback generation
- [ ] Async grading support

### Phase 3: Testing & Documentation
- [ ] Unit tests
- [ ] Integration tests
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Postman collection

### Phase 4: Optimization
- [ ] Query optimization (select_related, prefetch_related)
- [ ] Caching implementation
- [ ] Pagination
- [ ] Performance profiling

## Contributing

This is an assessment project. However, best practices for contributions would include:

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## Testing

Run tests with:
```bash
python3 manage.py test api
```

Run with coverage:
```bash
pip install coverage
coverage run --source='api' manage.py test api
coverage report
```

## License

This project is created as part of a backend assessment task for Acad AI.

## Contact

For questions or feedback, please contact the project maintainer.

---

**Built with Django** | **Designed for Excellence** | **Focused on Security**
