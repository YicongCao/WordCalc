FROM python:3.7-slim

ENV APP_HOME=/app \
    APP_PYTHON_PACKAGES=/usr/local/lib/python3.7/dist-packages

WORKDIR ${APP_HOME}

RUN apt-get update \
    && apt-get install -y tar \
    && apt-get install -y wget \
    && apt-get install -y --no-install-recommends build-essential git-core \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . ${APP_HOME}

RUN ["chmod", "+x", "./dockermain.sh"]

EXPOSE 5000

ENTRYPOINT [ "sh", "./dockermain.sh" ]