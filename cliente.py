import socket
import pyaudio
import threading
import time

TAMANHO_PEDACO = 1024

def mandar_musica(socket_escolhido):
    p = pyaudio.PyAudio()
    transmissao = p.open(format=p.get_format_from_width(2),
                         channels=2,
                         rate=44100,
                         output=True,
                         frames_per_buffer=TAMANHO_PEDACO)

    while True:
        data = cliente_socket.recv(TAMANHO_PEDACO)
        if not data:
            pass

        transmissao.write(data)

    transmissao.stop_stream()
    transmissao.close()


def reproduzir_musica(cliente_socket):
    p = pyaudio.PyAudio()
    transmissao = p.open(format=p.get_format_from_width(2),
                         channels=2,
                         rate=44100,
                         output=True,
                         frames_per_buffer=TAMANHO_PEDACO)

    while True:
        data = cliente_socket.recv(TAMANHO_PEDACO)
        if not data:
            pass

        transmissao.write(data)

    transmissao.stop_stream()
    transmissao.close()

'''def enviar_comando(cliente_socket, comando):
    cliente_socket.send(comando.encode())'''

def iniciar_cliente():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(("127.0.0.1", 9999))


    opcoes_servico = cliente_socket.recv(TAMANHO_PEDACO).decode()
    print(opcoes_servico)
    escolha = input("Digite o número do serviço desejado: ")
    cliente_socket.send(escolha.encode())
    
    print()
    time.sleep(1)

    print(cliente_socket.recv(TAMANHO_PEDACO).decode())

    print()
    time.sleep(1)
    
    if escolha == "1": 
        # Recuperar a lista de músicas do servidor
        musicas_disponiveis = cliente_socket.recv(1024)
        print("Lista de músicas disponíveis:")
        print(musicas_disponiveis.decode())

        # Escolher uma música para reproduzir
        musica_escolhida = input("Digite o nome da música que deseja reproduzir: ")
        cliente_socket.send(musica_escolhida.encode())

        # Verificar se a música está no cache local
        cache_status = cliente_socket.recv(TAMANHO_PEDACO)

        if cache_status.decode() == "200":
            print("Música encontrada no servidor.")
        elif cache_status.decode() == "404":
            print("Música não encontrada no servidor.")

        # Iniciar a reprodução da música em uma thread separada
        musica_thread = threading.Thread(target=reproduzir_musica, args=(cliente_socket,))
        musica_thread.start()
    
    elif escolha == "2": 
        
        print(cliente_socket.recv(TAMANHO_PEDACO))
        print(cliente_socket.recv(TAMANHO_PEDACO))
        
    elif escolha == "3":

        musicas_disponiveis = cliente_socket.recv(1024)
        print("Lista de músicas disponíveis:")
        print(musicas_disponiveis.decode())

        # Escolher uma música para reproduzir
        musica_escolhida = input("Digite o nome da música que deseja reproduzir: ")
        cliente_socket.send(musica_escolhida.encode())

        musica_thread = threading.Thread(target=mandar_musica, args=(cliente_socket,))
        musica_thread.start()



        
        pass

    else:
        print(cliente_socket.recv(TAMANHO_PEDACO).decode())

    '''while True:
        comando = input("Comando (pausar, despausar, prox, ant): ")

        enviar_comando(cliente_socket, comando)

        if comando == "prox" or comando == "ant":
            break'''

    # Aguardar a reprodução da música
    musica_thread.join()

    # Fechar a conexão com o servidor
    cliente_socket.close()

iniciar_cliente()
