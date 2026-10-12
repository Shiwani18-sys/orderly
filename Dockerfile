

FROM python:3.12

WORKDIR /app

COPY . .

RUN python -m pip install --no-cache-dir -r requirements.txt




CMD ["python"]