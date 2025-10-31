import os
import json
from flask import Blueprint, render_template, current_app, flash
from flask_login import login_required

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("base.html")

@main.route("/mes-ressources")
@login_required
def mes_ressources():
    """
    Lit le fichier JSON généré par Ansible et l'affiche.
    PAS d'ansible-playbook ici, on lit juste la sortie.
    """
    json_path = "/srv/infrastructure/ansible/environnements.json"

    if not os.path.exists(json_path):
        flash("Fichier d'environnements non trouvé (lance le playbook Ansible)", "warning")
        return render_template("my_resources.html", data=None)

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        flash("Le fichier d'environnements n'est pas un JSON valide", "danger")
        return render_template("my_resources.html", data=None, raw=open(json_path).read())

    # ici data peut être :
    #  - soit une liste de strings : ["/env_1", "/env_2", ...]
    #  - soit une liste d'objets plus riches
    return render_template("my_resources.html", data=data)
