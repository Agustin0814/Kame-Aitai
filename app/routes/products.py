from flask import Blueprint, request, redirect, url_for, render_template # type: ignore
from app.models import Producto, db

# Crear el blueprint
products_bp = Blueprint('products', __name__, url_prefix='/products')

# Ruta para ver todos los productos
@products_bp.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('pages/productos.html', productos=productos)

# Ruta para agregar un producto
@products_bp.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    costo = request.form['costo']
    precio = request.form['precio']
    existencia = request.form['existencia']
    marca_id = request.form['marca_id'] if request.form['marca_id'] else None
    foto = request.form['foto']
    categoria_id = request.form['categoria_id']
    propietario_id = request.form['propietario_id']

    nuevo_producto = Producto(
        nombre=nombre,
        descripcion=descripcion,
        costo=costo,
        precio=precio,
        existencia=existencia,
        marca_id=marca_id,
        foto=foto,
        categoria_id=categoria_id,
        propietario=propietario_id  # Asignar propietario
    )

    db.session.add(nuevo_producto)
    db.session.commit()

    return redirect(url_for('perfil'))

# Ruta para editar un producto
@products_bp.route('/editar_producto', methods=['POST'])
def editar_producto():
    producto_id = request.form['id']
    producto = Producto.query.get(producto_id)
    producto.nombre = request.form['nombre']
    producto.descripcion = request.form['descripcion']
    producto.costo = request.form['costo']
    producto.precio = request.form['precio']
    producto.existencia = request.form['existencia']
    producto.marca_id = request.form['marca_id'] if request.form['marca_id'] else None
    producto.foto = request.form['foto']
    producto.categoria_id = request.form['categoria_id']

    db.session.commit()

    return redirect(url_for('perfil'))

# Ruta para eliminar un producto
@products_bp.route('/eliminar_producto/<int:producto_id>')
def eliminar_producto(producto_id):
    producto = Producto.query.get(producto_id)
    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for('perfil'))
