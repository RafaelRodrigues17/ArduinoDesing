import mysql.connector
from config import MYSQL_CONFIG
import socket
import time

class BancoRemoto:
    # Dicionário com os IPs dos dispositivos e seus nomes
    ARDUINO_IPS = {
        "Rafael1": "192.168.1.157",
        "Rafael2": "192.168.1.10",
        "Dayane": "192.168.1.11",
        "Rian": "192.168.1.167",
        "Kauan": "192.168.1.105",
        "Rodrigo": "192.168.1.174",
        "Diemerson": "192.168.1.106",
        "Davi": "192.168.1.178",
        "Erick": "192.168.1.12"
    }

    def __init__(self):
        self.conectar()  # Conecta ao banco de dados ao inicializar

    # Método para conectar ao banco de dados MySQL
    def conectar(self):
        try:
            self.__conexao = mysql.connector.connect(**MYSQL_CONFIG)
            self.__cursor = self.__conexao.cursor(buffered=True)
            print("Conexão com o banco estabelecida!")
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco: {err}")

    # Verifica se a conexão está ativa
    def verificar_conexao(self):
        try:
            self.__cursor.execute("SELECT 1")
        except mysql.connector.Error:
            self.conectar()

    # Cria a tabela de dispositivos se não existir
    def criar_tabela(self):
        self.verificar_conexao()
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS dispositivos (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome TEXT,
                email TEXT,
                senha TEXT,
                estado INTEGER DEFAULT 0,
                distancia TEXT,
                ip TEXT,
                luminosidade TEXT,
                movimento TEXT,
                som TEXT,
                teclado TEXT,
                toque TEXT,
                temperatura TEXT,
                umidade TEXT,
                led TEXT
            )
        """)
        self.__conexao.commit()

    # Método principal para enviar comandos aos dispositivos
    def enviar_comando(self, dispositivo, comando):
        """Envia comandos para os dispositivos via socket"""
        self.verificar_conexao()
        
        # Configurações da conexão
        PORT = 5000
        MAX_TENTATIVAS = 3
        TIMEOUT = 5
        
        # Verifica se o dispositivo existe
        if dispositivo not in self.ARDUINO_IPS:
            return False, "Dispositivo não encontrado"
        
        ip = self.ARDUINO_IPS[dispositivo]
        
        # Mapeamento de comandos para mensagens binárias
        comandos = {
            'ligar': b"ligar\n",
            'desligar': b"desligar\n",
            'distancia': b"distancia\n",
            'lcd': b"lcd_on\n",
            'temperatura': b"temperatura\n",
            'movimento' : b'movimento\n'
        }
        
        # Verifica se o comando é válido
        if comando not in comandos:
            return False, "Comando inválido"
        
        msg = comandos[comando]
        
        # Tenta enviar o comando (com retentativas)
        for tentativa in range(1, MAX_TENTATIVAS + 1):
            try:
                print(f"Enviando {comando} para {dispositivo} ({ip})")
                s = socket.create_connection((ip, PORT), timeout=2)
                s.settimeout(TIMEOUT)
                s.sendall(msg)
                resposta = s.recv(128).decode().strip()
                s.close()
                
                # NÃO atualiza o campo 'estado' que não existe
                
                return True, resposta
                
            except (socket.timeout, OSError) as e:
                print(f"Erro na tentativa {tentativa}: {e}")
                if tentativa == MAX_TENTATIVAS:
                    return False, str(e)
                time.sleep(1)  # Espera antes de tentar novamente
    
    def mudar_estado_led(self, ip, estado_led):
        self.__cursor.execute("SELECT ip, led FROM dispositivos WHERE ip = %s", (ip,))
        ip_usuario = self.__cursor.fetchone()
        
        if ip_usuario:
            self.__cursor.execute("UPDATE dispositivos SET led = %s WHERE ip = %s", (estado_led, ip))
            # Removido comando INSERT inválido
            self.__conexao.commit()
            return True
        return False
    
    def enviar_mensagem_lcd(self, dispositivo, mensagem):
        """Método para enviar mensagens ao LCD"""
        self.verificar_conexao()
        PORT = 5000
        MAX_TENTATIVAS = 3
        
        if dispositivo not in self.ARDUINO_IPS:
            return False, "Dispositivo não encontrado"
        
        ip = self.ARDUINO_IPS[dispositivo]
        
        # Formato especial para mensagens LCD
        msg = f"LCD:{mensagem}\n".encode()  # Formato "LCD:mensagem"
        
        for tentativa in range(1, MAX_TENTATIVAS + 1):
            try:
                s = socket.create_connection((ip, PORT), timeout=2)
                s.sendall(msg)
                resposta = s.recv(256).decode().strip()
                s.close()
                return True, resposta
            except (socket.timeout, OSError) as e:
                print(f"Erro na tentativa {tentativa}: {e}")
                if tentativa == MAX_TENTATIVAS:
                    return False, str(e)
                time.sleep(1)

    def mudar_mensagem_lcd(self, ip, mensagem):
        """Atualiza a mensagem no banco de dados"""
        self.verificar_conexao()
        try:
            # Usando a coluna 'teclado' para armazenar a mensagem LCD
            self.__cursor.execute(
                "UPDATE dispositivos SET teclado = %s WHERE ip = %s",
                (mensagem, ip)
            )
            self.__conexao.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao atualizar mensagem LCD: {err}")
            return False

    def mudar_estado_ultrassonico(self, ip, estado_ultrassonico):
        self.__cursor.execute("SELECT ip, distancia FROM dispositivos WHERE ip = %s", (ip,))
        ip_usuario = self.__cursor.fetchone()
        
        if ip_usuario:
            self.__cursor.execute("UPDATE dispositivos SET distancia = %s WHERE ip = %s", (estado_ultrassonico, ip))
            # Removido comando INSERT inválido
            self.__conexao.commit()
            return True
        return False
    
    def mudar_estado_pir(self, ip, estado_pir):
        self.__cursor.execute("SELECT ip, movimento FROM dispositivos WHERE ip = %s", (ip,))
        ip_usuario = self.__cursor.fetchone()
        
        if ip_usuario:
            self.__cursor.execute("UPDATE dispositivos SET movimento = %s WHERE ip = %s", (estado_pir, ip))
            # Removido comando INSERT inválido
            self.__conexao.commit()
            return True
        return False
    
    def mudar_estado_lcd(self, ip, estado_lcd):
        self.__cursor.execute("SELECT ip, teclado FROM dispositivos WHERE ip = %s", (ip,))
        ip_usuario = self.__cursor.fetchone()
        
        if ip_usuario:
            self.__cursor.execute("UPDATE dispositivos SET teclado = %s WHERE ip = %s", (estado_lcd, ip))
            self.__conexao.commit()
            return True
        return False
            
    def mudar_estado_fotoresistor(self, ip, estado_fotoresistor):
        self.__cursor.execute("SELECT ip, luminosidade FROM dispositivos WHERE ip = %s", (ip,))
        ip_usuario = self.__cursor.fetchone()
        
        if ip_usuario:
            self.__cursor.execute("UPDATE dispositivos SET luminosidade = %s WHERE ip = %s", (estado_fotoresistor, ip))
            # Removido comando INSERT inválido
            self.__conexao.commit()
            return True
        return False
            
    def mudar_estado_buzzer(self, ip, estado_buzzer):
        self.__cursor.execute("SELECT ip, som FROM dispositivos WHERE ip = %s", (ip,))
        ip_usuario = self.__cursor.fetchone()
        
        if ip_usuario:
            self.__cursor.execute("UPDATE dispositivos SET som = %s WHERE ip = %s", (estado_buzzer, ip))
            # Removido comando INSERT inválido
            self.__conexao.commit()
            return True
        return False
            
    def mudar_estado_touch(self, ip, estado_touch):
        self.__cursor.execute("SELECT ip, toque FROM dispositivos WHERE ip = %s", (ip,))
        ip_usuario = self.__cursor.fetchone()
        
        if ip_usuario:
            self.__cursor.execute("UPDATE dispositivos SET toque = %s WHERE ip = %s", (estado_touch, ip))
            # Removido comando INSERT inválido
            self.__conexao.commit()
            return True
        return False
        
    def fechar(self):
        self.__cursor.close()
        self.__conexao.close()

    # Métodos de cadastro e login
    def cadastro(self, informacoes):
        self.verificar_conexao()
        # Verifica se email já existe
        self.__cursor.execute("SELECT COUNT(email) FROM dispositivos WHERE email=%s", 
                             (informacoes['email'],))
        if self.__cursor.fetchone()[0] > 0:
            return False

        # Insere novo usuário
        self.__cursor.execute(
            "INSERT INTO dispositivos (email, nome, senha, ip) VALUES (%s, %s, %s, %s)",
            (informacoes['email'], informacoes['nome'], informacoes['senha'], informacoes['ip'])
        )
        self.__conexao.commit()
        return True

    def login(self, form):
        self.verificar_conexao()
        self.__cursor.execute("SELECT * FROM dispositivos WHERE email = %s", (form['email'],))
        usuario = self.__cursor.fetchone()
        return usuario and usuario[3] == form['senha']
