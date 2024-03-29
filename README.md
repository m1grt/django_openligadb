# Simple Django app for Openligadb API
> Show different data about games in the league.

1. Current ranking of the teams.
2. Following matches for the weekend to come.
3. All matches from current season.
4. Search function by team.

## Installation

Project is based on python 3.10 with Django 3.2.5

You can setup and run it in a virtual environment.

```in my ~/.bash_profile
export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.10
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/bin/virtualenv2
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
source /usr/bin/virtualenvwrapper.sh
```

then
```sh
source ~/.bash_profile
```

Linux:

Since i am on Arch linux where python3 is a system-default, i'll be using python2 and pip2 instead of python and pip respectively.


Ok let's begin....

```sh
git clone https://github.com/m1grt/django_openligadb.git
```

Go to the project directory.
```sh
cd django_openligadb
```

Initiate the command
```sh
pip install -r requirements.txt
```

When done, run the project.
```sh
cd openligadb
```

```sh
python manage.py runserver
```
Open 127.0.0.1:8000 in your browser.

That's it.

## Tests, need more
```sh
python manage.py test stats.tests
```

## Usage example

Nothing to say about how to use it :)

## Release History

* Version 2