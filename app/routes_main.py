import os
import json
from flask import Blueprint, render_template, flash, current_app
from flask_login import login_required

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("base.html")

@main.route("/mes-ressources")
@login_required
def mes_ressources():
    json_path = "/srv/infrastructure/ansible/environnements.json"

    debug_info = {"file": json_path, "exists": os.path.exists(json_path)}

    if not os.path.exists(json_path):
        current_app.logger.warning(f"[mes-ressources] fichier introuvable: {json_path}")
        flash("Fichier d'environnements non trouvé", "warning")
        return render_template("my_resources.html", data=None)

    try:
        with open(json_path, "r") as f:
            content = f.read()
        data = json.loads(content)
        debug_info["data_type"] = type(data).__name__
        if isinstance(data, list) and data:
            debug_info["first_item_type"] = type(data[0]).__name__
    except Exception as e:
        current_app.logger.error(f"[mes-ressources] erreur JSON: {e}")
        return render_template("my_resources.html", data=None, raw=content)

    print("DEBUG INFO >>>", debug_info)

    return render_template("my_resources.html", data=data)
