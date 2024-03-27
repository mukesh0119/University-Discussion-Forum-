
FROM python:3.10

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /user-service

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /user-service/requirements.txt

RUN python3 -m venv env

RUN source env/bin/activate

RUN pip3 install -r requirements.txt

COPY . /user-service

CMD [ "./wait-for-it.sh", "user-db:3306", "--timeout=0" ,"--","python3", "run.py"]