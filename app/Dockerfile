# Use a lightweight Python image
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MONGO_URI=''
ENV POSTGRES_URI=''


# Command to run the application
CMD ["python", "tests.py"]
