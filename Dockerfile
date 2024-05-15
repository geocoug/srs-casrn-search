# ~~~~~~~~~~~
# Build stage
# ~~~~~~~~~~~
FROM python:3.11-slim as staging
WORKDIR /tmp

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y

RUN pip install --no-cache-dir --upgrade pip==24.0

COPY ./requirements.txt .

RUN pip wheel --no-cache-dir --wheel-dir /usr/local/app/wheels -r requirements.txt


# ~~~~~~~~~~~
# Build final
# ~~~~~~~~~~~
FROM python:3.11-slim

ENV HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p $HOME

WORKDIR $HOME

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

COPY --from=staging /usr/local/app/wheels /wheels

# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip==24.0 && \
    pip install --no-cache-dir /wheels/*

COPY casrn_search.py $HOME

ENTRYPOINT ["python", "casrn_search.py"]
