# Use a smaller base image for production
FROM python:3.11-slim-buster

# Set environment variables for Python optimizations
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project
COPY . .

# Expose the port the application will run on
EXPOSE 8000

# Set the default command to run the application
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
