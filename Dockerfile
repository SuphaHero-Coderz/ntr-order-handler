FROM python:3.11-slim

# Install all the requirements
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy everthing from . to /app inside the 'box'
COPY . /app/
WORKDIR /app

# How to run it when we start up the box?
CMD ["python", "main.py"]