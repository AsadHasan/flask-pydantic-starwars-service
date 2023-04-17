install-dependencies:
	pip install -r requirements.txt
flask-db-init:
	flask --app src/main db init
flask-db-migrate:
	flask --app src/main db migrate
flask-db-upgrade:
	flask --app src/main db upgrade
run-service:
	gunicorn -c src/gconfig.py src.wsgi:gunicorn_app
run-dev:
	flask --app src/main run
e2e-tests:
	pytest -s tests/
