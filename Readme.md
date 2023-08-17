## Requirements
 - `OpenSSL`
 - `Python 3.8+`
 - `Django 4.2`

## Installation
### Create virtual environment
```shell
$ python3 -m venv .venv
```
### Activate venv
- In windows
```shell
$ .\.venv\Scripts\activate
```

- In Linux
```shell
$ source .venv/bin/activate
```
### Install requirements (libraries)
```shell
$ pip install -r requirements.txt
```
### Copy environment variables
```shell
$ cp .env.example .env
```
Edit `.env` file.

### Django database migrations
```shell
$ python manage.py makemigrations
$ python manage.py migrate
```

### Django createsuperuser
```shell
$ python manage.py createsuperuser
```

## Notes
Check the `OpenSSL`:
```shell
$ openssl version
```
If you have `OpenSSL 3.1+` version you are fine.
 
If `OpenSSL` is not installed on your computer install it:
 - Debian/Linux
 ```shell
$ sudo apt install openssl
```
 - In Windows: [Official OpenSSL download page](https://www.openssl.org/source/)

## Running
```shell
$ python manage.py runserver
```

