from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(15))  # Nuevo campo agregado
    creado_en = db.Column(db.DateTime, default=db.func.current_timestamp())
    es_admin = db.Column(db.Boolean, default=False)

class Perfil(db.Model):
    __tablename__ = 'Perfil'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    foto = db.Column(db.String(255))
    direccion = db.Column(db.Text)
    usuario = db.relationship('Usuario', backref=db.backref('perfil', uselist=False))

class Categoria(db.Model):
    __tablename__ = 'Categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class Marca(db.Model):
    __tablename__ = 'Marca'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

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
    categoria = db.relationship('Categoria', backref=db.backref('productos', lazy=True))
    marca = db.relationship('Marca', backref=db.backref('productos', lazy=True))