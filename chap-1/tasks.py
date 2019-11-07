"tasks to be invoked via Invoke python"
import os
from invoke import task


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
        export FLASK_ENV=development &&
        export FLASK_APP="app:create_app('{config_name}')" &&
        flask run --host={host}
        """,
        pty=True,
        echo=True,
    )
