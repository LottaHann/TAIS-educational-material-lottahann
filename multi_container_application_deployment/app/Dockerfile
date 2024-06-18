# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /code

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
       gcc \
       python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy app code
COPY . /code
COPY ./templates /code/templates

# Set environment variables
ENV MODE=production

# Command to run the app
CMD ["sh", "-c", "if [ \"$MODE\" = 'development' ]; then uvicorn app:app:app --host 0.0.0.0 --port 8081 --reload; else uvicorn app:app --host 0.0.0.0 --port 8081; fi"]
