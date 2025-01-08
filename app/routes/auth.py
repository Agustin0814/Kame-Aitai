from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Usuario
from app import db

auth_bp = Blueprint('auth', __name__)

# Ruta para login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['username']
        contraseña = request.form['password']
        user = Usuario.query.filter_by(correo=correo).first()
        if user and check_password_hash(user.contraseña, contraseña):
            session['usuario'] = {'username': user.username, 'correo': user.correo, 'es_admin': user.rol.rol == 'admin'}  # Guardar usuario en la sesión
            return redirect(url_for('default.index'))
        return redirect(url_for('auth.login'))
    return render_template('pages/auth.html')

# Ruta para logout
@auth_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('default.index'))

# Ruta para registro
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        if not username or not nombre or not correo or not contraseña:
            # Manejar error de campos faltantes
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(contraseña, method='pbkdf2:sha256')
        nuevo_usuario = Usuario(username=username, nombre=nombre, correo=correo, contraseña=hashed_password, rol_id=1)  # Asignar rol de cliente
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('pages/auth.html')
