
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

## Running
```shell
$ python manage.py runserver
```

