import mysql.connector

class Arduino:

    def __init__(self):
        self.__conexao = mysql.connector.connect(
            host = 'paparella.com.br',
            user = 'paparell_aluno_4',
            password = '@Senai2025',
            database = 'paparell_python'
        )
        self.__cursor = self.__conexao.cursor()

    def criar_tabela(self):
        query = ("create table if not exists (id integer primary key, nome varchar(255)) ")
    