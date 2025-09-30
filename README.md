# Online Poll System Backend

A robust and scalable backend service for creating polls, casting votes, and retrieving real-time results. Built with Django and PostgreSQL.

## Features

- **Poll Management:** Create polls with multiple options and set expiry dates.
- **Secure Voting:** Cast votes with validation to prevent duplicates.
- **Real-Time Results:** Compute and fetch poll results efficiently.
- **API Documentation:** Interactive API docs powered by Swagger.

## Technology Stack

- **Framework:** Django & Django REST Framework
- **Database:** PostgreSQL
- **API Documentation:** Swagger (drf-yasg)

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Installation & Setup

Follow these steps to get your development environment running:

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd online-poll-backend
    ```

2.  **Create a Virtual Environment**
    (It's like a separate toolbox for this project so its parts don't get mixed up with your other projects)
    ```bash
    python -m venv venv
    ```
    - On macOS/Linux: `source venv/bin/activate`
    - On Windows: `.\venv\Scripts\activate`

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up the Database**
    - Create a new PostgreSQL database named `poll_db`.
    - Update the `DATABASES` configuration in `settings.py` with your database credentials (we will do this in a later step).

5.  **Run Database Migrations**
    (This creates the necessary tables in your database, like building the shelves before you can store things.)
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser** (Optional)
    (This gives you an admin account to log into the Django admin interface and see your data.)
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

## API Usage Examples

Once the server is running, you can interact with the API. Below are examples using `curl`.

### 1. Create a Poll

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/polls/ \
-H "Content-Type: application/json" \
-d '{
  "question": "What is your favorite color?",
  "options": ["Red", "Blue", "Green"],
  "expires_at": "2024-12-31T23:59:59Z"
}'
