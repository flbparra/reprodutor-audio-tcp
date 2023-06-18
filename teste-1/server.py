import socket
import threading
import os
import time


def download_musica(cliente_socket,cliente_endereco, musicas_disponiveis):

    resposta = "Você escolheu o Serviço Tocar Música"
    cliente_socket.send(resposta.encode())
    time.sleep(3)
    cliente_socket.send(musicas_disponiveis.encode())
    # Receber a música escolhida pelo cliente
    musica_escolhida = cliente_socket.recv(1024).decode()
    print(f'----------{musica_escolhida}')


    if os.path.exists(f"./musicas/{musica_escolhida}"):
        
        cliente_socket.send("404".encode())

        with open(f"./musicas/{musica_escolhida}", "rb") as musica_dados:
            
            data = musica_dados.read(1024)
            TAMANHO_BLOCO = 1024

            try:
                while True:
                    data = musica_dados.read(TAMANHO_BLOCO)
                    if not data:
                        break  # Todos os dados foram enviados

                    cliente_socket.send(data)

                cliente_socket.close()
                print("Envio de música concluído")

            except ConnectionResetError:
                print("A conexão foi fechada pelo cliente de forma abrupta")
            
            

            cliente_socket.close()
            print(f"Conexão encerrada com o cliente {cliente_endereco}")      

    else:
        cliente_socket.send("200".encode())
    
    
def receber_musica():
    pass

def lidar_cliente(cliente_socket, cliente_endereco, clientes_enderecos, pasta_musicas, clientes_sockets):
    print(f"Conexão feita com cliente: {cliente_endereco}")

    TAMANHO_PEDACO = 1024

    # Recuperar a lista de músicas disponíveis no servidor
    musicas_lista = os.listdir(pasta_musicas)
    musicas_lista = [musica for musica in musicas_lista]
    musicas_disponiveis = "\n".join(musicas_lista)

    #escolha de serviço
    opcoes_servico = """Escolha um desses três serviços :
    1. Selecionar uma música para tocar
    2. Receber Música para tocar de outro cliente
    3. Escolher cliente para tocar música"""
    cliente_socket.send(opcoes_servico.encode())
    escolha_servico = cliente_socket.recv(TAMANHO_PEDACO).decode()

    if escolha_servico == "1": #Reproduzir música no meu dispositivo
        download_thread = threading.Thread(target=download_musica, args=(cliente_socket,cliente_endereco, musicas_disponiveis))
        download_thread.start()
        download_thread.join()
            
       

    elif escolha_servico == "2": #Aguardando para receber música do servidor
        resposta = "Você escolheu o Serviço  Receber música"
        cliente_socket.send(resposta.encode())

        clientes_sockets.append([cliente_socket])
        clientes_enderecos.append(cliente_endereco)

        '''print()
        print(clientes_enderecos)
        print()
        print(f'------ SOCKETS DISPONIVEIS {clientes_sockets}')'''


        time.sleep(3)

        msg = "Aguardando cliente enviar pacotes..."
        
        cliente_socket.send(msg.encode())

    elif escolha_servico == "3":
        resposta = "Você escolheu o Serviço Escolher cliente para reprodução da música"
        cliente_socket.send(resposta.encode())


        time.sleep(3)

        clientes_disponiveis = "\n".join(f"ID: {index} - PORTA: {str(cliente[1])}" for index, cliente in enumerate(clientes_enderecos))
        print(clientes_disponiveis)
        cliente_socket.send(clientes_disponiveis.encode())
        
        cliente_escolhido = int(cliente_socket.recv(TAMANHO_PEDACO).decode())
        print(f"O cliente escolhido foi o INDEX: {cliente_escolhido}")


####################################################
        socket_cliente_escolhido = clientes_sockets.pop(cliente_escolhido)
        socket_cliente_escolhido = socket_cliente_escolhido[0]
        print(socket_cliente_escolhido)

        cliente_socket.send(str(socket_cliente_escolhido).encode())
##############################################################################3
        cliente_socket.send(musicas_disponiveis.encode())

        # Receber a música escolhida pelo cliente
        musica_escolhida = cliente_socket.recv(TAMANHO_PEDACO).decode()

        # Verificar se a música está presente no cache local
        if os.path.exists(f"./musicas/{musica_escolhida}"):
            socket_cliente_escolhido.send("200".encode())


            with open(f"./musicas/{musica_escolhida}", "rb") as musica_dados:
                data = musica_dados.read(1024)

                while data:

                    if musica_reproduzir:
                         socket_cliente_escolhido.send(data)
                         data = musica_dados.read(TAMANHO_PEDACO)

                    #if indice_atual != musicas.index(musica_atual):
                    #    break
                    else:
                        pass
                    #se musica tiver pausada ele apenas vai ficar aguardando um comando do cliente para despausar
                    

        else:
            socket_cliente_escolhido.send("MUSIC_NOT_FOUND".encode())
            

        # Remover o cliente da lista de clientes conectado

        # Fechar a conexão com o cliente
        cliente_socket.close()


    
    else:
        resposta = "Escolha inválida. Tente novamente."
        cliente_socket.send(resposta.encode())


def StartServer():
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


StartServer()


