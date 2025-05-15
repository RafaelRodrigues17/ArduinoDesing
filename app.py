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

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/lcd')
def lcd():
    return render_template('lcd.html')

@app.route('/ultrassonico')
def ultrassonico():
    return render_template('ultrassonico.html')

@app.route('/fotoresistor')
def fotoresistor():
    return render_template('fotoresistor.html')

@app.route('/buzzer')
def buzzer():
    return render_template('buzzer.html')

@app.route('/pir')
def pir():
    return render_template('pir.html')

@app.route('/touch')
def touch():
    return render_template('touch.html')


@app.route('/acender_led', methods=['POST'])
def acender_led():
    ip = request.form.get('ip')
    estado_led = int(request.form.get('estado_led'))
    
    if request.method == "POST":
        if banco.acender(ip) == True:
            return redirect(url_for('led'))
        
        else:
            flash("ip nao encontrado")
            return redirect(url_for('led'))

 
@app.route ('/ativar_ultrassonico', methods = ['POST'])
def ativar_ultrassonico ():
    ip = request.form.get ('ip')
    estado_ultrassonico = int (request.form.get ('estado_ultrassonico'))

    if request.method == "POST":
        if banco.atualizar(ip) == True:
            return redirect(url_for('ultrassonico'))
        
        else:
            flash("ip nao encontrado")
            return redirect(url_for('ultrassonico'))
        
@app.route('/cadastrar',methods = ["POST"])
def cadastrar():
    banco = Banco()
    form = request.form
    
    if banco.cadastro(form) == True:
        return render_template('index.html')
    else:
        return ("erro1")

@app.route('/login',methods = ['GET','POST'])   
def login():
    if request.method == 'POST':
        form =  request.form
        email = form['email']

        if banco.login(form) == True:

            session['ip']= "144555115" #ip deve vir do banco de dados

            return redirect(url_for('home'))

        else:
            flash("senha ou email incorreto")
        
    return render_template('login.html')

@app.route("/led")
def led():
    mensagem = request.args.get("mensagem")
    return render_template("led.html", mensagem=mensagem)




if __name__ == '__main__':
        app.run(debug=True)