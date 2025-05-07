from flask import Flask, render_template, flash
import database

database.conectar()

app = Flask(__name__)
app.secret_key = "chave_muito_segura"

@app.route('/') #rota para a página inicial
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/led')
def led(ip):
    if database.acender(ip) == True:
        return render_template('led.html')
    
    else:
        flash("ip nao encontrado")
        return render_template('led.html')
    




if __name__ == '__main__':
   app.run(debug=True)