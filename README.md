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
├── users/              — приложение пользователей (CustomUser)
├── templates/          — HTML-шаблоны
├── static/             — статические файлы
├── .env.example        — шаблон переменных окружения
├── .gitignore
├── requirements.txt
└── manage.py
```

## Функциональность

### Роли и права доступа
- **Пользователь** — видит и редактирует только свои данные (клиентов, сообщения, рассылки).
- **Менеджер** (группа `Менеджеры`) — видит данные всех пользователей, может блокировать пользователей и управлять чужими рассылками.
- Блокировка пользователя: при попытке входа заблокированный пользователь получает сообщение об ошибке.

### Отправка рассылок
- Сервисная функция `send_mailing()` в `mailing/services.py`.
- Проверяет время старта, проходит по получателям и отправляет письма.
- Все попытки логируются в модели `MailingAttempt` (успех/ошибка, ответ сервера).
- Используется `console.EmailBackend` (письма выводятся в консоль).

### Статистика
- На главной странице отображается:
  - количество рассылок;
  - количество попыток;
  - количество успешных попыток;
  - количество получателей.

### Кеширование
- Используется **Redis** (настройка в `settings.py` → `CACHES`).
- Кешируется список рассылок: ключ `mailing_list_{user_id}`, TTL 5 минут.
- При создании/удалении рассылки кеш автоматически сбрасывается.

### CI (Continuous Integration)
- Настроен GitHub Actions (`.github/workflows/ci.yml`).
- При создании Pull Request запускаются тесты (`python manage.py test`) с использованием PostgreSQL и Redis.

## Автор

DenWhite77
