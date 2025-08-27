EduMaterials — LMS на Django REST Framework

EduMaterials — это RESTful API-сервис для системы управления обучением (LMS), созданный с использованием Django REST Framework и PostgreSQL.
Платформа позволяет пользователям размещать полезные материалы и курсы, управлять ими, а также подписываться на интересующие курсы.

✨ Возможности

Создание и управление курсами

Добавление и редактирование материалов

Управление пользователями и доступами

Аутентификация по JWT

Автоматическая блокировка неактивных пользователей

Подписка и обновления по курсам

Документация API через Swagger и Redoc

🛠 Технологии

Python ≥ 3.10

Django ≥ 3.2

PostgreSQL ≥ 12

Docker + docker-compose

GitHub Actions (CI/CD)

📦 Установка и запуск
1. Запуск локально через docker-compose
# Клонируем репозиторий
git clone https://github.com/gulnaramari/drf_docker.git

# Переходим в проект
cd drf_docker

# Переименовываем файл окружения и настраиваем переменные
mv .env.smple .env

# Запускаем проект
docker-compose up -d --build


Остановка и удаление контейнеров:

docker-compose down

2. Развёртывание на удалённом сервере
Подготовка сервера
sudo apt update && sudo apt upgrade
sudo ufw enable
sudo ufw allow 80/tcp 443/tcp 22/tcp

Установка Git и Docker
sudo apt install git docker.io docker-compose

Клонирование и запуск
git clone https://github.com/gulnaramari/drf_docker.git
cd drf_docker
mv .env.smple .env
nano .env   # Заполните переменные окружения
docker-compose up -d

3. Доступ к сервису

Регистрация: http://localhost:8000/users/registration

Swagger UI: http://localhost:8000/swagger/

Redoc UI: http://localhost:8000/redoc/

🧪 Примеры API-запросов
1. Регистрация пользователя
POST /users/registration/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "StrongPassword123",
  "first_name": "John",
  "last_name": "Doe"
}

2. Логин и получение JWT токена
POST /users/token/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "StrongPassword123"
}


Ответ:

{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}

3. Создание курса
POST /courses/
Authorization: Bearer JWT_ACCESS_TOKEN
Content-Type: application/json

{
  "title": "Python для начинающих",
  "description": "Базовый курс по Python"
}

⚙ Автоматический деплой (CI/CD)

В проекте настроен GitHub Actions (.github/workflows/ci.yaml):

При каждом push запускаются тесты

Если тесты успешны — проект деплоится на сервер

Необходимые секреты в GitHub
CELERY_BROKER_URL
CELERY_BROKER_URL_FOR_TEST
CELERY_RESULT_BACKEND
CELERY_RESULT_BACKEND_FOR_TEST
DATABASE_HOST
DEPLOY_DIR
DOCKER_HUB_ACCESS_TOKEN
DOCKER_HUB_USERNAME
EMAIL_HOST
EMAIL_HOST_PASSWORD
EMAIL_HOST_USER
EMAIL_PORT
EMAIL_USE_SSL
EMAIL_USE_TLS
POSTGRES_DB
POSTGRES_PASSWORD
POSTGRES_USER
SECRET_KEY
SERVER_IP
SSH_KEY
SSH_USER
STRIPE_SECRET_KEY


Если используете собственную БД, удалите из ci.yml строку:

docker run -d --network=mynetwork --name postgres ...

📜 Лицензия

Этот проект распространяется под лицензией MIT.