from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Categorie, Actualite, Concert, Commentaire, User
from app.forms import CategorieForm, ActualiteForm, ConcertForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Sécurité : On vérifie avant chaque requête que l'utilisateur est bien un admin
@admin_bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        flash("Accès refusé. Vous n'avez pas les droits d'administration.", "danger")
        return redirect(url_for('main.index'))

# --- TABLEAU DE BORD ---
@admin_bp.route('/')
def dashboard():
    nb_categories = Categorie.query.count()
    nb_concerts = Concert.query.count()
    nb_actus = Actualite.query.count()
    nb_commentaires = Commentaire.query.count()
    return render_template('admin_dashboard.html', categories=nb_categories, concerts=nb_concerts, actus=nb_actus, commentaires=nb_commentaires)

# --- GESTION DES CATÉGORIES ---
@admin_bp.route('/categories')
def categories_list():
    categories = Categorie.query.all()
    return render_template('admin_categories.html', categories=categories)

@admin_bp.route('/categories/ajouter', methods=['GET', 'POST'])
def add_category():
    form = CategorieForm()
    if form.validate_on_submit():
        nouvelle_cat = Categorie(titre=form.titre.data, description=form.description.data)
        db.session.add(nouvelle_cat)
        db.session.commit()
        flash('Catégorie ajoutée avec succès.', 'success')
        return redirect(url_for('admin.categories_list'))
    return render_template('admin_edit.html', form=form, title="Ajouter une catégorie")

@admin_bp.route('/categories/modifier/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    categorie = Categorie.query.get_or_404(id)
    form = CategorieForm(obj=categorie)
    if form.validate_on_submit():
        categorie.titre = form.titre.data
        categorie.description = form.description.data
        db.session.commit()
        flash('Catégorie mise à jour.', 'success')
        return redirect(url_for('admin.categories_list'))
    return render_template('admin_edit.html', form=form, title="Modifier la catégorie")

@admin_bp.route('/categories/supprimer/<int:id>', methods=['POST'])
def delete_category(id):
    categorie = Categorie.query.get_or_404(id)
    db.session.delete(categorie)
    db.session.commit()
    flash('Catégorie supprimée.', 'success')
    return redirect(url_for('admin.categories_list'))

# --- GESTION DES CONCERTS ---
@admin_bp.route('/concerts')
def concerts_list():
    concerts = Concert.query.order_by(Concert.date_concert.desc()).all()
    return render_template('admin_concerts.html', concerts=concerts)

@admin_bp.route('/concerts/ajouter', methods=['GET', 'POST'])
def add_concert():
    form = ConcertForm()
    # On remplit la liste déroulante avec les catégories existantes
    form.categorie_id.choices = [(c.id, c.titre) for c in Categorie.query.all()]
    if form.validate_on_submit():
        concert = Concert(
            titre=form.titre.data, lieu=form.lieu.data, ville=form.ville.data,
            date_concert=form.date_concert.data, places_totales=form.places_totales.data,
            description=form.description.data, image_url=form.image_url.data,
            avis_redacteur=form.avis_redacteur.data, categorie_id=form.categorie_id.data
        )
        db.session.add(concert)
        db.session.commit()
        flash('Concert ajouté.', 'success')
        return redirect(url_for('admin.concerts_list'))
    return render_template('admin_edit.html', form=form, title="Ajouter un concert")

@admin_bp.route('/concerts/modifier/<int:id>', methods=['GET', 'POST'])
def edit_concert(id):
    concert = Concert.query.get_or_404(id)
    form = ConcertForm(obj=concert)
    form.categorie_id.choices = [(c.id, c.titre) for c in Categorie.query.all()]
    if form.validate_on_submit():
        form.populate_obj(concert) # Petite astuce pour tout mettre à jour d'un coup
        db.session.commit()
        flash('Concert mis à jour.', 'success')
        return redirect(url_for('admin.concerts_list'))
    return render_template('admin_edit.html', form=form, title="Modifier le concert")

@admin_bp.route('/concerts/supprimer/<int:id>', methods=['POST'])
def delete_concert(id):
    concert = Concert.query.get_or_404(id)
    db.session.delete(concert)
    db.session.commit()
    flash('Concert supprimé.', 'success')
    return redirect(url_for('admin.concerts_list'))

# --- GESTION DES ACTUALITÉS ---
@admin_bp.route('/actualites')
def actualites_list():
    actus = Actualite.query.order_by(Actualite.date_publication.desc()).all()
    return render_template('admin_actualites.html', actualites=actus)

@admin_bp.route('/actualites/ajouter', methods=['GET', 'POST'])
def add_actualite():
    form = ActualiteForm()
    form.categorie_id.choices = [(c.id, c.titre) for c in Categorie.query.all()]
    if form.validate_on_submit():
        actu = Actualite(
            titre=form.titre.data, resume=form.resume.data, contenu=form.contenu.data,
            image_url=form.image_url.data, categorie_id=form.categorie_id.data
        )
        db.session.add(actu)
        db.session.commit()
        flash('Actualité publiée.', 'success')
        return redirect(url_for('admin.actualites_list'))
    return render_template('admin_edit.html', form=form, title="Ajouter une actualité")

@admin_bp.route('/actualites/modifier/<int:id>', methods=['GET', 'POST'])
def edit_actualite(id):
    actu = Actualite.query.get_or_404(id)
    form = ActualiteForm(obj=actu)
    form.categorie_id.choices = [(c.id, c.titre) for c in Categorie.query.all()]
    if form.validate_on_submit():
        form.populate_obj(actu)
        db.session.commit()
        flash('Actualité mise à jour.', 'success')
        return redirect(url_for('admin.actualites_list'))
    return render_template('admin_edit.html', form=form, title="Modifier l'actualité")

@admin_bp.route('/actualites/supprimer/<int:id>', methods=['POST'])
def delete_actualite(id):
    actu = Actualite.query.get_or_404(id)
    db.session.delete(actu)
    db.session.commit()
    flash('Actualité supprimée.', 'success')
    return redirect(url_for('admin.actualites_list'))

# --- MODÉRATION DES COMMENTAIRES ---
@admin_bp.route('/commentaires')
def commentaires_list():
    commentaires = Commentaire.query.order_by(Commentaire.date_post.desc()).all()
    return render_template('admin_commentaires.html', commentaires=commentaires)

@admin_bp.route('/commentaires/supprimer/<int:id>', methods=['POST'])
def delete_commentaire(id):
    commentaire = Commentaire.query.get_or_404(id)
    db.session.delete(commentaire)
    db.session.commit()
    flash('Commentaire modéré (supprimé).', 'warning')
    return redirect(url_for('admin.commentaires_list'))