FROM python:3-alpine
RUN apk add --no-cache chromium chromium-chromedriver unzip
#RUN ln -s /usr/bin/chromium-browser /usr/bin/chromium

WORKDIR /usr/src/app
COPY src .
RUN pip install --no-cache-dir -r ./requirements.txt

CMD [ "python", "./main.py" ]
EXPOSE 80