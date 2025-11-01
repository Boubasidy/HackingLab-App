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
    import os, json
    from datetime import datetime
    from flask import flash, render_template

    # Chemin absolu vers le fichier JSON
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    json_path = os.path.join(base_dir, 'infrastructure', 'ansible', 'environnements.json')

    instances = []

    try:
        # Lire le JSON existant
        with open(json_path, 'r') as f:
            data = json.load(f)

        for container in data:
            instances.append({
                'name': container.get('name', 'N/A').lstrip('/'),
                'ip_address': container.get('ip_address'),
                'username': container.get('username', 'root'),
                'password': container.get('password', ''),
                'ssh_port': container.get('ssh_port', 22),
                'status': 'active',
                'created_at': datetime.now()
            })

        if not instances:
            flash("Aucun conteneur provisionné pour l'instant.", "info")

    except FileNotFoundError:
        flash("Le fichier 'environnements.json' n'existe pas. Exécutez d'abord le playbook.", "warning")
    except json.JSONDecodeError:
        flash("Erreur lors de la lecture du fichier JSON.", "danger")
    except Exception as e:
        flash(f"Erreur inattendue : {e}", "danger")

    return render_template('my_resources.html', instances=instances)
 
