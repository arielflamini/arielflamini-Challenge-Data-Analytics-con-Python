import db
import cultura

def run():
    pass
if __name__ == '__main__':

    #Elimina y luego crea todo en la base de datos
    db.Base.metadata.drop_all(db.engine)
    db.Base.metadata.create_all(db.engine)
    run()