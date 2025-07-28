# PubSub Events

A Django-based PubSub (Publish-Subscribe) events system.

## Features

- Event publishing and subscription system
- RESTful API endpoints
- Django-based architecture

## Setup

1. Clone the repository:
```bash
git clone https://github.com/Mujtaba-Syed/PubSub-Events.git
cd PubSub-Events
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## Usage

Visit `http://localhost:8000/` to see the application running.

## Project Structure

- `PSEvents/` - Main Django app containing views and models
- `PuBSub/` - Django project settings and configuration
- `manage.py` - Django management script 