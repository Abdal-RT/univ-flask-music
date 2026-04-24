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
2. Configurez votre base de données MariaDB.
   Exemple de variable d'environnement :
   ```bash
   export DATABASE_URL="mysql+pymysql://user:password@127.0.0.1:3306/univ_music"
   ```
   Vous pouvez également copier `.env.example` vers `.env` et adapter les valeurs.
3. Lancez l'application :
   ```bash
   python app.py
   ```
4. Ouvrez votre navigateur sur `http://127.0.0.1:5000`.

### Installation avec Docker
1. Créez `docker-compose.yml` et `Dockerfile` (déjà présents dans ce projet).
2. Démarrez les services :
   ```bash
   docker compose up --build
   ```
3. Ouvrez votre navigateur sur `http://127.0.0.1:5000`.

### Base MariaDB
- Le script de démarrage tente de créer automatiquement la base `univ_music` si elle n'existe pas.
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
