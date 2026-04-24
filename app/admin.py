from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.forms import CategoryForm, ConcertForm, NewsForm
from app.models import Category, Concert, NewsArticle

admin_bp = Blueprint("admin", __name__, template_folder="templates")


def admin_required(view):
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Accès administrateur requis.", "danger")
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    categories = Category.query.count()
    concerts = Concert.query.count()
    news = NewsArticle.query.count()
    return render_template("admin/dashboard.html", categories=categories, concerts=concerts, news=news)


@admin_bp.route("/categories")
@login_required
@admin_required
def categories():
    categories = Category.query.order_by(Category.title).all()
    return render_template("admin/categories.html", categories=categories)


@admin_bp.route("/categories/ajouter", methods=["GET", "POST"])
@login_required
@admin_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(title=form.title.data, description=form.description.data)
        db.session.add(category)
        db.session.commit()
        flash("Catégorie ajoutée.", "success")
        return redirect(url_for("admin.categories"))
    return render_template("admin/edit_category.html", form=form, title="Ajouter une catégorie")


@admin_bp.route("/categories/<int:category_id>/modifier", methods=["GET", "POST"])
@login_required
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.title = form.title.data
        category.description = form.description.data
        db.session.commit()
        flash("Catégorie mise à jour.", "success")
        return redirect(url_for("admin.categories"))
    return render_template("admin/edit_category.html", form=form, title="Modifier une catégorie")


@admin_bp.route("/categories/<int:category_id>/supprimer", methods=["POST"])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Catégorie supprimée.", "success")
    return redirect(url_for("admin.categories"))


@admin_bp.route("/news")
@login_required
@admin_required
def news_list():
    articles = NewsArticle.query.order_by(NewsArticle.published_at.desc()).all()
    return render_template("admin/news.html", articles=articles)


@admin_bp.route("/news/ajouter", methods=["GET", "POST"])
@login_required
@admin_required
def add_news():
    form = NewsForm()
    form.category_id.choices = [(c.id, c.title) for c in Category.query.order_by(Category.title)]
    if form.validate_on_submit():
        article = NewsArticle(
            title=form.title.data,
            summary=form.summary.data,
            content=form.content.data,
            category_id=form.category_id.data,
            image_url=form.image_url.data,
        )
        db.session.add(article)
        db.session.commit()
        flash("Article ajouté.", "success")
        return redirect(url_for("admin.news_list"))
    return render_template("admin/edit_news.html", form=form, title="Ajouter un article")


@admin_bp.route("/news/<int:article_id>/modifier", methods=["GET", "POST"])
@login_required
@admin_required
def edit_news(article_id):
    article = NewsArticle.query.get_or_404(article_id)
    form = NewsForm(obj=article)
    form.category_id.choices = [(c.id, c.title) for c in Category.query.order_by(Category.title)]
    if form.validate_on_submit():
        article.title = form.title.data
        article.summary = form.summary.data
        article.content = form.content.data
        article.category_id = form.category_id.data
        article.image_url = form.image_url.data
        db.session.commit()
        flash("Article mis à jour.", "success")
        return redirect(url_for("admin.news_list"))
    return render_template("admin/edit_news.html", form=form, title="Modifier l’article")


@admin_bp.route("/news/<int:article_id>/supprimer", methods=["POST"])
@login_required
@admin_required
def delete_news(article_id):
    article = NewsArticle.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash("Article supprimé.", "success")
    return redirect(url_for("admin.news_list"))


@admin_bp.route("/concerts")
@login_required
@admin_required
def concerts_list():
    concerts = Concert.query.order_by(Concert.date.asc()).all()
    return render_template("admin/concerts.html", concerts=concerts)


@admin_bp.route("/concerts/ajouter", methods=["GET", "POST"])
@login_required
@admin_required
def add_concert():
    form = ConcertForm()
    form.category_id.choices = [(c.id, c.title) for c in Category.query.order_by(Category.title)]
    if form.validate_on_submit():
        concert = Concert(
            title=form.title.data,
            venue=form.venue.data,
            city=form.city.data,
            date=form.date.data,
            ticket_limit=form.ticket_limit.data,
            category_id=form.category_id.data,
            description=form.description.data,
            image_url=form.image_url.data,
            review=form.review.data,
        )
        db.session.add(concert)
        db.session.commit()
        flash("Concert ajouté.", "success")
        return redirect(url_for("admin.concerts_list"))
    return render_template("admin/edit_concert.html", form=form, title="Ajouter un concert")


@admin_bp.route("/concerts/<int:concert_id>/modifier", methods=["GET", "POST"])
@login_required
@admin_required
def edit_concert(concert_id):
    concert = Concert.query.get_or_404(concert_id)
    form = ConcertForm(obj=concert)
    form.category_id.choices = [(c.id, c.title) for c in Category.query.order_by(Category.title)]
    if form.validate_on_submit():
        concert.title = form.title.data
        concert.venue = form.venue.data
        concert.city = form.city.data
        concert.date = form.date.data
        concert.ticket_limit = form.ticket_limit.data
        concert.category_id = form.category_id.data
        concert.description = form.description.data
        concert.image_url = form.image_url.data
        concert.review = form.review.data
        db.session.commit()
        flash("Concert mis à jour.", "success")
        return redirect(url_for("admin.concerts_list"))
    return render_template("admin/edit_concert.html", form=form, title="Modifier le concert")


@admin_bp.route("/concerts/<int:concert_id>/supprimer", methods=["POST"])
@login_required
@admin_required
def delete_concert(concert_id):
    concert = Concert.query.get_or_404(concert_id)
    db.session.delete(concert)
    db.session.commit()
    flash("Concert supprimé.", "success")
    return redirect(url_for("admin.concerts_list"))
