FROM python:3.9-slim

WORKDIR /app

COPY app.py .

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV MONGODB_URI=mongodb://mongo:27017/flask_db

EXPOSE 5000

ENTRYPOINT [ "flask" ]

CMD [ "run", "--host=0.0.0.0" ]