from flask import Flask
'''
app = Flask(__name__, instance_relative_config=True) # pondremos dos parámetros. "instance_relative_config=True" le indico a flask que las variables de ejecución están en un fichero externo
#ahora le decimos cual es el fichero externo:
app.config.from_object('config') #vamos a cargar las variables que he puesto en el fichero config.py en app.config
'''

app = Flask(__name__, instance_relative_config=True) # LA CONFIGURACIÓN la meteré como u fichero. Esta orden levanta mi servidor web!!!
app.config.from_object('config') # le pongo el nombre que quiera al fichero q contienen la configuración

# importante: este from debe estar en esta posición (!!!)
from movements import views # aquí le metemos las rutas (los puntos de entrada)







