# version-checker

## Presentation

This tool checks the version of a MONARC instance.

The goal is to reduce the problem of outdated MONARC servers. These servers are
a potentially security problem.

MONARC users who open the home page in the web interface will see an image in
the bottom left corner with the text "up-to-date" in green, "update available"
in orange  or "security update available" in red.
This will make outdated version more visible for user of a MONARC instance.

When the home page is loaded, the browser of the user requests an image file
from version.monarc.lu.
The browser request tells version.monarc.lu the MONARC version which is
currently running and it responds with the appropriate image so the user can
see if the MONARC version is up to date. The version number sent in the request
is encrypted.

The SVG image is rendered by version.monarc.lu. This way we are for example
able to write a CVE id in the image.

Information from the browser request that are stored:

- HTTP referrer URL (local or public hostname);
- the MONARC version;
- information about the browser (User-Agent: browser name, version, language
  and platform).

The timestamp of the request is also kept.

The IP of the requestor is never stored.
Of course an HTTP referrer can be an IP (public or private). And since an HTTP
referrer can be easily spoofed, it is impossible to be completely sure if any
derived information is actually valid.

This information provides better insights into where and how MONARC is used.
Only the CASES team has access to this database. MONARC users have always the
choice to Opt-out.

This tool has been designed to work with any software, not only MONARC.


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
