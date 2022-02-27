from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Configuro conexión
motor_bd = 'postgresql'
usuario_bd = 'postgres'
contrasena_bd = 'root'
ip_bd = 'localhost'
nombre_bd = 'cultura'
nuevo_engine = create_engine(motor_bd+'://'+usuario_bd+':'+contrasena_bd+'@'+ip_bd+'/'+nombre_bd)
engine = nuevo_engine.connect()

#Creamos session para manipular datos
Session = sessionmaker(engine)
session = Session()

Base = declarative_base()