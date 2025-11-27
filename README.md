# Django AuthZ System

Django-проект, связанный с системой аутентификации и авторизации пользователей. Этот проект представляет собой серверную часть веб-приложения, предназначенного для реализации собственного механизма аутентификации и авторизации. Основная цель — создание настраиваемого решения разграничения прав доступа для сложных корпоративных приложений, управляемого вручную через административную панель.

## Основные возможности

### Работа с пользователями:
- Регистрация новых пользователей с указанием имени, фамилии, отчества, электронной почты и пароля.
- Авторизация пользователей по электронной почте и паролю.
- Возможность редактирования своего профиля.
- Безопасное удаление учетных записей («мягкое удаление»), без физического удаления данных из базы.

### Система управления доступом:
- Создание произвольных ролей (например, администратор, редактор, читатель).
- Назначение конкретных разрешений пользователям (просмотр, изменение, удаление).
- Управление ролями и полномочиями через административный интерфейс.

## Структура проектирования

### Модели:
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

class Role(models.Model):
    name = models.CharField(max_length=100)

class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    resource = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
```

### Проверка доступа к ресурсам:
Система проверяет наличие необходимого разрешения перед выполнением каждого запроса:
- Если пользователь не авторизован → ошибка HTTP 401 (`Unauthorized`).
- Если пользователь авторизован, но запрашиваемый ресурс недоступен → ошибка HTTP 403 (`Forbidden`).

## Установка и запуск проекта

### Требования к среде:
- Python >= 3.8
- База данных: PostgreSQL или SQLite (для локального тестирования)
- Docker (не используется)

### Шаги установки:
1. Склонируйте репозиторий:
```bash
git clone https://github.com/VladimirElsukov/django-authz-system.git
cd django-authz-system
```

2. Настройте виртуальное окружение и установите зависимости:
```bash
python -m venv env
source env/bin/activate  # Linux/MacOS
env\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Создайте файл настроек окружения:
```bash
cp .env.example .env
```

4. Чтобы установить Django, выполните следующую команду в терминале:
   
```
bash
pip install django
Эта команда установит последнюю доступную версию Django. Если вам нужна определенная версия, укажите её явно:

```
bash
Копировать
pip install django==X.Y.Z
```
Замените X.Y.Z на нужную версию Django.

Проверка установки
Для проверки успешной установки Django выполните команду:

```
bash
Копировать
django-admin --version
```
Она выведет установленную версию Django.

5. Для установки пакета Django REST framework (DRF) выполните следующую команду в терминале вашей среды разработки Python/Django:
```
pip install djangorestframework
```

6. Проведите первоначальные миграции базы данных:
```bash
python manage.py migrate
```

7. Запустите сервер разработки:
```bash
python manage.py runserver
```

### Тестирование
Тестовые данные для демонстрации возможностей системы:
- Создать собственного суперпользователя python manage.py createsuperuser (вход по email)
- Создать со страницы браузера новых тестовых пользователей, например:  `admin@example.com`, `editor@example.com`
- Пароль: одинаковый — `password`
- Роли и права доступа для ресурсов выбираются суперпользователем из админпанели.


## Итоговая архитектура проекта

Файлы организованы следующим образом(здесь не указано, что базовый шаблон и шаблон главной страницы вынесены в корень проекта, остальные шаблоны в самом приложении):

```shell
django-authz-system/
│
├── authz_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── db.sqlite3
├── manage.py
├── .env.example
├── requirements.txt
└── README.md
```

---

### Дополнительные заметки:
- Полноценная обработка ошибок 401 и 403 должна быть выполнена в ваших представлениях (view-функциях).
- Предложенная структура допускает простое расширение путем добавления новых ролей и действий.

---

Автор проекта: Владимир Елусков  
Обратная связь и поддержка приветствуются.



















