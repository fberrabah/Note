import os
from datetime import timedelta

from flask import Flask, session
from flask_login import LoginManager

from .views import app
from . import models

models.db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.refresh_view = 'login'
login_manager.refresh_message = (u"Votre session a expiré")
login_manager.refresh_message_category = "warning"


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@app.cli.command("init_db")
def init_db():
    models.init_db()

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))
