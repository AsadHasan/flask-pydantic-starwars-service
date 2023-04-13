from flask import Flask
from src.main import app

if __name__ == "__main__":
    app.run()
else:
    gunicorn_app: Flask = app
