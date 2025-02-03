# CSV Upload API

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

## Usage
- Endpoint: `POST /api/upload/`
- Send a `.csv` file containing `name`, `email`, and `age`.

## Testing
Run `python manage.py test` to execute unit tests.
