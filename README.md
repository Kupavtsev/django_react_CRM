<!-- django_react_CRM -->
https://www.youtube.com/watch?v=DiSoVShaOLI

<!-- User Registration -->
https://www.youtube.com/watch?v=tUqUdu0Sjyc&t=504s

<!-- API Token -->
https://www.youtube.com/watch?v=Wq6JqXqOzCE&t=504s

admin
admin@admin.ru
admin

ToDo
v- admin webservice
v- login to this admin
v- postgres
v- bot
v- При создании клиента, должно передаваться имя залогиненого пользователя (email)
v- Авторизация по Токену из Реакт фронтенд

Регистрация и авторизация через БОТ
    Есть два пути API или локально через БД
Закрыть доступ, только для авторизованных пользователей, со стороны сервера
    Рекат принимает токен во время авторизации и помещает в локальное хранилище
    использет его для для запросов на сервер

/frontend npm start
./manage.py run_bot
./manage.py runserver

Опимание особых моментов
bot пуляет даннае на прямую в БД, поэтому ему не нужен Токен!
И значит проверку пользователя Телеги, надо делать на прямую из БД?!
