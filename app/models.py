"""Module to hold the entities class stored in the database with sqlalchemy"""
"""Module pour contenir la classe d'entités stockée dans la base de données avec sqlalchemy"""

import hashlib
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Create database connection object
# Création d'un objet connection bdd
db = SQLAlchemy()

class Thought(db.Model):
    """Represent a Thought entity, basically a sentence from a user"""
    """Représenter une entité Thought, essentiellement une phrase d'un utilisateur"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    # Relation with the user who has written the thought
    # Relation avec l'utilisateur qui a écrit la pensée
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

class User(UserMixin, db.Model):
    """Represent a User entity with credentials for authentication from UserMixin"""
    """Représenter une entité utilisateur avec des informations d'identification pour l'authentification à partir de UserMixin"""
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    pseudo = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=True)
    registering_date = db.Column(db.DateTime(), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # Store all the thoughts published by a user
    # Stockez toutes les pensées publiées par un utilisateur
    thoughts = db.relationship('Thought', backref='user', lazy=True)

    def __init__(self, last_name, first_name, pseudo, description, registering_date=None, password=None):
        self.last_name = last_name
        self.first_name = first_name
        self.pseudo = pseudo
        self.description = description
        self.registering_date = registering_date
        self.password = password

    def set_password(self, password):
        """Function to hash the password before setting it in the attribut"""
        """Fonction pour hacher le mot de passe avant de le définir dans l'attribut"""
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    def check_password(self, password):
        """Function to check that the user password match another password"""
        """Fonction pour vérifier que le mot de passe utilisateur correspond à un autre mot de passe"""
        if hashlib.sha256(password.encode('utf-8')).hexdigest() == self.password:
            return True
        return False

def init_db():
    """Function to init the database tables with a sample user"""
    """Fonction pour lancer les tables de base de données avec un exemple d'utilisateur"""
    db.drop_all()
    db.create_all()
    user = User("test", "test", "test", None, datetime.now(), None)
    user.set_password("Test1234")
    db.session.add(user)
    db.session.commit()
    print("Database initialized !")
