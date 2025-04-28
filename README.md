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

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/software-students-spring2025/5-final-bten.git
cd 5-final-bten
```

2. Create and set up environment variables:
```bash
cd web-app
cp ../sample_env.txt .env
# Edit .env with your MongoDB URI
```

3. Run with Docker (recommended):
```bash
docker-compose up
```

Or run locally:
```bash
cd web-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt
python app.py
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

## Team Members
- [Your team members' GitHub profiles here]
