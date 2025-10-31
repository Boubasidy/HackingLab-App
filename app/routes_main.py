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
    result = subprocess.run([
        "ansible-playbook",
        "-i", "inventories/hosts.ini",
        "playbooks/deploy_docker.yml",
        "-e", "number=3",
        "--extra-vars", "output=json"
    ], capture_output=True, text=True)

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return jsonify({"error": "Erreur lors du parsing JSON", "raw": result.stdout}), 500

    return jsonify(data)