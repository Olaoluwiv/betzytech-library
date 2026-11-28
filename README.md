# betzytech-library
# BetzyTech Library

A containerized library management application built with **FastAPI, SQLite, HTML, CSS, JavaScript, Docker and Docker Compose**.

## Project Overview

BetzyTech Library is a web-based library application designed to manage and display book records through a frontend connected to a Python FastAPI backend.

The application uses SQLite for data storage and Docker to package the frontend and backend into separate containers.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- HTML5
- CSS3
- JavaScript
- Docker
- Docker Compose
- Git and GitHub
- Docker Hub

## Project Architecture

The application consists of three main components:

1. **Frontend:** Provides the user interface and communicates with the backend API.
2. **Backend:** Uses FastAPI to handle application requests and book data.
3. **Database:** SQLite stores the library's book records.

Docker Compose manages the frontend and backend containers, while a named Docker volume provides persistent database storage.

## Project Structure

```text
betzytech-library/
│
├── backend/
│   ├── database.py
│   ├── main.py
│   └── models.py
│
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── Dockerfile
├── compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

## Running the Application with Docker

### Prerequisites

- Docker Desktop
- Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/Olaoluwiv/betzytech-library.git
cd betzytech-library
```

### 2. Create the persistent database volume

```bash
docker volume create betzytech-library-data
```

### 3. Build and start the application

```bash
docker compose up --build -d
```

### 4. Access the application

| Component | Address |
|---|---|
| Frontend | http://localhost:8084 |
| Backend | http://localhost:8100 |
| API documentation | http://localhost:8100/docs |
| Books API | http://localhost:8100/api/books |

### 5. Check running containers

```bash
docker compose ps
```

### 6. View application logs

```bash
docker compose logs -f
```

### 7. Stop the application

```bash
docker compose down
```

The named database volume is external to the Compose services, so this command does not remove it.

## Database Persistence

The application uses SQLite for storing book records.

The backend supports the `DATABASE_PATH` environment variable to configure the database location.

Docker Compose configures:

```text
DATABASE_PATH=/data/betzytech.db
```

The `/data` directory is connected to the named Docker volume:

```text
betzytech-library-data
```

This allows database records to persist when the backend container is replaced.

## API

The backend exposes the books endpoint:

```text
GET /api/books
```

Example local address:

```text
http://localhost:8100/api/books
```

Book records include fields such as:

- ID
- Title
- Author
- Category

Additional API operations can be documented as they are verified.

## Docker Hub Images

The project images are published on Docker Hub:

- Backend: `olaoluwiv/betzytech-library-backend:v1.0.0`
- Frontend: `olaoluwiv/betzytech-library-frontend:v1.0.0`

## DevOps Roadmap

The project is being developed as a practical DevOps learning project covering:

1. **Commit:** Git and GitHub version control.
2. **Build:** Docker image creation and containerization.
3. **Test:** Automated application and container testing.
4. **Release:** Versioning and publishing application releases.
5. **Deploy:** Application deployment using container and infrastructure tools.
6. **Monitor:** Application monitoring, logs, metrics and Grafana.

## Project Status

The application has been containerized using Docker and Docker Compose. Backend and frontend images have been published to Docker Hub, and the source code is hosted on GitHub.

Further CI/CD automation, release management, deployment and monitoring are planned as part of the DevOps learning process.

