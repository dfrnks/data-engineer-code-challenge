FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app
COPY ./main.py /app
COPY ./src /app/src

COPY originations.zip /app
COPY payments.zip /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python", "main.py"]