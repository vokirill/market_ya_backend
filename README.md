Устанавливаем pip
sudo apt-get install python3-pip
Устанавливаем virtualenv
sudo pip3 install virtualenv
Создаем среду
virtualenv venv
активируем среду и заходим в ее папку
.  /venv/bin/activate
cd venv
Копируем файлы проекта на виртуальную машину
scp /path/to/file username@a:/path/to/destination
Устанавливаем необходимые пакте
pip install -r requirements.txt
Проверяем хорошо ли установился uwsgi. Создаем файл test_uwsgi.py в который кладем следующий код
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]
    
Запускаем uWSGI:
uwsgi --http :8000 --wsgi-file test.py

В браузере переходим по адресу IP:8000.
Видим: «Hello, world», значит, мы все сделали правильно и следующие компоненты работают:

Проверка Django
запускаем тесты
python manage.py
если все хорошо, то запускаем проект
python manage.py runserver 0.0.0.0:8000

Для  запуска проекта при старте операциаонной системы устанавливаем uWSGI глобально
Деактивируем виртуальное окружение:
deactivate
Устанавливаем uwsgi:
sudo pip install uwsgi

в папке проект создаем файл project_name_uwsgi.ini  по шаблону 
#mysite_uwsgi.ini 
[uwsgi]
chdir           = /path/to/your/project
 Django wsgi файл
module          = project.wsgi
полный путь к виртуальному окружению
home            = /path/to/virtualenv
 общие настройки
 master
master          = true
максимальное количество процессов
processes       = 10
 полный путь к файлу сокета
socket          = /path/to/your/project/mysite.sock
очищать окружение от служебных файлов uwsgi по завершению
vacuum          = true

выполняем следующие команды
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals
sudo uwsgi --emperor /etc/uwsgi/vassals --uid www
(www - id пользователя id -u username)

В файл /etc/rc.local, перед строкой “exit 0” добавляем:
/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www

Запускаем проект 
uwsgi --ini project_name_uwsgi.ini














