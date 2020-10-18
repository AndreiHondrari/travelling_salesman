FROM python:3.9

RUN python -m pip install --upgrade pip

RUN python -m pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && python -m pipenv install --system --dev

COPY worker /worker

WORKDIR /worker

CMD python -m celery -A optimisation_worker worker
