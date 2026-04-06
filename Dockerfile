FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn pydantic requests

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]