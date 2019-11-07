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
    from app import db, create_app
    from app.models.user import User
    from hashlib import sha256

    os.environ["DATABASE_URL"] = get_db_url(ctx)
    app = create_app(config_name)

    with app.app_context():

        # !!!!!!!ALERT!!!!!!!
        # Passwords are stored as plain text. See Chapter 3 for security adjustment!
        def add_users():
            db.session.add(User(username="admin", password="password", roles="admin"))
            db.session.add(User(username="user", password="pass"))

        add_users()

        db.session.commit()
