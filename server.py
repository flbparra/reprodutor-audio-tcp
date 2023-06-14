import socket
import threading
import os
import time


def lidar_cliente(cliente_socket, cliente_endereco, pasta_musicas, clientes_conectados):
    print(f"Conexão feita com cliente: {cliente_endereco}")
   
    TAMANHO_PEDACO = 1024
    # tamanho do bloco em segundos  
    BLOCO_PEDACO = 30

    musica_pausada = False

    # Recuperar a lista de músicas disponíveis no servidor
    musicas = os.listdir(pasta_musicas)
    musicas = [musica for musica in musicas] #if musica.endswith(".mp3")
    musicas_disponiveis = "\n".join(musicas) #uma string que lida com as músicas que tem disponiveis
    cliente_socket.send(musicas_disponiveis.encode())

    # Receber a música escolhida pelo cliente
    musica_escolhida = cliente_socket.recv(1024).decode()
    print(musica_escolhida)

    # Verificar se a música está presente no cache local
    if os.path.exists(f"./musicas/{musica_escolhida}"):
        print("oii")
        cliente_socket.send("200".encode())

        with open(f"./musicas/{musica_escolhida}", "rb") as musica_dados:
            data = musica_dados.read(1024)
            tempo_inicio = time.time()
            
            cliente_selecionado = None  # Cliente selecionado para receber a música

            while data:
                if cliente_selecionado:
                    cliente_selecionado.send(data)
                else:
                    for cliente in clientes_conectados:
                        cliente.send(data)

                tempo_decorrido = time.time() - tempo_inicio

                if tempo_decorrido >= BLOCO_PEDACO:
                    time.sleep(BLOCO_PEDACO - tempo_decorrido % BLOCO_PEDACO)
                    tempo_inicio = time.time()
                        
                data = musica_dados.read(TAMANHO_PEDACO)

    else:
        cliente_socket.send("404".encode())

    # Remover o cliente da lista de clientes conectados
    clientes_conectados.remove(cliente_socket)

    # Fechar a conexão com o cliente
    cliente_socket.close()
    print(f"Conexão encerrada com o cliente {cliente_endereco}")


def lidar_comando(cliente_socket, comando, clientes_conectados):
    if comando.startswith("select"):
        cliente_selecionado = comando.split(" ")[1]  # Extrair o nome do cliente selecionado
        for cliente in clientes_conectados:
            if cliente.getpeername()[1] == cliente_selecionado:
                cliente_socket.send(f"Cliente {cliente_selecionado} selecionado para receber a música.".encode())
                cliente_selecionado = cliente
                break
        else:
            cliente_socket.send(f"Cliente {cliente_selecionado} não encontrado.".encode())
            cliente_selecionado = None

    # Retornar o cliente selecionado para tocar a música
    return cliente_selecionado


def inicia_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 9999))
    server_socket.listen(5)

    print("Servidor iniciado. Aguardando conexões...")
    
    pasta_musicas = r"C:\Users\parra\Desktop\redes-computadores-thiago-branch\fabio_version\musicas"
    clientes_conectados = []

    while True:
        cliente_socket, cliente_endereco = server_socket.accept()
        clientes_conectados.append(cliente_socket)
        print(clientes_conectados)

        client_thread = threading.Thread(target=lidar_cliente, args=(cliente_socket, cliente_endereco, pasta_musicas, clientes_conectados))
        client_thread.start()

        comando_thread = threading.Thread(target=lidar_comando, args=(cliente_socket, comando, clientes_conectados))
        comando_thread.start()


inicia_server()
