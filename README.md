# Python Project Challenge Setup Guide

This guide provides step-by-step instructions to set up the Monetary Movements project locally. The project is built using Python, Django REST Framework, Poetry, and PostgreSQL.

## Prerequisites

Ensure you have the following tools installed on your local machine:
- PostgreSQL (with PgAdmin for database manipulation if possible)
- Poetry
- Python 3.9

## Getting Started

### 1. Create a Local Folder:

- Create a folder on your local system where you want to store the project.

### 2. Clone the Repository:

```git clone <repository_url>```
```cd monetary-movements-test```

### 3. Initialize Poetry:

```poetry init```
```poetry add Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 typing-extensions==4.9.0 djangorestframework-simplejwt==5.3.1 django-simple-history==3.4.0 psycopg2-binary==2.9.9 django-filter==23.4 requests==2.31.0 requests-mock==1.11.0 --group dev```

- Open your preferred code editor.

### 4. Configure Python Version:

- Set the Python version to 3.9 in the pyproject.toml file:

```[tool.poetry.dependencies]```
```python = "^3.9"```

### 5. Activate Poetry Environment:

- In the console, run:

```poetry env use $(which python3)```

### 6. Install Dependencies:

```poetry install```

- If it is necessary:
```poetry install --no-root```
```poetry lock --no-update```

- Run:

```poetry shell```

### 7. Create PostgreSQL Database:

- In PgAdmin, create a database named "monetary-movements."

### 8. Update Database Settings:

- If the database host is not "localhost", update the HOST in the settings.py file in the DATABASES section.

### 9. Run Migrations:

```python manage.py makemigrations```
```python manage.py migrate```

### 10. Start the Development Server & Create Superuser

```python manage.py runserver```
```python manage.py createsuperuser```
- Use the superuser credentials to log in to the admin interface at [localhost:8000/admin/](localhost:8000/admin/).

### 11. Run Tests:

- Optionally, run tests with the following command:

```python manage.py test movements.tests.MovementsTests```

- You have successfully set up the Monetary Movements project locally.