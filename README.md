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

### Deploy locally

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
$ heroku run python src/manager.py create_admin <username> <password>
$ heroku ps:scale web=1
```

#### Query the database with the command line tool

```bash
$ heroku run python src/manager.py logs MONARC
Running python src/manager.py logs MONARC on ⬢ monarc-version-checker... up, run.2944 (Free)

Software: MONARC
Software version: 2.5.0
HTTP Referrer: http://127.0.0.1:5001/
Browser: chrome
Timestamp: 2018-07-05 12:07:58.746161

Software: MONARC
Software version: 2.5.0
HTTP Referrer: None
Browser: firefox
Timestamp: 2018-07-05 12:08:09.234619
```

## Usage

### Checking the version of a software

```bash
$ curl https://monarc-version-checker.herokuapp.com/check/MONARC?version=2.5.0
<?xml version="1.0" encoding="utf-8" ?>
<svg baseProfile="full" height="20" version="1.1" width="95" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><rect fill="green" height="20" width="95" x="0" y="0" /><g fill="white" font-family="DejaVu Sans" font-size="14"><text fill="white" font-weight="bold" x="5" y="15">up-to-date</text></g></svg>

$ curl https://monarc-version-checker.herokuapp.com/check/MONARC?version=2.4.0
<?xml version="1.0" encoding="utf-8" ?>
<svg baseProfile="full" height="20" version="1.1" width="140" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><rect fill="orange" height="20" width="140" x="0" y="0" /><g fill="white" font-family="DejaVu Sans" font-size="14"><text fill="white" font-weight="bold" x="5" y="15">update available</text></g></svg>
```

A SVG picture is rendered so that it is possible to include it in a Web page.

### Asking about version information for a software

```bash
$ curl https://monarc-version-checker.herokuapp.com/version/MONARC
{"stable":"2.5.0"}

$ curl -sD - https://monarc-version-checker.herokuapp.com/version/monarc
HTTP/1.1 404 NOT FOUND
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Content-Length: 17
Server: Werkzeug/0.14.1 Python/3.6.6
Date: Thu, 05 Jul 2018 13:25:55 GMT
Via: 1.1 vegur

Unknown software.
```

The information sent by the client browser is only stored when the *check*
endpoint is reached.


### Query the database

```bash
curl http://127.0.0.1:5000/admin/logs/export?software=MONARC&software_version=2.5.0
```

The result will be a CSV file.


## License

This software is licensed under
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html)

- Copyright (C) 2018 Cédric Bonhomme
- Copyright (C) 2018 SMILE gie securitymadein.lu
