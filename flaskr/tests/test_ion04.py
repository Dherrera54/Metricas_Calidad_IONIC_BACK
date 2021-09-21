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
    
    