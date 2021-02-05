FROM python:3.9

RUN mkdir /search_app6/
WORKDIR /search_app6/

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY .coveragerc .coveragerc

COPY data data
COPY src src

CMD ["python", "src/search/shard2server.py"]