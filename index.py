from flask import Flask, render_template, Response
from main import mainRun

#Captura do nome do arquivo para o servidor
app = Flask(__name__)

#Página de índice
@app.route('/index')
def index():
    return render_template('index.html')

#Página do estacionamento
@app.route('/estacionamento_G')
def estacionamento_G():
    return render_template('estacionamento_G.html')

#Transmissão
@app.route('/feed')
def feed():
    return Response(mainRun(), mimetype='multipart/x-mixed-replace; boundary=lot')

#Inicia o servidor
if __name__ == "__main__":
    app.run(debug=True)