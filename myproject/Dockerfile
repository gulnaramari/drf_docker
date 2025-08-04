# Используем официальный образ Python 3.9
FROM python:3.9

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
COPY requirements.txt ./



# Устанавливаем зависимости Python

RUN pip install --upgrade pip setuptools
RUN pip install -r myproject/requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Определяем переменные окружения

ENV CELERY_BROKER_URL=os.getenv('CELERY_BROKER_URL')
ENV CELERY_BACKEND='django.core.cache.backends.redis.RedisCache'

# Определяем переменные окружения
ENV SECRET_KEY=your_secret_key
ENV POSTGRES_DB=os.getenv('POSTGRES_DB')
ENV POSTGRES_USER=os.getenv('POSTGRES_USER')
ENV POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
ENV POSTGRES_HOST=os.getenv('POSTGRES_HOST')
ENV DATABASE_URL=os.getenv('DATABASE_URL')
ENV DEBUG=True

# Создаем директорию для медиафайлов
RUN mkdir -p /app/static
RUN mkdir -p /app/media

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000
EXPOSE 5432
EXPOSE 6379

# Команда для запуска приложения
CMD ["sh", "-c", "python", "manage.py", "runserver", "0.0.0.0:8000"]
