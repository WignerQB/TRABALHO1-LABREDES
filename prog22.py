import socket
import pickle
import time
import numpy as np
import sys

t2 = time.time()

HOST = sys.argv[1]
PORT = 8000
HOST2 = sys.argv[2]
PORT2 = 9000

Socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Socket1.bind((HOST, PORT))
Socket1.listen(5)
print('\nConectando...')

def MontarArq(RecDados):
    Arquivo = pickle.loads(b"".join(RecDados))
    return Arquivo

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
    RecDados = conn.recv(2048)
    Dados.append(RecDados)
    if Dados[-1] == b'\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00\x8c\x06PacEnv\x94.':
        Dados.pop(-1)
        DadosTrat = MontarArq(Dados)
        Minvs = np.linalg.inv(DadosTrat['Matrizes'])
        Mdets = np.linalg.det(Minvs)
        break

#print(DadosTrat['Matrizes'])
#print('\n', Minvs)
#print('\n', Mdets, '\n')

Dicionario = dict()
Dicionario['Determinantes'] = Mdets
Dicionario['MatrizInversa'] = Minvs

Tempo1 = DadosTrat['Tempo']
Tempo2 = float(Tempo1[0]) + time.time() - t2

Dicionario['Tempo'] = Tempo2

print("\nMatrizes recebidas e calculadas!\n")

Socket2.connect((HOST2, PORT2))

while True:

    Pacote = pickle.dumps(Dicionario)
    PacBytes = sys.getsizeof(Pacote) #Tamanho do Pacote em bytes
    QtPac = int(np.ceil(PacBytes/1024)) #Quantidade necessário de pacotes para enviar
    TamPacs = int(len(Pacote)/QtPac) #Tamanho do pacote
    TamPacsBytes = sys.getsizeof(Pacote[:TamPacs]) #Tamanho do pacote em bytes

    Dados = []

    if QtPac == 1:
        Dados.append(Pacote)
        for i in Dados:
            Socket2.sendall(i)
        time.sleep(0.1)
        Socket2.sendall(pickle.dumps('PacEnv'))
        print("Dados (Matriz inversa, determinante da matriz inversa e tempo) enviados!")
        Socket2.close()
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
            Socket2.sendall(i)
        time.sleep(0.1)
        Socket2.sendall(pickle.dumps('PacEnv'))
        print("Dados (Matriz inversa, determinante da matriz inversa e tempo) enviados!")
        Socket2.close()
    break


