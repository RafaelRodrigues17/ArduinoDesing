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

@app.route('/led')
def led():
    return render_template('led.html')

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

@app.route('/acender_led', methods=['POST'])
def acender_led():
    ip = request.form.get('ip')

    if request.method == "POST":
        if banco.acender(ip) == True:
            return redirect(url_for('led'))
        
        else:
            flash("ip nao encontrado")
            return redirect(url_for('led'))
        
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
    form =  request.form

    if request.method == 'POST':
        email = form['email']
        senha = form['senha']

        if Banco.login(form) == True:
            return redirect(url_for('home'))

        else:
            flash("senha ou email incorreto")
        
    return render_template('index.html')

# @app.route('acender_lcd',methods = ['GET','POST'])
# def acender_lcd():
#     ip = request.form.get('ip')
    
#     if request.method == "POST":
#         if banco.acender_lcd(ip) == True:
#             return redirect(url_for('led'))
        
#         else:
#             flash("ip nao encontrado")
#             return redirect(url_for('led'))


if __name__ == '__main__':
   app.run(debug=True)