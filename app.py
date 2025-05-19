from flask import Flask, render_template, flash, session, request, redirect, url_for
from database_remoto import BancoRemoto
from database_local import BancoLocal
from flask import Flask, jsonify

# Inicializa a aplicação Flask e o banco de dados
banco_remoto = BancoRemoto()
banco_local = BancoLocal()
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
def alterar_led():
    ip = "10.0.0.178"  # IP fixo do dispositivo
    estado_led = int(request.form.get('estado_led'))

    if banco_remoto.enviar_comando('Davi', 'ligar' if estado_led == 1 else 'desligar')[0]:
        flash("LED controlado com sucesso!")
        if banco_remoto.mudar_estado_led(ip, estado_led):
            return redirect(url_for('led'))
        else:
            flash("IP não encontrado ou erro ao enviar comando")
            return redirect(url_for('led'))

@app.route ('/alterar_ultrassonico', methods = ['POST'])
def alterar_ultrassonico ():

    ip = request.form.get ('ip')
    estado_ultrassonico = int (request.form.get ('estado_ultrassonico'))

    if banco_remoto.mudar_estado_ultrassonico(ip, estado_ultrassonico):
        registros_ultrassonico = banco_local.dados_ultrassonico()
        return render_template('ultrassonico.html', registros_ultrassonico = registros_ultrassonico)
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('ultrassonico'))
    
@app.route ('/alterar_pir', methods = ['POST'])
def alterar_pir ():
    ip = request.form.get ('ip')
    estado_pir = int (request.form.get ('estado_pir'))

    if banco_remoto.mudar_estado_pir(ip, estado_pir):
        registros_pir = banco_local.dados_pir()
        return render_template('pir.html', registros_pir = registros_pir)
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('pir'))
    
@app.route ('/alterar_lcd', methods = ['POST'])
def alterar_lcd ():
    ip = request.form.get ('ip')
    estado_lcd = int (request.form.get ('estado_lcd'))

    if banco_remoto.mudar_estado_lcd(ip, estado_lcd):
        return redirect(url_for('lcd'))
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('lcd'))
    
@app.route ('/alterar_fotoresistor', methods = ['POST'])
def alterar_fotoresistor ():
    ip = request.form.get ('ip')
    estado_fotoresistor = int (request.form.get ('estado_fotoresistor'))

    if banco_remoto.mudar_estado_fotoresistor(ip, estado_fotoresistor):
        registros_fotoresistor = banco_local.dados_fotoresistor()
        return render_template('fotoresistor.html', registros_fotoresistor = registros_fotoresistor)
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('fotoresistor'))
    
@app.route ('/alterar_buzzer', methods = ['POST'])
def alterar_buzzer ():
    ip = request.form.get ('ip')
    estado_buzzer = int (request.form.get ('estado_buzzer'))

    if banco_remoto.mudar_estado_buzzer(ip, estado_buzzer):
        registros_buzzer = banco_local.dados_buzzer()
        return render_template('buzzer.html', registros_buzzer = registros_buzzer)
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('buzzer'))
    
@app.route ('/alterar_touch', methods = ['POST'])
def alterar_touch ():
    ip = request.form.get ('ip')
    estado_touch = int (request.form.get ('estado_touch'))

    if banco_remoto.mudar_estado_touch(ip, estado_touch):
        registros_touch = banco_local.dados_buzzer()
        return render_template('touch.html', registros_touch = registros_touch)
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('touch'))

# Nova rota para controle geral dos dispositivos
@app.route('/controle', methods=['GET', 'POST'])
def controle():
    if request.method == 'POST':
        dispositivo = request.form.get('dispositivo')
        comando = request.form.get('comando')
        
        # Envia o comando para o dispositivo selecionado
        sucesso, mensagem = banco_remoto.enviar_comando(dispositivo, comando)
        
        if sucesso:
            flash(f"Sucesso: {mensagem}")
        else:
            flash(f"Erro: {mensagem}")
            
        return redirect(url_for('controle'))
    
    # Lista de dispositivos e comandos para o template
    dispositivos = list(banco_remoto.ARDUINO_IPS.keys())
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
    if banco_remoto.cadastro(form):
        flash("Cadastro realizado com sucesso!")
        return redirect(url_for('index'))
    else:
        flash("Erro ao realizar cadastro!")
        return redirect(url_for('cadastro'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if banco_remoto.login(request.form):
            return redirect(url_for('home'))
        else:
            flash("Senha ou e-mail incorreto!")
    return render_template('login.html')

# Rota para a página do LED (mantida para compatibilidade)
@app.route("/led")
def led():
    mensagem = request.args.get("mensagem")
    return render_template("led.html", mensagem=mensagem)
  
@app.route('/sensor/status', methods=['GET'])
def sensor_status():
    try:

        dispositivo_ip = "192.168.1.157"  
        banco_remoto.verificar_conexao()
        banco_remoto.__cursor.execute(
            "SELECT touch FROM dispositivos WHERE ip = %s", (dispositivo_ip,)
        )
        status = banco_remoto.__cursor.fetchone()
        
        if status:
            
            return jsonify({"status": bool(int(status[0]))}), 200
        else:
            return jsonify({"status": False}), 404
            
    except Exception as e:
        print(f"Erro ao buscar status do sensor: {e}")
        return jsonify({"error": "Erro ao buscar status"}), 500





if __name__ == '__main__':
    app.run(debug=True)  # Executa o servidor Flask em modo debug