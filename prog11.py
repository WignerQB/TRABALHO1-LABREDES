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
        Lista_matrizes.append(m)

    Tempo1 = time.time() - t1
    Tempo.append(Tempo1)
    Dicionario['Matrizes'] = Lista_matrizes
    Dicionario['Tempo'] = Tempo

    Pacote = pickle.dumps(Dicionario)

    PacBytes = sys.getsizeof(Pacote) #Tamanho do Pacote em bytes
    QtPac = int(np.ceil(PacBytes/1024)) #Quantidade necessário de pacotes para enviar
    TamPacs = int(len(Pacote)/QtPac) #Tamanho do pacote
    TamPacsBytes = sys.getsizeof(Pacote[:TamPacs]) #Tamanho do pacote em bytes
    #print("TamPacsBytes: ", TamPacsBytes)
    #print("QtPac: ", QtPac)

    Dados = []

    if QtPac == 1:
        Dados.append(Pacote)
        for i in Dados:
            Socket.sendall(i)
        time.sleep(0.1)
        Socket.sendall(pickle.dumps('PacEnv'))
        #print('\n', pickle.dumps('PacEnv'), '\n')
        print("Dados (matrizes e tempo) enviados!")
        Socket.close()
    else:
        while TamPacs>1024:  #Garantir o tamanho máximo de 1024 bytes
              QtPac += 2
              TamPacs = int(len(Pacote)/QtPac)
              TamPacsBytes = sys.getsizeof(Pacote[:TamPacs])

        for i in range(QtPac):  #Lista com os pacotes
             PacoteAux = Pacote[(i)*TamPacs:(i+1)*TamPacs]
             Dados.append(PacoteAux)

             if i==(QtPac-1) and (i+1)*TamPacs<len(Pacote): #Garantir que tudo esta dentro da lista
                PacoteAux=Pacote[(i+1)*TamPacs:]
                Dados.append(PacoteAux)
        for i in Dados:
            Socket.sendall(i)
        time.sleep(0.1)
        Socket.sendall(pickle.dumps('PacEnv'))
        #print('\n', pickle.dumps('PacEnv'), '\n')
        print("Dados (matrizes e tempo) enviados!")
        Socket.close()
    break

