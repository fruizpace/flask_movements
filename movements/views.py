from movements import app
from movements.forms import MovementForm # importo la clase del formulario que me he creado
from flask import render_template, request, url_for, redirect # request es un objeto que flask crea con todos los datos que se hace en una petición
import csv
import sqlite3
from datetime import date

DBFILE = app.config['DBFILE']

def consulta(query, params=()): # por defecto ponemos una tupla vacía para que no falle
    ## función 1: establecer conexión con sqlite3
    conn = sqlite3.connect(DBFILE) # establecemos la conexión con SQLITE3
    c = conn.cursor() # creamos el cursor
    c.execute(query, params)
    conn.commit() # IMPORTANTE!! para que se fije el cambio realizado
    filas = c.fetchall() # imp ponerlo antes del fetchall
    print(filas)
    conn.close() # IMPORTANTE!!
    
    ## función 2: dar formato a la consulta como lista de diccionarios
    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0]) # el primer elemento de c.description es el nombre de la columna

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames): # enumerate() te da una tupla con el índice y el elemento.
            d[columnName] = fila[ix] # en este bucle monta un diccionario y luego lo guardo en una lista.
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios 


@app.route('/') # por defecto el método que permite es GET. / es la página principal.
def listaMovimientos():
    query = "SELECT fecha, concepto, cantidad, id FROM movimientos ORDER BY fecha"
    ingresos = consulta(query) or [] 
    
    sumador = 0
    for ingreso in ingresos:
        sumador += float(ingreso['cantidad'])
    
    return render_template('movementsList.html', datos=ingresos, total=sumador) # así le decimos que ponga en la web lo que escriba en el archivo html.


@app.route("/creaalta", methods=['GET', 'POST']) # por defecto recibe GET. para POST hay que indicárselo. Le ponemos los verbos que este punto de entrada aceptará.
def nuevoIngreso():
    form = MovementForm()
    #print(form.concepto, form.cantidad, form.fecha)
    if request.method == 'POST':
        
        if form.validate():
            print(form.cantidad.data, form.concepto.data, form.fecha.data)
            consulta('INSERT INTO movimientos (cantidad, concepto, fecha) VALUES (?, ? ,? );', (
                form.cantidad.data, form.concepto.data, form.fecha.data))
            return redirect(url_for('listaMovimientos'))
        else:
            return render_template("alta.html", form=form)

    return render_template("alta.html", form=form)


@app.route("/modifica/<id>", methods=['GET', 'POST']) # así meto una variable en la ruta: <id>
def modificaIngreso(id):
    
    if request.method == 'GET': # si hago click en modificar un registro: selecciona toda la info del id=? y muéstrame modifica.html
        
        
        query = "SELECT fecha, concepto, cantidad, id FROM movimientos WHERE id=?;"
        miingreso = consulta(query, (id,))[0] # el registro que me interesa modificar. cogemos todas las variables que usaremos. Dejamos la coma para q me de una tupla
        # en lugar de c.fetchone uso consulta()[0]
        miingreso['fecha'] = date.fromisoformat(miingreso['fecha'])
        form = MovementForm(data=miingreso) # haz un formulario usando datos que vienen de una tabla
        
        return render_template('modifica.html', form=form, id=id ) # antiguo "datomodificado"
    
    else: #request.method == 'POST': # si desde la web envío los nuevos datos hago UPDATE y me envía a la página principal
        form = MovementForm()
        if form.validate():
            query = "UPDATE movimientos SET fecha=?, concepto=?, cantidad=?  WHERE id=?;"
            consulta(query, (request.form.get('fecha'), request.form.get('concepto'),float(request.form.get('cantidad')),id))
            
            return redirect(url_for('listaMovimientos')) # redirigimos hacia la pagina principal pero como python
        else:
            return render_template('modifica.html', form=form, id=id )



@app.route("/delete/<id>", methods=['GET', 'POST']) 
def delete(id):
    if request.method == 'POST':
        query = "DELETE FROM movimientos WHERE id=?;"
        consulta(query, (id,))
        
        return redirect(url_for('listaMovimientos'))
    
    return render_template('modifica.html')