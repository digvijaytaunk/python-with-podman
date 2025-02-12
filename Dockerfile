# syntax=docker/dockerfile:1

FROM python:3.13.2-slim

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./src ./src

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]
