# filepath: c:\Users\alien\Desktop\Test Projects\Port-1\run_peewee.py
"""
Flask application entry point with Peewee ORM
This version is compatible with Python 3.13
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
