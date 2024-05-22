# Verification System

## Description

This is a Django-based application to manage and validate operations for technicians. It uses PostgreSQL for the database, Redis for caching, and Django REST framework for the API. Additionally, it integrates with the OpenWeather API to validate operations based on weather conditions.

## Setup

### Prerequisites

- Python 3.12
- Docker

### Steps

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Set up a virtual environment (optional, for local development):**

    ```bash
    python3.12 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies (optional, for local development):**

    Create a `requirements.txt` file with the following content:

    ```txt
    Django>=3.2,<4.0
    djangorestframework
    psycopg2-binary
    django-redis
    dj-database-url
    requests
    ```

    Then run:

    ```bash
    pip install -r requirements.txt
    ```

4. **Create environment variables:**

    Create a `.env` file at the root of your project with the following content:

    ```env
    DEBUG=True
    DATABASE_URL=postgres://user:password@db:5432/verification_db
    REDIS_URL=redis://redis:6379
    OPENWEATHER_API_KEY=your_openweather_api_key_here
    ```

    Replace `your_openweather_api_key_here` with your actual OpenWeather API key.

5. **Set up Docker Compose:**

    Create a `compose.yml` file with the following content:

    ```yaml
    version: '3'

    services:
      db:
        image: postgres:13
        environment:
          POSTGRES_DB: verification_db
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
        volumes:
          - postgres_data:/var/lib/postgresql/data

      redis:
        image: redis:alpine

      web:
        build: .
        command: sh -c ". venv/bin/activate && python manage.py runserver 0.0.0.0:8000"
        volumes:
          - .:/app
        ports:
          - "8000:8000"
        depends_on:
          - db
          - redis
        env_file:
          - .env

    volumes:
      postgres_data:
    ```

6. **Build and start the services:**

    ```bash
    docker compose -f compose.yml up --build
    ```

7. **Run migrations:**

    ```bash
    docker compose -f compose.yml run web sh -c ". venv/bin/activate && python manage.py migrate"
    ```

8. **Create a superuser (optional, for admin access):**

    ```bash
    docker compose -f compose.yml run web sh -c ". venv/bin/activate && python manage.py createsuperuser"
    ```

## Endpoints

- `POST /operations/add/` - Add a new operation.
- `POST /operations/validate/` - Validate an operation for a technician.

### Example JSON for adding an operation:

```json
{
    "name": "Test Operation",
    "priority": 1,
    "restrictions": [
        {
            "@date": {
                "after": "2023-01-01",
                "before": "2023-12-31"
            }
        },
        {
            "@level": {
                "lt": 5,
                "gt": 1
            }
        },
        {
            "@meteo": {
                "temp": {
                    "gt": 10
                },
                "is": "clear"
            }
        }
    ]
}
