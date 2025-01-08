
CREATE DATABASE IF NOT EXISTS Kame;
USE Kame;

CREATE TABLE Rol (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rol VARCHAR(50) NOT NULL
);

CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    correo VARCHAR(120) UNIQUE NOT NULL,
    contraseña VARCHAR(200) NOT NULL,
    telefono VARCHAR(15),
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    rol_id INT NOT NULL,
    FOREIGN KEY (rol_id) REFERENCES Rol(id)
);

CREATE TABLE Categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    foto VARCHAR(255),
    color VARCHAR(50)
);

CREATE TABLE Marca (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    foto VARCHAR(255)
);

CREATE TABLE Producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    costo DECIMAL(10, 2) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    existencia INT NOT NULL,
    marca_id INT,
    foto VARCHAR(255),
    categoria_id INT NOT NULL,
    propietario INT,
    FOREIGN KEY (marca_id) REFERENCES Marca(id),
    FOREIGN KEY (categoria_id) REFERENCES Categoria(id),
    FOREIGN KEY (propietario) REFERENCES Usuarios(id)
);

CREATE TABLE Historial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id),
    FOREIGN KEY (producto_id) REFERENCES Producto(id)
);

CREATE TABLE Perfil (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    foto VARCHAR(255),
    direccion TEXT,
    historial_id INT,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (historial_id) REFERENCES Historial(id)
);