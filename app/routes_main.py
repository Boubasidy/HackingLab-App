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

@main.route('/mes-ressources')
@login_required
def my_resources():
    # Exécute le playbook Ansible
    result = subprocess.run([
        "ansible-playbook",
        "-i", "inventories/hosts.ini",
        "playbooks/deploy_docker.yml",
        "-e", "number=3",
        "--extra-vars", "output=json"
    ], capture_output=True, text=True)

    try:
        # Parse la sortie JSON
        data = json.loads(result.stdout)
        
        # Formate les données pour le template
        instances = []
        for container in data.get('docker_containers', []):
            instances.append({
                'name': container.get('name', 'N/A'),
                'ip_address': container.get('ip_address'),
                'username': 'admin',  # ou dynamique selon votre config
                'password': container.get('password', '********'),
                'status': 'active' if container.get('state') == 'running' else 'inactive',
                'created_at': datetime.strptime(container.get('created', ''), '%Y-%m-%dT%H:%M:%SZ')
                if container.get('created') else None
            })
    except json.JSONDecodeError:
        flash('Erreur lors de la récupération des ressources', 'danger')
        instances = []

    return render_template('my_resources.html', instances=instances)
