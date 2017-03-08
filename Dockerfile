FROM coorpacademy/docker-pyspark:2.0.0-alpine

# GENERAL DEPENDENCIES
RUN apk update && \
    apk add zip

# PYTHON DEPENDENCIES
RUN apk add python-dev build-base

RUN pip install setuptools-scm && pip install --upgrade setuptools
COPY luigi.cfg /luigi.cfg
RUN export LUIGI_CONFIG_PATH=/luigi.cfg

COPY init.sh /init.sh

COPY names.txt /names.txt

RUN chmod +x /init.sh
COPY requirements.txt /etc/requirements.txt
RUN pip install -r /etc/requirements.txt && \
    rm /etc/requirements.txt
