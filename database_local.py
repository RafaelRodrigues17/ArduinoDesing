import sqlite3
from config import DB_LOCAL_PATH

class BancoLocal:
    def __init__ (self):
        self.conexao = sqlite3.connect (DB_LOCAL_PATH, check_same_thread = False)
        self.cursor = self.conexao.cursor ()
        self.criar_tabela ()

    def criar_tabela(self):
        self.cursor.execute ("""create table if not exists ultrassonico (id integer primary key autoincrement, distancia text, nome text, hora text, data text)""")
        self.cursor.execute ("""create table if not exists pir (id integer primary key autoincrement, movimento text, nome text, hora text, data text)""")
        self.cursor.execute ("""create table if not exists fotoresistor (id integer primary key autoincrement, luminosidade integer, nome text)""")
        self.cursor.execute ("""create table if not exists buzzer (id integer primary key autoincrement, som text, nome text, hora text, data text)""")
        self.cursor.execute ("""create table if not exists touch (id integer primary key autoincrement, status text, nome text, hora text, data text)""")
        self.cursor.execute ("""create table if not exists dht (id integer primary key autoincrement, status, nome text, hora text, data text)""")
        self.conexao.commit ()
        
    def dados_ultrassonico (self):
        self.cursor.execute("SELECT distancia, nome, hora, data FROM ultrassonico ORDER BY id DESC LIMIT 10")
        return self.cursor.fetchall ()
    
    def dados_pir (self):
        self.cursor.execute ("SELECT movimento, nome, hora, data FROM pir ORDER BY id DESC LIMIT 10")
        return self.cursor.fetchall ()
    
    def dados_fotoresistor (self):
        self.cursor.execute ("SELECT luminosidade, nome FROM fotoresistor ORDER BY id DESC LIMIT 10")
        return self.cursor.fetchall ()
    
    def dados_buzzer (self):
        self.cursor.execute ("SELECT nota, status, nome, hora, data  FROM buzzer ORDER BY id DESC LIMIT 10")
        return self.cursor.fetchall ()
    
    def dados_touch (self):
        self.cursor.execute ("SELECT status, nome, hora, data  FROM buzzer ORDER BY id DESC LIMIT 10")
        return self.cursor.fetchall ()
    
    def dados_dht (self):
        self.cursor.execute ("SELECT status, nome, hora, data  FROM dht ORDER BY id DESC LIMIT 10")
        return self.cursor.fetchall ()