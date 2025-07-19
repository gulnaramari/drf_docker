# Используем официальный slim-образ Python 3.12
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN pip install --upgrade pip
RUN pip install
RUN poetry config virtualenvs.create false

# Копируем файл зависимостей в контейнер
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости Python
RUN poetry install --no-root

# Копируем исходный код приложения в контейнер
COPY . .

# Определяем переменные окружения
ENV POSTGRES_DB=os.getenv('POSTGRES_DB')
ENV POSTGRES_USER=os.getenv('POSTGRES_USER')
ENV POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
ENV POSTGRES_HOST=os.getenv('POSTGRES_HOST')
ENV CELERY_BROKER_URL=os.getenv('LOCATION')
ENV CELERY_BACKEND='django.core.cache.backends.redis.RedisCache'
ENV DATABASE_URL=os.getenv('DATABASE_URL')
ENV DEBUG=os.getenv('DATABASE_URL')

# Создаем директорию для медиафайлов
RUN mkdir -p /app/static
RUN mkdir -p /app/media
RUN mkdir -p /app/data
RUN mkdir -p /app/data/htmlcov

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000
EXPOSE 5432
EXPOSE 6379

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
