# 📢 Сервис объявлений с отзывами (Ads Board)

> Бэкенд-приложение на Django + DRF для платформы объявлений с системой отзывов, аутентификацией и правами доступа.

---

## 📌 Описание проекта

Проект реализует backend-часть сайта объявлений, где пользователи могут:
- Публиковать, просматривать, редактировать и удалять свои объявления.
- Оставлять отзывы под чужими объявлениями.
- Искать объявления по названию.
- Восстанавливать пароль через email.

Администраторы имеют полный доступ ко всем данным.

---

## 🛠 Технологии

- **Python 3.11**
- **Django 5.2**
- **Django REST Framework (DRF)**
- **JWT-аутентификация** (`simplejwt`)
- **PostgreSQL** — основная БД
- **Django Filters** — фильтрация по названию
- **Poetry** — управление зависимостями
- **Swagger** (`drf-spectacular`) — документация API
- **Django CORS Headers** — безопасный доступ с фронтенда
- **Django Email Backend** — восстановление пароля

---
## 🧱 Модели

### 🔐 `User` (Пользователь)
| Поле | Тип | Описание                                          |
|------|-----|---------------------------------------------------|
| `id` | AutoField | Уникальный ID                                     |
| `email` | EmailField | Email адрес, используется как логин (уникальный). |
| `first_name` | CharField | Имя                                               |
| `last_name` | CharField | Фамилия                                           |
| `phone` | CharField | Номер телефона                                    |
| `role` | CharField | `user` или `admin`                                |
| `image` | ImageField | Аватар (загружается в `users/avatars/`)                                           |


**Аутентификация:** через JWT (access/refresh токены).

---
### 📣`Ad` (Объявление)
| Поле | Тип | Описание |
|------|-----|--------|
| `id` | AutoField | Уникальный ID |
| `title` | CharField | Название товара |
| `price` | PositiveIntegerField | Цена (≥ 0) |
| `description` | TextField | Описание |
| `author` | ForeignKey → User | Автор объявления |
| `created_at` | DateTimeField | Дата создания (авто) |

**Сортировка:** по убыванию `created_at`.

---
### 💬`Review` (Отзыв)
| Поле | Тип | Описание |
|------|-----|--------|
| `id` | AutoField | Уникальный ID |
| `text` | TextField | Текст отзыва |
| `author` | ForeignKey → User | Автор отзыва |
| `ad` | ForeignKey → Ad | Объявление |
| `created_at` | DateTimeField | Дата создания (авто) |

---

## 🌐 API Endpoints

### 🔐 Авторизация и пользователи
| Метод | Эндпоинт | Права | Описание |
|-------|---------|-------|---------|
| `POST` | `/users/token/` | Все | Получение JWT |
| `POST` | `/users/token/refresh/` | Все | Обновление токена |
| `POST` | `/users/register/` | Все | Регистрация |
| `GET` | `/users/` | Только админ | Список пользователей |
| `GET` | `/users/retrieve/{id}/` | Автор / Админ | Детали пользователя |
| `PATCH` | `/users/update/{id}/` | Автор / Админ | Обновить профиль |
| `DELETE` | `/users/destroy/{id}/` | Только админ | Удалить пользователя |
| `POST` | `/users/reset_password/` | Все | Сброс пароля (по email) |
| `POST` | `/users/reset_password_confirm/` | Все | Установка нового пароля |
---
### 📣 Объявления (`/ads/`)
| Метод | Эндпоинт | Права | Описание |
|-------|---------|-------|---------|
| `GET` | `/ads/` | Все | Список объявлений |
| `GET` | `/ads/retrieve/{id}/` | Авторизованный | Детали объявления |
| `POST` | `/ads/create/` | Пользователь | Создать объявление |
| `PATCH` | `/ads/update/{id}/` | Автор / Админ | Обновить объявление |
| `DELETE` | `/ads/destroy/{id}/` | Автор / Админ | Удалить объявление |

🔍 **Фильтрация:** `?title=...` — поиск по названию (регистронезависимо).  
📊 **Пагинация:** 4 объекта на страницу (настроена в `ads/pagination.py`).

---
### 💬 Отзывы (`/reviews/`)
| Метод | Эндпоинт | Права | Описание |
|-------|---------|-------|---------|
| `GET` | `/reviews/` | Авторизованный | Список всех отзывов |
| `GET` | `/reviews/retrieve/{id}/` | Только админ | Детали отзыва |
| `POST` | `/reviews/create/` | Пользователь | Оставить отзыв |
| `PATCH` | `/reviews/update/{id}/` | Автор / Админ | Редактировать отзыв |
| `DELETE` | `/reviews/destroy/{id}/` | Автор / Админ | Удалить отзыв |

---

## 🔐 Права доступа

Реализованы через кастомный `IsAdminOrAuthor`:

| Действие | Аноним | Пользователь | Админ |
|--------|--------|-------------|-------|
| Список объявлений | ✅ | ✅ | ✅ |
| Детали объявления | ❌ | ✅ | ✅ |
| Создать объявление | ❌ | ✅ | ✅ |
| Обновить объявление | ❌ | Только своё | ✅ Все |
| Удалить объявление | ❌ | Только своё | ✅ Все |
| Список отзывов | ❌ | ✅ | ✅ |
| Детали отзыва | ❌ | ❌ | ✅ |
| Оставить отзыв | ❌ | ✅ | ✅ |
| Редактировать отзыв | ❌ | Только своё | ✅ Все |
| Удалить отзыв | ❌ | Только своё | ✅ Все |

---

## 🧪 Тестирование

- Написаны **юнит- и интеграционные тесты** для:
  - CRUD объявлений и отзывов.
  - Проверка прав доступа.
  - Валидация данных (цена ≥ 0, пароль).
  - Сброс пароля (email, токен).  
Для их запуска выполните команду:
```sh
  coverage run --source='.' manage.py test   
```  
Для получения отчета о тестировании выполните команду:
```sh
  coverage html   
```
Отчет расположен по пути `htmlcov/index.html`

---

## 🐳 Docker

Проект упакован в Docker.  
Конфигурация находится в файлах:
- `Dockerfile` — сборка образа.
- `docker-compose.yml` — запуск сервисов (Backend + PostgreSQL).
- `nginx/Dockerfile` — сборка образа Nginx.
- `nginx/nginx.conf` — конфигурация Nginx.

---

## 📚 Документация API

Доступна по:
- **Swagger UI**: `http://localhost:8000/swagger/` в режиме разработка.
- **Swagger UI**: `http://localhost/swagger/` в Docker-compose.

---

## 🚀 Запуск проекта (разработка)

1. Установите [Poetry](https://python-poetry.org/docs/#installation):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/prime72rus/Graduation_project.git
   ```
   ```bash
   cd ads-board
   ```
3. Установите зависимости:
   ```bash
   poetry install
   ```
   Используется виртуальное окружение Poetry. Чтобы активировать: poetry shell  

4. Создайте базу данных PostgreSQL (через командную строку):
   ```bash
   sudo -u postgres psql
   ```
   ```bash
   CREATE DATABASE ads_db;
   CREATE USER postgres WITH PASSWORD 'postgres';
   ALTER ROLE postgres SET client_encoding TO 'utf8';
   ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
   ALTER ROLE postgres SET timezone TO 'Asia/Yekaterinburg';
   GRANT ALL PRIVILEGES ON DATABASE ads_db TO postgres;
   \q
   ```

5. Настройте переменные окружения:
   ```bash
   cp .env.example .env
   ```
   Отредактируйте .env с вашими данными (см. .env.sample).

6. Примените миграции:
   ```bash
   python manage.py migrate
   ```
   
7. Создайте суперпользователя (опционально):
   ```bash
   python manage.py createsuperuser
   ```
8. Запустите сервер:
   ```bash
   python manage.py runserver
   ```
9. Документация API доступна по:  
   Swagger UI: http://localhost:8000/swagger/  

---
## 🚀 Запуск проекта (Docker-compose)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/prime72rus/Graduation_project.git
   ```
   ```bash
   cd ads-board
   ```
2. Установите зависимости:
   ```bash
   poetry install
   ```
   Используется виртуальное окружение Poetry. Чтобы активировать: poetry shell  


3. Выполните сборку и запуск контейнеров Docker:
   ```bash
   docker-compose up -d
   ```

4. Создайте суперпользователя (опционально):
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```
   
5. Документация API доступна по:  
   Swagger UI: http://localhost/swagger/

---
## 📂 Структура проекта

ads_board/  
├── config/               # Настройки Django  
├── users/                # Пользователи, авторизация  
├── ads/                  # Объявления и отзывы  
├── nginx/                # nginx  
├── media/                # Загруженные файлы  
├── htmlcov/              # Покрытие тестами  
├── staticfiles/          # Статика  
├── .env.example          # Шаблон переменных окружения  
├── pyproject.toml        # Зависимости через Poetry  
├── poetry.lock           # Версии пакетов  
├── Dockerfile            # Сборка образа  
├── docker-compose.yml    # Запуск сервисов  
└── README.md             # Этот файл  


## 📎 Важные файлы
pyproject.toml — зависимости проекта.  
.env.example — шаблон переменных окружения.  
Dockerfile и docker-compose.yml — конфигурация контейнеров.  
nginx/Dockerfile - конфигурация контейнера nginx.
nginx/nginx.conf - конфигурация сервиса nginx.
config/settings.py — настройки Django, включая JWT, email, Swagger.  

## 📞 Поддержка
Разработчик: Dmitrii Grechko  
Email: prime72rus@gmail.com  
GitHub: https://github.com/prime72rus/
