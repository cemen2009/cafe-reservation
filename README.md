# cafe-reservation

Django project for reservation tables in cafe in different cities

## Check it out!

https://cafe-reservation-g91q.onrender.com

## Installation

Python3 must be already installed

```shell
git clone https://github.com/cemen2009/cafe-reservation
cd cafe-reservation
python3 -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata alldata.json
python manage.py runserver # starts Django Server
```

admin:
* username: admin
* password: 1qazcde3

## Features

* Authentication functionality for visitors/user
* Managing reservations directly from website interface
* Reservation of tables in advance
* A lot of cities to reserve a table in cafe that you like

## Demo

![img.png](demo.png)
