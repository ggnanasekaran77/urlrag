FROM python:3.9.6

WORKDIR /app

EXPOSE 80

COPY app .

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
