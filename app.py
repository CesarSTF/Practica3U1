from flask import Flask, render_template, Response
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ejecutar/<ejercicio>')
def ejecutar(ejercicio):
    archivos = {
        'taquilla': 'Taquilla.py',
        'gimnasio': 'Gimnasio.py',
        'vitrina': 'Vitrina.py',
        'tablon': 'TablonNotas.py',
        'encuentro': 'Encuentro.py'
    }
    
    archivo = archivos.get(ejercicio)
    if not archivo:
        return "Ejercicio no encontrado", 404

    def generar_salida():
        proceso = subprocess.Popen(
            ['python3', '-u', archivo], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True
        )
        
        for linea in iter(proceso.stdout.readline, ''):
            print(linea, end='') 
            yield f"data: {linea}\n\n"
        
        proceso.stdout.close()
        proceso.wait()
    return Response(generar_salida(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)