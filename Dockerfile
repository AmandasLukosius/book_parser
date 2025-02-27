FROM python:3.13.2

ENV POETRY_VERSION=2.1.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

RUN apt-get update \
    && apt-get install -y cron

COPY . /app
WORKDIR /app

ENV PATH="${PATH}:${POETRY_VENV}/bin"
RUN poetry install

COPY --chmod=0644 cron /etc/cron.d/cron
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log