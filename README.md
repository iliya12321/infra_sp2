## REST API YamDB - база отзывов о фильмах, музыке и книгах

## Используемые технологии
![Alt-Текст](https://img.shields.io/badge/python-3.9-blue)
![Alt-Текст](https://img.shields.io/badge/django-2.2.16-blue)
![Alt-Текст](https://img.shields.io/badge/djangorestframework-3.12.4-blue)
![Alt-Текст](https://img.shields.io/badge/docker-20.10.16-blue)
![Alt-Текст](https://img.shields.io/badge/nginx-1.21.3-blue)
![Alt-Текст](https://img.shields.io/badge/gunicorn-20.0.4-blue)

## Описание

Это практическое задание, выполненное в ходе подготовки к командной работе.

## Результат

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр (Genre) из списка предустановленных. Новые жанры может создавать только администратор. Пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

## Как запустить проект:

Клонировать репозиторий:

- Создайте `.env` файл в директории `infra/`, в котором должны содержаться следующие переменные:
    >DB_ENGINE=django.db.backends.postgresql\
    >DB_NAME= # название БД\ 
    >POSTGRES_USER= # ваше имя пользователя\
    >POSTGRES_PASSWORD= # пароль для доступа к БД\
    >DB_HOST=db\
    >DB_PORT=5432\

Перейти в папку infra и запустить docker-compose.yaml
(при установленном и запущенном Docker)
```
cd infra_sp2/infra
```

## Соберите и запустите контейнер с помощью Docker-compose
(находясь в папке infra, при запущенном Docker)
```
docker-compose build
docker-compose up
```
## Выполните миграции через Docker-compose
```
docker-compose exec web python manage.py makemigrations --noinput  
docker-compose exec web python manage.py migrate --noinput
```
## Соберите через Docker-compose статику
```
docker-compose exec web python manage.py collectstatic --no-input
```
## Создайте суперпользователя
```
docker-compose exec web python manage.py createsuperuser
```
## Заполнить базу начальными данными
```
docker-compose exec web python manage.py loaddata fixtures.json
```

Проверьте работоспособность приложения, для этого перейдите на страницу:

```
 http://localhost/admin/
```

***Документация*** (запросы для работа с API):

```
 http://localhost/redoc/
```
