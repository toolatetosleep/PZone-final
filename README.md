# PZone

A Online Original Photography Community Django Web Project using Python 2.7 and MySQL 5

## How Can I set it up

I will show you how to set it up in Ubuntu in the following steps. The other systems are pretty much the same.

#### Python

Python is already installed in Ubuntu, If you don't have one, Try to apt-get one.

#### MySQL

```
    sudo apt-get install mysql-server
    sudo apt-get install mysql-client && sudo apt-get install libmysqlclient-dev
```

#### Pip

```
    sudo apt-get install python-pip
```

#### MySQLdb

To install MySQLdb, You may need to install Python2.7-dev first or it may go south.

```
    sudo apt-get install python2.7-dev
    sudo pip install mysql-python
```

#### Django

```
    sudo pip install Django==1.10.4
```

#### uWSGI

```
    sudo pip install uwsgi --upgrade
```

#### Pil

```
    sudo apt-get install python-imaging
```

#### Nginx

```
    sudo apt-get install python-dev nginx
```

#### Settings.py

Now, All the packages has been installed. Try to change the Database connections and static directories in the <code>Settings.py</code> to meet yours.

Like:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pzone',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/mydata/www/PZone/static/'

MEDIA_URL = '/upload/'
MEDIA_ROOT = '/mydata/www/PZone/upload/'

```

#### Manage.py

Run the manage file to create a superuser and colleting static files:

```
Python manage.py createsuperuser

Python manage.py collectstatic
```

#### Database

Use the sql file in the project to build the Database.

#### Nginx Config

And start a new Nginx Site configuration Like:

```
server {
    listen      80;
    server_name www.pzone.com;
    charset     utf-8;

    client_max_body_size 75M;
    access_log /mydata/www/PZone/log/access.log;
    error_log  /mydata/www/PZone/log/error.log;

    location /media  {
        alias /mydata/www/PZone/media;
    }

    location /static {
        alias /mydata/www/PZone/static;
    }

    location /upload {
        alias /mydata/www/PZone/upload;
    }

    location / {
        uwsgi_pass  unix:///mydata/www/PZone/pzone.sock;
        include     /etc/nginx/uwsgi_params;
    }
}

```

#### Run it

Run the shell script in the project to Start it and The site is on.

#### Initializing

Open the http://127.0.0.1/initdb to initialize the site and all is done.



