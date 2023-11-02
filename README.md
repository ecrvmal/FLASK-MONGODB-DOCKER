# Микросервис уведомления пользователей. 

Микросервис представляет из себя RestAPI сервер, который создавает записи уведомления
в документе пользователя в MongoDB, отправляет email, 
а так же предоставляет листинг уведомлений из документа пользователя.

Уведомления пользователей храняться в поле в документе пользователя
и их максимальное кол-во ограничено (лимит можно установить произвольный)

При отправке Email отпраляестя key от создаваемого уведомления.


## Project stack:
- Flask
  - werkzeug
  - requests
  - pymongo
  - email
- MongoDB



## Implementation with docker-compose:
### 1. Correct file myapp/variables.py
enter correct data

### 2. Create & run docker image
```shell
docker compose up
```
### 3. Access to server
Access to server on port 5000 
The port can be configured in file variables.py

### 4. For DB Initiation:
For DB Initiation after server starts to access to DB need to run "client" app
and perform:
- press "P" for post
- press "R" for registration
By this you will create first record for user.

## Client
### Client start
to start client please un commands:
```shell
pip install pprint
pip install requests
python client/client/py
```

### Client operations:
#### 1-st level menu: 
[G]et or [P]ost or [Q]uit or lis[T] ? : 

[Q] - for exit program
[T] - for full list of records in DB

#### 2-nd level menu on GET:
Enter User_ID (or all) :
need to enter user_id (3-letter for test)  or "all"

#### 2-nd level menu on Post:
[R]egistration | new_[M]essage | new_[P]ost | new_[L]ogin | rea[D] | [Q]uit  : 
need to enter
- [R] - for registration , 3-digit user_id is generating automatically
- [M] - for new message , later need to enter 3-digit user_id  and message text
- [P] - for new post , later need to enter 3-digit user_id  and post text
- [L] - for new Login , later need to enter 3-digit user_id  (sending mail to admin)
- [D] - for mark message as "Read" , later need to enter 3-digit user_id
- [Q] - for return to 1-st level menu

# Operation datails:
## Для целей тестирования используются 3-символьные идентификаторы пользователей и записей
## Установку можно изменть в файле variables.py

#### Пример уведомления в документе пользователя

```json
{
    "id": "some_notification_id",
    "timestamp": 1698138241,
    "is_new": false,
    "user_id": "638f394d4b7243fc0399ea67",
    "key": "new_message",
    "target_id": "0399ea67638f394d4b7243fc",
    "data": {
        "some_field": "some_value"
    },
},
```

Для теста в случае отсутствия пользователя следует создать новый профиль с email, который задан через параметры.

## Переменные окружения, через которые конфигурируется сервис

- PORT - порт на котором будет работать приложение
- EMAIL - тестовый email
- DB_URI - строка для подключения к mongoDB
- SMTP_HOST - хост smtp сервера
- SMTP_PORT - порт smtp сервера
- SMTP_LOGIN - логин пользователя
- SMTP_PASSWORD - пароль пользователя
- SMTP_EMAIL - email с которого будет отправлено сообщение
- SMTP_NAME - Имя отображаемое у получателя письма

## API Handlers: 

### [POST] /create создает новое уведомление.

#### Тело запроса:

- user_id - строка на 24 символа (является ObjectID документа пользователя которому отправляется уведомление)
- target_id - строка на 24 символа (является ObjectID документа сущности, к которой относится уведомление) (Может отсутствовать)
- key - ключ уведомления enum
    - registration (Только отправит пользователю Email)
    - new_message (только создаст запись в документе пользователя)
    - new_post (только создаст запись в документе пользователя)
    - new_login (Создаст запись в документе пользователя и отправит email)
- data - произвольный объект из пар ключ/значение (Может отсутствовать)

#### Пример тела запроса:

```json
{
    "user_id": "638f394d4b7243fc0399ea67",
    "key": "registration",
}
```

#### Пример ответа

HTTP 201 Created

```json
{
    "success": true,
}
```

### [GET] /list производит листинг уведомлений пользователя.

#### query params
- user_id [string] - идентификатор пользователя
- skip [int] - кол-во уведомлений, которые следует пропустить
- limit [int] - кол-во уведомлений которые следует вернуть

#### Пример ответа

HTTP 200 Ok

```json
{
    "success": true,
    "data": {
        "elements": 23, // всего уведомлений
        "new": 12, // Кол-во непрочитанных уведомлений
        "request": {
            "user_id": "638f394d4b7243fc0399ea67",
            "skip": 0,
            "limit": 10,
        }
        "list": [
            {
                "id": "some_notification_id",
                "timestamp": 1698138241,
                "is_new": false,
                "user_id": "638f394d4b7243fc0399ea67",
                "key": "new_message",
                "target_id": "0399ea67638f394d4b7243fc",
                "data": {
                    "some_field": "some_value"
                },
            },
            ...
        ]
    }
}
```

#### [POST] /read создает отметку о прочтении уведомления.

#### query params
- user_id [string] - идентификатор пользователя
- notification_id [string] - Идентификатор уведомления

#### Пример ответа

HTTP 200 Ok

```json
{
    "success": true,
}
```


## LICENSE
license: MIT


