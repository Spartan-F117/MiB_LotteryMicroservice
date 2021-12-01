#
# Docker file for Message in a Bottle v1.0
#
FROM python:3.8
LABEL maintainer="02_squad"
LABEL version="1.0"
LABEL description="Message in a Bottle Lottery Microservice"

# creating the environment
COPY . /app

# setting the workdir
WORKDIR /app

ENV FLASK_ENV=production

# installing all requirements
RUN ["pip", "install", "-r", "requirements.prod.txt"]

# exposing the port
EXPOSE 5004/tcp

# Main command
CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]