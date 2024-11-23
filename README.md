**Django News Portal**
=====================

Новостной портал на Django
-------------------------

Проект представляет собой простой новостной портал, написанный на Django. Он позволяет создавать, редактировать и удалять новости, а также просматривать их в удобном виде.
К данному новостному сайту есть API со Swagger документацией.

### Функционал

* Создание, редактирование и удаление новостей
* Просмотр новостей в виде списка или отдельной страницы, поиск новостей по категориям и не только
* Возможность подписаться на категории с последующей рассылкой новых новостей по этой категории
* Еженедельная рассылка новостей
* Локализация сайта (en, ru)
* Возможность выбора временной зоны
* Разное оформление в зависимости от времени суток

### Установка

#### Шаг 1: Клонировать репозиторий
```bash
git clone https://github.com/DyachkovaD/django_news_portal.git
```

#### Шаг 2: Перейти в папку с проектом
```bash
cd django_news_portal
```

#### Шаг 3: Установить зависимости
```bash
pip install -r requirements.txt
```

#### Шаг 4: Запустить миграции
```bash
python manage.py migrate
```

#### Шаг 5: Запустить сервер
```bash
python manage.py runserver
```

### Использование

#### Шаг 1: Открыть в браузере
Откройте в браузере адрес [http://localhost:8000/](http://localhost:8000/)

#### Шаг 2: Зарегистрироваться или авторизоваться
Зарегистрируйтесь или авторизуйтесь на сайте

#### Шаг 3: Создать новость
Создайте новость, указав ее название, текст и категорию

#### Шаг 4: Просмотреть новости
Просмотрите новости в списке или на отдельной странице

### Требования

* Python 3.8+
* Django 3.2+
* DRF
* SQLite (по умолчанию)
* Celery
* gettext
* locale

### Автор

* [DyachkovaD](https://github.com/DyachkovaD)