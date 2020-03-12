"""Module to hold the different forms for the application"""
"""Module pour contenir les différents formulaires de candidature"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp

from .models import User

# Note that each form corresponds to an entities from the model
# Notez que chaque formulaire correspond à une entité du modèle
# Form fields are defiened by class attributs holding object of the correspnding type field
# Les champs de formulaire sont définis par des attributs de classe contenant un objet du champ de type correspondant

class NewThoughtForm(FlaskForm):
    """Class to generate a form to add a thought to the database"""
    """Classe pour générer un formulaire pour ajouter une pensée à la base de données"""
    content = StringField('Citation', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class LoginForm(FlaskForm):
    """Class to generate a form for the login"""
    """Classe pour générer un formulaire pour la connexion"""
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    """Class to generate a form for the user to register on the site"""
    """Classe pour générer un formulaire d'inscription de l'utilisateur sur le site"""
    last_name = StringField('Nom', validators=[DataRequired()])
    first_name = StringField('Prénom', validators=[DataRequired()])
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    description = TextField('Description personnelle')
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,}$", message="Attention le mot de passe doit contenir 6 caractères, une minuscule, une majuscule et un chiffre")
    ])
    password_confirm = PasswordField('Confirmez le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', "Les deux mot de passes doivent être identiques")
    ])
    submit = SubmitField("S'inscrire")

    # NOTE: this a special validation system from wtfform
    # REMARQUE: ceci est un système de validation spécial de wtfform
    # each method of a form starting with validate_ + the field name is called when submitting the form
    # chaque méthode d'un formulaire commençant par validate_ + le nom du champ est appelée lors de la soumission du formulaire
    def validate_pseudo(self, pseudo):
        """Function that checks that the pseudo is not already used in database"""
        """Fonction qui vérifie que le pseudo n'est pas déjà utilisé dans la base de données"""
        user = User.query.filter_by(pseudo=pseudo.data).first()
        if user is not None:
            raise ValidationError('Ce pseudo est déjà pris :(')
