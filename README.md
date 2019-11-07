# Effortless REST w/ FLask

---

### Chapter 1: "Say Hello to the REAL world"

#### A word about dependencies

- Python uses `pip` as a package manager
- Many data scientist use `conda` to install packages.

##### example dependency export

_PIP_

```bash
pip freeze > requirements.txt
```

_Conda_

```bash
conda env export > environment.yml
```

##### example dependency import/load

_PIP_

```bash
pip install -r requirements.txt
```

_Conda_

```bash
conda env create -f environment.yml
```

app/\_\_init\_\_.py

- The main Flask application
- Application factory
  - Allows for easier testing

#### Q: How do you configure a Flask application?

app/config.py

- Place configs for Flask and its plugins here

#### Q: How do you start the server?

```bash
export FLASK_APP="app:create_app('dev')"
export FLASK_ENV="development" &&
flask run
```

> :warning: DO NOT USE 'flask' cli for produciton

#### Q: How do you start the server for PRODUCTION?

```bash
gunicorn --bind 0.0.0.0 --workers 2 "app:create_app('prod')"
```

- 0.0.0.0: An alias IP to say expose on all network interfaces.
- workers: number of unique web application processes to spin up.

#### Q: Do I have to type that _EVERY TIME_?

- Check out [Invoke](http://www.pyinvoke.org/)
- Build pre-defined tasks with easy configuration for options
- see `./tasks.py`

_Example_

```bash
invoke start
```
