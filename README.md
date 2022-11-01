### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/HegoZz/eresh.git
```
```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```

Для доступа к админке, запустить проект:
```
python3 manage.py runserver
```

И после зайти с браузера по адресу:
```
http://127.0.0.1:8000/admin/
```

Для запуска бота, создать файл с именем '.env' в корневом каталоге;
создать в нём константу TOKEN;
присвоить константе значение токена бота;
выполнить команду 
```
python3 manage.py bot
```
