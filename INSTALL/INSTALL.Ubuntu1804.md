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

## JavaScript dependencies

```bash
$ git clone https://github.com/monarc-project/version-checker.git
$ cd version-checker/
$ npm install
```

## Software

Software are defined in ''src/data/software.py''. Edit this file accordingly
to your need:

```bash
$ cp src/data/software.py.example src/data/software.py
```

## Database

Configure the connection to the database and initialize it:

```bash
$ cp src/instance/production.cfg.example  src/instance/production.cfg
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

## RSA key pair

version-checker only needs the private key:

```bash
$ openssl genrsa -out rsa_4096_priv.pem 4096
$ cp rsa_4096_priv.pem src/data/privatekey.pem
```

This private key will be used in order to decrypt the software version which
will be sent by the client.

### Encrypt the software version in the client side

```bash
$ openssl rsa -pubout -in rsa_4096_priv.pem -out rsa_4096_pub.pem
$ cat rsa_4096_pub.pem
```

Example with node-forge:

```javascript
var publicKey = forge.pki.publicKeyFromPem('-----BEGIN PUBLIC KEY-----' +
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' +
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' +
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' +
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' +
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' +
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' +
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' +
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' +
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' +
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX==' +
    '-----END PUBLIC KEY-----');
var encrypted = publicKey.encrypt(self.config.appVersion, "RSA-OAEP", {
    md: forge.md.sha256.create(),
    mgf1: forge.mgf1.create()
});
var base64encrypted = encodeURIComponent(forge.util.encode64(encrypted));
```

The client will uses the encrypted value like this:

```bash
GET /check/MONARC?version=<base64encrypted>&timestamp=1532069103899
```



# Run the server

```bash
$ python src/runserver.py
```
