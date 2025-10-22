from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import ResourceInstance, ResourceRequest  # assure-toi que ces modèles existent

# Blueprint pour les pages principales
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('base.html')  # plutôt que base.html, sinon le contenu principal est vide

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/mes-ressources')
@login_required
def my_resources():
    # Récupère toutes les instances liées aux demandes de l'utilisateur
    instances = []
    for req in current_user.requests:
        instances.extend(req.instances)

    # Alternative plus directe (si relation définie correctement dans les modèles) :
    # instances = ResourceInstance.query.join(ResourceRequest).filter(ResourceRequest.user_id == current_user.id).all()

    return render_template('my_resources.html', instances=instances)
