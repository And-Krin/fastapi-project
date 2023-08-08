FROM python:3.8

WORKDIR /code

RUN apt-get update

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8

COPY requirements/ /code/requirements

RUN pip config set --user global.trusted-host files.pythonhosted.org
RUN pip install -U pip
RUN pip install --no-cache-dir -r /code/requirements/dev.txt

COPY . /code

WORKDIR /code/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]