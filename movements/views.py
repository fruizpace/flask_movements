from movements import app
from flask import render_template
'''
@app.route('/')
def listaMovimientos():
    return 'Tengo que devolver una lista de movimientos' # esto me saldrá en la web
'''

@app.route('/')
def listaMovimientos():
    return render_template('movementsList.html', miTexto="Ya veremos si hay movimientos") # así le decimos que ponga en la web lo que escriba en el archivo html.