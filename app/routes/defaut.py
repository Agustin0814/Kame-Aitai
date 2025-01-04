from flask import Blueprint, render_template, session
from app.models import Categoria, Marca

# Crea un Blueprint para este módulo
default_bp = Blueprint('default', __name__, url_prefix='/default')

@default_bp.route('/')
def index():
    usuario = session.get('usuario')
    categorias = Categoria.query.all()
    marcas = Marca.query.all()
    return render_template('pages/home.html', usuario=usuario, categorias=categorias, marcas=marcas)

@default_bp.route('/contacto')
def contacto():
    return render_template('pages/contacto.html')
