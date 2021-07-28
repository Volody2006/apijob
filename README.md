# Какие pre-install зависимости нужны.
На сервере должен быть установлен doker, docker-compose
`sudo apt install doker docker-compose`

# Как собрать и развернуть проект.
```
docker-compose up -d
docker-compose run django python manage.py migrate
``````

# Как запустить тесты.
```
docker-compose up -d
docker-compose run django python manage.py test
docker-compose run django flake8
docker-compose down
``````

# Остановить контейнеры
`docker-compose down`

# Архитектура.
Сервис состоит из контейнеров:
- rabbitmq - очередь задач
- postgres - база данных
- django - веб приложение
- celery - фоновая обработка долго выполняющихся задач. Если очередь задач привышает допустимые значения, то достаточно запустить еще один контейнер celery

| Url          | Метод | Данные                                                                                             | Ответ                                                                                                                    |
|--------------|-------|----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| /jobs/       | GET   |                                                                                                    | Список job                                                                                                               |
| /jobs/       | POST  | 'image_filter',  'severity',  'rotate',  'value_hue',  'value_saturation', 'per_channel', 'file' |  перенаправление на /jobs/ID/                                                                                                              |
| jobs/ID/ | GET   |                                                                                                    | Job c полями 'url',   'status',  'image_filter'  Если задача имеет завершенный статус то и ссылку на изображение 'file'  |
