from datetime import date, datetime

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    reservations = db.relationship("Reservation", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    news = db.relationship("NewsArticle", backref="category", lazy=True)
    concerts = db.relationship("Concert", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.title}>"


class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    summary = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<NewsArticle {self.title}>"


class Concert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    venue = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    ticket_limit = db.Column(db.Integer, nullable=False, default=120)
    reserved_seats = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    review = db.Column(db.Text, nullable=True)

    comments = db.relationship("Comment", backref="concert", lazy=True)
    reservations = db.relationship("Reservation", backref="concert", lazy=True)

    @property
    def available_seats(self):
        return max(self.ticket_limit - self.reserved_seats, 0)

    @property
    def is_past(self):
        return self.date < date.today()

    def __repr__(self):
        return f"<Concert {self.title} @ {self.venue}>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    concert_id = db.Column(db.Integer, db.ForeignKey("concert.id"), nullable=False)

    def __repr__(self):
        return f"<Comment {self.author} on {self.concert_id}>"


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seats = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    concert_id = db.Column(db.Integer, db.ForeignKey("concert.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Reservation {self.seats} seats for {self.user_id}>"


def seed_data():
    if not User.query.filter_by(email="admin@musique.local").first():
        user = User(
            email="admin@musique.local",
            name="Administrateur",
            password="adminpass",
            is_admin=True,
        )
        db.session.add(user)

    if not Category.query.first():
        pop = Category(title="Pop", description="Actualités et concerts Pop.")
        rock = Category(title="Rock", description="Concerts et événements Rock.")
        jazz = Category(title="Jazz", description="Informations sur le jazz.")
        db.session.add_all([pop, rock, jazz])
        db.session.flush()

        news1 = NewsArticle(
            title="Festival de la ville annonce sa programmation",
            summary="Une programmation riche en pop et rock pour l’été.",
            content="Les plus grands artistes de la scène locale partageront la scène...",
            category_id=pop.id,
            image_url="https://picsum.photos/seed/news1/800/450",
        )
        news2 = NewsArticle(
            title="Un groupe rock local en tournée",
            summary="La bande revient avec un nouvel album plein d’énergie.",
            content="Après un succès critique, le groupe investit les salles de la région...",
            category_id=rock.id,
            image_url="https://picsum.photos/seed/news2/800/450",
        )
        news3 = NewsArticle(
            title="Soirée jazz au théâtre historique",
            summary="Une rencontre entre jeunes talents et légendes du jazz.",
            content="La scène locale accueille des musiciens de renommée internationale...",
            category_id=jazz.id,
            image_url="https://picsum.photos/seed/news3/800/450",
        )

        concert1 = Concert(
            title="Pop Night Festival",
            venue="Grande Scène du Parc",
            city="Lyon",
            date=date.today().replace(day=min(date.today().day + 10, 28)),
            ticket_limit=250,
            reserved_seats=84,
            category_id=pop.id,
            description="Une soirée Pop avec des artistes locaux et internationaux.",
            image_url="https://picsum.photos/seed/concert1/900/450",
        )
        concert2 = Concert(
            title="Rock Roots Live",
            venue="Salle des Fêtes",
            city="Villeurbanne",
            date=date.today().replace(day=min(date.today().day + 18, 28)),
            ticket_limit=180,
            reserved_seats=112,
            category_id=rock.id,
            description="Le meilleur du rock indépendant pour une nuit énergique.",
            image_url="https://picsum.photos/seed/concert2/900/450",
        )
        concert3 = Concert(
            title="Brunch Jazz Session",
            venue="Café du Quai",
            city="Villeurbanne",
            date=date.today().replace(day=max(date.today().day - 12, 1)),
            ticket_limit=90,
            reserved_seats=90,
            category_id=jazz.id,
            description="Un concert intimiste avec piano, contrebasse et trompette.",
            image_url="https://picsum.photos/seed/concert3/900/450",
            review="Le chef d’orchestre a offert une performance intime et captivante.",
        )

        comment1 = Comment(author="Camille", content="Super ambiance, un moment inoubliable.", concert=concert3)

        db.session.add_all([news1, news2, news3, concert1, concert2, concert3, comment1])

    db.session.commit()
