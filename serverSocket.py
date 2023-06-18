import socket
import threading
import os
import time

def ClientSelect(cliente_socket):

    msg = "Escolha cliente!"
    cliente_socket.send(msg.encode())
    print(cliente_socket.recv(1024).decode())

def OnlineCustomers(clientes_conectados, cliente_socket):
    """Funcionalidades:
    - Mostra os clientes online, todas as vezes que são conectados"""

    print(10 * "-")
    print("Enviando para o cliente a lista de clientes online")
    msg = "Clientes online:"
    cliente_socket.send(msg.encode())
    clientes_online = "\n".join([f"IP: {ip} - PORTA: {porta}" for ip, porta in clientes_conectados])
    cliente_socket.send(clientes_online.encode())
    print(10 * "-")
   

def donwload_musica(data, cliente_socket, musica_dados):

    """Funcionalidades:
    - envia para o cliente as músicas do servidor em bloco de 30 segundos (IMPLEMENTADO)"""
    
    CHUNK = 44100 * 16 * 30 
    TIME30 = 30 
    tempo_inicio = time.time()
    tempo_atual = tempo_inicio
    while data:
        if musica_reproduzir:
            cliente_socket.send(data)
            data = musica_dados.read(CHUNK)
            tempo_atual = time.time()

        else:
            pass


def lidar_cliente(cliente_socket, cliente_endereco, clientes_enderecos, pasta_musicas, clientes_sockets):
    print(f"Conexão feita com cliente: {cliente_endereco}")

    OnlineCustomers(clientes_conectados, cliente_socket)

    TAMANHO_PEDACO = 1024
    global musica_reproduzir
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
            
            with open(f"./musicas/{musica_escolhida}", "rb") as musica_dados:
                data = musica_dados.read(1024)
                
                donwload_musica(data, cliente_socket, musica_dados)
                    #se musica tiver pausada ele apenas vai ficar aguardando um comando do cliente para despausar
                    

        else:
            cliente_socket.send("404".encode())

        # Fechar a conexão com o cliente
        cliente_socket.close()
        print(f"Conexão encerrada com o cliente {cliente_endereco}")

    elif escolha == "2": #Aguardando para receber música do servidor
        
        socket_clientes = 'sockets'
        endereco_cliente = 'enderecos'
        clientes_ativos = {}
        resposta = """Você escolheu o Serviço Receber Música.
        Iremos te adicionar em uma lista de clientes para receber músicas de outros clientes."""

       
        
        cliente_socket.send(resposta.encode())
        
        if socket_clientes and endereco_cliente in clientes_ativos:

            clientes_ativos[socket_clientes].append([cliente_socket])
            clientes_ativos[endereco_cliente].append(cliente_endereco)
        
        else:

            clientes_ativos[socket_clientes] = [cliente_socket]
            clientes_ativos[endereco_cliente] = cliente_endereco

        print(clientes_ativos)

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
            
            ClientSelect(clientes_ativos)

            # implmentar -> servidor 
            cliente_socket.send("200".encode())

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
    global clientes_conectados
    clientes_conectados = []

    while True:
        cliente_socket, cliente_endereco = server_socket.accept()
        clientes_conectados.append(cliente_endereco)
        client_thread = threading.Thread(target=lidar_cliente, args=(cliente_socket, cliente_endereco, clientes_enderecos, pasta_musicas, clientes_sockets))
        client_thread.start()

inicia_server()
