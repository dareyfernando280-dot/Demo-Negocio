
from flask import Flask, request
import sqlite3

app = Flask(__name__)

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
def iniciar_db():
    conn = sqlite3.connect('barberia.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            servicio TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

iniciar_db()

@app.route('/')
def formulario():
    return '''
    <style>
        body { background: #1a1a1a; color: #f0c330; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #262626; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; border: 1px solid #f0c330; width: 300px; }
        input { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; box-sizing: border-box; }
        button { background: #f0c330; color: #1a1a1a; border: none; padding: 10px 20px; font-weight: bold; border-radius: 5px; cursor: pointer; width: 100%; margin-top: 10px; }
        button:hover { background: #fff; }
    </style>
    <div class="card">
        <h1>💈 Barbería Pro 💈</h1>
        <p>Agenda tu cita en Chihuahua</p>
        <form action="/agendar" method="POST">
            <input type="text" name="cliente" placeholder="Tu nombre" required>
            <input type="text" name="servicio" placeholder="¿Corte o Barba?" required>
            <input type="date" name="fecha" required>
            <button type="submit">RESERVAR AHORA</button>
        </form>
    </div>
    '''

@app.route('/agendar', methods=['POST'])
def agendar():
    nombre = request.form['cliente'].strip()
    servicio = request.form['servicio'].strip()
    fecha = request.form['fecha']
    if not nombre or len(nombre) < 3:
        return "<h1>❌ Error: Nombre inválido.</h1><a href='/'>Volver</a>"
    conn = sqlite3.connect('barberia.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO citas (nombre, servicio, fecha) VALUES (?, ?, ?)", (nombre, servicio, fecha))
    conn.commit()
    conn.close()
    return f"<h1>✅ ¡Cita Confirmada!</h1><p>Gracias {nombre}.</p><a href='/admin'>Ver Agenda</a>"

@app.route('/admin/<password>')
def ver_citas(password):
    # Solo si la contraseña es 'dary123' (puedes cambiarla) dejará pasar
    if password != "dary123":
        return "<h1>🚫 Acceso Denegado: No tienes permiso.</h1>"

    conn = sqlite3.connect('barberia.db')
    # ... (todo el resto de tu código de la tabla sigue igual abajo)
    conn = sqlite3.connect('barberia.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM citas")
    todas_las_citas = cursor.fetchall()
    conn.close()

    html_tabla = '''
    <style>
        body { background: #1a1a1a; color: white; fo¿Qué sigue para que esto sea un negocio real?
Ya tienes el sistema que funciona en tu laptop, pero para ganar esos $1,500 - $3,000nt-family: sans-serif; padding: 20px; }
        table { width: 100%; border-collapse: collapse; background: #262626; }
        th, td { border: 1px solid #f0c330; padding: 12px; text-align: left; }
        th { background: #f0c330; color: #1a1a1a; }
        .btn-borrar { color: #FF0000; text-decoration: none; font-weight: bold; }
    </style>
    <h1>📋 Agenda de la Barbería</h1>
    <table>
        <tr>
            <th>ID</th><th>Cliente</th><th>Servicio</th><th>Fecha</th><th>Acción</th>
        </tr>
    '''
    
    for cita in todas_las_citas:
        html_tabla += f'''
        <tr>
            <td>{cita[0]}</td>
            <td>{cita[1]}</td>
            <td>{cita[2]}</td>
            <td>{cita[3]}</td>
            <td><a class="btn-borrar" href="/borrar/{cita[0]}">❌ Completado</a></td>
        </tr>
        '''
    
    html_tabla += '</table><br><a href="/" style="color: #f0c330;">Regresar</a>'
    return html_tabla # ESTA LINEA ES LA QUE FALTABA

@app.route('/borrar/<int:id_cita>')
def borrar(id_cita):
    conn = sqlite3.connect('barberia.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM citas WHERE id = ?", (id_cita,))
    conn.commit()
    conn.close()
    return '<h1>✅ Cita completada</h1><script>setTimeout(function(){window.location.href="/admin";}, 1000);</script>'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
