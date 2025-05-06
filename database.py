import mysql.connector

from flask import session

def conectar():
        return mysql.connector.connect(
            host = 'paparella.com.br',
            user = 'paparell_aluno_4',
            password = '@Senai2025',
            database = 'paparell_python'
        )
# Função para criar as tabelas do banco de dados, caso não existam
if __name__ == '__main__':
   conectar()
    