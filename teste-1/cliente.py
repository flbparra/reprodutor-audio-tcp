import socket
import pyaudio
import threading
import time

def baixar_musica(musica, socket_cliente):
    pass

def receber_musica(cliente_socket, musica_escolhida):
    
    TAMANHO_BLOCO= 1024
    p = pyaudio.PyAudio()
    transmissao = p.open(format=p.get_format_from_width(2),
                         channels=2,
                         rate=44100,
                         output=True,
                         frames_per_buffer=TAMANHO_BLOCO)

    while True:
        try:
            data = cliente_socket.recv(TAMANHO_BLOCO)
            if not data:
                break

            transmissao.write(data)

        except OSError:
            break

    transmissao.stop_stream()
    transmissao.close()

'''def enviar_comando(cliente_socket, comando):
    cliente_socket.send(comando.encode())'''

def iniciar_cliente():
    TAMANHO_PEDACO = 1024
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(("127.0.0.1", 9999))


    opcoes_servico = cliente_socket.recv(1024).decode()
    print(opcoes_servico)
    escolha = input("Digite o número do serviço desejado: ")
    cliente_socket.send(escolha.encode())
    
    print()
    time.sleep(1)

    print(cliente_socket.recv(1024).decode())

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
        teste = cliente_socket.recv(1024)

        if teste.decode() == "404":
            print("Música não encontrada no CacheLocal, recebendo do servidor")
            musica_thread = threading.Thread(target=receber_musica, args=(cliente_socket, musica_escolhida))
            musica_thread.start()
            
        elif teste.decode() == "200":
            print("Música encontrada no cache local.")
            pass

    
    elif escolha == "2": 
        
        print(cliente_socket.recv(TAMANHO_PEDACO))
        print(cliente_socket.recv(TAMANHO_PEDACO))
        
    elif escolha == "3": #Escolher cliente para mandar a musica
        

        clientes_disponiveis = cliente_socket.recv(TAMANHO_PEDACO)
        print("Clientes disponiveis para reproduzir música:")
        time.sleep(1)
        print(clientes_disponiveis.decode())

        cliente_escolhido = input("Digite o ID que quer que toque a música: ")
        cliente_socket.send(cliente_escolhido.encode())

        socket_cliente_escolhido = cliente_socket.recv(1024).decode()

        print(f"Esse socket vai recebe as músicas: {socket_cliente_escolhido}")

        musicas_disponiveis = cliente_socket.recv(1024)
        print("Lista de músicas disponíveis:")
        print(musicas_disponiveis.decode())

        # Escolher uma música para reproduzir
        musica_escolhida = input("Digite o nome da música que deseja reproduzir: ")
        cliente_socket.send(musica_escolhida.encode())

        musica_thread = threading.Thread(target=tocar_musica, args=(cliente_socket))
        musica_thread.start()

        
        pass

    else:
        print(cliente_socket.recv(TAMANHO_PEDACO).decode())


    cliente_socket.close()

cache_local = {}
lista_cache = []

iniciar_cliente()
