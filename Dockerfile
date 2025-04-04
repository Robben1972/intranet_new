# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Copy project files
COPY . /app

# Install project dependencies with uv
RUN pip install -r requirements.txt

# Expose port 8000 for Django
EXPOSE 8000

# Run Django migrations and start the server with uv
CMD ["sh", "-c", "uv run python manage.py makemigrations && uv run python manage.py migrate && uv run python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.filter(username='IntranetAdmin').exists() or User.objects.create_superuser('IntranetAdmin', 'admin@example.com', '361361361$Int')\" && uv run python manage.py runserver 0.0.0.0:8000 && uv run python manage.py archieve_trainings"]