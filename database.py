import mysql.connector
from flask import session
from leds import principal

class Banco:
    def __init__(self):
        self.__conexao = mysql.connector.connect(
            host = 'paparella.com.br',
            user = 'paparell_aluno_4',
            password = '@Senai2025',
            database = 'paparell_python'
        )
        self.__cursor = self.__conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS dispositivos (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome TEXT,
                email TEXT,
                senha TEXT,
                estado_led INTEGER DEFAULT 0,
                distancia TEXT,
                ip text,
                potenciometro TEXT,
                pir TEXT,
                relay TEXT,
                teclado TEXT,
                touch TEXT,
                temperatura TEXT,
                umidade TEXT,
                led TEXT
            )
        """)
        self.__cursor.execute("INSERT INTO dispositivos (ip) VALUES (%s)", ('123',))
        self.__conexao.commit()

    def acender(self, ip):
        
        self.__cursor.execute("SELECT ip, estado_led FROM dispositivos WHERE ip = %s", (ip,))
        ip_usuario = self.__cursor.fetchone()

        if ip_usuario:
            estado_led = 1  
            self.__cursor.execute("UPDATE dispositivos SET estado_led = %s WHERE ip = %s", (estado_led, ip,))
            self.__conexao.commit()
            
            # Enviar comando para o dispositivo
            if principal(ip_usuario[0], estado_led):
                return True
            else:
                return False
        else:
            return False
        
    def fechar(self):
        self.__cursor.close()
        self.__conexao.close()

    def cadastro(self, informacoes):
        self.__cursor.execute("SELECT COUNT(email) FROM dispositivos WHERE email=%s", (informacoes['email'],))
        quantidade_de_emails = self.__cursor.fetchone()  # ← Lê o resultado antes do commit
        self.__conexao.commit()

        if quantidade_de_emails[0] > 0:
            print("Email já cadastrado, tente novamente")
            return False

        self.__cursor.execute(
            "INSERT INTO dispositivos (email, nome, senha, ip) VALUES (%s, %s, %s, %s)", 
            (informacoes['email'], informacoes['nome'], informacoes['senha'], informacoes['ip'])
        )
        self.__conexao.commit()
        return True

    def login(self, form):
        self.__cursor.execute("SELECT * FROM dispositivos WHERE email = %s", (form['email'],))
        usuario = self.__cursor.fetchone()
        if usuario and usuario[3] == form['senha']:
            session['id'] = usuario[0]
            session['email'] = usuario[1]
            return True
        return False
    
    # def acender_lcd(self,informacoes):
        
    #     self.__cursor.execute("SELECT ip, estado_led FROM dispositivos WHERE ip = %s", (ip,))
    #     ip_usuario = self.__cursor.fetchone()

    #     if ip_usuario:
    #         estado_led = 1  
    #         self.__cursor.execute("UPDATE dispositivos SET estado_led = %s WHERE ip = %s", (estado_led, ip,))
    #         self.__conexao.commit()
            
    #         # Enviar comando para o dispositivo
    #         if principal(ip_usuario[0], estado_led):
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False
