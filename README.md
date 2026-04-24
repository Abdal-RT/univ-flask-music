# Site d'actualité musicale

Ce projet implémente un site d'actualité musicale en Flask avec un modèle MVC, une gestion de concerts, d'actualités, et une administration sécurisée.

## Fonctionnalités
- Page d'accueil avec dernières actualités et concerts à venir
- Liste des concerts avec filtres par catégorie, ville et date
- Détail du concert, réservation de places et commentaires
- Page des concerts passés avec avis rédactionnel
- Rubrique actualités groupée par catégorie
- Interface d'administration pour gérer catégories, concerts et articles
- Authentification utilisateur avec création de comptes
- Validation des formulaires via Flask-WTF
- CSS avec Bootstrap

## Installation

### Installation locale
1. Créez un environnement Python et installez les dépendances :
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Initialisez MariaDB et créez l’utilisateur dédié :
   ```bash
   bash init_db.sh
   ```
   Si tu veux définir d’autres identifiants, tu peux exporter des variables avant :
   ```bash
   export DB_NAME="univ_music"
   export DB_USER="univ_user"
   export DB_PASS="univ_pass"
   export DB_HOST="127.0.0.1"
   export DB_PORT="3306"
   bash init_db.sh
   ```
   Si tu utilises un socket Unix, définis plutôt :
   ```bash
   export DB_SOCKET="/run/mysqld/mysqld.sock"
   bash init_db.sh
   ```
3. Configurez votre application :
   ```bash
   export DATABASE_URL="mysql+pymysql://univ_user:univ_pass@127.0.0.1:3306/univ_music"
   ```
   ou si tu utilises le socket Unix :
   ```bash
   export DB_SOCKET="/run/mysqld/mysqld.sock"
   export DATABASE_URL="mysql+pymysql://univ_user:univ_pass@localhost/univ_music?unix_socket=/run/mysqld/mysqld.sock"
   ```
   Vous pouvez également copier `.env.example` vers `.env` et adapter les valeurs.
4. Lancez l'application :
   ```bash
   python app.py
   ```
5. Ouvrez votre navigateur sur `http://127.0.0.1:5000`.

### Base MariaDB
- `init_db.sh` crée la base `univ_music` et l’utilisateur `univ_user` par défaut.
- Les informations de connexion sont lues depuis `DATABASE_URL`.
- Si MariaDB n'est pas disponible, l'application bascule automatiquement sur une base SQLite locale pour le développement.

## Compte administrateur
- Email : `admin@musique.local`
- Mot de passe : `adminpass`

## Structure du projet
- `app/__init__.py` : création de l'application et configuration
- `app/models.py` : modèles de données SQLAlchemy
- `app/forms.py` : formulaires Flask-WTF
- `app/routes.py` : routes publiques
- `app/admin.py` : routes d'administration
- `app/templates/` : pages HTML
- `app/static/css/` : styles personnalisés

## Notes
- Le projet est conçu pour fonctionner avec MariaDB via SQLAlchemy.
- Si la base de données n'existe pas, elle sera créée automatiquement au premier lancement.
