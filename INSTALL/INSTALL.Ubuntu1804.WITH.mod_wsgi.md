
Follow the instructions in [INSTALL.UBUNTU1804.md](INSTALL.UBUNTU1804.md)
but be careful to use Python 3.6 for mod_wsgi.


# Configure the application for a production environment

```bash
$ cp src/instance/production.cfg  src/instance/prod.cfg
$ export APPLICATION_SETTINGS=prod.cfg
```

# Configure mod_wsgi for Python 3.6


```bash
$ pyenv install 3.6.6
$ pyenv global 3.6.6
$ cd /var/wwww/version.monarc.lu/
$ pipenv install
$ pipenv shell
$ python src/manager.py db_create
$ python src/manager.py db_init
```

```bash
$ sudo apt install apache2 libapache2-mod-wsgi-py3
$ cp webserver.wsgi.example webserver.wsgi
```

Edit webserver.wsgi accordingly with the path of your Python virtualenv. Here
is an example:

```python
#! /usr/bin/env python

import sys

sys.path.insert(0, '/var/wwww/version.monarc.lu/src/')

python_home = '/home/user/.local/share/virtualenvs/version-checker--AuKpeUm'

activate_this = python_home + '/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from runserver import application
```


# Configuration of a VirtualHost

```conf
<VirtualHost *:80>
    ServerName version.monarc.lu

    ServerAdmin webmaster@localhost
    DocumentRoot /var/wwww/version.monarc.lu/

    WSGIDaemonProcess versionchecker user=www-data group=www-data threads=5 python-home=/home/user/.local/share/virtualenvs/version-checker--AuKpeUm/
    WSGIScriptAlias / /var/wwww/version.monarc.lu/webserver.wsgi

    <Directory /var/wwww/version.monarc.lu/>
        WSGIApplicationGroup %{GLOBAL}
        WSGIProcessGroup versionchecker
        WSGIPassAuthorization On

        Options Indexes FollowSymLinks
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```


# Enable HTTPS

```bash
sudo apt install letsencrypt python-certbot-apache
```
