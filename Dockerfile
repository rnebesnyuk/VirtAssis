FROM python:3.10.4

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["python", "virtassis/manage.py", "runserver", "0.0.0.0:8050"]