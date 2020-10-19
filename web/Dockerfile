FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /optimisation_web

COPY . /optimisation_web

RUN pipenv install --system --dev

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
