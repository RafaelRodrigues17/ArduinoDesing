import socket
import time
from enum import Enum

class componente(Enum):
    LED = 1
    ULTRASSONICO = 2
    PIR = 3

def principal(ip_usuario, estado, circuitos):

    PORT = 5000
    MAX_TENTATIVAS = 30
    TIMEOUT = 5


    if circuitos == componente.LED:
        msg = b"ligar\n" if estado == 1 else b"desligar\n" 
    elif circuitos  == componente.ULTRASSONICO:
        msg = b"ligar\n" if estado== 1 else b"desligar\n"
    elif circuitos == componente.PIR:
        msg = b"ligar\n" if estado == 1 else b"desligar\n"

    s = None 
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            print(f"Tentando abrir conexão com IP: {ip_usuario}")  
            s = socket.create_connection((ip_usuario, PORT), timeout=2)
            print("Conexão aberta")
            s.settimeout(TIMEOUT)
            s.sendall(msg)
            print(f"Comando executado: {s.recv(16).decode()}")
            break
        except socket.timeout:
            print(f"Tempo esgotado (tentativa {tentativa}/{MAX_TENTATIVAS}).")
        except OSError as e:
            print(f"Falha de rede ({e}) (tentativa {tentativa}/{MAX_TENTATIVAS}).")
        finally:
            if s:
                s.close()
                print("Conexão fechada.\n")

