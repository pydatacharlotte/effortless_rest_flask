# Effortless REST w/ FLask

There are 5 chapters with 5 corresponding branches. The `master` branch is a boilerplate starter kit.

**For the below to be relevant chapters, make sure to check out the chapter branches**

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

---

### Chapter 2: Database: SQLAlchemy

app/\_\_init\_\_.py

- Add SQLAlchemy INIT
- Add route to get users

app/models/user.py

- Create a model for the user table

app/config.py

- Add the SQLALCHEMY_DATABASE_URI config

app/tasks.py

- Add task to init db tables
- Add task to seed users
- run the seed on both local SQLite and PSQL

#### Q: Why does the /uhoh route not return?

jsonify() doesn’t know how to convert a SQLAlchemy class to JSON.

If only there were a way to convert a serialized Python class into a deserialized dict. Then we could convert the dict with jsonify()…

In comes...![marshmallow](https://marshmallow.readthedocs.io/en/stable/_static/marshmallow-logo.png =200x200)

app/\_\_init\_\_.py

- The `/marsh` route uses a marshmallow Schema to deserialize a Python class.
- We can control what’s being deserialized with the different Schemas. (UserSchema vs UserSchemaWithPassword)
- Marshmallow can also serialize and validate a dict with .load()
  - e.g. an ISO date time stamp can be converted to a datetime object easily

---

### Chapter 3: Security: FlaskPraetorian

![FlaskPraetorian](https://i.imgur.com/UfzDAaw.png)
![](https://i.imgur.com/FN24BNa.png)

app/config.py

- Add the proper configs: JWT_ACCESS_LIFESPAN JWT_REFRESH_LIFESPAN

app/\_\_init\_\_.py

- INIT Praetorian()
- Add login() route
- Protect routes with @auth_required decorator

tasks.py

- Use utils for password hashing

---

### Chapter 4: Documentation & API Scale

![](https://i.imgur.com/rXutex7.png) ![](https://i.imgur.com/5YXIolS.png)
![](https://i.imgur.com/VAEuYji.png)

app/\_\_init\_\_.py

- INIT Flask Rest Plus
- Define prefix for all routes
- Convert routes to Flask Rest Plus
- Add Namespaces for segmenting API routes within swagger
- Define authorizations section to easily add a JWT header to requests

Open up Swagger docs!

---

### Chapter 5: Flask-Accepts

app/schemas/user.py

- Add UserLoginSchema

app/\_\_init\_\_.py

- Flask_accepts allows for easy Marshmallow schema conversion to JSON as well as adding Schema to Swagger docs
- Decorate endpoints with @accepts & @responds
