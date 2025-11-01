from datetime import datetime
import subprocess
import os 
import json
import platform
from unittest import result
from flask import Blueprint, flash, render_template
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

@main.route('/mes_ressources')
@login_required
def my_resources():
    # Chemins
    path_base = os.getcwd()
    base = os.path.dirname(path_base)
    ini_dir = os.path.join(base, 'infrastructure', 'ansible')
    ini_path = os.path.join(ini_dir, 'inventories', 'hosts.ini')
    playbook_path = os.path.join(ini_dir, 'playbooks', 'deploy_docker.yml')
    json_output_path = os.path.join(ini_dir , "environnements.json")

    # Exécution du playbook avec output JSON
    result = subprocess.run([
    "ansible-playbook",
    "-i", ini_path,
    playbook_path,
    "-e", "output=json"
   ], capture_output=True, text=True)

    instances = []

    try:
        # La sortie stdout contient du JSON
        data = json.loads(result.stdout)

        # Parcours des conteneurs
        for container in data:
            instances.append({
                'name': container.get('name', 'N/A').lstrip('/'),  # supprime le / devant env_1
                'ip_address': container.get('ip_address'),
                'username': container.get('username', 'root'),
                'password': container.get('password', ''),
                'ssh_port': container.get('ssh_port', 22),
                'status': 'active',  # par défaut, ou ajouter la logique si disponible
                'created_at': datetime.now()
            })
    except json.JSONDecodeError:
        flash("Erreur lors de la récupération des ressources", "danger")
    except Exception as e:
        flash(f"Erreur inattendue : {e}", "danger")

    return render_template('my_resources.html', instances=instances)