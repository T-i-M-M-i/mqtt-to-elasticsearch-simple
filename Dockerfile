FROM python:3.8

COPY . /daemon

WORKDIR /daemon

RUN pip install -r requirements.txt

CMD ["python", "./mqttToElasticSearch.py"]