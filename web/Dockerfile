FROM python:3.9

RUN python -m pip install --upgrade pip

RUN python -m pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && python -m pipenv install --system --dev

COPY optimisation_web /optimisation_web

WORKDIR /optimisation_web

CMD python -m manage.py runserver
