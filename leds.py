import socket
import time

def principal(ip_usuario, estado_led, circuitos):
    PORT = 5000
    MAX_TENTATIVAS = 30
    TIMEOUT = 5

    if circuitos == 1:
        msg = b"ligar\n" if estado_led == 1 else b"desligar\n"  

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