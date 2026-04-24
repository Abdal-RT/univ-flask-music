from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Se connecter")

class InscriptionForm(FlaskForm):
    nom = StringField("Nom", validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=4)])
    confirm = PasswordField("Confirmer le mot de passe", validators=[DataRequired(), EqualTo("password", message="Les mots de passe doivent correspondre")])
    submit = SubmitField("Créer un compte")

class CategorieForm(FlaskForm):
    titre = StringField("Titre", validators=[DataRequired(), Length(max=80)])
    description = TextAreaField("Description", validators=[Length(max=300)])
    submit = SubmitField("Enregistrer")

class ActualiteForm(FlaskForm):
    titre = StringField("Titre", validators=[DataRequired(), Length(max=150)])
    resume = TextAreaField("Résumé", validators=[DataRequired(), Length(max=300)])
    contenu = TextAreaField("Contenu", validators=[DataRequired()])
    categorie_id = SelectField("Catégorie", coerce=int, validators=[DataRequired()])
    image_url = StringField("URL de l'image", validators=[Length(max=255)])
    submit = SubmitField("Enregistrer l’article")

class ConcertForm(FlaskForm):
    titre = StringField("Titre", validators=[DataRequired(), Length(max=150)])
    lieu = StringField("Lieu", validators=[DataRequired(), Length(max=120)])
    ville = StringField("Ville", validators=[DataRequired(), Length(max=80)])
    date_concert = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    places_totales = IntegerField("Nombre de places", validators=[DataRequired(), NumberRange(min=1)])
    categorie_id = SelectField("Catégorie", coerce=int, validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    image_url = StringField("URL de l'image", validators=[Length(max=255)])
    avis_redacteur = TextAreaField("Avis du rédacteur")
    submit = SubmitField("Enregistrer le concert")

class ReservationForm(FlaskForm):
    places = IntegerField("Nombre de places", validators=[DataRequired(), NumberRange(min=1, max=10)])
    reserve = SubmitField("Réserver")

class CommentaireForm(FlaskForm):
    auteur = StringField("Nom", validators=[DataRequired(), Length(max=80)])
    contenu = TextAreaField("Commentaire", validators=[DataRequired(), Length(max=300)])
    publish = SubmitField("Publier")