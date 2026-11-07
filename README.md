# InternTrack — Internship & Job Application Manager

**InternTrack** is a multi-user web application built with **Python and Django** to help individuals organize, track, and manage their internship and job application journey.

It replaces fragmented spreadsheets and manual tracking with a structured system featuring relational data management, application pipeline tracking, dashboard analytics, upcoming interview schedules, and user-specific data isolation.

The project was developed as a practical learning milestone to apply Django backend development concepts in a real-world application.

---

## ✨ Core Features

### 👤 User Authentication & Profile Management
- Custom User Model extending Django's `AbstractUser`.
- User registration, login, and logout.
- Profile management.
- Authentication-protected views.
- User-specific data access.

### 🏢 Company Management
- Create, view, update, and delete company records.
- Store company information, including name, website, location, and notes.
- Maintain ownership of company records.
- Prevent unintended deletion when related opportunities exist.

### 💼 Opportunity Management
- Create and manage internship and job opportunities.
- Associate opportunities with companies.
- Track opportunity types:
  - Internship
  - Full-time
  - Part-time
  - Graduate Trainee
- Store application URLs, descriptions, locations, and deadlines.
- Support remote opportunity tracking.

### 📋 Application Tracking
- Create and manage job or internship applications.
- Track application progress through seven statuses:
  - `SAVED`
  - `APPLIED`
  - `ASSESSMENT`
  - `INTERVIEW`
  - `OFFER`
  - `REJECTED`
  - `WITHDRAWN`
- Record application dates, interview dates, and personal notes.
- Search applications and filter by status.
- Prevent duplicate applications for the same opportunity per user.

### 📊 Dashboard & Insights
- View application statistics.
- Monitor the application pipeline.
- Track recently updated applications.
- Identify upcoming interviews.
- Get a consolidated overview of the job-search journey.

---

## 🏗️ Architecture & Technical Highlights

### 1. Multi-Tenant Data Isolation

InternTrack follows an ownership-based data access approach to keep each user's records separate.

- Core entities (`Company`, `Opportunity`, and `Application`) are associated with authenticated users.
- Views enforce ownership checks before accessing or modifying protected records.
- Object retrieval uses ownership-aware queries, such as `get_object_or_404()`.
- Form querysets are filtered dynamically to prevent users from selecting another user's records.
- These safeguards help prevent Insecure Direct Object Reference (IDOR) vulnerabilities.

### 2. Relational Integrity & Business Rule Validation

The application uses Django ORM and database constraints to maintain consistent data.

- ForeignKey relationships connect users, companies, opportunities, and applications.
- Database-level `UniqueConstraint` prevents duplicate application records for the same user and opportunity.
- Form-level validation enforces business rules:
  - Application dates cannot be in the future.
  - Interview dates cannot precede application dates.
- Deletion confirmation workflows help prevent accidental removal of important application records.

### 3. Environment-Based Configuration

The application supports separate development environments and configurable database settings.

- Environment variables are managed using `python-dotenv`.
- Sensitive configuration is kept outside the source code.
- Application startup validates the required `SECRET_KEY` configuration.
- SQLite is configured as the default database for quick setup and evaluation.
- MySQL can be enabled through environment configuration.
- Timezone support is configured for `Asia/Dhaka`.

### 4. Automated Testing

The project includes **37 automated test cases** using Django's built-in testing framework.

Test coverage includes:

- Authentication workflows.
- User-specific data access.
- Ownership and permission isolation.
- Model and form validation.
- Application business rules.
- Status filtering.
- Duplicate application prevention.
- Regression testing for important application workflows.

The test suite can be executed locally using Django's test runner.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Backend Framework | Django |
| Database | SQLite / MySQL |
| ORM | Django ORM |
| Frontend | Django Templates, HTML, CSS |
| UI Framework | Bootstrap 5 |
| Icons | Bootstrap Icons |
| Authentication | Django Authentication System |
| User Model | Custom User Model (`AbstractUser`) |
| Environment Management | python-dotenv |
| Testing | Django TestCase |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

The project follows a modular Django application structure:

```text
Project 1/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── tests.py
│
├── internships/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── tests.py
│
├── applications/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── tests.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
├── templates/
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 🚀 Getting Started

Follow these instructions to run InternTrack locally.

### Prerequisites

Make sure the following are installed:

- Python 3
- Git
- pip
- SQLite (included with standard Python installations) or MySQL, depending on your configuration.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd "Project 1"
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file from the provided example.

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

**Linux / macOS:**

```bash
cp .env.example .env
```

Open `.env` and configure the required values:

```env
SECRET_KEY=your-secure-random-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=sqlite
```

**Database Configuration**

SQLite is enabled by default and requires no additional database server setup.

To use MySQL, change the database configuration in `.env`:

```env
DB_ENGINE=mysql
DB_NAME=interntrack_db
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Make sure the MySQL server is running and the configured database exists.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create an Administrator Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

**http://127.0.0.1:8000/**

---

## 🧪 Running Tests

Run the complete automated test suite:

```bash
python manage.py test
```

The project currently includes 37 automated test cases.

Expected result:

```text
Ran 37 tests in ...s

OK
```

Running the test suite locally verifies the current codebase and its expected behavior.

---

## 🔒 Security Considerations

Security and data isolation are important parts of InternTrack's backend implementation.

- **Authentication Protection:** Protected views require authenticated users.
- **Ownership Checks:** Users can only access records they own.
- **IDOR Prevention:** Ownership-aware object retrieval and filtered form querysets restrict unauthorized object access.
- **CSRF Protection:** Django CSRF protection is used for state-changing forms.
- **HTTP Method Restrictions:** Destructive operations are restricted to POST requests.
- **Database Integrity:** Unique constraints prevent duplicate application tracking.
- **Secret Management:** Sensitive environment configuration is excluded from version control.
- **Input Validation:** Server-side form validation enforces application business rules.

**Production Note:** This project is currently intended as a local development and portfolio application. Additional production hardening, deployment configuration, and operational safeguards are required before a public production release.

---

## 🧠 Development Journey & AI Collaboration Disclosure

InternTrack was developed over an intensive learning period alongside undergraduate Software Engineering coursework.

The project represents a practical step in learning how Django handles application architecture, database relationships, authentication, request-response workflows, validation, and access control.

### Human-Led Development & Learning

The core backend concepts—including data modeling, relational design, authentication workflows, application logic, and testing—were studied and implemented as part of a guided learning process.

The development process focused on understanding:

- How Django processes HTTP requests.
- How models and QuerySets interact with databases.
- How ownership-based access control works.
- How application workflows are structured.
- How automated tests help verify backend behavior.

### AI-Assisted Collaboration

AI tools, including Gemini and Claude, were used as technical assistants and review partners for selected development tasks.

Their contributions included:

- Generating and refining boilerplate UI templates.
- Reviewing code structure and readability.
- Identifying potential security and validation issues.
- Reviewing timezone and datetime edge cases.
- Providing technical explanations and code review suggestions.

AI-generated suggestions were reviewed and tested as part of the learning and development process.

The objective was not simply to generate an application, but to understand the underlying engineering concepts and progressively improve the implementation.

---

## 🗺️ Future Development Roadmap

InternTrack is designed with room for further development.

Potential future enhancements include:

- Smart application reminders.
- Email notifications.
- Gmail integration.
- Email-based application detection.
- Job opportunity import through URLs.
- Advanced career analytics.
- Background task processing with Celery.
- Redis caching.
- REST API support using Django REST Framework.
- Docker-based development and deployment.

**Note:** These are planned enhancements and are not part of the currently implemented feature set.

---

## 🎯 Project Purpose

InternTrack was built as the first major practical project in a structured Python and Django backend engineering learning journey.

It demonstrates the application of foundational backend development concepts through a multi-user system with relational data management, authentication, business logic, ownership-based access control, and automated testing.

The project is an evolving portfolio milestone focused on learning, implementation, and continuous improvement.

---

**Built with Python & Django.** 🐍
