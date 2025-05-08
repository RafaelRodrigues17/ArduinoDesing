from flask import Flask, render_template, flash, session, request, redirect, url_for
from database import Banco

banco = Banco()

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

@app.route('/acender_led', methods=['POST'])
def acender_led():
    ip = request.form.get('ip')

    if request.method == "POST":
        if banco.acender(ip) == True:
            return redirect(url_for('led'))
        
        else:
            flash("ip nao encontrado")
            return redirect(url_for('led'))

@app.route('/cadastrar',methods = ["GET","POST"])
def cadastrar():
    form = request.form
    if Banco.cadastro(form) == True:
        return render_template('index.html')
    
    else:
        return ("erro1")


@app.route('/login',methods = ['GET','POST'])   
def login():
    form =  request.form

    if request.method == 'POST':
        email = form['email']
        senha = form['senha']

        if Banco.login(form) == True:
            return redirect(url_for('home'))

        else:
            flash("senha ou email incorreto")
        
    return render_template('index.html')

        
    




if __name__ == '__main__':
   app.run(debug=True)
