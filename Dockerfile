FROM python:3.8-alpine

RUN apk add --virtual .build-dependencies \
            --no-cache \
            python3-dev \
            build-base \
            linux-headers \
            postgresql-libs \
            postgresql-dev \
            cargo \
            pcre-dev

#RUN apk add build-base wget
#ENV PATH="/root/.cargo/bin:${PATH}"
#ENV RUSTFLAGS="-C target-feature=-crt-static"
#RUN wget https://sh.rustup.rs -O rustup-init \
#    && sh rustup-init -y --default-toolchain nightly-2020-09-14 \

RUN apk add --no-cache pcre

WORKDIR /app
COPY ./requirements.txt /app
COPY main.py /app

COPY originations.zip /app
COPY payments.zip /app

RUN pip install -r /app/requirements.txt

RUN apk del .build-dependencies && rm -rf /var/cache/apk/*

ENTRYPOINT ["python", "main.py"]