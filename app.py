'''
Este código importa diferentes módulos y clases necesarios para el desarrollo de una aplicación Flask.

Flask: Es la clase principal de Flask, que se utiliza para crear instancias de la aplicación Flask.
jsonify: Es una función que convierte los datos en formato JSON para ser enviados como respuesta desde la API.
request: Es un objeto que representa la solicitud HTTP realizada por el cliente.
CORS: Es una extensión de Flask que permite el acceso cruzado entre dominios (Cross-Origin Resource Sharing),
 lo cual es útil cuando se desarrollan aplicaciones web con frontend y backend separados.
SQLAlchemy: Es una biblioteca de Python que proporciona una abstracción de alto nivel para interactuar con bases de datos relacionales.
Marshmallow: Es una biblioteca de serialización/deserialización de objetos Python a/desde formatos como JSON.
Al importar estos módulos y clases, estamos preparando nuestro entorno de desarrollo para utilizar las funcionalidades que ofrecen.

En este código, se está creando una instancia de la clase Flask y se está configurando para permitir el acceso cruzado entre dominios utilizando el módulo CORS.

app = Flask(__name__): Se crea una instancia de la clase Flask y se asigna a la variable app. El parámetro __name__ es una variable que representa el nombre del módulo o paquete en el que se encuentra este código. Flask utiliza este parámetro para determinar la ubicación de los recursos de la aplicación.

CORS(app): Se utiliza el módulo CORS para habilitar el acceso cruzado entre dominios en la aplicación Flask. Esto significa que el backend permitirá solicitudes provenientes de dominios diferentes al dominio en el que se encuentra alojado el backend. Esto es útil cuando se desarrollan aplicaciones web con frontend y backend separados, ya que permite que el frontend acceda a los recursos del backend sin restricciones de seguridad del navegador. Al pasar app como argumento a CORS(), se configura CORS para aplicar las políticas de acceso cruzado a la aplicación Flask representada por app.

'''
from flask import Flask, jsonify, request
#del modulo flask importa la clase Flask y los métodos jsonify y request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#app = Flask(__name__) # crea  el objeto app de la clase Flask
#CORS(app) # modulo cors es para que me permita acceder desde el frontend al backend
#Conexion del backend con el frontend
app = Flask(__name__)
CORS(app, resources={r"/cafeteria/productos/": {"origins": "https://carladlp.github.io/frontend-Los-Baristas/"}})
 


# Configura la URI de la base de datos con el driver de MySQL, usuario, contraseña y nombre de la base de datos
# URI de la BD == Driver de la BD://user:password@UrlBD/nombreBD
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/proyecto"
#app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:M@lta2020@localhost/proyecto"  ASI NO FUNCIONA
# configuro la base de datos, con el nombre, el usuario y la clave 
########################################################################
# CONEXION A LA BD:
#   en mi caso como la psw de mi BD tiene un @ q es un caracter especial 
# que también se utiliza como separador en la cadena de conexión, no me funciona la linea
# de arriba, entonces para no cambiar la psw, hago lo siguiente:
########################################################################
from urllib.parse import quote_plus

# Codificar la contraseña para evitar problemas con caracteres especiales
password = quote_plus('M@lta2020')

# Configurar la cadena de conexión
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{password}@localhost:3306/cafeteria"

#--------------------------------------------------
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False #none
db = SQLAlchemy(app)# crea el objeto db de la clase SQLALchemy
ma = Marshmallow(app) # crea el objeto ma de la clase Marshmallow

#################Modelos##########################
#defino la tabla
class Producto(db.Model): # la clase Producto hereda de db.Model
    id = db.Column(db.Integer, primary_key=True) #define los campos de la tabla
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Integer)
#    cantidad =  db.Column(db.Integer)
    imagen = db.Column(db.String(400)) #string porq pongo el path a la imagen
    def __init__(self,nombre,precio,imagen):  #crea el constructor de la clase
        self.nombre = nombre    #no hace fala el id, porq lo crea mysql por ser autoincremental
        self.precio = precio
    #    self.cantidad = cantidad
        self.imagen = imagen


    #si hubiesen mas tablas, las creo aca

######################################################

with app.app_context():
    db.create_all() # Con esto creo las tabla, si no estuviese creada

#######################################################

class ProductoSchema(ma.Schema):
    """
    Esquema de la clase Producto.

    Este esquema define los campos que serán serializados/deserializados
    para la clase Producto.
    """
    class Meta:
        fields= ('id','nombre', 'precio', 'imagen') # Defino campos de mi tabla


producto_schema = ProductoSchema()      # el objeto producto_schema es para traer un producto, almacenar un producto
                                        # Objeto para serializar/deserializar un producto
productos_schema = ProductoSchema(many=True)  # el objeto productos_schema es para traer multiples, almacenar muchos, ej una tabla completa
                                             # Objeto para serializar/deserializar múltiples productos

'''Esta línea define una variable ruta_destino que almacena una ruta
de directorio como un string.
La ruta static/img/ implica que hemos creado un directorio imagenes dentro de un directorio
static en la misma ubicación que el script Python, en el servidor.
Esta convención de nomenclatura es común en aplicaciones web donde los archivos estáticos
(como imágenes, CSS y JavaScript) se almacenan. En nuestro caso, es el lugar donde se
almacenarán las imágenes cargadas en la aplicación.'''

'''
Este código define un endpoint que permite obtener todos los productos de la base de datos y los
 devuelve como un JSON en respuesta a una solicitud GET a la ruta /productos.
@app.route("/productos", methods=["GET"]): Este decorador establece la ruta /productos 
para este endpoint y especifica que solo acepta solicitudes GET.
def get_Productos(): Esta es la función asociada al endpoint. Se ejecuta cuando se 
realiza una solicitud GET a la ruta /productos.
all_productos = Producto.query.all(): Se obtienen todos los registros de la tabla de productos
 mediante la consulta Producto.query.all(). Esto se realiza utilizando el modelo Producto que 
 representa la tabla en la base de datos. El método query.all() heredado de db.Model se utiliza 
 para obtener todos los registros de la tabla.
result = productos_schema.dump(all_productos): Los registros obtenidos se serializan en formato 
JSON utilizando el método dump() del objeto productos_schema. El método dump() heredado de ma.Schema 
se utiliza para convertir los objetos Python en representaciones JSON.
return jsonify(result): El resultado serializado en formato JSON se devuelve como respuesta
 al cliente utilizando la función jsonify() de Flask. Esta función envuelve el resultado en 
 una respuesta HTTP con el encabezado Content-Type establecido como application/json.

'''
#######################################################
#         Creo los controladores.
#   Creo los endpoints o rutas (json)
#######################################################

@app.route('/cafeteria/productos', methods = ['GET'])
def get_Productos():
    all_productos = Producto.query.all()          # el met query.all() lo hereda de db.Model
    result = productos_schema.dump(all_productos) #  el met dump() lo hereda  de ma.schema y trae todos los
                                                  # registros de la tabla
    return jsonify(result)                        # retorna un JSON de todos los registros


# ahora genero un endpoint para traer un solo producto

@app.route('/cafeteria/productos/<id>', methods = ['GET']) # paso id como parametro en la ruta 
def get_producto(id):
    producto = Producto.query.get(id)  # busca en la bd el producto por el id
    if producto:
        return producto_schema.jsonify(producto)  # retorna el Json de un producto 
    else:
        return jsonify({'error':'Producto no encontrado'}), 404

# armo un endpoint para borrar un producto de la BD

@app.route('/cafeteria/productos/<id>', methods = ['DELETE']) # Paso por id el elemento a borrar
def delete_producto(id):
    '''Endpoint para eliminar un producto de la base de datos.

    Elimina el producto correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    '''
    producto = Producto.query.get(id)  # Obtiene el producto correspondiente al ID recibido
    db.session.delete(producto)        # Elimina el producto de la sesión de la base de datos
    db.session.commit()                # Guarda los cambios en la base de datos
    return producto_schema.jsonify(producto) #me devuelve un json con el registro eliminado
    
    
 #armo un endpoint para agregar un producto a la BD
@app.route("/cafeteria/productos", methods=["POST"])  # Endpoint para crear un producto
def create_producto():
    """
    Endpoint para crear un nuevo producto en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de producto en la base de datos.
    Retorna un JSON con el nuevo producto creado.
    """
    nombre = request.json["nombre"]  # Obtiene el nombre del producto del JSON proporcionado
    precio = request.json["precio"]  # Obtiene el precio del producto del JSON proporcionado
#    cantidad = request.json["cantidad"]  # Obtiene la cantidad del producto del JSON proporcionado
    imagen = request.json["imagen"]  # Obtiene la imagen del producto del JSON proporcionado
    new_producto = Producto(nombre, precio, imagen)  # Crea un nuevo objeto Producto con los datos proporcionados
    db.session.add(new_producto)  # Agrega el nuevo producto a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return producto_schema.jsonify(new_producto)  # Retorna el JSON del nuevo producto creado

@app.route("/cafeteria/productos/<id>", methods=["PUT"])  # Endpoint para actualizar un producto
def update_producto(id):
    """
    Endpoint para actualizar un producto existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del producto con el ID especificado.
    Retorna un JSON con el producto actualizado.
    """
    producto = Producto.query.get(id)  # Obtiene el producto existente con el ID especificado

    # Actualiza los atributos del producto con los datos proporcionados en el JSON
    producto.nombre = request.json["nombre"]
    producto.precio = request.json["precio"]
#    producto.cantidad = request.json["cantidad"]
    producto.imagen = request.json["imagen"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return producto_schema.jsonify(producto)  # Retorna el JSON del producto actualizado

######################################
# armo un endpoint para traer un imagen por id
######################################
# Carpeta para guardar las imagenes
ruta_destino = 'static/img/'

from flask import send_from_directory

@app.route('/cafeteria/productos/imagen/<id>', methods=['GET'])
def get_producto_imagen(id):
    producto = Producto.query.get(id)
    if producto and producto.imagen:
        return send_from_directory(ruta_destino, producto.imagen) # carpeta static al mismo nivel q mi app.py
    else:
        #return 'Imagen no encontrada'
        return jsonify({'error':'Imagen no encontrada'}), 404

'''
Este código es el programa principal de la aplicación Flask. Se verifica si el archivo actual está siendo ejecutado directamente y no importado como módulo. Luego, se inicia el servidor Flask en el puerto 5000 con el modo de depuración habilitado. Esto permite ejecutar la aplicación y realizar pruebas mientras se muestra información adicional de depuración en caso de errores.

'''
# Programa Principal
if __name__ == "__main__":
    # Ejecuta el servidor Flask en el puerto 5000 en modo de depuración
    app.run(debug=True, port=5000)