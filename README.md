# version-checker


## Presentation

Checks the version of a MONARC instance.

Which information does the browser request contain?

- HTTP referrer URL (local or public hostname);
- the MONARC version;
- the timestamp of the request;
- information about the browser (User-Agent: browser name, version, language
  and platform).

This is collected when a client hits a specific endpoint from
version.monarc.lu. The IP of the requestor is not stored, but a HTTP referrer
can contain a public or private IP.

This information provides better insights into where and how MONARC is used.


## Installation


```bash
$ git clone https://github.com/monarc-project/version-checker.git
$ cd version-checker/
$ npm install
$ pipenv install
$ pipenv shell
$ python src/manager.py db_create
$ python src/manager.py db_init
$ python src/manager.py create_admin <username> <password>
$ python src/runserver.py
```

### Deploy on Heroku

```bash
$ heroku create --region eu <name-of-your-instance>
$ heroku addons:add heroku-postgresql:hobby-dev
$ heroku config:set APPLICATION_SETTINGS='heroku.cfg'
$ heroku buildpacks:add --index 1 heroku/python
$ heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-nodejs
$ git push heroku master
$ heroku run init
$ heroku ps:scale web=1
```

#### Query the database with the command line tool

```bash
$ heroku run python src/manager.py logs MONARC
Running python src/manager.py logs MONARC on ⬢ monarc-version-checker... up, run.2944 (Free)

Software: MONARC
HTTP Referrer: http://127.0.0.1:5001/
Browser: chrome
Timestamp: 2018-07-05 11:47:36.127974
```


## License

This software is licensed under
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html)

- Copyright (C) 2018 Cédric Bonhomme
- Copyright (C) 2018 SMILE gie securitymadein.lu
