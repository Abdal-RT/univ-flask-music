from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager
from app.forms import CommentForm, ConcertForm, LoginForm, RegisterForm, ReservationForm
from app.models import Category, Concert, NewsArticle, Reservation, User

main_bp = Blueprint("main", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main_bp.route("/")
def home():
    latest_news = NewsArticle.query.order_by(NewsArticle.published_at.desc()).limit(4).all()
    upcoming = Concert.query.filter(Concert.date >= date.today()).order_by(Concert.date.asc()).limit(4).all()
    return render_template("home.html", latest_news=latest_news, upcoming=upcoming)


@main_bp.route("/concerts")
def concerts():
    categories = Category.query.order_by(Category.title).all()
    selected_category = request.args.get("category", type=int)
    selected_city = request.args.get("city", type=str)
    selected_date = request.args.get("date", type=str)

    query = Concert.query.filter(Concert.date >= date.today())
    if selected_category:
        query = query.filter_by(category_id=selected_category)
    if selected_city:
        query = query.filter(Concert.city.ilike(f"%{selected_city}%"))
    if selected_date:
        try:
            query = query.filter(Concert.date == selected_date)
        except ValueError:
            pass

    concerts = query.order_by(Concert.date.asc()).all()
    return render_template(
        "concerts.html",
        concerts=concerts,
        categories=categories,
        selected_category=selected_category,
        selected_city=selected_city,
        selected_date=selected_date,
    )


@main_bp.route("/concerts/passes")
def past_concerts():
    concerts = Concert.query.filter(Concert.date < date.today()).order_by(Concert.date.desc()).all()
    return render_template("past_concerts.html", concerts=concerts)


@main_bp.route("/concerts/<int:concert_id>", methods=["GET", "POST"])
def concert_detail(concert_id):
    concert = Concert.query.get_or_404(concert_id)
    reservation_form = ReservationForm()
    comment_form = CommentForm()

    if reservation_form.validate_on_submit() and "submit" in request.form:
        if not current_user.is_authenticated:
            flash("Vous devez être connecté pour réserver.", "warning")
            return redirect(url_for("main.login"))

        seats = reservation_form.seats.data
        if seats > concert.available_seats:
            flash("Le nombre de places demandé dépasse la capacité disponible.", "danger")
        else:
            concert.reserved_seats += seats
            reservation = Reservation(seats=seats, concert=concert, user=current_user)
            db.session.add(reservation)
            db.session.commit()
            flash("Réservation réussie !", "success")
            return redirect(url_for("main.concert_detail", concert_id=concert_id))

    if comment_form.validate_on_submit() and "author" in request.form:
        comment = Comment(
            author=comment_form.author.data,
            content=comment_form.content.data,
            concert=concert,
        )
        db.session.add(comment)
        db.session.commit()
        flash("Commentaire publié.", "success")
        return redirect(url_for("main.concert_detail", concert_id=concert_id))

    return render_template(
        "concert_detail.html",
        concert=concert,
        reservation_form=reservation_form,
        comment_form=comment_form,
    )


@main_bp.route("/news")
def news():
    categories = Category.query.order_by(Category.title).all()
    articles = NewsArticle.query.order_by(NewsArticle.published_at.desc()).all()
    return render_template("news.html", categories=categories, articles=articles)


@main_bp.route("/news/categorie/<int:category_id>")
def news_category(category_id):
    category = Category.query.get_or_404(category_id)
    articles = NewsArticle.query.filter_by(category_id=category.id).order_by(NewsArticle.published_at.desc()).all()
    return render_template("news_category.html", category=category, articles=articles)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Connexion réussie.", "success")
            return redirect(request.args.get("next") or url_for("main.home"))

        flash("Email ou mot de passe invalide.", "danger")

    return render_template("login.html", form=form)


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Un compte avec cet e-mail existe déjà.", "warning")
        else:
            user = User(
                email=form.email.data,
                name=form.name.data,
                password=generate_password_hash(form.password.data),
                is_admin=False,
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Compte créé avec succès.", "success")
            return redirect(url_for("main.home"))

    return render_template("register.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for("main.home"))
