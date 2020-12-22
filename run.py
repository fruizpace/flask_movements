# este fichero tiene lo mínimo imprescindible
# si queremos que una carpea actue como módulo hay que poner dentro de la carpeta un archivo __init__.py
# dentro de init está la orden de instanciar Flask, es decir crear el "app"
from movements import app # vienen del fichero init!!


if __name__=='__main__':
    app.run() #ejecuta app que está en otro archivo