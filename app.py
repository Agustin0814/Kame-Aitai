from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, Usuario, Producto, Categoria, Marca, Perfil, Rol, Historial

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    usuario = session.get('usuario')
    categorias = Categoria.query.all()
    marcas = Marca.query.all()
    return render_template('pages/home.html', usuario=usuario, categorias=categorias, marcas=marcas)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['username']
        contraseña = request.form['password']
        user = Usuario.query.filter_by(correo=correo).first()
        if user:
            if check_password_hash(user.contraseña, contraseña):
                session['usuario'] = {'username': user.username, 'correo': user.correo, 'es_admin': user.rol.rol == 'admin'}  # Guardar usuario en la sesión
                return redirect(url_for('index'))
        return redirect(url_for('login'))
    return render_template('pages/login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        if not username or not nombre or not correo or not contraseña:
            # Manejar error de campos faltantes
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(contraseña, method='pbkdf2:sha256')
        nuevo_usuario = Usuario(username=username, nombre=nombre, correo=correo, contraseña=hashed_password, rol_id=1)  # Asignar rol de cliente
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('pages/register.html')

@app.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('pages/productos.html', productos=productos)

@app.route('/contacto')
def contacto():
    return render_template('pages/contacto.html')

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    usuario = session['usuario']
    user = Usuario.query.filter_by(correo=usuario['correo']).first()
    perfil = Perfil.query.filter_by(usuario_id=user.id).first()
    user_role = user.rol.rol.lower()  # Obtener el rol del usuario en minúsculas
    productos = Producto.query.all()  
    categorias = Categoria.query.all()  
    marcas = Marca.query.all()
    return render_template('pages/perfil.html', usuario=user, perfil=perfil, user_role=user_role, admin_username=user.username if user.rol.rol == 'Administrador' else None, productos=productos, categorias=categorias, marcas=marcas)

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    costo = request.form['costo']
    precio = request.form['precio']
    existencia = request.form['existencia']
    marca_id = request.form['marca_id'] if request.form['marca_id'] else None
    foto = request.form['foto']
    categoria_id = request.form['categoria_id']

    nuevo_producto = Producto(
        nombre=nombre,
        descripcion=descripcion,
        costo=costo,
        precio=precio,
        existencia=existencia,
        marca_id=marca_id,
        foto=foto,
        categoria_id=categoria_id
    )

    db.session.add(nuevo_producto)
    db.session.commit()

    return redirect(url_for('perfil'))

@app.route('/editar_producto', methods=['POST'])
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

@app.route('/eliminar_producto/<int:producto_id>')
def eliminar_producto(producto_id):
    producto = Producto.query.get(producto_id)
    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for('perfil'))

@app.route('/editar_perfil', methods=['POST'])
def editar_perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']
    user = Usuario.query.filter_by(correo=usuario['correo']).first()
    perfil = Perfil.query.filter_by(usuario_id=user.id).first()

    user.telefono = request.form['telefono']
    
    if perfil:
        perfil.foto = request.form['foto']
        perfil.direccion = request.form['direccion']
    else:
        new_profile = Perfil(usuario_id=user.id, foto=request.form['foto'], direccion=request.form['direccion'])
        db.session.add(new_profile)

    db.session.commit()

    session['usuario'] = {'username': user.username, 'correo': user.correo, 'es_admin': user.rol.rol == 'admin'}
    return redirect(url_for('perfil'))

if __name__ == '__main__':
    app.run(debug=True)