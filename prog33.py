import socket
import pickle
import time
import sys


t3 = time.time()

def MontarArq(RecDados):
    Arquivo = pickle.loads(b"".join(RecDados))
    return Arquivo

try:
    HOST = sys.argv[1]
    PORT = 9000

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.bind((HOST, PORT))
    Socket.listen(5)

    print(" ")
    print('Conectando...')

    conn, address = Socket.accept()

    print('Conectado em ', address)
except:
    exit()

Dados = []

while True:
    RecDados = conn.recv(2048)
    Dados.append(RecDados)
    if Dados[-1] == b'\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00\x8c\x06PacEnv\x94.':
        Dados.pop(-1)
        DadosTrat = MontarArq(Dados)
        break

Determinante = DadosTrat['Determinantes']
Inversa = DadosTrat['MatrizInversa']
Tempo2 = DadosTrat['Tempo']

print("Matriz inversa: ")
print(Inversa, '\n')
print("Determinante da  inversa: ")
print(Determinante, '\n')

Tempo2 = round(Tempo2,4)
TempoFinal = Tempo2 + time.time() - t3

print("Tempo de processamento (ms): ")
print(round(TempoFinal,2))
