
install:
	pip install -r requirements.txt

test:
	python -m unittest discover

run:	
	python manage.py runserver
