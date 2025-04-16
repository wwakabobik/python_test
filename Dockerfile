FROM python:3.12

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install libgl1 -y
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD sleep 30 && pytest tests
