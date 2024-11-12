FROM alpine:3.19

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add --no-cache chromium chromium-chromedriver unzip
RUN apk add --update --no-cache py3-pip

WORKDIR /usr/src/app
COPY src .
RUN pip install --no-cache-dir -r ./requirements.txt --break-system-packages

CMD [ "python", "./main.py" ]
EXPOSE 8080
