from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from app.forms import RegistrationForm, LoginForm, ResetPasswordForm
from app.models import User
from app import db, bcrypt


# Blueprint pour l'authentification
auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Créer un utilisateur
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Compte créé ! Connectez-vous.", "success")
        return redirect(url_for('auth.login'))

    return render_template('registration.html', form=form)


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

