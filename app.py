from flask import Flask, render_template, flash, session, request, redirect, url_for, jsonify
from database_remoto import BancoRemoto
from database_local import BancoLocal

# Inicializa a aplicação Flask e o banco de dados
app = Flask(__name__)
app.secret_key = "chave_muito_segura"

banco_remoto = BancoRemoto()
banco_local = BancoLocal()

COMPONENTES_VALIDOS = ['lcd', 'ultrassonico', 'fotoresistor', 'buzzer', 'pir', 'touch', 'rfid', 'led']

@app.route('/lcd')
def lcd():
    """Rota para exibir a página do LCD"""
    mensagem = request.args.get("mensagem", "")
    return render_template("lcd.html", mensagem=mensagem)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

# Rotas dos componentes (exibe template se válido)
@app.route('/<componente>')
def componentes(componente):
    if componente in COMPONENTES_VALIDOS:
        return render_template(f'{componente}.html')
    return redirect(url_for('index'))


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

@app.route('/dht')
def dht():
    return render_template('dht.html')

# Rota para controle do LED (mantida para compatibilidade)
@app.route('/alterar_led', methods=['POST'])
def alterar_led():
    ip = "192.168.1.105"  # IP fixo do dispositivo
    estado_led = int(request.form.get('estado_led'))

    if banco_remoto.enviar_comando('Kauan', 'ligar' if estado_led == 1 else 'desligar')[0]:
        flash("LED controlado com sucesso!")
        if banco_remoto.mudar_estado_led(ip, estado_led):
            return redirect(url_for('led'))
        else:
            flash(f"Erro ao enviar mensagem: ")
            return redirect(url_for('lcd'))
            

@app.route('/alterar_<componente>', methods=['POST'])
def alterar_componente(componente):
    if componente not in COMPONENTES_VALIDOS:
        flash("Componente inválido")
        return redirect(url_for('index'))

    ip = request.form.get('ip')
    estado = int(request.form.get(f'estado_{componente}'))

    alterar_func = getattr(banco_remoto, f"mudar_estado_{componente}", None)
    dados_func = getattr(banco_local, f"dados_{componente}", None)

    if callable(alterar_func) and alterar_func(ip, estado):
        if callable(dados_func):
            registros = dados_func()
            return render_template(f"{componente}.html", **{f"registros_{componente}": registros})
        return redirect(url_for(componente))
    
    flash("IP não encontrado ou erro ao enviar comando")
    return redirect(url_for(componente))

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

@app.route ('/alterar_ultrassonico', methods = ['POST'])
def alterar_ultrassonico ():
    ip = "192.168.1.178"  # IP fixo do dispositivo
    estado_ultrassonico = int (request.form.get ('estado_ultrassonico'))

    if banco_remoto.mudar_estado_ultrassonico("Davi", "ligar" if estado_ultrassonico == 1 else 'desligar'):
        flash("ultrassonico controlado com sucesso!")
        if banco_remoto.mudar_estado_ultrassonico(ip, estado_ultrassonico):
            print(estado_ultrassonico)
            return redirect(url_for('ultrassonico'))
        else:
            flash(f"Erro ao enviar mensagem: ")
            return redirect(url_for('lcd'))

@app.route ('/alterar_touch', methods = ['POST'])
def alterar_touch ():
    ip = request.form.get ('ip')
    estado_touch = int (request.form.get ('estado_touch'))

    if banco_remoto.mudar_estado_touch(ip, estado_touch):
        registros_touch = banco_local.dados_touch()
        return render_template('touch.html', registros_touch = registros_touch)
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('touch'))
    
@app.route ('/alterar_dht', methods = ['POST'])
def alterar_dht ():
    ip = request.form.get ('ip')
    estado_dht = int (request.form.get ('estado_dht'))

    if banco_remoto.mudar_estado_dht(ip, estado_dht):
        registros_dht = banco_local.dados_dht()
        return render_template('dht.html', registros_dht = registros_dht)
    else:
        flash("IP não encontrado ou erro ao enviar comando")
        return redirect(url_for('touch'))

# Nova rota para controle geral dos dispositivos
@app.route('/controle', methods=['GET', 'POST'])
def controle():
    if request.method == 'POST':
        dispositivo = request.form.get('dispositivo')
        comando = request.form.get('comando')
        sucesso, mensagem = banco_remoto.enviar_comando(dispositivo, comando)
        flash(f"{'Sucesso' if sucesso else 'Erro'}: {mensagem}")
        return redirect(url_for('controle'))

    dispositivos = list(getattr(banco_remoto, 'ARDUINO_IPS', {}).keys())
    comandos = ['ligar', 'desligar', 'ultra', 'lcd', 'temperatura']
    return render_template('controle.html', dispositivos=dispositivos, comandos=comandos)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    if banco_remoto.cadastro(request.form):
        flash("Cadastro realizado com sucesso!")
        return redirect(url_for('index'))
    flash("Erro ao realizar cadastro!")
    return redirect(url_for('cadastro'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if banco_remoto.login(request.form):
            return redirect(url_for('home'))
        flash("Senha ou e-mail incorreto!")
    return render_template('login.html')

@app.route("/led")
def led():
    mensagem = request.args.get("mensagem")
    return render_template("led.html", mensagem=mensagem)

@app.route('/alterar_lcd', methods=['POST'])
def alterar_lcd():
    try:
        ip = request.form.get('ip')  # Pega o IP do formulário
        mensagem = request.form.get('mensagem')  # Pega a mensagem
        
        if not ip or not mensagem:
            flash("IP ou mensagem não fornecidos!")
            return redirect(url_for('lcd'))
        
        # Envia o comando para o Arduino (modificado no BancoRemoto)
        sucesso, resposta = banco_remoto.enviar_mensagem_lcd('Davi', mensagem)
        
        if sucesso:
            # Atualiza no banco (modificado no BancoRemoto)
            banco_remoto.mudar_mensagem_lcd(ip, mensagem)
            flash(f"Mensagem enviada: {mensagem}")
        else:
            flash(f"Erro: {resposta}")
            
        return redirect(url_for('lcd'))
        
    except Exception as e:
        flash(f"Erro inesperado: {str(e)}")
        return redirect(url_for('lcd'))

@app.route('/sensor/status', methods=['GET'])
def sensor_status():
    try:
        dispositivo_ip = "192.168.1.157"
        banco_remoto.verificar_conexao()
        # Acessando cursor "privado" corretamente:
        cursor = getattr(banco_remoto, '_BancoRemoto__cursor', None)
        if cursor is None:
            raise Exception("Cursor não encontrado no banco_remoto")

        cursor.execute("SELECT touch FROM dispositivos WHERE ip = %s", (dispositivo_ip,))
        status = cursor.fetchone()

        if status:
            return jsonify({"status": bool(int(status[0]))}), 200
        return jsonify({"status": False}), 404
    except Exception as e:
        print(f"Erro ao buscar status do sensor: {e}")
        return jsonify({"error": "Erro ao buscar status"}), 500

if __name__ == '__main__':
    app.run(debug=True)

# print ("Te amamos Luca❤")
# print ("Me da nota ")