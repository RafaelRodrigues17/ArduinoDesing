import socket
import time
 
def principal(ip_usuario, estado_led):
    
    HOST = ["10.0.0.18", "10.0.0.178", "192.168.1.105"]
    PORT = 5000
    MAX_TENTATIVAS = 30
    TIMEOUT = 5

    
    if ip_usuario not in HOST:
        print("Dispositivo inválido! Programa encerrado.")
        return False  

    if estado_led == 1:
        msg = b"ligar\n"
    else:
        msg = b"desligar\n"
        
   
    ip = HOST.index(ip_usuario)

    
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            print(f"Tentando abrir conexão com IP: {HOST[ip]}")
            s = socket.create_connection((HOST[ip], PORT), timeout=2)
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