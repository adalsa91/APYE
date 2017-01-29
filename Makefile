
install:
	pip install -r requirements.txt

test:
	python3.4 -m unittest discover

run:	
	python3.4 manage.py runserver --host 0.0.0.0
