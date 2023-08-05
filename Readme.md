## Setup


Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Then run these commands:

```sh
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```

Use this command to create superuser

```sh
(env)$ python manage.py createsuperuser
```

Once `pip` has finished downloading the dependencies:

```sh
(env)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.



```sh
APIs:

```
