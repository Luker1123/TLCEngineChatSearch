FROM python:latest

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

#Change this to be the Variable in .env
EXPOSE 5000

CMD ["python", "chatSearchServer.py"]