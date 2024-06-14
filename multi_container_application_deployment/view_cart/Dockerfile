# Base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /code

# Copy requirements file
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy app code
COPY ./view_cart /code/viewcart

COPY ./templates /code/templates

# Set environment variables
ENV MODE=production

# Command to run the app
CMD ["sh", "-c", "if [ \"$MODE\" = 'development' ]; then uvicorn viewcart.viewcart:app --host 0.0.0.0 --port 8081 --reload; else uvicorn viewcart.viewcart:app --host 0.0.0.0 --port 8081; fi"]
