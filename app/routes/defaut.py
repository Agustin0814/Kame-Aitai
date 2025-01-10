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
    usuario = session.get('usuario')
    return render_template('pages/contacto.html', usuario=usuario)

@default_bp.route('/servicios')
def servicios():
    usuario = session.get('usuario')
    return render_template('pages/servicios.html', usuario=usuario)

@default_bp.route('/subasta')
def subasta():
    usuario = session.get('usuario')
    return render_template('pages/subasta.html', usuario=usuario)