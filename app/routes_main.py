from datetime import datetime
import subprocess
import os 
import json
import platform
from unittest import result
from flask import Blueprint, flash, render_template
from flask_login import login_required, current_user
from . models import ResourceInstance, ResourceRequest  # assure-toi que ces modèles existent

# Blueprint pour les pages principales
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('base.html')  # plutôt que base.html, sinon le contenu principal est vide

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/mes_ressources')
@login_required
def mes_ressources():
    import json
    from datetime import datetime
    from flask import flash, render_template

    json_path = "/srv/infrastructure/ansible/environnements.json"
    instances = []

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        username = current_user.username

        for container in data:
            # support au cas où l'ancien format (liste de strings) traîne
            if not isinstance(container, dict):
                continue

            owner = container.get('owner')

            # On n'affiche QUE les conteneurs appartenant à l'utilisateur courant
            if owner != username:
                continue

            instances.append({
                'name': container.get('name', 'N/A').lstrip('/'),
                'ip_address': container.get('ip_address'),
                'username': container.get('username', 'root'),
                'password': container.get('password', ''),
                'ssh_port': container.get('ssh_port', 22),
                'status': 'active',
                'created_at': datetime.now()
            })

    except FileNotFoundError:
        flash(f"Le fichier '{json_path}' n'existe pas. Exécute d'abord le playbook.", "warning")
    except json.JSONDecodeError:
        flash("Erreur lors de la lecture du fichier JSON.", "danger")
    except Exception as e:
        flash(f"Erreur inattendue : {e}", "danger")

    return render_template('my_resources.html', instances=instances)
