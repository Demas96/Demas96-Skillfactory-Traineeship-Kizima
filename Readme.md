Данное API (DRF) предназначено для спортивно-туристического мобильного приложения.

Адреса для работы с API:
http://127.0.0.1:8000/submitData/ - POST запрос в формате JSON. 
Пример:
{
  "beauty_title": "пер.",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
 
  "add_time": "2021-09-22 13:18:13",
  "user": {
    "email": "qwerty@mail.ru",
    "fam": "Пупкин",
	"name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"}, 
 
  "coords":{
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"},
 
  "level":{
        "winter": "", 
        "summer": "1А",
        "autumn": "1А",
        "spring": ""},
 
"images": [
    {
        "data":"<картинка1>", 
        "title":"Седловина"}, 
    {
        "data":"<картинка>", 
        "title":"Подъём"
    }
    ]
}

http://127.0.0.1:8000/submitData/<id>/ - GET запрос, для вывода записи с id перевала, PATCH запрос в формате JSON, для изменения записи с id перевала
http://127.0.0.1:8000/submitData/user__email=<email> - GET запрос для вывода всех записей пользователя по email