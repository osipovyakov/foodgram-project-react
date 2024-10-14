# Сайт Foodgram
## Описание проекта
    Проект — сайт Foodgram, «Продуктовый помощник». Онлайн-сервис и API для 
    него. На этом сервисе пользователи смогут публиковать рецепты, подписываться 
    на публикации других пользователей, добавлять понравившиеся рецепты в список 
    «Избранное», а перед походом в магазин скачивать сводный список продуктов, 
    необходимых для приготовления одного или нескольких выбранных блюд.
	
# ![example workflow](https://github.com/osipovyakov//foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Запуск проекта на боевом сервере.

- Войти на удаленный сервер в облаке:
```
ssh <имя_пользователя>@<публичный_IP-адрес_виртуальной_машины>
```
- Остановить службу nginx:
```
sudo systemctl stop nginx
```
- Установить Docker и Docker Compose https://docs.docker.com/compose/install/:
```
sudo apt install docker-ce docker-compose -y
```
- В файле main.yml измените следующие строки:
```
tags: <логин_на_dockerhub>/<репозиторий_на_dockerhub:latest>
sudo docker pull <логин_на_dockerhub>/<репозиторий_на_dockerhub:latest>

```
- Скопировать файлы из проекта на сервер:
```
В облаке в home/<имя_пользователя>/ создать папку mkdir infra и mkdir docs
Скопировать из проекта:
infra/docker-compose.yaml и infra/dump.json в infra/,
docs/redoc.yaml и docs/openapi-schema.yml в в home/<имя_пользователя>/docs, 
nginx.conf в infra/nginx.conf
```
- Для подключения GitHub Actions необходимо создать директорию .github/workflows и скопировать в него main.yml

- В настройках репозитория Settings перейти в Secrets and variables -> Actions и 
добавить следующие переменные окружения, токены и пароли:
```
    DOCKER_USERNAME - имя_пользователя для подключения к dockerhub
    DOCKER_PASSWORD - пароль_пользователя dockerhub
    HOST - IP-адрес боевого сервера
    USER - имя_пользователя для подключения к боевому серверу
    SSH_KEY - приватный ключ с компьютера, имеющего доступ к боевому серверу (cat ~/.ssh/id_rsa)
    SECRET_KEY - секретный ключ в api_yamdb/settings.py
    DB_ENGINE - указываем, что работаем с postgresql (django.db.backends.postgresql) 
    DB_NAME - имя базы данных (postgres)
    POSTGRES_USER - логин для подключения к базе данных (postgres)
    POSTGRES_PASSWORD - пароль для подключения к БД (установите свой)
    DB_HOST - название сервиса (контейнера - db)
    DB_PORT - порт для подключения к БД (5432)
    TELEGRAM_ID - ID телеграм-аккаунта
    TELEGRAM_TOKEN - токен бота
```
- Сделать коммит и запушить его в удалённый репозиторий:
```
git commit -m 'комментарий'
git push 
```
- Перейти во вкладку Actions
- Результат выполнения workflow назван именем коммита
- Все steps успешно выполнились
- Войти на удаленный сервер в облаке:
```
ssh <имя_пользователя>@<публичный_IP-адрес_виртуальной_машины>
```
- Создать суперпользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
- Войти в админку создать одну-две записи объектов(рецептов)
- Создать дамп (резервную копию) базы данных:
```
sudo docker-compose exec backend python manage.py dumpdata > fixtures.json
```
- Файл fixtures.json сохранится в директорию /infra

## Административная панель Django доступна по адресу:

- http://<публичный_IP-адрес_виртуальной_машины>/admin/

## Докуметация по адресу:

- http://<публичный_IP-адрес_виртуальной_машины>/api/docs/

## Сайт Foodgram:

- http://<публичный_IP-адрес_виртуальной_машины>/

## Логин и пароль для админки
- login: admin@admin.com
- password: admin
