FROM python:3.8

WORKDIR /opt/etl

RUN pip install --upgrade pip \
    && pip install psycopg2-binary==2.9 \
    && pip install python-dotenv==0.21.0 \
    && pip install backoff \
    && pip install requests

COPY . .

CMD ["bash", "etl_transfer.sh"]