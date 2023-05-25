#
FROM python:3.9

#
WORKDIR /code

#
RUN apt-get update

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8

COPY requirements/ /code/requirements

RUN pip install -U pip && \
    pip install --no-cache-dir -r /code/requirements/requirements.txt
#
COPY ./src /code/src

# RUN pip install --no-cache-dir --upgrade -r /code/app/requirements/requirements.txt
# RUN useradd -m -d /src -s /bin/bash app \
#     && chown -R app:app /src/* && chmod +x /src/scripts/*
# ENV .env

WORKDIR /code/src
# USER app

# CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000", "--reload"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]