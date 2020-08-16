FROM python:3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./*.py ./

EXPOSE 5000
ENV FLASK_APP=backend.py
CMD ["flask", "run", "--host=0.0.0.0"]