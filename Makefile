runserver:
	docker compose up -d --build

migrate:
	docker compose exec web python manage.py migrate --noinput

collectstatic:
	docker compose exec web python manage.py collectstatic --no-input --clear

createsuperuser:
	docker compose exec web python manage.py createsuperuser

down:
	docker compose down -v

test:
	 docker compose exec web python manage.py test semlor

black:
	docker compose exec web black --check source

flake8:
	docker compose exec web flake8 source