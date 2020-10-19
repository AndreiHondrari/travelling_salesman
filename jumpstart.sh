# first put all services live
docker-compose up -d

# run migrations
docker-compose exec web python manage.py migrate

# create a superuser
docker-compose exec -e DJANGO_SUPERUSER_PASSWORD='Superpass1234' web \
  python manage.py createsuperuser --noinput \
  --username 'admin' --email 'admin@example.com'

# finally launch a browser
open http://localhost:8005
