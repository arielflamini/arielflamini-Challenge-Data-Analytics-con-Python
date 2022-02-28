from itertools import count
from msilib import Table
from tkinter import Tk, Canvas, Label, Frame, ttk, Entry
import tkinter as tk
import requests
import psycopg2
from datetime import date
import os
import pandas as pd
import db
from sqlalchemy import Column, Integer, String, DateTime
import json
from sqlalchemy.orm import sessionmaker

#Obtengo fecha actual
fecha = date.today()

#obtengo el mes de la fecha
mes = fecha.strftime("%B")

#Cambia al formato deseado
formato = fecha.strftime('%d-%m-%Y')

#class Cultura(db.Base):
class Cultura(db.Base):
  
  #armamos la base de datos
  __tablename__ = 'cultura'
  
  id = Column(Integer(), primary_key=True)
  cod_localidad = Column(Integer())
  id_provincia = Column(Integer())
  id_departamento = Column(Integer())
  categoria = Column(String(100))
  provincia = Column(String(100))
  localidad = Column(String(100))
  nombre = Column(String(200))
  domicilio = Column(String(200))
  codigo_postal = Column(String(100))
  telefono = Column(String(100))
  mail = Column(String(200))
  web = Column(String(200))
  fecha_carga = Column(DateTime(), default=fecha)

  #Creamos session para manipular datos
  Session = sessionmaker(db.engine)
  session = Session()
  
  #Contructor de la clase
  def __init__(self, id, cod_localidad, id_provincia, id_departamento, categoria, provincia, localidad, nombre, domicilio, codigo_postal, telefono, mail, web, fecha_carga):

   self.id = id
   self.cod_localidad = cod_localidad
   self.id_provincia = id_provincia
   self.id_departamento = id_departamento
   self.categoria = categoria
   self.provincia = provincia
   self.localidad = localidad
   self.nombre = nombre
   self.domicilio = domicilio
   self.codigo_postal = codigo_postal
   self.telefono = telefono
   self.mail = mail
   self.web = web
   self.fecha_carga = fecha_carga

def __str__(self):
    return self.categoria

#Descarga los archivos fuentes 
def descargar_archivos():
      
   #Defino el nombre de la carpeta o directorio a crear para museos
   directorio_museo = 'museos/'+str(fecha.year)+'-'+mes

   #Defino el nombre de la carpeta o directorio a crear para salas
   directorio_sala = 'salas/'+str(fecha.year)+'-'+mes

   #Defino el nombre de la carpeta o directorio a crear para biblio
   directorio_biblio = 'biblios/'+str(fecha.year)+'-'+mes

   #Si no existe el directorio, lo crea
   if(os.path.isdir(directorio_museo) == False):
      #crea el directorio
      os.makedirs(directorio_museo)
      print("Se ha creado el directorio: %s " % directorio_museo)

   if(os.path.isdir(directorio_sala) == False):
      #crea el directorio
      os.makedirs(directorio_sala)
      print("Se ha creado el directorio: %s " % directorio_sala)

   if(os.path.isdir(directorio_biblio) == False):
      #crea el directorio
      os.makedirs(directorio_biblio)
      print("Se ha creado el directorio: %s " % directorio_biblio)
   
   url_museo="https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museo.csv"
   url_sala="https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv"
   url_biblio="https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv"
      
   #respuesta_museo = requests.get(url_museo)
   respuesta_museo = requests.get(url_museo)
   respuesta_sala = requests.get(url_sala)
   respuesta_biblio = requests.get(url_biblio)

   archivo_museo = "/museos-"+str(formato)+".csv"
   archivo_sala = '/salas-'+str(formato)+".csv"
   archivo_biblio = '/biblios-'+str(formato)+".csv"

   ruta_archivo_museo = directorio_museo + archivo_museo
   ruta_archivo_sala = directorio_sala + archivo_sala
   ruta_archivo_biblio = directorio_biblio + archivo_biblio

   try:
          respuesta_museo
          #El código 200 me indica que se comunicó
          if respuesta_museo.status_code == 200:

             #genera y guarda el contenido en el archivo
             open(ruta_archivo_museo, 'wb').write(respuesta_museo.content)
             print("Se generó el archivo "+archivo_museo+" y se guardó en el directorio")
          else:
             print("no se ha encontrado recurso: ")
   except:
          print("la URL no existe")

   try:
          respuesta_sala
          #El código 200 me indica que se comunicó
          if respuesta_sala.status_code == 200:

             #genera y guarda el contenido en el archivo
             open(ruta_archivo_sala, 'wb').write(respuesta_sala.content)
             print("Se generó el archivo "+archivo_sala+" y se guardó en el directorio")
          else:
             print("no se ha encontrado recurso: ")
   except:
          print("la URL no existe")

   try:
          respuesta_biblio
          #El código 200 me indica que se comunicó
          if respuesta_biblio.status_code == 200:

             #genera y guarda el contenido en el archivo
             open(ruta_archivo_biblio, 'wb').write(respuesta_biblio.content)
             print("Se generó el archivo "+archivo_biblio+" y se guardó en el directorio")
          else:
             print("no se ha encontrado recurso: ")
   except:
          print("la URL no existe")
   
   crear_db(ruta_archivo_museo, ruta_archivo_biblio, ruta_archivo_sala)

def descargar_salas():
   pass

def descargar_biblios():
   pass

def mostrar_cantidades():
   pass

def mostrar_info_cines():
   pass 

def crear_db(ruta_museo, ruta_biblio, ruta_sala):  
  #leo los archivos
  museo = pd.read_csv(ruta_museo)
  objeto = json.loads(museo.to_json())

  i = 0
  while i < len(museo):
      loc = Cultura(i, objeto['Cod_Loc'][str(i)], 
                objeto['IdProvincia'][str(i)],
                objeto['IdDepartamento'][str(i)],
                objeto['categoria'][str(i)],
                objeto['provincia'][str(i)],
                objeto['localidad'][str(i)],
                objeto['nombre'][str(i)],
                objeto['direccion'][str(i)],
                objeto['CP'][str(i)],
                objeto['telefono'][str(i)],
                objeto['Mail'][str(i)],
                objeto['Web'][str(i)],
                fecha)

      db.Session()
      db.session.add(loc)
      db.session.commit()
      i=i+1

  db.engine.close()

def cerrar_ventana():
    pass

def crear_interfaz():

   #Creo la interfaz
   ventana = tk.Tk()
   #inicio la interfaz
   ventana.title("App Cultura")
   Label(ventana,text="Ingrese URL para descargar el archivo").grid(row=1, column=1, pady=10)
   url = Entry(ventana)
   url.focus()
   url.grid(row=2, column=1)

   boton_descarga = ttk.Button(ventana, text="Descargar archivos", command=descargar_archivos)
   #boton_descarga.pack()
   boton_descarga.grid(row=3, column=1)

   boton_cantidades = ttk.Button(ventana, text="Mostrar cantidades de registros", command=mostrar_cantidades)
   #boton_descarga.pack()
   boton_cantidades.grid(row=3, column=2)

   boton_cines = ttk.Button(ventana, text="Mostrar información de cines", command=mostrar_info_cines)
   #boton_descarga.pack()
   boton_cines.grid(row=3, column=3)

   boton_cerrar = ttk.Button(ventana, text="Cerrar Ventana", command=cerrar_ventana())
   #boton_descarga.pack()
   boton_cines.grid(row=3, column=3)
   ventana.mainloop()

#para asegurarme que ejecuta mi archivo
if __name__ == "__main__":
   #Cultura(cod_localidad, id_provincia, id_departamento, categoria, provincia, localidad, nombre, domicilio, codigo_postal, telefono, mail, web, fecha_carga)
   crear_interfaz()
   db.Base.metadata.drop_all(db.engine)
   db.Base.metadata.create_all(db.engine)

   
   




