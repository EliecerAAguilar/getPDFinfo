FROM python:3.11.0-slim-bullseye


WORKDIR /app

RUN apt update
RUN apt upgrade -y
RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./ ./

CMD ["python3", "main.py"]