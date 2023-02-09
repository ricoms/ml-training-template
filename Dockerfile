FROM python:3.10-buster

ENV PATH=/usr/local/bin:$PATH \
    PYTHONUNBUFFERED=TRUE \
    PYTHONDONTWRITEBYTECODE=TRUE \
    WORKSPACE_TMP="/opt/reports" \
    POETRY_VERSION=1.3.2 \
    OPENBLAS_NUM_THREADS=1

RUN apt-get update \
    && pip install --no-cache-dir "poetry==$POETRY_VERSION" \
    && rm -r /var/lib/apt/lists/* \
    && mkdir -p /opt/program \
    && mkdir -p /opt/reports

COPY . /opt/program
WORKDIR /opt/program

ARG ENVIRON=production

# hadolint ignore=SC2046
RUN poetry config virtualenvs.create false \
    && poetry install \
        $(if [ "$ENVIRON" = 'production' ]; then echo '--no-dev'; fi) \
        --no-interaction --no-ansi
