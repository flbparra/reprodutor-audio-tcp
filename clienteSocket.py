import socket
import pyaudio
import threading
import time
import os

TAMANHO_PEDACO = 1024
global PASTA_CACHE
PASTA_CACHE = r"C:\Users\parra\Desktop\redes-computadores-thiago-branch\fabio_version\cache"

def PlayInClient(cliente_socket):
    
    msg = "OKAY!"
    cliente_socket.send(msg.encode())
    

def CheckCache(musica_escolhida):

    """Funcionalidade:
    - Verifica se a música escolhida existe no cache local"""

    caminho_cache = f"C:/Users/parra/Desktop/redes-computadores-thiago-branch/fabio_version/cache/{musica_escolhida}"
    if os.path.exists(caminho_cache):
        return True
    else:
        return False

def PlayCache(musica_escolhida):

    """Funcionalidade:
    - Reproduz músicas salvas no cacheLocal"""

    CHUNK = 1024
    p = pyaudio.PyAudio()
    transmissao = p.open(format=p.get_format_from_width(2),
                         channels=2,
                         rate=44100,
                         output=True,
                         frames_per_buffer=CHUNK)

    caminho_cache = f"C:/Users/parra/Desktop/redes-computadores-thiago-branch/fabio_version/cache/{musica_escolhida}"
    
    try:
        #ler música escolhida
        with open(PASTA_CACHE, "rb") as cache_musica:
            while True:
                # Ler um pedaço dos dados do cache
                data = cache_musica.read(CHUNK)
                if not data:
                    break
                
                # Reproduzir o pedaço de dados lido
                transmissao.write(data)
    except FileNotFoundError:
        print("Música não encontrada no cache.")
    
    transmissao.stop_stream()
    transmissao.close()
    p.terminate()
    """Implementar o play do chache"""
    pass

def PlayAndReceive(cliente_socket, musica_escolhida):
    
    """Funcionalidades:
    - Reproduz as músicas do servidor 
    - Guarda em cache local"""

    CHUNK = 1024
    p = pyaudio.PyAudio()
    transmissao = p.open(format=p.get_format_from_width(2),
                         channels=2,
                         rate=44100,
                         output=True,
                         frames_per_buffer=CHUNK)

    while True:

        data = cliente_socket.recv(CHUNK)
        if not data:
            break

        transmissao.write(data)

        caminho_cache = os.path.join(PASTA_CACHE, musica_escolhida)
        
        if not os.path.exists(PASTA_CACHE):
            os.makedirs(PASTA_CACHE)
        
        # Escrever os dados da música no arquivo do cache
        with open(caminho_cache, "ab") as cache_file:
            cache_file.write(data)



    transmissao.stop_stream()
    transmissao.close()
    p.terminate()

def StartClient():

    """Melhorias:
    - Tratar erro apos cliente enviar musica escolhida
    Implementar:
    - Funcionalidade para enviar música para cliente"""

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(("127.0.0.1", 9999))

    # cliente consegue ver clientes que estão online

    print(10 * "--")

    msg = cliente_socket.recv(1024).decode()
    print(msg)

    clientes_online = cliente_socket.recv(1024).decode()
    print(clientes_online)

    print(10 * "--")
    print()

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
        
        # recebe as lista de músicas disponiveis no servidor.

        musicas_disponiveis = cliente_socket.recv(1024)
        print("Lista de músicas disponíveis:")
        print(musicas_disponiveis.decode())

        musica_escolhida = input("Digite o nome da música que deseja reproduzir: ")
        cliente_socket.send(musica_escolhida.encode())
        

        # checar musica em cache local (implementando)
        
        if CheckCache(musica_escolhida):
            PlayCache(musica_escolhida)

        else:
            
            status = cliente_socket.recv(TAMANHO_PEDACO)

            if status.decode() == "200":
                print("Música encontrada no servidor.")
                musica_thread = threading.Thread(target=PlayAndReceive, args=(cliente_socket, musica_escolhida))
                musica_thread.start()
            elif status.decode() == "404":
                print("Música não encontrada no servidor.")
                cliente_socket.close()

            # Iniciar a reprodução da música em uma thread separada
            
    
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

        msg = cliente_socket.recv(1024).decode()

        print(msg)

        PlayInClient(cliente_socket)

        

        pass

    else:
        print(cliente_socket.recv(TAMANHO_PEDACO).decode())

    # Aguardar a reprodução da música

    # Fechar a conexão com o servidor
    cliente_socket.close()


StartClient()