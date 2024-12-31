from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, Usuario, Producto, Categoria, Marca, Perfil 

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
                session['usuario'] = {'username': user.username, 'correo': user.correo, 'es_admin': user.es_admin}  # Guardar usuario en la sesión
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
        telefono = request.form.get('telefono') 

        if not username or not nombre or not correo or not contraseña:
            return redirect(url_for('register'))
        
        existing_user = Usuario.query.filter_by(correo=correo).first()
        if existing_user:
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(contraseña, method='pbkdf2:sha256')
        new_user = Usuario(username=username, nombre=nombre, correo=correo, contraseña=hashed_password, telefono=telefono)
        db.session.add(new_user)
        db.session.commit()

        new_profile = Perfil(usuario_id=new_user.id)
        db.session.add(new_profile)
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
    user_role = 'admin' if user.es_admin else 'cliente' 
    productos = Producto.query.all()  
    categorias = Categoria.query.all()  
    marcas = Marca.query.all()
    return render_template('pages/perfil.html', usuario=user, perfil=perfil, user_role=user_role, admin_username=user.username if user.es_admin else None, productos=productos, categorias=categorias, marcas=marcas)

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

    user.username = request.form['username']
    user.nombre = request.form['nombre']
    user.correo = request.form['correo']
    user.telefono = request.form['telefono']
    if request.form['contraseña']:
        user.contraseña = generate_password_hash(request.form['contraseña'], method='pbkdf2:sha256')

    if perfil:
        perfil.foto = request.form['foto']
        perfil.direccion = request.form['direccion']
    else:
        new_profile = Perfil(usuario_id=user.id, foto=request.form['foto'], direccion=request.form['direccion'])
        db.session.add(new_profile)

    db.session.commit()

    session['usuario'] = {'username': user.username, 'correo': user.correo, 'es_admin': user.es_admin}
    return redirect(url_for('perfil'))

if __name__ == '__main__':
    app.run(debug=True)