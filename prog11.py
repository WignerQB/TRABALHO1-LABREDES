import socket
import pickle
import time
import numpy as np
import sys

HOST = sys.argv[1]
PORT = 8000

Lista_matrizes = []
Tempo = []
Dicionario = dict()
t1 = time.time()

Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(" ")

while True:

    try:
        print(f"Tentando conectar ao endereço '{HOST}' pela porta {PORT}")
        Socket.connect((HOST, PORT))
    except:
        print(f"Endereço '{HOST}' não conectado!")
        HOST = input("Por favor informe o endereço da Maquina que deseja conectar [Enter = própria máquina]: ")
        PORT = int(input("Informe o numero da porta de conexão: "))
        if HOST == '':
            HOST = '127.0.0.1'
    else:
        print(f"Endereço '{HOST}' conectado!")
        break

print(" ")

while True:
    print("PROGRAMA QUE ENVIA MATRIZES")
    print(" ")
    print("Digite a quantidade de matrizes:")
    n = int(input())
    print(" ")
    print("Digite a ordem da(s) matriz(es):")
    tam = int(input())
    print(" ")
    for i in range(n):
        m = np.random.randint(99, size=(tam, tam))
        print(m)
        print(" ")
        Lista_matrizes.append(m)

    Tempo1 = time.time() - t1
    Tempo.append(Tempo1)
    Dicionario['Matrizes'] = Lista_matrizes
    Dicionario['Tempo'] = Tempo

    Pacote = pickle.dumps(Dicionario)
    #Cálculo do tamanho do pacote
    TamPacote = len(Pacote)
    NEnvios = int(TamPacote/1024) + 1
    print("Tamanho do pacote a ser enviado: ", TamPacote)
    print("Será feito ",NEnvios, " envios de até 1024 bytes!")
    
    if NEnvios == 1:
        Socket.sendall(bytes(Pacote))
        print("Pacote enviado!")
    else:
        for Naux in range(NEnvios+1):
            if Naux > 0:
                LimInf = (Naux-1)*1024
                LimSup = Naux*1023
                PacoteAux = Pacote[LimInf:LimSup]
                Socket.sendall(bytes(PacoteAux))
                print("Pacote ", Naux, " enviado!")
    #time.sleep(5)
    Socket.close()
    break
