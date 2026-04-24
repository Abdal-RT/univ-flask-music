from flask import Blueprint
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def dashboard():
    return "Bienvenue dans l'administration (En construction)"