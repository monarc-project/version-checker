# System requirements

Install PostgreSQL and NPM:

```bash
sudo apt install postgresql npm build-essential
```


# Setting your Python environment

Install [pyenv](https://github.com/pyenv/pyenv),
then [pipsi](https://github.com/mitsuhiko/pipsi).
Then install pipenv:


```bash
$ pyenv install 3.7.0
$ pyenv global 3.7.0
$ pipsi install pipenv
```


# Configuration

```bash
$ git clone https://github.com/monarc-project/version-checker.git
$ cd version-checker/
$ npm install
```


Software are defined in ''src/data/software.py''. Edit this file accordingly
to your need:

```bash
$ cp src/data/software.py.example src/data/software.py
```

Configure the connection to the database and initialize it:

```bash
$ cp src/instance/production.cfg  src/instance/prod.cfg
$ vim src/instance/prod.cfg
$ export APPLICATION_SETTINGS=prod.cfg
$ sudo -u postgres createuser <db-user> --createdb
$ echo "ALTER USER <db-user>  WITH ENCRYPTED PASSWORD '<db-user-password>';" | sudo -u postgres psq

$ pipenv install
$ pipenv shell
$ python src/manager.py db_create
$ python src/manager.py db_init

$ python src/manager.py create_admin <username> <password>
```

Run the server:

```bash
$ python src/runserver.py
```

