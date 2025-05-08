from flask import Flask, render_template, request, url_for, redirect, flash, session
import database

app = Flask(__name__)
app.secret_key = "chave_muito_segura"

@app.route('/') #rota para a página inicial
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/led')
def led():
    return render_template('led.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        if database.login(form) == True:
            session['usuario'] = form['email'] 
            return redirect(url_for('home'))
        else:
            return "Ocorreu um erro ao fazer o login do usuário"  
    else:
        return render_template('login.html')  

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        form = request.form 
        if database.criar_usuario(form) == True:
            return render_template('login.html') 
        else:
            return "Ocorreu um erro ao cadastrar usuário" 
    else:
        return render_template('cadastro.html')

if __name__ == '__main__':
   app.run(debug=True)