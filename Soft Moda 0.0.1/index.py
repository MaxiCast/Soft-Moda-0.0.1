from tkinter import ttk
from tkinter import *

import sqlite3

class Product:

    db_name = "database.db"     # self es una propiedad

    def __init__(self, window):
        self.wind = window
        self.wind.title("CARGA Y CONTROL DE PRODUCTOS")

        # CREANDO EL FRAME
        frame = LabelFrame(self.wind, text = "Registrar nuevo Producto") #asi creamos el frame (recuadro)
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20) # asi posicionamos el frame (recuadro)

        # NAME INPUT
        Label(frame, text = "Nombre: ").grid(row = 1, column = 0) #
        self.name = Entry(frame) #es para agregar el dato
        self.name.focus() #es para que se posicione el cursor ni bien se abra la ventana
        self.name.grid(row = 1, column = 1)  #donde se posisiona el dato que agregamos

        # PRICE INPUT
        Label(frame, text = "Precio: ").grid(row = 2, column = 0) #
        self.price = Entry(frame) #es para agregar el dato
        self.price.grid(row = 2, column = 1)  #donde se posisiona el dato que agregamos


        # BUTTON ADD PRODUCT
        ttk.Button(frame, text ="Guardar Producto", command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        # OUPUT MESSAGES
        self.message = Label(text = "", fg = "red")
        self.message.grid(row = 3, column = 0, columnspan =2, sticky = W + E)

        # TABLE
        self.tree = ttk.Treeview(height = 10, column = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading("#0", text = "Nombre", anchor = CENTER)   # Los headding son los encabezados de las columnas
        self.tree.heading("#1", text = "Precio", anchor = CENTER)

        # BUTTONS
        ttk.Button(text = "ELIMINAR", command = self.delete_product).grid(row = 5, column = 0, sticky = W + E) # este es el boton eliminar
        ttk.Button(text = "EDITAR", command = self.edit_product).grid(row = 5, column = 1, sticky = W + E) #este es el boton editar


        # FUNCION PARA CARGAR LOS DATOS DE LA BASE DE DATOS
        self.get_products()



    def run_query(self, query, parameters = ()):  #esta funcion es para poder ejecutar las funciones cada vez que yo quiera interactuar con la base de datos
        with sqlite3.connect(self.db_name) as conn:   # Este es el metodo para conectarse a la base de datos db_name
          cursor = conn.cursor()
          result = cursor.execute(query, parameters) #ees para definir la consulta
          conn.commit()  # es para ejecutar la consula
        return result  

    def get_products(self):  #funcion para traer productos que estan guardados
        # LIMPIANDO LA TABLA
        records = self.tree.get_children() #es para obtener todos los datos que hay
        for element in records:
          self.tree.delete(element)

        # CONSULTANDO LOS DATOS
        query = "SELECT * FROM product ORDER BY name DESC" # es como traer los datos estando oredenadoss por nombres de manera decendente
        db_rows = self.run_query(query)  # es para ejecutar la consulta

        # RELLENANDO LOS DATOS
        for row in db_rows:
            self.tree.insert("", 0, text = row [1], values = row[2]) # esto es para ver lo agregado en la base de datos por la ventana

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0 # Es para validar los datos ingresados en name y price

    def add_product(self):
        if self.validation():
          query = "INSERT INTO product VALUES(NULL, ?, ?)"     # esta query es para buscar los valores en la base de datos  
          parameters = (self.name.get(), self.price.get())  # Estos son los valores que quiero insertar dentro de la base de datos
          self.run_query(query, parameters)   # esto es para ejecutar la consulta y la insercion de datos
          self.message["text"] = "El producto {} fue AGREGADO satisfactoriamente".format(self.name.get())  #este es el mensaje que va a mostrar al agregar el producto
          self.name.delete(0, END)  #esto es para que se borre lo que escribimos en los input y vuelva a estado inicial
          self.price.delete(0, END)
        else:
          self.message["text"] = "El NOMBRE y el PRECIO son requeridos"
        self.get_products()

        # FUNCION BORRAR PRODUCTO

    def delete_product(self):
        self.message["text"] = ""  #es para que no haya ningun mensage al comienzo
        try:
          self.tree.item(self.tree.selection())["text"][0] #esto es para poder seleccionar y obtener el valor del texto selecionado
        except IndexError as e:   #si el usuario selecciono algo que continue
          self.message["text"] = "Por favor seleccione un producto" # caso contrario que nos devuelva el siguiente mensaje
          return
        self.message["text"] = ""
        name = self.tree.item(self.tree.selection())["text"]  # obtenemos el nombre desde lo que ha seleccionado el usuario
        query = "DELETE FROM product WHERE name = ?"   # elimina desde la tabla productos, el siguiente producto con el nombre tal
        self.run_query(query, (name, ))  #ejecuta la caonsulta y el parametro que voy a elegir para eliminar es el nombre
        self.message["text"] = "El producto {} fue ELIMINADO satisfactoriamente".format(name)  #el format al final es lo que va a poner entre corchetes en el mensaje
        self.get_products()  # esto es para que se limpia la tabla

        # FUNCION EDITAR PRODUCTO

    def edit_product(self):
        self.message["text"] = ""  #es para que no haya ningun mensage al comienzo
        try:
          self.tree.item(self.tree.selection())["text"][0] #esto es para poder seleccionar y obtener el valor del texto selecionado
        except IndexError as e:   #si el usuario selecciono algo que continue
          self.message["text"] = "Por favor seleccione un producto" # caso contrario que nos devuelva el siguiente mensaje
          return 
        name = self.tree.item(self.tree.selection())["text"]   
        old_price = self.tree.item(self.tree.selection())["values"][0]
        self.edit_wind = Toplevel()  #esta uncion es para que abra una ventana nueva  para editar el producto
        self.edit_wind.title = "EDITAR PRODUCTO" #este es para agregar el titulo de la ventana

        # OLD NAME
        Label(self.edit_wind, text = "NOMBRE ANTERIOR ",).grid(row = 0, column = 1) #este input es solo de lectura
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = "readonly").grid(row = 0, column = 2) # stringvar es para que nos de un valor en formato de string y readonly es para que no se puede tocar lo escrito
        # NEW NAME
        Label(self.edit_wind, text = "NOMBRE NUEVO ",).grid(row = 1, column = 1) #este input es para agregar el dato nuevo
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # OLD PRICE
        Label(self.edit_wind, text = "PRECIO ANTERIOR ",).grid(row = 2, column = 1) #este input es solo de lectura
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = "readonly").grid(row = 2, column = 2) # stringvar es para que nos de un valor en formato de string y readonly es para que no se puede tocar lo escrito
        # NEW PRICE
        Label(self.edit_wind, text = "PRECIO NUEVO ",).grid(row = 3, column = 1) #este input es para agregar el dato nuevo
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)   

        Button(self.edit_wind, text = "Actualizar", command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)

    def edit_records(self, new_name, name, new_price, old_price):
        query = "UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?" #voy a actualizar los datos que selecciono el usuario desde la tabla
        parameters =(new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()  #esto es para que cuando el usuario haya terminado la actualizacion, se cierre la ventana
        self.message["text"] = "El producto {} se ha ACTUALIZADO satisfactoriamente".format(name)
        self.get_products()



if  __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
