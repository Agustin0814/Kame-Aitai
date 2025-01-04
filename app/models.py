from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

# Tabla para roles
class Rol(db.Model):
    __tablename__ = 'Rol'
    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(50), nullable=False)

# Tabla para usuarios
class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(15))
    creado_en = db.Column(db.DateTime, default=db.func.current_timestamp())
    rol_id = db.Column(db.Integer, db.ForeignKey('Rol.id'), nullable=False)
    rol = db.relationship('Rol', backref=db.backref('usuarios', lazy=True))

# Tabla para perfiles
class Perfil(db.Model):
    __tablename__ = 'Perfil'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    foto = db.Column(db.String(255))
    direccion = db.Column(db.Text)
    historial_id = db.Column(db.Integer, db.ForeignKey('Historial.id'))
    usuario = db.relationship('Usuario', backref=db.backref('perfil', uselist=False))
    historial = db.relationship('Historial', backref=db.backref('perfil', uselist=False))

# Tabla para categorias
class Categoria(db.Model):
    __tablename__ = 'Categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(255))  
    color = db.Column(db.String(50))

# Tabla para marcas
class Marca(db.Model):
    __tablename__ = 'Marca'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(255))

# Tabla para productos
class Producto(db.Model):
    __tablename__ = 'Producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    costo = db.Column(db.Numeric(10, 2), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    existencia = db.Column(db.Integer, nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('Marca.id'))
    foto = db.Column(db.String(255))
    categoria_id = db.Column(db.Integer, db.ForeignKey('Categoria.id'), nullable=False)
    propietario = db.Column(db.Integer, db.ForeignKey('Usuarios.id')) 
    categoria = db.relationship('Categoria', backref=db.backref('productos', lazy=True))
    marca = db.relationship('Marca', backref=db.backref('productos', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('productos', lazy=True))

# Tabla para historial
class Historial(db.Model):
    __tablename__ = 'Historial'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('Producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    usuario = db.relationship('Usuario', backref=db.backref('historial', lazy=True))
    producto = db.relationship('Producto', backref=db.backref('historial', lazy=True))