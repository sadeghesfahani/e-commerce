FROM python:3.8

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/e_commerce

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

COPY ./entrypoint /entrypoint

RUN sed -i 's/\r$//g' /entrypoint

RUN chmod +x /entrypoint

ENTRYPOINT [ "/entrypoint" ]

EXPOSE 8000
