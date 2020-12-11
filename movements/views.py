from movements import app
from flask import render_template, request, redirect, url_for
import csv
import sqlite3

DBFILE = 'movements/data/basededatos.db'
def consulta(query, params=()):
    conn = sqlite3.connect(DBFILE) # establecemos la conexión con SQLITE3
    c = conn.cursor() # creamos el cursor
    c.execute(query, params)
    conn.commit() # IMPORTANTE!! para que se fije el cambio realizado
    resultado = c.fetchall()
    conn.close() # IMPORTANTE!!
    return resultado

@app.route('/') # por defecto el método que permite es GET. / es la página principal.
def listaMovimientos():
    query = "SELECT fecha, concepto, cantidad, id FROM movimientos ORDER BY fecha"
    ingresos = consulta(query)
    
    '''
    conn = sqlite3.connect(DBFILE) # establecemos la conexión con SQLITE3
    c = conn.cursor() # creamos el cursor
    
    c.execute("SELECT fecha, concepto, cantidad, id FROM movimientos ORDER BY fecha") # ejecutas la consulta y da una tupla
    ingresos = c.fetchall() # así guardamos en un objeto la consulta anterior que es una tupla
'''
    sumador = 0
    for ingreso in ingresos:
        sumador += float(ingreso[2])
        
    #conn.close() # IMPORTANTE!!

    return render_template('movementsList.html', datos=ingresos, total=sumador) # así le decimos que ponga en la web lo que escriba en el archivo html.

@app.route("/creaalta", methods=['GET', 'POST']) # por defecto recibe GET. para POST hay que indicárselo. Le ponemos los verbos que este punto de entrada aceptará.
def nuevoIngreso():
    if request.method == 'POST':
        conn = sqlite3.connect(DBFILE) # establecemos la conexión con SQLITE3
        c = conn.cursor() # creamos el cursor
        
        c.execute("INSERT INTO movimientos (cantidad, concepto, fecha) VALUES (?,?,?);", (float(request.form.get('cantidad')), request.form.get('concepto'), request.form.get('fecha')))
        conn.commit() # IMPORTANTE!! para que se fije el cambio realizado
        conn.close() # IMPORTANTE!!
        
        return redirect(url_for('listaMovimientos')) # ruta: llévame a la página principal y muéstrame los datos.
    
    return render_template('alta.html') # a partir de ahora alta.html se llamará creaalta



@app.route("/modifica/<id>", methods=['GET', 'POST']) # así meto una variable en la ruta: <id>
def modificaIngreso(id):
    conn = sqlite3.connect(DBFILE) # establecemos la conexión con SQLITE3
    c = conn.cursor()
    
    if request.method == 'GET':
        c.execute("SELECT fecha, concepto, cantidad, id FROM movimientos WHERE id=?", (id,)) # el registro que me interesa modificar. cogemos todas las variables que usaremos. Dejamos la coma para q me de una tupla
        miingreso = c.fetchone() # aquí guardamos la única tupla que he pedido arriba.
        
        conn.close()
        
        return render_template('modifica.html', datomodificado=miingreso)
    
    else: #request.method == 'POST':
        print(request.form.get('fecha'),request.form.get('concepto'),float(request.form.get('cantidad')),id)
        
        c.execute("UPDATE movimientos SET fecha=?, concepto=?, cantidad=?  WHERE id=?;", (
            request.form.get('fecha'), 
            request.form.get('concepto'), 
            float(request.form.get('cantidad')), 
            id))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('listaMovimientos')) # redirigimos hacia la función de python


@app.route("/delete/<id>", methods=['GET', 'POST']) ## REVISAR!!!
def delete(id):
    conn = sqlite3.connect(DBFILE) # establecemos la conexión con SQLITE3
    c = conn.cursor()
    
    if request.method == 'POST':
        c.execute("DELETE FROM movimientos WHERE id=?;", (id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('listaMovimientos')) # redirigimos hacia la función de python
    
    return render_template('modifica.html')