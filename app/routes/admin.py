from flask import Blueprint, render_template, url_for # type: ignore
from app.models import Producto, Categoria, Marca, Usuario

# Crear el blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Identifica que tabla se va a mostrar
@admin_bp.route('/admin/<component>')
def admin_panel(component):
    productos = Producto.query.all()  # Obtener productos desde la base de datos
    categorias = Categoria.query.all()
    marcas = Marca.query.all()
    usuarios = Usuario.query.all()
    
    if component == 'productos':
        return render_template('pages/perfil.html', user_role='administrador', productos=productos, categorias=categorias, marcas=marcas, usuarios=usuarios, active_component='tabla_producto')
    elif component == 'catalogo':
        return render_template('pages/perfil.html', user_role='administrador', categorias=categorias, marcas=marcas, usuarios=usuarios, active_component='tabla_catalogo')
    elif component == 'marcas':
        return render_template('pages/perfil.html', user_role='administrador', categorias=categorias, marcas=marcas, usuarios=usuarios, active_component='tabla_marcas')
    else:
        return render_template('pages/perfil.html', user_role='administrador', categorias=categorias, marcas=marcas, usuarios=usuarios, active_component='default')
    