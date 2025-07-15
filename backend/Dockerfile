FROM python:3.12-slim

# Install libmagic
RUN apt-get update && apt-get install -y libmagic1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
seraea
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
