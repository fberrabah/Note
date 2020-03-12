"""Module that contains the routes with associated methods"""
"""Module qui contient les routes avec les méthodes associées"""

from datetime import datetime

from flask import Flask, render_template, redirect, flash, request, abort, url_for
from .models import Thought, User, db
from .forms import NewThoughtForm, LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin

# Start the app called in run.py and configure it
# Démarrez l'application appelée dans run.py et configurez-la
app = Flask(__name__)
app.config.from_object('config')

def is_safe_url(target):
    """Function to check that the redirection url is safe and from the same server"""
    """Fonction pour vérifier que l'URL de redirection est sûre et à partir du même serveur"""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

# Here we define two different routes matching the method
# Ici, nous définissons deux itinéraires différents correspondant à la méthode
@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Function to show login form and check user credentials in database"""
    """Fonction pour afficher le formulaire de connexion et vérifier les informations d'identification de l'utilisateur dans la base de données"""
    # if the user is already logged in we send him to the main page
    # si l'utilisateur est déjà connecté, nous l'envoyons à la page principale
    if current_user.is_authenticated:
        return redirect('/index/')
    # Instance of the form object used to display an HTML form in the view
    # Instance de l'objet de formulaire utilisé pour afficher un formulaire HTML dans la vue
    form = LoginForm()
    # If the form is correctly filled according to specifications of the forms file
    # Si le formulaire est correctement rempli selon les spécifications du fichier de formulaires
    if form.validate_on_submit():
        # Check in database for user with the given pseudo
        # Vérifier dans la base de données pour l'utilisateur avec le pseudo donné
        user = User.query.filter_by(pseudo=form.pseudo.data).first()
        # one has been found and the passwords are the same
        # un a été trouvé et les mots de passe sont les mêmes
        # we log him in and redirect to the main page
        # nous le connectons et nous redirigeons vers la page principale
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or '/index/')
        # otherwise we show an error message and the login form again
        # sinon nous affichons à nouveau un message d'erreur et le formulaire de connexion
        flash("Pseudo ou mot de passe incorect(s)", "danger")
    return render_template("login.html.j2", form=form)

@app.route('/logout/')
@login_required
def logout():
    """Function to log the user out with flask_login"""
    """sinon nous affichons à nouveau un message d'erreur et le formulaire de connexion"""
    logout_user()
    flash("Vous avez bien été déconnecté", "success")
    return redirect('/login/')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Function to show a registration form and save a new user in database"""
    """Fonction pour afficher un formulaire d'inscription et enregistrer un nouvel utilisateur dans la base de données"""
    # Instance of the form object used to display an HTML form in the view
    # Instance de l'objet de formulaire utilisé pour afficher un formulaire HTML dans la vue
    form = RegisterForm()
    # If the form is correctly filled according to specifications of the forms file
    # Si le formulaire est correctement rempli selon les spécifications du fichier de formulaires
    if form.validate_on_submit():
        try:
            # Instanciate a user object from form data
            # Instancier un objet utilisateur à partir des données du formulaire
            user = User(
                last_name = form.last_name.data,
                first_name = form.first_name.data,
                pseudo = form.pseudo.data,
                description = form.description.data
            )
            # Encode the password and store the current date
            # Encode le mot de passe et enregistre la date actuelle
            user.set_password(form.password.data)
            user.registering_date = datetime.now()
            # Register the user in the Database
            # Enregistrer l'utilisateur dans la base de données
            db.session.add(user)
            db.session.commit()
            # Store a success message and go to login page
            # Enregistrez un message de réussite et accédez à la page de connexion
            flash("Votre compte a été créé", "success")
            return redirect('/login/')
        except Exception as e:
            flash("Une erreur est survenue, nous n'avons pas pu vous enregistrer", "danger")
    return render_template("register.html.j2", form=form)

# ALL THE NEXT ROUTES HAVE THE LOGIN REQUIERED DECORATOR
# TOUT LES PROCHAINS ITINÉRAIRES ONT LE LOGIN REQUIS DECORATOR
# BECAUSE THEY ARE RESERVED TO AUTHENTICATED MEMBERS ONLY
# PARCE QU'ILS SONT RÉSERVÉS AUX MEMBRES AUTHENTIFIÉS UNIQUEMENT

@app.route('/index/')
@login_required
def index():
    """Function to show the user thoughts by default"""
    """Fonction pour afficher les pensées des utilisateurs par défaut"""
    # Retrieve thoughts for a specific user from database
    thoughts = Thought.query.filter_by(user=current_user).all()
    return render_template("index.html.j2", thoughts=thoughts)


@app.route('/admin/thoughts/')
@login_required
def thoughts():
    """Function to show the thoughts in the admin panel"""
    """Fonction pour afficher les pensées dans le panneau d'administration"""
    thoughts = Thought.query.filter_by(user=current_user).all()
    return render_template("admin/thoughts.html.j2", thoughts=thoughts)

@app.route('/admin/thought/new', methods=['GET', 'POST'])
@login_required
def new_thought():
    """Function to show a form and add a thought in database"""
    """Fonction pour afficher un formulaire et ajouter une pensée dans la base de données"""
    # Instance of the form object used to display an HTML form in the view
    # Instance de l'objet de formulaire utilisé pour afficher un formulaire HTML dans la vue
    form = NewThoughtForm()
    if form.validate_on_submit():
        # If everything is OK we instanciate a thought objet
        # Si tout va bien on instancie un objet de pensée
        thought = Thought(form.content.data, current_user.id)
        # Register the thought oject in the database and redirect to home page
        # Enregistrez l'objet de pensée dans la base de données et redirigez-le vers la page d'accueil
        db.session.add(thought)
        db.session.commit()
        return redirect('/index')
    return render_template("admin/new_thought.html.j2", form=form)

# This route has a paramater in the url, the id we want to delete
# Cette route a un paramètre dans l'url, l'identifiant que nous voulons supprimer
@app.route('/admin/thought/delete/<int:id>')
@login_required
# Do not forget to add an id parameter in the function corresponding to the route parameter
# N'oubliez pas d'ajouter un paramètre id dans la fonction correspondant au paramètre route
def delete_thought(id):
    """Function to delete a thought in database"""
    """Fonction pour supprimer une pensée dans la base de données"""
    # Retrieve the thought object we want to delete by it's id from database
    # Récupérez l'objet de pensée que nous voulons supprimer par son identifiant de la base de données
    thought = Thought.query.get(id)
    # if we found a matching thought and it is owned by the logged user we delete it
    # si nous avons trouvé une pensée correspondante et qu'elle appartient à l'utilisateur connecté, nous la supprimons
    if thought and thought.user == current_user:
        db.session.delete(thought)
        db.session.commit()
        flash("Votre note a bien été supprimée", "success")
    return redirect('/admin/thoughts/')

# This route has a paramater in the url, the id of the thought we want to update
# Cette route a un paramètre dans l'url, l'id de la pensée que nous voulons mettre à jour
@app.route('/admin/thought/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_thought(id):
    """Function to show a form with thought's info and update it in the database"""
    """Fonction pour afficher un formulaire avec les informations de la pensée et le mettre à jour dans la base de données"""
    # Retrieve the thought object we want to update by it's id from database
    # Récupérez l'objet de pensée que nous voulons mettre à jour par son identifiant dans la base de données
    thought = Thought.query.get(id)
    # If do not find the thougth or it is not owned by the user we redirect with error message
    # Si vous ne trouvez pas la pensée ou qu'elle n'appartient pas à l'utilisateur, nous redirigeons avec un message d'erreur
    if not thought or thought.user != current_user:
        flash("Il semble qu'il y ait eu un problème", "danger")
        return redirect("/admin/thoughts/")
    # Instance of the form object used to display a prefilled form in the view
    # Instance de l'objet de formulaire utilisé pour afficher un formulaire prérempli dans la vue
    form = NewThoughtForm(obj=thought)
    if form.validate_on_submit():
        # update the content in the object NOT the database
        # mettre à jour le contenu de l'objet PAS la base de données
        thought.content = form.content.data
        # update the database
        # mettre à jour la base de données
        db.session.commit()
        return redirect('/admin/thoughts/')
    return render_template('admin/update_thought.html.j2', thought=thought, form=form)
