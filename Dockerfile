FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app
COPY ./main.py /app
COPY ./src /app/src

COPY originations.zip /app
COPY payments.zip /app

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /app/wait-for-it.sh

RUN chmod +x /app/wait-for-it.sh

RUN pip install -r /app/requirements.txt

CMD ["python", "main.py"]