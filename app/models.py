from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

# --- Utilisateurs ---
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Catégories ---
class Categorie(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    actualites = db.relationship('Actualite', backref='categorie', lazy=True)
    concerts = db.relationship('Concert', backref='categorie', lazy=True)

# --- Actualités ---
class Actualite(db.Model):
    __tablename__ = 'actualites'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    resume = db.Column(db.String(300), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    date_publication = db.Column(db.DateTime, default=datetime.utcnow)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

# --- Concerts ---
class Concert(db.Model):
    __tablename__ = 'concerts'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    lieu = db.Column(db.String(120), nullable=False)
    ville = db.Column(db.String(80), nullable=False)
    date_concert = db.Column(db.Date, nullable=False)
    places_totales = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    avis_redacteur = db.Column(db.Text, nullable=True)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    reservations = db.relationship('Reservation', backref='concert', lazy=True, cascade="all, delete-orphan")
    commentaires = db.relationship('Commentaire', backref='concert', lazy=True, cascade="all, delete-orphan")

    def places_disponibles(self):
        reservees = sum(r.places for r in self.reservations)
        return self.places_totales - reservees

    @property
    def est_passe(self):
        return self.date_concert < datetime.utcnow().date()

# --- Réservations ---
class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    places = db.Column(db.Integer, nullable=False)
    date_reservation = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    concert_id = db.Column(db.Integer, db.ForeignKey('concerts.id'), nullable=False)

# --- Commentaires ---
class Commentaire(db.Model):
    __tablename__ = 'commentaires'
    id = db.Column(db.Integer, primary_key=True)
    auteur = db.Column(db.String(80), nullable=False)
    contenu = db.Column(db.String(300), nullable=False)
    date_post = db.Column(db.DateTime, default=datetime.utcnow)
    concert_id = db.Column(db.Integer, db.ForeignKey('concerts.id'), nullable=False)

# --- Initialisation des données ---
def seed_data():
    # 1. Création de l'admin
    if not User.query.filter_by(email='root@root.com').first():
        admin = User(nom='Root Admin', email='root@root.com', is_admin=True)
        admin.set_password('root')
        db.session.add(admin)

    # 2. Création des catégories (si elles n'existent pas)
    if not Categorie.query.first():
        cat_rock = Categorie(titre="Rock", description="Tout sur la musique Rock")
        cat_electro = Categorie(titre="Electro", description="Musique électronique")
        db.session.add_all([cat_rock, cat_electro])
        db.session.commit() # On sauvegarde pour générer les IDs des catégories

    # 3. Création d'une actualité de test
    if not Actualite.query.first():
        cat_electro = Categorie.query.filter_by(titre="Electro").first()
        actu = Actualite(
            titre="Le retour de la French Touch",
            resume="Un nouvel album très attendu pour cet été.",
            contenu="Les plus grands DJ français se réunissent pour une compilation historique...",
            categorie_id=cat_electro.id
        )
        db.session.add(actu)

    # 4. Création d'un concert de test (dans le futur)
    if not Concert.query.first():
        cat_rock = Categorie.query.filter_by(titre="Rock").first()
        concert = Concert(
            titre="Musilac 2026",
            lieu="Esplanade du Lac",
            ville="Aix-les-Bains",
            # On met une date dans le futur pour qu'il apparaisse dans "Prochains concerts"
            date_concert=datetime(2026, 7, 10).date(),
            places_totales=15000,
            description="Le plus grand festival pop-rock de la région revient fort !",
            categorie_id=cat_rock.id
        )
        db.session.add(concert)

    # On valide tous les ajouts finaux
    db.session.commit()