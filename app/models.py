from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from datetime import datetime


# ======================
# UTILISATEUR
# ======================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Méthodes pour gérer le mot de passe
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# ======================
# POST (existant)
# ======================
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relation vers l'utilisateur
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.title}>'


# ======================
# DEMANDE DE RESSOURCES
# ======================
class ResourceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requested_containers = db.Column(db.Integer, nullable=False)
    duration_hours = db.Column(db.Integer, nullable=False)  # durée en heures
    status = db.Column(db.String(20), default='pending')  # pending / active / expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation vers l'utilisateur
    user = db.relationship('User', backref=db.backref('requests', lazy=True))

    # Relation vers les instances de conteneurs
    instances = db.relationship('ResourceInstance', backref='request', lazy=True)


# ======================
# INSTANCE DE RESSOURCE
# ======================
class ResourceInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('resource_request.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)        # Nom du conteneur
    ip_address = db.Column(db.String(45), nullable=True)    # IP attribuée
    username = db.Column(db.String(80), nullable=False)     # Login pour accès
    password = db.Column(db.String(128), nullable=False)    # Mot de passe généré
    status = db.Column(db.String(20), default='pending')    # pending / active / expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ResourceInstance {self.name} ({self.ip_address})>'
