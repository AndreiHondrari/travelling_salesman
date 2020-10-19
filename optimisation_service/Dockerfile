FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /optimisation_service

COPY . /optimisation_service

RUN pipenv install --system --dev

CMD celery -A worker.optimisation_worker worker -l INFO
