# Library Management Application

This application is a simple library management system built with Django and Django Rest Framework (DRF). Follow the steps below to set it up and running on your local machine.

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
git clone https://github.com/AndrejTS/libraryproject.git
```

### 2. Navigate to the Project Directory

Change your directory to the project folder:

```bash
cd libraryproject
```

### 3. Run Docker Compose

Start the application using Docker Compose:

```bash
docker-compose up
```

### 4. Create a Superuser 

Create a superuser for administrative access:

```bash
docker-compose exec web python manage.py createsuperuser 
```

### 5. Access the Application

You can now use the application. The list of available API endpoints can be accessed through the Swagger UI at: http://127.0.0.1:8000/api/schema/swagger-ui/


