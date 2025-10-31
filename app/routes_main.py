from datetime import datetime
import subprocess
import os
import json
from flask import Blueprint, flash, render_template, current_app
from flask_login import login_required

# Blueprint principal
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('base.html')

@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/mes-ressources')
@login_required
def mes_ressources():
    """
    Exécute le playbook Ansible en local et affiche le JSON de sortie sur la page.
    """

    # --- chemins absolus ---
    ansible_root = "/srv/infrastructure/ansible"
    inventory_path = os.path.join(ansible_root, "inventories", "hosts.ini")
    playbook_path = os.path.join(ansible_root, "playbooks", "test.yml")  # ton playbook réel

    # --- commande ansible ---
    cmd = [
        "ansible-playbook",
        "-i", inventory_path,
        playbook_path,
        "--extra-vars", "output=json number=3"
    ]

    # --- exécution ---
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=ansible_root
    )

    # --- gestion des erreurs d'exécution ---
    if result.returncode != 0:
        current_app.logger.error("Ansible stderr:\n%s", result.stderr)
        current_app.logger.error("Ansible stdout:\n%s", result.stdout)
        flash("Erreur lors de l'exécution du playbook Ansible", "danger")
        return render_template("my_resources.html", data={}, stderr=result.stderr)

    # --- tentative de parsing JSON ---
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        # si pas du JSON, on renvoie le texte brut pour inspection
        flash("Sortie Ansible non au format JSON", "warning")
        current_app.logger.warning("Sortie non JSON :\n%s", result.stdout)
        return render_template("my_resources.html", data={}, raw=result.stdout)

    # --- succès ---
    flash("Playbook exécuté avec succès", "success")
    return render_template("my_resources.html", data=data)
