FROM python:3.11-slim
WORKDIR /Core
COPY . /Core
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8020
ENV PYTHONUNBUFFERED=1
# Change this line to match the exposed por
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8020"]