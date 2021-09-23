import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from flaskr.modelos import Usuario, db, Cancion, Comentario

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
        cancion = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        user = Usuario(nombre='Angelica R', contrasena='1234')
        comentario = Comentario(comentario='Este es un comentario de prueba')
        db.session.add(user)
        user.canciones.append(cancion)
        user.comentarios.append(comentario)
        cancion.comentarios.append(comentario)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        canciones = [ca for ca in usuario.canciones]
        self.assertEqual(comentario.comentario, canciones[0].comentarios[0].comentario)
    
    def test_crear_comentario_cancion_compartida(self):
        cancion = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        user1 = Usuario(nombre='Angelica R', contrasena='1234')
        user2 = Usuario(nombre='Maria T', contrasena='12345')
        comentario = Comentario(comentario='Este es un comentario de prueba en una cancion compartida')
        db.session.add(user1)
        db.session.add(user2)
        user1.canciones.append(cancion)
        user2.cancionescompartidas.append(cancion)
        user2.comentarios.append(comentario)
        cancion.comentarios.append(comentario)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Maria T', Usuario.contrasena == '12345').first()
        canciones_compartidas = [cac for cac in usuario.cancionescompartidas]
        self.assertEqual(comentario.comentario, canciones_compartidas[0].comentarios[0].comentario)
    
    def test_ver_comentarios_cancion(self):
        cancion = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        user = Usuario(nombre='Angelica R', contrasena='1234')
        comentario = Comentario(comentario='Este es un comentario de prueba')
        comentario2 = Comentario(comentario='Este es otro comentario de prueba')
        db.session.add(user)
        user.canciones.append(cancion)
        cancion.comentarios.append(comentario)
        cancion.comentarios.append(comentario2)
        user.comentarios.append(comentario)
        user.comentarios.append(comentario2)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        canciones = [ca for ca in usuario.canciones]
        self.assertEqual(len(canciones[0].comentarios),2)

    def test_ver_comentarios_cancion_compartida(self):
        cancion = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        user1 = Usuario(nombre='Angelica R', contrasena='1234')
        user2 = Usuario(nombre='Maria T', contrasena='12345')
        comentario = Comentario(comentario='Este es un comentario de prueba en una cancion compartida del usuario dueno')
        comentario2 = Comentario(comentario='Este es un comentario de prueba en una cancion compartida del usuario al que se la compartieron')
        db.session.add(user1)
        db.session.add(user2)
        user1.canciones.append(cancion)
        user2.cancionescompartidas.append(cancion)
        user1.comentarios.append(comentario)
        user2.comentarios.append(comentario2)
        cancion.comentarios.append(comentario)
        cancion.comentarios.append(comentario2)
        db.session.commit()
        usuario1 = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        usuario2 = Usuario.query.filter(Usuario.nombre == 'Maria T', Usuario.contrasena == '12345').first()
        canciones_compartidas = [cac for cac in usuario2.cancionescompartidas]
        canciones = [ca for ca in usuario1.canciones]
        self.assertEqual(comentario.comentario, canciones_compartidas[0].comentarios[0].comentario)
        self.assertEqual(comentario.comentario, canciones[0].comentarios[0].comentario)
        self.assertEqual(comentario2.comentario, canciones_compartidas[0].comentarios[1].comentario)
        self.assertEqual(comentario2.comentario, canciones[0].comentarios[1].comentario)

    def test_ver_comentarios_de_usuario(self):
        cancion = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        user = Usuario(nombre='Angelica R', contrasena='1234')
        comentario = Comentario(comentario='Este es un comentario de prueba')
        comentario2 = Comentario(comentario='Este es otro comentario de prueba')
        db.session.add(user)
        user.canciones.append(cancion)
        cancion.comentarios.append(comentario)
        cancion.comentarios.append(comentario2)
        user.comentarios.append(comentario)
        user.comentarios.append(comentario2)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        canciones = [ca for ca in usuario.canciones]
        self.assertEqual(len(canciones[0].comentarios),2)
        self.assertEqual(len(usuario.comentarios),2)
        self.assertEqual(canciones[0].comentarios[0],usuario.comentarios[0])
        
        