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
    TamPacote = sys.getsizeof(Pacote)
    QtPac = int(TamPacote/1024) + 1
    print("TamPacote: ", TamPacote)
    print("QtPac: ", QtPac)

    if QtPac == 1:
        Dados = Pacote
    else:
        Dados = []
        for i in range(QtPac+1):
            if i > 0:
                LimInf = (i-1)*1024
                if i == 1:
                    LimSup = 1023
                else:
                    LimSup = i*1023 + 1
                PacoteAux = Pacote[LimInf:LimSup]
                Dados.append(str(PacoteAux))

    Socket.sendall(bytes(pickle.dumps(Dados)))
    print("Dados enviados!")
    #time.sleep(5)
    Socket.close()
    break
