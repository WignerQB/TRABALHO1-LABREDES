import socket
import pickle
import time
import numpy as np

t2 = time.time()
HOST = '192.168.124.2'
PORT = 8000
Socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Socket1.bind((HOST, PORT))
Socket1.listen(5)
print(" ")
print('Conectando...')

while True:
    try:
        conn, address = Socket1.accept()
        print('Conectado em ', address)
    except:
        pass
    else:
        break

Dados = []
Minvs = []
Mdets = []

while True:
    RecDados = conn.recv(1024)
    if RecDados == b'':
        Socket1.close()
        break
    Dados.append(RecDados)
    DadosTrat = pickle.loads(b''.join(Dados))
    Inversa = np.linalg.inv(DadosTrat['Matrizes'])
    Determinante = np.linalg.det(Inversa)
    Minvs.append(Inversa)
    Mdets.append(Determinante)

Tempo1 = DadosTrat['Tempo']
Tempo2 = float(Tempo1[0]) + time.time() - t2
Dicionario = dict()
Dicionario['Determinantes'] = Mdets
Dicionario['MatrizInversa'] = Minvs
Dicionario['Tempo'] = Tempo2

print(" ")
print("Matrizes recebidas e calculadas!")

HOST2 = '192.168.124.18'
PORT2 = 9000

print(" ")

while True:
    Socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket2.connect((HOST2, PORT2))
    Pacote = pickle.dumps(Dicionario)
    Socket2.sendall(bytes(Pacote))
    print("Pacote enviado!")
    time.sleep(3)
    Socket2.close()
    break
