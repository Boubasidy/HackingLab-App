from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from . forms import RegistrationForm, LoginForm, ResetPasswordForm
from . models import User
import json
import subprocess


from . import db, bcrypt


# Blueprint pour l'authentification
auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    # Lecture du JSON pour connaître les environnements disponibles
    json_path = "/srv/infrastructure/ansible/environnements.json"
    available_envs = None
    data = []

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        free_containers = [
            c for c in data
            if isinstance(c, dict) and c.get("owner") is None
        ]
        available_envs = len(free_containers)

    except FileNotFoundError:
        available_envs = 0
        flash("Aucun environnement n'a encore été créé. Contactez l'administrateur.", "warning")
    except json.JSONDecodeError:
        available_envs = 0
        flash("Erreur de lecture du fichier d'environnements. Contactez l'administrateur.", "danger")

    if form.validate_on_submit():
        # petite contrainte V1 : pas d'espace dans le mot de passe SSH
        if " " in form.ssh_password.data:
            flash("Le mot de passe SSH ne doit pas contenir d'espaces pour cette version.", "danger")
            return render_template('registration.html', form=form, available_envs=available_envs)

        if available_envs is None or available_envs <= 0:
            flash("Aucun environnement n'est disponible pour le moment.", "danger")
            return render_template('registration.html', form=form, available_envs=available_envs)

        requested = form.requested_containers.data

        if requested > available_envs:
            flash(
                f"Il n'y a que {available_envs} environnement(s) disponible(s), "
                f"vous en avez demandé {requested}.",
                "danger",
            )
            return render_template('registration.html', form=form, available_envs=available_envs)

        # Création de l'utilisateur
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Appel du playbook Ansible pour assigner les conteneurs
        try:
            subprocess.run(
                [
                    "ansible-playbook",
                    "-i", "/srv/infrastructure/ansible/inventories/hosts.ini",
                    "/srv/infrastructure/ansible/playbooks/assign_containers.yml",
                    "--extra-vars",
                    f"username={user.username} requested={requested} ssh_password={form.ssh_password.data}",
                ],
                check=True,
            )
            flash("Compte créé et conteneur(s) réservé(s) ! Connectez-vous.", "success")
        except subprocess.CalledProcessError:
            flash(
                "Votre compte a été créé, mais une erreur est survenue lors de l'assignation "
                "des environnements. Contactez l'administrateur.",
                "warning",
            )

        return redirect(url_for('auth.login'))

    # GET ou validation échouée
    return render_template('registration.html', form=form, available_envs=available_envs)




@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.mes_ressources'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Connexion réussie !", "success")

            # Gestion du paramètre 'next'
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.mes_ressources')

            return redirect(next_page)

        flash("Email ou mot de passe invalide.", "danger")

    return render_template('authentification.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie", "info")
    return redirect(url_for('auth.login'))


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user.set_password(form.new_password.data)
            db.session.commit()
            flash("Mot de passe réinitialisé avec succès.", "success")
            return redirect(url_for('auth.login'))
        flash("Email non trouvé.", "danger")

    return render_template('reset_password.html', form=form)

