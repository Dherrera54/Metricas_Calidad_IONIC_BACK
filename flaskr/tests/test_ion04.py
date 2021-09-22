import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from modelos import Usuario, db, Cancion, Comentario

#from flaskr.modelos import db, Cancion, Usuario, CancionSchema


class ComentariosTest(unittest.TestCase):
    
    @staticmethod
    def create_app(self):
        app = Flask(__name__)         
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY']='frase-secreta'       
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial_canciones.db'
        return app

    def setUp(self):
        app = ComentariosTest.create_app(self)
        SQLAlchemy(app)
        app_context = app.app_context()
        app_context.push()
        db.init_app(app)
        db.create_all()         

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_crear_comentario(self):
        c = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        u = Usuario(nombre='Angelica R', contrasena='1234')
        comentario = Comentario(comentario='Este es un comentario de prueba')
        db.session.add(u)
        u.canciones.append(c)
        u.comentarios.append(comentario)
        c.comentarios.append(comentario)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        print(usuario.nombre)
        canciones = [ca for ca in usuario.canciones]
        print(canciones[0].comentarios[0].comentario)
        self.assertEqual(comentario.comentario, canciones[0].comentarios[0].comentario)
    
    def test_crear_comentario_cancion_compartida(self):
        c = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        u = Usuario(nombre='Angelica R', contrasena='1234')
        u2 = Usuario(nombre='Maria T', contrasena='12345')
        comentario = Comentario(comentario='Este es un comentario de prueba en una cancion compartida')
        db.session.add(u)
        db.session.add(u2)
        u.canciones.append(c)
        u2.cancionescompartidas.append(c)
        u2.comentarios.append(comentario)
        c.comentarios.append(comentario)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Maria T', Usuario.contrasena == '12345').first()
        print(usuario.nombre)
        canciones_compartidas = [cac for cac in usuario.cancionescompartidas]
        print(canciones_compartidas[0].comentarios[0].comentario)
        self.assertEqual(comentario.comentario, canciones_compartidas[0].comentarios[0].comentario)
    
    def test_ver_comentarios_cancion(self):
        c = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        u = Usuario(nombre='Angelica R', contrasena='1234')
        comentario = Comentario(comentario='Este es un comentario de prueba')
        comentario2 = Comentario(comentario='Este es otro comentario de prueba')
        db.session.add(u)
        u.canciones.append(c)
        c.comentarios.append(comentario)
        c.comentarios.append(comentario2)
        u.comentarios.append(comentario)
        u.comentarios.append(comentario2)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        print(usuario.nombre)
        canciones = [ca for ca in usuario.canciones]
        print(len(canciones[0].comentarios))
        self.assertEqual(len(canciones[0].comentarios),2)

    def test_ver_comentarios_cancion_compartida(self):
        c = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        u = Usuario(nombre='Angelica R', contrasena='1234')
        u2 = Usuario(nombre='Maria T', contrasena='12345')
        comentario = Comentario(comentario='Este es un comentario de prueba en una cancion compartida del usuario dueno')
        comentario2 = Comentario(comentario='Este es un comentario de prueba en una cancion compartida del usuario al que se la compartieron')
        db.session.add(u)
        db.session.add(u2)
        u.canciones.append(c)
        u2.cancionescompartidas.append(c)
        u.comentarios.append(comentario)
        u2.comentarios.append(comentario2)
        c.comentarios.append(comentario)
        c.comentarios.append(comentario2)
        db.session.commit()
        usuario1 = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        usuario2 = Usuario.query.filter(Usuario.nombre == 'Maria T', Usuario.contrasena == '12345').first()
        canciones_compartidas = [cac for cac in usuario2.cancionescompartidas]
        canciones = [ca for ca in usuario1.canciones]
        print(canciones_compartidas[0].comentarios[0].comentario)
        self.assertEqual(comentario.comentario, canciones_compartidas[0].comentarios[0].comentario)
        self.assertEqual(comentario.comentario, canciones[0].comentarios[0].comentario)
        self.assertEqual(comentario2.comentario, canciones_compartidas[0].comentarios[1].comentario)
        self.assertEqual(comentario2.comentario, canciones[0].comentarios[1].comentario)

    def test_ver_comentarios_de_usuario(self):
        c = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        u = Usuario(nombre='Angelica R', contrasena='1234')
        comentario = Comentario(comentario='Este es un comentario de prueba')
        comentario2 = Comentario(comentario='Este es otro comentario de prueba')
        db.session.add(u)
        u.canciones.append(c)
        c.comentarios.append(comentario)
        c.comentarios.append(comentario2)
        u.comentarios.append(comentario)
        u.comentarios.append(comentario2)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        canciones = [ca for ca in usuario.canciones]
        print(len(canciones[0].comentarios))
        self.assertEqual(len(canciones[0].comentarios),2)
        self.assertEqual(len(usuario.comentarios),2)
        self.assertEqual(canciones[0].comentarios[0],usuario.comentarios[0])
        
        