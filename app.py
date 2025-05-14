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

@app.route("/acender_led", methods=["POST"])
def acender_led():
    estado_led = request.form.get("estado_led")
    ip = session.get("ip")  # já armazenado no home.html
    if not ip:
        return "IP não definido", 400
    

    # Aqui você colocaria o código para enviar o comando ao LED, como via requests

    mensagem = "LED ligado com sucesso!" if estado_led == "1" else "LED desligado com sucesso!"
    return redirect(url_for("led", mensagem=mensagem))


if __name__ == '__main__':
        app.run(debug=True)