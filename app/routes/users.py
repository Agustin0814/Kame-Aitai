from flask import Blueprint, render_template, request, session, redirect, url_for # type: ignore
from app.models import Categoria, Marca, Producto, Usuario, Perfil, db

# Crear el blueprint
users_bp = Blueprint('users', __name__, url_prefix='/users')

# Ruta para ver el perfil de usuario
@users_bp.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
    
    usuario = session['usuario']
    user = Usuario.query.filter_by(correo=usuario['correo']).first()
    perfil = Perfil.query.filter_by(usuario_id=user.id).first()
    user_role = user.rol.rol.lower()  # Obtener el rol del usuario en minúsculas
    productos = Producto.query.all()
    categorias = Categoria.query.all()
    marcas = Marca.query.all()
    
    return render_template(
        'pages/perfil.html',
        usuario=user,
        perfil=perfil,
        user_role=user_role,
        admin_username=user.username if user.rol.rol == 'administrador' else None,
        productos=productos,
        categorias=categorias,
        marcas=marcas
    )
@users_bp.route('/editar_perfil', methods=['POST'])
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
    return redirect(url_for('users.perfil'))
