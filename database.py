import mysql.connector
from flask import session

class Banco:

    def __init__(self):
        self.__conexao = mysql.connector.connect(
            host='paparella.com.br',
            user='paparell_aluno_4',
            password='@Senai2025',
            database='paparell_python'
        )
        self.__cursor = self.__conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS dispositivos (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome TEXT,
                estado_led INTEGER DEFAULT '0',
                distancia TEXT DEFAULT 'null',
                ip TEXT DEFAULT 'null',
                potenciometro TEXT DEFAULT 'null',
                pir TEXT DEFAULT 'null',
                relay TEXT DEFAULT 'null',
                teclado TEXT DEFAULT 'null',
                touch TEXT DEFAULT 'null',
                temperatura TEXT DEFAULT 'null',
                umidade TEXT DEFAULT 'null',
                led TEXT DEFAULT 'null'
            )
        """)
        self.__conexao.commit()

    def acender(self, ip):
        self.__cursor.execute("SELECT ip FROM dispositivos WHERE ip = %s", (ip,))
        ip_usuario = self.__cursor.fetchone()

        if ip_usuario and ip_usuario[0] != 'null':
            self.__cursor.execute("UPDATE dispositivos SET estado_led = %s WHERE ip = %s", (1,ip,))
            return True
        else:
            return False
           

    def fechar(self):
        self.__cursor.close()
        self.__conexao.close()

if __name__ == '__main__':
    banco = Banco()
    banco.acender('192.168.1.10')  # Exemplo
    banco.fechar()
