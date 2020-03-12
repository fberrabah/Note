# Application de carnet de notes ou de pensées avec Flask

Il s'agit d'une application développée dans le cadre de mon poste de formateur en développement web. L'objectif est que les apprenants produisent une application à l'aide du framework Python Flask et se familiarisent ainsi avec ses fonctionnalités principales. L'application en question est très simple, il s'agit d'un carnet de notes où ils peuvent écrire ce qu'ils pensent sous forme de post-it.

Au travers de cet exercice, les étudiants apprennent à :
- Démarrer une application Flask
- Organiser une application Flask
- Gérer le routing d'une application
- Importer et utiliser Sqlalchemy en réalisant un CRUD basique
- Gérer un modèle en orienté objet
- Comprendre le protocole HTTP
- Renvoyer un template sous forme de réponse
- Utiliser le moteur de template Jinja2
- Gérer des utilisateurs à l'aide de flask-login

## Consignes

Vous venez d'arriver en tant que stagiaire dans une start-up spécialisée dans la production d'applications open-source python et votre maître de stage vous a assigné une première application à produire. Comme vous êtes jeune stagiaire, on ne vous a pas intégré tout de suite sur un projet client. Afin de vous laisser le temps de prendre vos marques, on vous a assigné un side-project demandé depuis longtemps par le service ressources humaines. Comme vous le savez dans l'entreprise nouvelle le bonheur des salariés est très important, il faut être heureux d'aller au travail et s'y sentir bien afin de pouvoir s'y épanouir et développer l'ensemble de ses potentialités. Le tout bien-sûr dans une démarche RSE et éco-responsable cela va de soi !

Le service ressources humaines vous a donc demandé de produire une application à destination des employés qui leur permettra d'écrire, chacun de manière privée, leurs pensées du jour peu importe leur contenu. Ainsi grâce à cette nouvelle possibilité d'expression, il pourront écrire ce qui leur pèse sur le coeur et seront plus à même de communiquer et donc de travailler avec leurs collègues. Les RH voudraient une applications visuellement moderne, légère où le design ne prend pas le pas sur l'utilisateur mais qui possède quand même une âme marquée, comme ancrée dans l'imaginaire collectif... A lueur de ces explications, comme vous n'êtes pas bon en design vous utiliserez donc Bootstrap 4 pour le front-end de l'application.

Spécifications fonctionnelles:
- La page d'accueil affiche un formulaire de login pour l'utilisateur. On considère que les utilisateurs sont rentrés en base de données manuellement
- L'utilisateur ne peut accéder à son espace d'écriture que si le pseudo indiqué et le mot de passe correspondent à ceux en base de données
- La page d'accueil de l'espace personnel affichent les pensées déjà enregistrées par l'utilisateur et uniquement ses pensées personnelles
- L'utilisateur peut accéder à un espace d'administration d'où il peut supprimer une pensée ou modifier le contenu d'une pensée
- L'utilisateur peut se déconnecter à tout moment de l'application, il est alors renvoyé sur la page de login
- Un utilisateur non connecté ne peut pas accéder à autre chose que la page de login
- L'application est utilisable sur tous types d'appareils (smartphones, tablettes, ordinateurs...)

Spécifications techniques:
- Python3
- Framework Flask 1.0 ou supérieur
- SGBD: Sqlalchemy
- Gestion des formulaires: Wtforms
- Moteur de template : Jinja2
- Gestion des connexions : Flask-login
- Template organisé avec triple héritage
- Framework CSS Bootstrap 4

## Pour aller plus loin

Si vous souhaitez en apprendre plus sur le framework Flask et les librairie qu'on y utilise le plus fréquemment, pourquoi ne pas essayer d'ajouter les fonctionnalités suivantes :
- Permettre aux utilisateurs de se créer eux-même un compte à l'aide d'un formulaire
- Effectuer des vérifications sur les formulaires concernant le niveau de sécurité du mot de passe, la disponibilité du pseudo que l'utilisateur souhaite enregistrer (un pseudo ne peut être utilisé qu'une fois)
- Afficher des messages flash à l'utilisateur selon le succès ou l'échec de ses actions (connexion, création d'une note, enregistrement etc...)
- Essayez de donner une mise en forme sympathique à votre application, vous verrez cela sera utile plus tard
