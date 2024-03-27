FROM python:3.10

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /post-service

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /post-service/requirements.txt

RUN python3 -m venv env

RUN source env/bin/activate

RUN pip3 install -r requirements.txt

COPY . /post-service

CMD [ "./wait-for-it.sh", "post-db:3306", "--timeout=0" ,"--","python3", "run.py"]
