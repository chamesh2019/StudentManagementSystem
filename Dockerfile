FROM python:3.9-buster

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN pip install -r requirements.txt

EXPOSE 8000
STOPSIGNAL SIGTERM

RUN python manage.py runserver
RUN nginx -g "daemon off;"
