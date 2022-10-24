import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from modelos import Usuario, db, Cancion

#from flaskr.modelos import db, Cancion, Usuario, CancionSchema


class VerCancionesTest(unittest.TestCase):
    
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
        app = VerCancionesTest.create_app(self)
        SQLAlchemy(app)
        app_context = app.app_context()
        app_context.push()
        db.init_app(app)
        db.create_all()         

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #Pruebas SCRUD
    def test_crear_cancion(self):
        cancion = Cancion(titulo='prueba', minutos=2, segundos=5,interprete='carolina')
        user = Usuario(nombre='Angelica R', contrasena='1234')
        db.session.add(user)
        user.canciones.append(cancion)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        canciones = [ca for ca in usuario.canciones]
        self.assertEqual(cancion.titulo, canciones[0].titulo)
    
    def test_visualizar_canciones_usuario(self):
        cancion1 = Cancion(titulo='prueba1', minutos=2, segundos=5,interprete='carolina')
        user1 = Usuario(nombre='Angelica R', contrasena='1234')
        cancion2 = Cancion(titulo='prueba2', minutos=2, segundos=5,interprete='carolina')
        user2 = Usuario(nombre='Maria R', contrasena='1234')
        db.session.add(user1)
        db.session.add(user2)
        user1.canciones.append(cancion1)
        user2.canciones.append(cancion2)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        usuario2 = Usuario.query.filter(Usuario.nombre == 'Maria R', Usuario.contrasena == '1234').first()
        canciones = [ca for ca in usuario.canciones]
        canciones2 = [ca for ca in usuario2.canciones]
        self.assertEqual(len(canciones), 1)
        self.assertEqual(cancion2.titulo, canciones2[0].titulo)

    def test_no_visualizar_canciones_de_otro_usuario(self):
        cancion1 = Cancion(titulo='prueba1', minutos=2, segundos=5,interprete='carolina')
        user1 = Usuario(nombre='Angelica R', contrasena='1234')
        cancion2 = Cancion(titulo='prueba2', minutos=2, segundos=5,interprete='carolina')
        user2 = Usuario(nombre='Maria R', contrasena='1234')
        db.session.add(user1)
        db.session.add(user2)
        user1.canciones.append(cancion1)
        user2.canciones.append(cancion2)
        db.session.commit()
        usuario = Usuario.query.filter(Usuario.nombre == 'Angelica R', Usuario.contrasena == '1234').first()
        usuario2 = Usuario.query.filter(Usuario.nombre == 'Maria R', Usuario.contrasena == '1234').first()
        canciones = [ca for ca in usuario.canciones]
        canciones2 = [ca for ca in usuario2.canciones]
        self.assertEqual(len(canciones), 1)
        self.assertNotEqual(cancion1.titulo, canciones2[0].titulo)
