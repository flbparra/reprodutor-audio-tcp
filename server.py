import socket
import threading
import os
import time

def escolher_cliente():
    pass
    
def tocar_musica():
    pass

def receber_musica():
    pass

def lidar_cliente(cliente_socket, cliente_endereco, clientes_enderecos, pasta_musicas, clientes_sockets):
    print(f"Conexão feita com cliente: {cliente_endereco}")

    TAMANHO_PEDACO = 1024

    #musica_atual = None
    #indice_atual = -1
    musica_reproduzir = True

    # Recuperar a lista de músicas disponíveis no servidor
    musicas = os.listdir(pasta_musicas)
    musicas_lista = [musica for musica in musicas]
    musicas_disponiveis = "\n".join(musicas_lista)

    #escolha de serviço
    opcoes_servico = """Escolha um desses três serviços :
    1. Selecionar uma música para tocar
    2. Receber Música para tocar de outro cliente
    3. Escolher cliente para tocar música"""
    cliente_socket.send(opcoes_servico.encode())
    escolha = cliente_socket.recv(TAMANHO_PEDACO).decode()

    if escolha == "1": #Reproduzir música no meu dispositivo

        resposta = "Você escolheu o Serviço Tocar Música"
        cliente_socket.send(resposta.encode())
        
        time.sleep(3)

        cliente_socket.send(musicas_disponiveis.encode())

        # Receber a música escolhida pelo cliente
        musica_escolhida = cliente_socket.recv(1024).decode()

        # Verificar se a música está presente no cache local
        if os.path.exists(f"./musicas/{musica_escolhida}"):
            cliente_socket.send("200".encode())

            musica_atual = musica_escolhida
            indice_atual = musicas.index(musica_atual)

            with open(f"./musicas/{musica_escolhida}", "rb") as musica_dados:
                data = musica_dados.read(1024)

                while data:

                    if musica_reproduzir:
                        cliente_socket.send(data)
                        data = musica_dados.read(TAMANHO_PEDACO)

                    #if indice_atual != musicas.index(musica_atual):
                    #    break
                    else:
                        pass
                    #se musica tiver pausada ele apenas vai ficar aguardando um comando do cliente para despausar
                    

        else:
            cliente_socket.send("MUSIC_NOT_FOUND".encode())
            

        # Remover o cliente da lista de clientes conectados
        clientes_conectados.remove(cliente_socket)

        # Fechar a conexão com o cliente
        cliente_socket.close()
        print(f"Conexão encerrada com o cliente {cliente_endereco}")



    elif escolha == "2": #Aguardando para receber música do servidor
        resposta = "Você escolheu o Serviço  Receber música"
        cliente_socket.send(resposta.encode())

        clientes_sockets.append(cliente_socket)
        clientes_enderecos.append(cliente_endereco)
        print()
        print(clientes_enderecos)
        print()
        print(clientes_sockets)


        time.sleep(3)

        msg = "Aguardando cliente enviar pacotes..."
        
        cliente_socket.send(msg.encode())





    
    elif escolha == "3":
        resposta = "Você escolheu o Serviço Escolher cliente para reprodução da música"
        cliente_socket.send(resposta.encode())

        print(clientes_sockets)

        time.sleep(3)

        cliente_socket.send(musicas_disponiveis.encode())

        # Receber a música escolhida pelo cliente
        musica_escolhida = cliente_socket.recv(1024).decode()

        # Verificar se a música está presente no cache local
        if os.path.exists(f"./musicas/{musica_escolhida}"):
            cliente_socket.send("200".encode())

            musica_atual = musica_escolhida
            indice_atual = musicas.index(musica_atual)

            with open(f"./musicas/{musica_escolhida}", "rb") as musica_dados:
                data = musica_dados.read(1024)

                while data:

                    if musica_reproduzir:
                        cliente_socket.send(data)
                        data = musica_dados.read(TAMANHO_PEDACO)

                    #if indice_atual != musicas.index(musica_atual):
                    #    break
                    else:
                        pass
                    #se musica tiver pausada ele apenas vai ficar aguardando um comando do cliente para despausar
                    

        else:
            cliente_socket.send("MUSIC_NOT_FOUND".encode())
            

        # Remover o cliente da lista de clientes conectados
        clientes_conectados.remove(cliente_socket)

        # Fechar a conexão com o cliente
        cliente_socket.close()


    
    else:
        resposta = "Escolha inválida. Tente novamente."
        cliente_socket.send(resposta.encode())

    

    


def inicia_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 9999))
    server_socket.listen(5)

    print("Servidor iniciado. Aguardando conexões...")

    pasta_musicas = r"C:\Users\parra\Desktop\redes-computadores-thiago-branch\fabio_version\musicas"
    clientes_sockets = []
    clientes_enderecos = []

    while True:
        cliente_socket, cliente_endereco = server_socket.accept()

        client_thread = threading.Thread(target=lidar_cliente, args=(cliente_socket, cliente_endereco, clientes_enderecos, pasta_musicas, clientes_sockets))
        client_thread.start()

inicia_server()
'''        comando_thread = threading.Thread(target=lidar_comandos, args=(cliente_socket,))
        comando_thread.start()


def lidar_comandos(cliente_socket):
    
    while True:
        comando = cliente_socket.recv(1024).decode()

        if comando == "pausar":
            pausar_musica()  
        else:
            return False
    
def pausar_musica():
    global musica_reproduzir
    musica_reproduzir = False

def despausar_musica():
    global musica_reproduzir
    musica_reproduzir = False

def proxima_musica():
    global musica_atual
    global indice_atual
    indice_atual += 1
    if indice_atual >= len(musicas):
        indice_atual = 0
    musica_atual = musicas[indice_atual]
    musica_reproduzir = True

def musica_anterior():
    global musica_atual
    global indice_atual
    indice_atual -= 1
    if indice_atual < 0:
        indice_atual = len(musicas) - 1
    musica_atual = musicas[indice_atual]
    musica_reproduzir = True'''


