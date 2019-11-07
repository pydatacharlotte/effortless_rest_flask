"tasks to be invoked via Invoke python"
import os
from invoke import task

HEROKU_APP_NAME = "pydata-effortless-rest-flask"


def get_db_url(ctx) -> str:
    """Get db url with local heroku setup

    Args:
        ctx (Context): Invoke context

    Returns:
        str: connection string for db
    """
    return ctx.run(
        f"heroku config:get DATABASE_URL -a {HEROKU_APP_NAME}"
    ).stdout.strip()


@task
def start(ctx, wsgi_server=False, config_name="dev", host="127.0.0.1"):
    """Start the backend as a dev server or production ready gunicorn server"""
    if wsgi_server:
        ctx.run(
            f"""gunicorn --bind {host}:5000 --workers 2 "app:create_app('{config_name}')" """,
            pty=True,
            echo=True,
        )
        return

    ctx.run(
        f"""
        export DATABASE_URL={get_db_url(ctx)} &&
        export FLASK_ENV=development &&
        export FLASK_APP="app:create_app('{config_name}')" &&
        flask run --host={host}
        """,
        pty=True,
        echo=True,
    )


@task
def save_dependencies(ctx):
    """Dump dependencies as config files"""
    ctx.run(
        "pip freeze > requirements.txt && conda env export > environment.yml",
        pty=True,
        echo=True,
    )


@task
def init_db(ctx, config_name="dev"):
    """Initialize Database"""
    from app import db, create_app

    os.environ["DATABASE_URL"] = get_db_url(ctx)

    app = create_app(config_name)
    db.drop_all(app=app)
    db.create_all(app=app)


@task
def seed_db(ctx, config_name="dev"):
    """Initialize Database"""
    from app import db, create_app, guard
    from app.models import User, Iris

    os.environ["DATABASE_URL"] = get_db_url(ctx)
    app = create_app(config_name)

    with app.app_context():

        def add_users(db):
            db.session.add(
                User(
                    username="admin",
                    password=guard.hash_password("password"),
                    roles="admin",
                )
            )
            db.session.add(User(username="user", password=guard.hash_password("pass")))

        def add_iris_dataset(db):
            from sklearn.datasets import load_iris
            import numpy as np
            import pandas as pd

            iris = load_iris()
            iris_df = pd.DataFrame(
                data=np.c_[iris["data"], iris["target"]],
                columns=[
                    "sep_length",
                    "sep_width",
                    "pet_length",
                    "pet_width",
                    "target",
                ],
            )
            print(iris_df.head())
            print(iris_df.shape)

            db.session.bulk_insert_mappings(Iris, iris_df.to_dict(orient="records"))

        add_users()
        add_iris_dataset()

        db.session.commit()


@task
def postman_dump(ctx, config_name="dev", output_path=None):
    from flask import json
    from app import create_app, api

    app = create_app(config_name)

    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = None

    with app.app_context():
        app.config["SERVER_NAME"] = "flask:5000"
        data = api.as_postman(urlvars=urlvars, swagger=swagger)

    if output_path:
        with open(output_path, "w") as new_file:
            new_file.write(json.dumps(data))
            return

    print(json.dumps(data))
