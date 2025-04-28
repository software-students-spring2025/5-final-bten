FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

ADD . .

EXPOSE 5000

ENV MONGO_URI mongodb://db:27017

CMD ["python3", "src/app.py", "--host=0.0.0.0"]