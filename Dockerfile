# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /src

RUN useradd --no-create-home -r -s /usr/sbin/nologin sqstw && chown -R sqstw /src

COPY --chown=sqstw:sqstw requirements.txt requirements.txt

RUN pip3 install --upgrade --user pip
RUN pip3 install -r requirements.txt

COPY --chown=sqstw:sqstw ./sqstw sqstw
COPY --chown=sqstw:sqstw ./cli.py cli.py

EXPOSE 8000

USER sqstw 

CMD ["python3", "cli.py"]
