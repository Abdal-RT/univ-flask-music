import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Categorie, Actualite, Concert, Reservation, Commentaire
from app.forms import LoginForm, InscriptionForm, ReservationForm, CommentaireForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    dernieres_actus = Actualite.query.order_by(Actualite.date_publication.desc()).limit(3).all()
    aujourd_hui = datetime.datetime.utcnow().date()
    prochains_concerts = Concert.query.filter(Concert.date_concert >= aujourd_hui).order_by(Concert.date_concert.asc()).limit(3).all()
    
    return render_template('index.html', actualites=dernieres_actus, concerts=prochains_concerts)

@main_bp.route('/concerts')
def concerts():
    aujourd_hui = datetime.datetime.utcnow().date()
    liste_concerts = Concert.query.filter(Concert.date_concert >= aujourd_hui).order_by(Concert.date_concert.asc()).all()
    return render_template('concerts.html', concerts=liste_concerts)

@main_bp.route('/concerts-passes')
def past_concerts():
    aujourd_hui = datetime.datetime.utcnow().date()
    concerts_passes = Concert.query.filter(Concert.date_concert < aujourd_hui).order_by(Concert.date_concert.desc()).all()
    return render_template('past_concerts.html', concerts=concerts_passes)

@main_bp.route('/concert/<int:concert_id>', methods=['GET', 'POST'])
def concert_detail(concert_id):
    concert = Concert.query.get_or_404(concert_id)
    reservation_form = ReservationForm()
    commentaire_form = CommentaireForm()

    # Logique de réservation
    if not concert.est_passe and reservation_form.validate_on_submit() and reservation_form.reserve.data:
        if not current_user.is_authenticated:
            flash("Vous devez être connecté pour réserver.", "warning")
            return redirect(url_for('main.login'))

        if reservation_form.places.data <= concert.places_disponibles():
            nouvelle_resa = Reservation(places=reservation_form.places.data, user_id=current_user.id, concert_id=concert.id)
            db.session.add(nouvelle_resa)
            db.session.commit()
            flash("Réservation confirmée avec succès !", "success")
            return redirect(url_for('main.concert_detail', concert_id=concert.id))
        else:
            flash("Désolé, il n'y a pas assez de places disponibles.", "danger")

    # Logique de commentaire
    if concert.est_passe and commentaire_form.validate_on_submit() and commentaire_form.publish.data:
        nouveau_commentaire = Commentaire(auteur=commentaire_form.auteur.data, contenu=commentaire_form.contenu.data, concert_id=concert.id)
        db.session.add(nouveau_commentaire)
        db.session.commit()
        flash("Votre commentaire a été publié !", "success")
        return redirect(url_for('main.concert_detail', concert_id=concert.id))

    return render_template('concert_detail.html', concert=concert, r_form=reservation_form, c_form=commentaire_form)

@main_bp.route('/actualites')
def actualites():
    liste_actus = Actualite.query.order_by(Actualite.date_publication.desc()).all()
    return render_template('actualites.html', actualites=liste_actus)

# --- Authentification ---

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Connexion réussie !', 'success')
            return redirect(url_for('admin.dashboard') if user.is_admin else url_for('main.index'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')
            
    return render_template('login.html', form=form)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = InscriptionForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Cet email est déjà utilisé.', 'danger')
        else:
            new_user = User(nom=form.nom.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('main.login'))
            
    return render_template('register.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))