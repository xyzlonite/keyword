# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Add Google Chrome's GPG key
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Add Google Chrome to the apt repositories
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update and install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8080

# Run gunicorn

CMD ["gunicorn", "--bind", ":8080", "app:app", "--timeout", "300"]
# CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "--timeout", "120", "app:app"]