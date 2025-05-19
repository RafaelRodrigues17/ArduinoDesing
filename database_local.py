import sqlite3
from config import DB_LOCAL_PATH

class BancoLocal:
    def __init__(self):
        self.conexao = sqlite3.connect(DB_LOCAL_PATH, check_same_thread=False)
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):        
        self.cursor.execute ("""create table if not exists ultrassonico (id integer primary key autoincrement, distancia integer, nome text, hora text, data text)""")
        self.cursor.execute ("""create table if not exists pir (id integer primary key autoincrement, nome text, hora text, data text)""")
        self.conexao.commit ()
        
    def dados_ultrassonico (self):
        self.cursor.execute("SELECT distancia, nome, hora, data FROM ultrassonico ORDER BY id DESC LIMIT 10")
        return self.cursor.fetchall()
    
    
    
    
    