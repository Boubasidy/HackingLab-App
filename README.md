# Système de mise à disposition d'environnements

Ce projet vise à concevoir un outil capable de déployer automatiquement des environnements isolés, reproductibles et hautement disponibles. En s'appuyant sur une architecture robuste alliant Ansible, Docker et Flask, le système réduit les erreurs humaines et automatise l'intégralité du cycle de vie des ressources (provisionnement, monitoring et récupération en cas de panne).

## Organisation des Fichiers
```
my-flask-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── templates
│   │   └── base.html
│   └── static
│       ├── css
│       │   └── style.css
│       └── js
│           └── main.js
├── tests
│   └── test_basic.py
├── instance
│   └── config.py
├── requirements.txt
├── config.py
├── wsgi.py
├── .flaskenv
├── .gitignore
└── README.md
```
L'infrastructure est centralisée dans le répertoire /srv, structuré comme suit :
• /srv/infrastructure/ : Cœur du système contenant les playbooks Ansible et les configurations Docker,.
• /srv/app/ : Code source de l'application Flask et fichiers versionnés,.
• /srv/infrastructure/machines_client/ : Simulation de l'environnement final de l'utilisateur.
(Note : Pour garantir la cohérence entre les membres de l'équipe, les dossiers ansible et docker sont synchronisés entre /infrastructure et /app avant chaque opération Git.)

## Fonctionnalités Clés

1. Gestion des Utilisateurs et Dashboard (Flask)
L'application permet aux utilisateurs de s'inscrire et de demander un nombre spécifique de conteneurs. Une fois authentifié, l'utilisateur accède à un tableau de bord personnel affichant, :
• L'état de santé des instances en temps réel.
• Les informations de connexion (IP, port, mot de passe).
• Une commande SSH prête à l'emploi.
2. Environnements Utilisateurs (Docker)
Chaque environnement est basé sur une image sécurisée (youri/secure-ssh). La gestion des ports est dynamique pour éviter les collisions, et chaque instance est isolée au sein d'un réseau Docker dédié,.
3. Logique d'Auto-Réparation (Ansible)
Le système utilise un fichier environments.json comme source de vérité. Un playbook s'exécute périodiquement pour appliquer une logique en 10 phases :
• Détection : Comparaison de l'état réel (Docker) vs état logique (JSON).
• Réparation : Jusqu'à 3 tentatives de redémarrage pour les conteneurs défaillants.
• Réallocation : Si un conteneur est définitivement perdu, le système alloue automatiquement une nouvelle ressource du pool à l'utilisateur.
• Nettoyage : Suppression des conteneurs orphelins ou inutilisables.

## Simulation Client (machines_client)

Pour valider la robustesse du système, nous avons intégré un module de simulation client. Chaque utilisateur dispose d'un conteneur "client" dédié agissant comme sa machine de travail.
Schéma de l'architecture client :  (Référence : source)
Ce module permet d'exécuter des tests automatisés via Ansible, :
• Tests de connectivité réseau.
• Simulations de charge système (CPU, mémoire).
• Génération de rapports d'état au format JSON, consultables sur le dashboard.

<img width="761" height="296" alt="image" src="https://github.com/user-attachments/assets/073f5abf-732b-475f-9f00-c653326395aa" />
Schéma : Architecture machines_client

## Installation

1. Cloner la repository:
   ```
   git clone <repository-url>
   cd my-flask-app
   ```

2. Créer un environment virtual :
   ```
   python -m venv venv
   ```

3. Activer l'environment virtual:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Installer les packages :
   ```
   pip install -r requirements.txt
   ```
Pour maintenir l'infrastructure synchronisée avec le dépôt Git, nous utilisons la stratégie suivante :
1. Avant un Push : Copier /srv/infrastructure/ansible et docker vers /srv/app.
2. Après un Pull : Remplacer le contenu de /srv/infrastructure par les fichiers issus de /srv/app.

## Utilisation

1. Démarrer l'application:
   ```
   flask run --host=0.0.0.0 --port=5000
   ```


## License

This project is licensed under the MIT License.
