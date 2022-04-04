FROM python:3.8

RUN apt update
RUN apt install -y default-jdk
RUN apt clean -y

WORKDIR /app

COPY ./requirements.txt /app
COPY ./main.py /app
COPY ./src /app/src

COPY postgresql-42.3.3.jar /app

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /app/wait-for-it.sh

RUN chmod +x /app/wait-for-it.sh

RUN pip install -r /app/requirements.txt

CMD ["python", "main.py"]