FROM python:3.8

WORKDIR /opt/data_transfer


RUN pip install --upgrade pip \
    && pip install psycopg2-binary==2.9 \
    && pip install python-dotenv==0.21.0


COPY . .

CMD [ "bash", "data_transfer.sh"]
