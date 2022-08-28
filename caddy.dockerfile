FROM python:3.8 as static

WORKDIR /static

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic

FROM caddy:latest

COPY --from=static /static/static /static

COPY ./Caddyfile /etc/caddy/Caddyfile

EXPOSE 443
EXPOSE 80