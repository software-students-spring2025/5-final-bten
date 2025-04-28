![Web App CI](https://github.com/software-students-spring2025/5-final-bten/actions/workflows/web-app.yml/badge.svg?branch=)

![Web App Image](https://hub.docker.com/repository/docker/nikitabhaskar/5-final-bten/tags/0.1.0/sha256-5627338269fd0b3aa2a296b68eb2a8a9f3c9c265dddacb3c12a980c8c6604ec9)

# Team Members:

[Ariya Mathrawala] (https://github.com/ariyamath29)
[Nikita Bhaskar] (https://github.com/nikitabhaskar)
[Jonathan Gao] (https://github.com/jg169)
[Ethan Zheng] (https://github.com/ez2146)

# Recipe Generator Web Application

A web application that generates personalized recipes based on available ingredients and health goals using AI.

## Project Structure

```
/web-app/              # Main application directory
├── app.py            # Flask application
├── mlclient.py       # AI/ML integration
├── test_app.py       # Tests
├── templates/        # HTML templates
│   └── index.html   # Main page
├── static/          # Static files (CSS, JS, etc.)
└── .env            # Environment variables (not in git)
```

## Prerequisites

Install the following software on your machine:

- [Docker](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://github.com/git-guides/install-git)
- [MongoDB](https://www.mongodb.com/docs/manual/installation/)

## Configuration

1. Clone the repository:

```bash
git clone https://github.com/software-students-spring2025/5-final-bten.git
cd 5-final-bten
```

### Run with Docker:

1. Build and Run

```bash
docker-compose-up --build
```

2. Run Tests

```bash
docker exec -it . pytest
```

Access the web interface at http://127.0.0.1:3000

### Run without Docker:

1. Virtual Environment Setup

Using `pipenv`:\*\*

```bash
pip install pipenv
pipenv shell
```

Using `venv`:\*\*

```bash
python3 -m venv .venv
source .venv/bin/activate #On Mac
.venv\Scripts\activate.bat #On Windows
```

2. Install Dependencies

```bash
pip install -r requirements.txt
```

2. Create and set up environment variables:

```bash
cp ./sample_env.txt .env
# Edit .env with your MongoDB URI
```

4. Connect to database using mongosh

5. Run Application

```bash
cd web-app
python3 app.py
```

6. Run Tests

```bash
cd web-app
pytest test_app.py
```

The application will be available at http://localhost:3000

## Features

- Input available ingredients
- Specify health goals and dietary preferences
- Get AI-generated recipes
- View recipe history
- MongoDB integration for recipe storage

## Development

- Main branch: Production-ready code
- Development happens in feature branches
- PRs required for merging into main
- CI/CD pipeline runs tests automatically
