# Mailing Service

Сервис управления рассылками (курсовой проект на Django).

## Описание

Приложение позволяет создавать клиентов, сообщения и рассылки, отправлять письма по расписанию и отслеживать попытки отправки.

## Технологии

- Python 3.10+
- Django
- PostgreSQL
- Redis (кеширование)
- Bootstrap 5

## Установка и запуск

### 1. Клонирование

```bash
git clone https://github.com/DenWhite77/mailing-service.git
cd mailing-service
```

### 2. Виртуальное окружение

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux / macOS:
```bash
source .venv/bin/activate
```

### 3. Зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройка окружения (`.env`)

Скопируйте шаблон `.env.example` в `.env` и заполните значения:

```bash
copy .env.example .env      # Windows
cp .env.example .env         # Linux / macOS
```

Пример содержимого `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=mailing_service
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/1
```

### 5. Создание базы данных PostgreSQL

В `psql` или pgAdmin:

```sql
CREATE DATABASE mailing_service;
```

### 6. Миграции и запуск

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

## Структура проекта

```text
mailing-service/
├── config/             — настройки Django-проекта
├── mailing/            — основное приложение (рассылки)
├── templates/          — HTML-шаблоны
├── static/             — статические файлы
├── .env.example        — шаблон переменных окружения
├── .gitignore
├── requirements.txt
└── manage.py
```

## Автор

DenWhite77