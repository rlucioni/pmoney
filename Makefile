serve:
	DEBUG=1 python manage.py runserver

load_data:
	python manage.py loaddata podcasts
