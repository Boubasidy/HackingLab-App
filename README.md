# My Flask App

This is a basic Flask application structure designed to help you get started with web development using Flask.

## Project Structure

```
my-flask-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── templates
│   │   └── base.html
│   └── static
│       ├── css
│       │   └── style.css
│       └── js
│           └── main.js
├── tests
│   └── test_basic.py
├── instance
│   └── config.py
├── requirements.txt
├── config.py
├── wsgi.py
├── .flaskenv
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-flask-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, set the environment variables and start the Flask server:

1. Set the environment variables in the `.flaskenv` file:
   ```
   FLASK_APP=wsgi.py
   FLASK_ENV=development
   ```

2. Run the application:
   ```
   flask run
   ```

## Testing

To run the tests, use the following command:
```
pytest tests/
```

## License

This project is licensed under the MIT License.