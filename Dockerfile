FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY web-app/ .

EXPOSE 3000

ENV MONGO_URI mongodb://db:27017

CMD ["python3", "app.py"]