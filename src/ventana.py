import tkinter as tk
from tkinter import ttk
from cultura import *
import os
from datetime import date
import requests

class Ventana(tk.Frame):
    cul = Cultura()
    
#Contructor de la clase
    def __init__(self, master=None):
      super().__init__(master, width=300, height=300)
      self.master = master
      self.pack()

      self.crear_interfaz()
      #self.descargar_archivos()
      #self.mostrar_cantidades()
      #self.mostrar_info_cines()

    def crear_interfaz(self):

      label_url_museo = ttk.Label(self,text="Ingrese URL para descargar el archivo").place(x=0, y=0)
      url_museo = ttk.Entry(self.master).place(x=0, y=30)

      self.boton_descarga = ttk.Button(self, text="Descargar archivos", command=self.descargar_archivos)
      #self.boton_descarga["command"] = self.descargar_archivos()
      self.boton_descarga.place(x=0, y=50)

      self.boton_cantidades = ttk.Button(self, text="Mostrar cantidades de registros", command=self.mostrar_cantidades)
      #self.boton_cantidades["command"] = self.mostrar_cantidades()
      self.boton_cantidades.place(x=0, y=80)

      self.boton_cines = ttk.Button(self, text="Mostrar información de cines", command=self.mostrar_info_cines)
      #self.boton_cines["command"] = self.mostrar_info_cines()
      self.boton_cines.place(x=0, y=110)

    #Descarga los archivos fuentes 
    def descargar_archivos(self):
      #Obtengo fecha actual
      fecha = date.today()

      #obtengo el mes de la fecha
      mes = fecha.strftime("%B")

      #Cambia al formato deseado
      formato = fecha.strftime('%d-%m-%Y')
      
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
      print("La ruta del museo es ",ruta_archivo_museo)
      self.cul.crear_db(ruta_archivo_museo)

    def mostrar_cantidades(self):
        pass

    def mostrar_info_cines(self):
        pass

    
    