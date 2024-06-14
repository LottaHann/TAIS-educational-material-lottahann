# Base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /code

# Copy requirements file
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy app code
COPY ./app /code/app
COPY ./templates /code/templates

# Set environment variables
ENV MODE=production

# Command to run the app
CMD ["sh", "-c", "if [ \"$MODE\" = 'development' ]; then uvicorn app.app:app --host 0.0.0.0 --port 8080 --reload; else uvicorn app.app:app --host 0.0.0.0 --port 8080; fi"]
