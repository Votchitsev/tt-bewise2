# Тестовое задание
#### API сервис, с помощью которого можно конвертировать аудио файлы
-------------------------------

<details><summary> Задача: </summary>
Необходимо реализовать веб-сервис, выполняющий следующие функции:
- Создание пользователя;
- Для каждого пользователя - сохранение аудиозаписи в формате wav, преобразование её в формат mp3 и запись в базу данных и предоставление ссылки для скачивания аудиозаписи.

### Детализация задачи:

- С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно - PostgreSQL). Предоставить все необходимые скрипты и конфигурационные (docker/compose) файлы для развертывания СУБД, а также инструкции для подключения к ней. Необходимо обеспечить сохранность данных при рестарте контейнера (то есть - использовать volume-ы для хранения файлов СУБД на хост-машине.
- Реализовать веб-сервис со следующими REST методами:
  - Создание пользователя, POST:
  - Принимает на вход запросы с именем пользователя;
  - Создаёт в базе данных пользователя заданным именем, так же генерирует уникальный идентификатор пользователя и UUID токен доступа (в виде строки) для данного пользователя;
  - Возвращает сгенерированные идентификатор пользователя и токен.
- Добавление аудиозаписи, POST:
  - Принимает на вход запросы, содержащие уникальный идентификатор пользователя, токен доступа и аудиозапись в формате wav;
  - Преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и сохраняет их в базе данных;
  - Возвращает URL для скачивания записи вида http://host:port/record?id=id_записи&user=id_пользователя.
- Доступ к аудиозаписи, GET:
  - Предоставляет возможность скачать аудиозапись по ссылке из п 2.2.3.
- Для всех сервисов метода должна быть предусмотрена предусмотрена обработка различных ошибок, возникающих при выполнении запроса, с возвращением соответствующего HTTP статуса.
- Модель данных (таблицы, поля) для каждого из заданий можно выбрать по своему усмотрению.
- В репозитории с заданием должны быть предоставлены инструкции по сборке докер-образа с сервисами из пп. 2. и 3., их настройке и запуску. А также пример запросов к методам сервиса.
- Желательно, если при выполнении задания вы будете использовать docker-compose, SQLAlchemy,  пользоваться аннотацией типов.
</details>

## Запуск проекта

Для запуска выполните следующие действия:
```
git clone https://github.com/Votchitsev/tt-bewise2.git
```

```
cd tt-bewise2/
```
```
docker-compose up
```

Проект будет запущен по адресу ```http://localhost:8008```

### Создание пользователя

Для создания пользователя нужно отправить POST-запрос на ```/auth```. В теле запроса указывается имя пользователя. При успешном создании пользователя вернётся ответ в теле которого будут содержаться идентификатор пользователя и уникальный ключ.
```
POST /auth

{
  name: username
}

RESPONSE 

{
  "id": 11,
  "uuid": "d5492088-0129-11ee-82ea-0242ac130003"
}
```

### Загрузка файла на сервер

Для загрузки файла отправляется запрос на ```/upload```. ```Content-type``` запроса должен быть ``` Multipart/form-data```.

```
POST /upload

{
  id: 11,
  uuid: "d5492088-0129-11ee-82ea-0242ac130003",
  file: file
}

RESPONSE

{
  url: ссылка для скачивания
}

```

### Скачивание файла

Скачивание загруженного файла производится по полученной после загрузки ссылке