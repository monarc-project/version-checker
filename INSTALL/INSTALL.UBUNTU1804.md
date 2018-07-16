# Requirements

Install PostgreSQL and NPM:

```bash
$ sudo apt install postgresql npm
```

Install [pyenv](https://github.com/pyenv/pyenv),
then [pipsi](https://github.com/mitsuhiko/pipsi). Then:

```bash
$ pyenv install 3.7.0
$ pyenv global 3.7.0
$ pipsi install pipenv
```


Installation and configuration of version-checker:

```bash
$ git clone https://github.com/monarc-project/version-checker.git
$ cd version-checker/
$ npm install
$ pipenv install
$ pipenv shell

$ cp src/data/software.py.example src/data/software.py

$ cp src/instance/production.cfg  src/instance/prod.cfg
$ vim src/instance/prod.cfg
$ export APPLICATION_SETTINGS=prod.cfg
$ sudo -u postgres createuser <db-user> --createdb
$ echo "ALTER USER <db-user>  WITH ENCRYPTED PASSWORD '<db-user-password>';" | sudo -u postgres psq
$ python src/manager.py db_create
$ python src/manager.py db_init

$ python src/manager.py create_admin <username> <password>
$ python src/runserver.py
```

