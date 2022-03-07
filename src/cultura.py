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

#rutas donde van a estar guardados los datos
ruta_museo = ""
ruta_biblio = ""
ruta_sala = ""

#class Cultura(db.Base):
class Cultura(db.Base):
  
  #armamos la base de datos
  __tablename__ = 'cultura'
  
  id = Column(Integer(), primary_key=True)
  cod_localidad = Column(Integer())
  id_provincia = Column(Integer())
  id_departamento = Column(Integer())
  categoria = Column(String(200))
  provincia = Column(String(200))
  localidad = Column(String(200))
  nombre = Column(String(200))
  domicilio = Column(String(200))
  codigo_postal = Column(String(100))
  telefono = Column(String(100))
  mail = Column(String(200))
  web = Column(String(200))
  fecha_carga = Column(DateTime(), default=fecha)
  
  #Contructor de la clase
  def __init__(self, id,cod_loc, id_prov, id_dep, cat, prov, loc, nom, dom, cp, tel, mail, web, fecha_carga):

   self.id = id
   self.cod_localidad = cod_loc
   self.id_provincia = id_prov
   self.id_departamento = id_dep
   self.categoria = cat
   self.provincia = prov
   self.localidad = loc
   self.nombre = nom
   self.domicilio = dom
   self.codigo_postal = cp
   self.telefono = tel
   self.mail = mail
   self.web = web
   self.fecha_carga = fecha_carga

   #print("Se guardó todo en la base de datos")

  def __str__(self):
    return self.categoria

#Descarga los archivos fuentes 
def descargar_archivos():
      #Está comentariado porque no existen los recursos en internet
   '''#Defino el nombre de la carpeta o directorio a crear para museos
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
          print("la URL no existe")'''
   
   #Los path son estáticos porque los recursos no están disponibles en internet
   ruta_archivo_museo = 'museos/2022-March/museos-02-03-2022.csv'
   ruta_archivo_biblio = 'biblios/2022-March/biblios-02-03-2022.csv'
   ruta_archivo_sala = 'salas/2022-March/salas-02-03-2022.csv'

   crear_db(ruta_archivo_museo, ruta_archivo_biblio, ruta_archivo_sala)

def cantidad_por_categoria():
   #Abro conexión y luego ejecuto
   db.Session()
   #arreglo para guardar todas las categorias de la bd
   categorias = []
   cat_db = pd.read_sql_query("Select categoria from cultura",db.engine)
   cat = json.loads(cat_db.to_json())
   i = 0
   #armo un arrelo con todas las categorias repetidas que recibo de la bd
   while i < len(cat['categoria']):
       categorias.append(cat['categoria'][str(i)])
       i=i+1
   #armo diccionario con las cantidades de cada categoría
   cant_cat = dict(zip(categorias,map(lambda x: categorias.count(x),categorias)))
   print("Cantidades por categorias",cant_cat)
   
   #consulto las provincias según cada categoría
   for cate in cant_cat:
      prov_cat = []
      prov_cat_bd = pd.read_sql_query("Select provincia from cultura where categoria = "+"'"+cate+"'",db.engine)
      provincias = json.loads(prov_cat_bd.to_json())
      j = 0
      #el primer elemento tiene el nombre de la categoría
      prov_cat.append(cate)
      #armo un arrelo con todas las provincias repetidas que recibo de la bd según la categoría
      while j < len(provincias['provincia']):
          prov_cat.append(provincias['provincia'][str(j)])
          j=j+1
      #armo diccionario con las cantidades de cada categoría
      cant_prov = dict(zip(prov_cat,map(lambda x: prov_cat.count(x),prov_cat)))
      print("Provincias por categorias",cant_prov)

   db.session.commit()

def cantidad_por_fuente():

    registros = []
    #Los path son estáticos porque los recursos no están disponibles en internet
    ruta_museo = 'museos/2022-March/museos-02-03-2022.csv'
    ruta_biblio = 'biblios/2022-March/biblios-02-03-2022.csv'
    ruta_sala = 'salas/2022-March/salas-02-03-2022.csv'
    rutas=[ruta_museo, ruta_biblio, ruta_sala]
    for r in rutas:
      #lo importo en formato DataFrame
      tipo_cultura = pd.read_csv(r)
      registros.append(len(tipo_cultura))
    print(registros)

def crear_db(ruta_museo, ruta_biblio, ruta_sala):
  db.Base.metadata.drop_all(db.engine)
  db.Base.metadata.create_all(db.engine)
  #leo los archivos. #El path está estático porque el recurso no está disponible en internet
  rutas=[ruta_museo, ruta_biblio, ruta_sala]

  #recorro todas las rutas para pasar por parámetro los registros que van a ser persistidos
  id = 0
  for r in rutas:
     #lo importo en formato DataFrame
     tipo_cultura = pd.read_csv(r)
     #convierto el DataFrame a json para trabajarlo más fácil
     objeto = json.loads(tipo_cultura.to_json())
     i = 0
     claves = []
     argumentos = []
     for tipo in objeto:
         #Tomo sólo las claves que me piden   
         if tipo == 'Cod_Loc' or tipo == 'IdProvincia' or tipo == 'IdDepartamento' or tipo == 'categoria' or tipo == 'Categoría' or tipo == 'provincia' or tipo == 'Provincia' or tipo == 'localidad' or tipo == 'Localidad' or tipo == 'nombre' or tipo == 'Nombre' or tipo == 'Domicilio' or tipo == 'direccion' or tipo == 'Dirección' or tipo == 'CP' or tipo == 'telefono' or tipo == 'Teléfono' or tipo == 'Mail' or tipo == 'Web':
            claves.append(tipo)
     while i < len(tipo_cultura):
        #for j in claves: 
         #  argumentos.append(objeto[j][str(i)]) 
        cultura = Cultura(id, objeto[claves[0]][str(i)], objeto[claves[1]][str(i)],objeto[claves[2]][str(i)],objeto[claves[3]][str(i)],objeto[claves[4]][str(i)],objeto[claves[5]][str(i)],objeto[claves[6]][str(i)],objeto[claves[7]][str(i)],objeto[claves[8]][str(i)],objeto[claves[9]][str(i)],objeto[claves[10]][str(i)],objeto[claves[11]][str(i)], fecha)
        #Abro conexión y luego ejecuto
        db.Session()
        db.session.add(cultura)
        i=i+1
        id=id+1
  db.session.commit()
  db.engine.close()
  print("Cierro BD")

def cerrar_ventana():
    pass

def crear_interfaz():

   #Creo la interfaz
   ventana = tk.Tk()
   #inicio la interfaz
   ventana.title("App Cultura")

   Label(ventana,text="Ingrese URL para descargar el archivo").grid(row=1, column=0, pady=10)
   url_museo = Entry(ventana).focus()

   boton_descarga = ttk.Button(ventana, text="Descargar archivos", command=descargar_archivos)
   #boton_descarga.pack()
   boton_descarga.grid(row=3, column=0)

   boton_cantidades = ttk.Button(ventana, text="Mostrar totales por categoría", command=cantidad_por_categoria)
   #boton_descarga.pack()
   boton_cantidades.grid(row=3, column=2)

   boton_cines = ttk.Button(ventana, text="Mostrar totales por fuente", command=cantidad_por_fuente)
   #boton_descarga.pack()
   boton_cines.grid(row=3, column=3)

   boton_cerrar = ttk.Button(ventana, text="Cerrar Ventana", command=cerrar_ventana())
   #boton_descarga.pack()
   boton_cines.grid(row=3, column=3)

   '''frame1 = Frame(self, bg="#bfdaff")
   frame1.place(x=0,y=0,width=93, height=259)        
   self.btnNuevo=Button(frame1,text="Nuevo", command=self.fNuevo, bg="blue", fg="white")
   self.btnNuevo.place(x=5,y=50,width=80, height=30 )        
   self.btnModificar=Button(frame1,text="Modificar", command=self.fModificar, bg="blue", fg="white")
   self.btnModificar.place(x=5,y=90,width=80, height=30)                
   self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
   self.btnEliminar.place(x=5,y=130,width=80, height=30)        
   frame2 = Frame(self,bg="#d3dde3" )
   frame2.place(x=95,y=0,width=150, height=259)                        
   lbl1 = Label(frame2,text="ISO3: ")
   lbl1.place(x=3,y=5)        
   self.txtISO3=Entry(frame2)
   self.txtISO3.place(x=3,y=25,width=50, height=20)                
   lbl2 = Label(frame2,text="Country Name: ")
   lbl2.place(x=3,y=55)        
   self.txtName=Entry(frame2)
   self.txtName.place(x=3,y=75,width=100, height=20)        
   lbl3 = Label(frame2,text="Capital: ")
   lbl3.place(x=3,y=105)        
   self.txtCapital=Entry(frame2)
   self.txtCapital.place(x=3,y=125,width=100, height=20)        
   lbl4 = Label(frame2,text="Currency Code: ")
   lbl4.place(x=3,y=155)        
   self.txtCurrency=Entry(frame2)
   self.txtCurrency.place(x=3,y=175,width=50, height=20)        
   self.btnGuardar=Button(frame2,text="Guardar", command=self.fGuardar, bg="green", fg="white")
   self.btnGuardar.place(x=10,y=210,width=60, height=30)
   self.btnCancelar=Button(frame2,text="Cancelar", command=self.fCancelar, bg="red", fg="white")
   self.btnCancelar.place(x=80,y=210,width=60, height=30)        
   self.grid = ttk.Treeview(self, columns=("col1","col2","col3","col4"))        
   self.grid.column("#0",width=50)
   self.grid.column("col1",width=60, anchor=CENTER)
   self.grid.column("col2",width=90, anchor=CENTER)
   self.grid.column("col3",width=90, anchor=CENTER)
   self.grid.column("col4",width=90, anchor=CENTER)        
   self.grid.heading("#0", text="Id", anchor=CENTER)
   self.grid.heading("col1", text="ISO3", anchor=CENTER)
   self.grid.heading("col2", text="Country Name", anchor=CENTER)
   self.grid.heading("col3", text="Capital", anchor=CENTER)
   self.grid.heading("col4", text="Currency Code", anchor=CENTER)        
   self.grid.place(x=247,y=0,width=420, height=259)'''


   ventana.mainloop()

#para asegurarme que ejecuta mi archivo
if __name__ == "__main__":
   crear_interfaz()
   
   
   




