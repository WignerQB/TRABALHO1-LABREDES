import socket
import pickle
import time


t3 = time.time()
try:
    HOST = '192.168.124.18'
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
    DadosRec = conn.recv(1024)
    if DadosRec == b'':
       break
    Dados.append(DadosRec)
    DadosTrat = pickle.loads(b''.join(Dados))
    #Inversa = DadosTrat['MatrizInversa']
    Determinante = DadosTrat['Determinantes']
    Tempo2 = DadosTrat['Tempo']
    print(" ")
    print("Determinante da inversa: ")
    print(Determinante)
    print(" ")
    #print("Matriz inversa: ")
    #print(Inversa)
    #print(" ")

    Tempo2 = round(Tempo2,4)
    TempoFinal = Tempo2 + time.time() - t3

    print("Tempo de processamento (ms): ")
    print(round(TempoFinal,2))
