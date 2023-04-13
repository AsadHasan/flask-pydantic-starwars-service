install-dependencies:
	pip install -r requirements.txt
run-service:
	gunicorn -c src/gconfig.py src.wsgi:gunicorn_app
run-dev:
	flask --app src/main run
e2e-tests:
	pytest -s tests/
