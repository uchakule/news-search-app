# News Search Application

A Django-based web application that allows users to search, track, and view news articles using the News API.

## Features
- Keyword-based search with result storage.
- View past searches and articles.
- Article refresh feature.
- Admin controls for user management and quotas.
- Filters by date, category, source, and language.

## Setup Instructions
1. Clone the repo: `git clone https://github.com/yourusername/news-search.git`
2. Create virtual env: `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables in `.env`.
5. Run migrations: `python manage.py migrate`
6. Run server: `python manage.py runserver`

## Tech Stack
- Python 3, Django
- News API
- html (for UI)

## Developer Notes
- Time spent: 6-7 hours
- Experience: Gained deeper understanding of building full-stack Django applications from scratch.
Learned to integrate third-party APIs (News API) and handle external data efficiently.
Implemented user authentication and admin access control.
Applied best practices for code structure, modularity, and environment management.
Explored background tasks using Celery (or apscheduler if used).
Practiced writing clean, PEP8-compliant, and maintainable code with proper documentation.
Strengthened skills in Git/GitHub for version control and collaboration.
Understood the importance of user experience in building a responsive and interactive news search portal.


