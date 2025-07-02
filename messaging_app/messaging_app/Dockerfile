# Use official Python image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port (if needed)
EXPOSE 8000

# Run Django dev server (or use gunicorn)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
