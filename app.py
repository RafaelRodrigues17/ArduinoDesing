from flask import Flask, render_template, flash, session, request, redirect, url_for
from database import Banco

# Inicializa a aplicação Flask e o banco de dados
banco = Banco()
app = Flask(__name__)
app.secret_key = "chave_muito_segura"  # Chave necessária para sessões Flask

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página home (após login)
@app.route('/home')
def home():
    return render_template('home.html')

# Rotas para as páginas de componentes
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

@app.route('/rfid')
def rfid():
    return render_template('rfid.html')


# Rota para controle do LED (mantida para compatibilidade)
@app.route('/alterar_led', methods=['POST'])
def acender_led():
    ip = "10.0.0.178"  # IP fixo do dispositivo
    estado_led = int(request.form.get('estado_led'))

    if banco.enviar_comando('Davi', 'ligar' if estado_led == 1 else 'desligar')[0]:
        flash("LED controlado com sucesso!")
        if banco.mudar_estado_led(ip, estado_led):
            return redirect(url_for('led'))
        else:
            flash("IP não encontrado ou erro ao enviar comando")
            return redirect(url_for('led'))

@app.route('/alterar_led', methods=['POST'])
def alterar_led():
    ip = request.form.get('ip')
    estado_led = int(request.form.get('estado_led'))  # 0 ou 1

    if banco.mudar_estado_led(ip, estado_led):
        return redirect(url_for('led'))
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('led'))
        

@app.route ('/alterar_ultrassonico', methods = ['POST'])
def alterar_ultrassonico ():

    ip = request.form.get ('ip')
    estado_ultrassonico = int (request.form.get ('estado_ultrassonico'))

    if banco.mudar_estado_ultrassonico(ip, estado_ultrassonico):
        return redirect(url_for('led'))
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('led'))
    
@app.route ('/alterar_pir', methods = ['POST'])
def alterar_pir ():
    ip = request.form.get ('ip')
    estado_pir = int (request.form.get ('estado_pir'))

    if banco.mudar_estado_pir(ip, estado_pir):
        return redirect(url_for('pir'))
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('pir'))
    
@app.route ('/alterar_lcd', methods = ['POST'])
def alterar_lcd ():
    ip = request.form.get ('ip')
    estado_lcd = int (request.form.get ('estado_lcd'))

    if banco.mudar_estado_lcd(ip, estado_lcd):
        return redirect(url_for('lcd'))
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('lcd'))

# Nova rota para controle geral dos dispositivos
@app.route('/controle', methods=['GET', 'POST'])
def controle():
    if request.method == 'POST':
        dispositivo = request.form.get('dispositivo')
        comando = request.form.get('comando')
        
        # Envia o comando para o dispositivo selecionado
        sucesso, mensagem = banco.enviar_comando(dispositivo, comando)
        
        if sucesso:
            flash(f"Sucesso: {mensagem}")
        else:
            flash(f"Erro: {mensagem}")
            
        return redirect(url_for('controle'))
    
    # Lista de dispositivos e comandos para o template
    dispositivos = list(banco.ARDUINO_IPS.keys())
    comandos = ['ligar', 'desligar', 'ultra', 'lcd', 'temperatura']
    
    return render_template('controle.html', 
                         dispositivos=dispositivos,
                         comandos=comandos)

# Rotas para cadastro e login
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    form = request.form
    if banco.cadastro(form):
        flash("Cadastro realizado com sucesso!")
        return redirect(url_for('index'))
    else:
        flash("Erro ao realizar cadastro!")
        return redirect(url_for('cadastro'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if banco.login(request.form):
            return redirect(url_for('home'))
        else:
            flash("Senha ou e-mail incorreto!")
    return render_template('login.html')

# Rota para a página do LED (mantida para compatibilidade)
@app.route("/led")
def led():
    mensagem = request.args.get("mensagem")
    return render_template("led.html", mensagem=mensagem)
  
if __name__ == '__main__':
    app.run(debug=True)  # Executa o servidor Flask em modo debug