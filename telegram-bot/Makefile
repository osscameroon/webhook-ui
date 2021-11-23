isort = ./env/bin/python3 -m isort app
black = ./env/bin/python3 -m black app
flake8 = ./env/bin/python3 -m flake8 app

set-env:
	virtualenv -p python3 env

install:
	./env/bin/pip install -r requirements.txt

start:
	./env/bin/python -m app.main

format:
	$(isort)
	$(black)

lint:
	$(flake8)
	$(isort) --check-only --df
	$(black) --check --diff
