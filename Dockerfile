FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV DJANGO_MANAGEPY_MIGRATE=true

CMD ["./entrypoint.sh"]
