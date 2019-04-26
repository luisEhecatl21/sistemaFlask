from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Conexion base de datos
app.config['MYSQL_HOST'] = 'clientes.cy1dshhchfxf.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'clientes123'
app.config['MYSQL_PASSWORD'] = 'clientes123'
app.config['MYSQL_DB'] = 'cliente'
mysql = MySQL(app)

# Sesion
app.secret_key = 'clave'

@app.route('/')
def index():
    return render_template('index.html')

#Agregar automovil
@app.route('/agregarCliente', methods = ['POST'])
def agregarCliente():
    if request.method == 'POST':
        #guardo en variables los valores
        idcliente = request.form['idcliente']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        correo = request.form['correo']
        #Insertar a mysql
        cur = mysql.connection.cursor()
        #Insertar consulta
        cur.execute('INSERT INTO cliente (idcliente, nombre, telefono, direccion, correo) VALUES (%s, %s, %s, %s, %s)',
        (idcliente, nombre, telefono, direccion, correo))
        #Ejecucion de consulta
        mysql.connection.commit()
        #Mensaje
        #Redireccionar a una url
        return redirect(url_for('control'))

@app.route('/editarCliente/<idcliente>')
def editarCliente(idcliente):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente WHERE idcliente = %s', [idcliente])
    cliente = cur.fetchall()
    return render_template('editarCliente.html', cliente = cliente[0])

@app.route('/actualizarCliente/<idcliente>', methods = ['POST'])
def actualizarCliente(idcliente):
    if request.method == 'POST':
        #guardado en variables
        idclienteantes = idcliente
        idcliente = request.form['idcliente']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        correo = request.form['correo']
        
        cur = mysql.connection.cursor()
        cur.execute(""" 
            UPDATE cliente
            SET idcliente = %s,
                nombre = %s,
                telefono = %s,
                direccion = %s,
                correo = %s
            WHERE idcliente = %s
        """, (idcliente, nombre, telefono, direccion, correo, idclienteantes))
        mysql.connection.commit()
        return redirect(url_for('control'))

@app.route('/eliminarCliente/<idcliente>')
def eliminarCliente(idcliente):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM cliente WHERE idcliente = %s', [idcliente])
    mysql.connection.commit()
    return redirect(url_for('control'))

@app.route('/control')
def control():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente')
    cliente = cur.fetchall()
    return render_template('control.html', cliente = cliente)

app.run(host='0.0.0.0', debug=True)