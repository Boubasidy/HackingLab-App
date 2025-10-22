# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
)


# =======================================
# FORMULAIRE D'INSCRIPTION (Registration)
# =======================================
class RegistrationForm(FlaskForm):
    username = StringField(
        "Nom d’utilisateur",
        validators=[DataRequired(), Length(min=2, max=80)],
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )

    password = PasswordField(
        "Mot de passe",
        validators=[DataRequired(), Length(min=6)],
    )

    confirm = PasswordField(
        "Confirmer le mot de passe",
        validators=[DataRequired(), EqualTo("password")],
    )

    # --- Champs spécifiques au projet Docker ---
    role = SelectField(
        "Type de compte",
        choices=[("client", "Client"), ("admin", "Administrateur")],
        default="client",
    )

    requested_containers = IntegerField(
        "Nombre de conteneurs souhaités",
        validators=[DataRequired(), NumberRange(min=1, max=50)],
        default=1,
    )

    duration = IntegerField(
        "Durée (en heures)",
        validators=[DataRequired(), NumberRange(min=1, max=168)],
        default=24,
    )

    submit = SubmitField("S'inscrire")


# ===========================
# FORMULAIRE DE CONNEXION
# ===========================
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )

    password = PasswordField(
        "Mot de passe",
        validators=[DataRequired()],
    )

    submit = SubmitField("Se connecter")


# ====================================
# FORMULAIRE DE RÉINITIALISATION MDP
# ====================================
class ResetPasswordForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )

    new_password = PasswordField(
        "Nouveau mot de passe",
        validators=[DataRequired(), Length(min=6)],
    )

    confirm_password = PasswordField(
        "Confirmer le nouveau mot de passe",
        validators=[DataRequired(), EqualTo("new_password")],
    )

    submit = SubmitField("Réinitialiser le mot de passe")
