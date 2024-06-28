# Petro_public
Сайт для онлайн-школы развития креативных навыков у детей и подростков.


## Варианты запуска проекта.
### 1. Сборка/запуск простого контейнера с проектом для разработки
Для сборки контейнера необходимы:
- папка git_con с содержимым
- Dockerfile.lite
- docker-compose.yml
- .env.lite

Сборка/запуск контейнера командой:
```sh
sudo docker-compose -f docker-compose.yml up --build
```

Запускается один контейнер.\
Содержимое папки проекта "app" подтягивается с Github  непосредственно в контейнер на стадии сборки.\
Сайт работает с внутренней БД db.sqlite3 (SQLite).\
Сайт отвечает на порту 8000 (от django).


### 2. Сборка/запуск контейнера в продакшене
Для сборки контейнеров необходимы:
- папка git_con с содержимым
- Dockerfile.prod
- docker-compose.prod.yml
- nginx.conf
- .env

Сборка/запуск контейнеров командой:
```sh
sudo docker-compose -f docker-compose.prod.yml up --build
```

Запускаются 4 контейнера:
- django-web 
- db - DB Postgres
- pgAdmin - управление для Postgres - отдаётся через порт 8050
- nginx  - отдаётся через порт 8080

Содержимое папки проекта "app" подтягивается с Github непосредственно в контейнер на стадии сборки.\
Сайт работает с DB Postgres из контейнера.\
Сайт отвечает на порту 8080 (gunicorn через nginx-proxy).\
При запуске проводятся миграции и сборка статических файлов.\
Папки проекта static и media синхронизируются с nginx через docker.

### 4. Запуск проекта в продакшене
Для запуска контейнеров необходимы:
- docker-compose.img.yml
- nginx.conf
- .env

Запуск контейнеров командой:
```sh
sudo docker-compose -f docker-compose.img.yml up
```


### Окружение разработки
- asgiref==3.7.2
- Django==4.2.5
- python-dotenv==1.0.0
- django-appconf==1.0.5
- django-bootstrap5==23.3
- django-cookie-consent==0.4.0
- django-markdownify==0.9.3
- django-phonenumber-field[phonenumberslite]==7.2.0
- psycopg2-binary==2.9.8
- requests==2.31.0
- Pillow==10.0.1
- pytz==2023.3
- PyYAML==6.0.1
- sqlparse==0.4.3

- gunicorn==21.2.0

- python 3.11.5
- vUbuntu Server 22_04.
