FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn pydantic requests openai

EXPOSE 8000

CMD ["python", "-m", "server.app"]