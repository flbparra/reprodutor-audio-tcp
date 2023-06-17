import socket
import threading
import pyaudio
import os

TAMANHO_PEDACO = 1024

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
            break

        transmissao.write(data)

    transmissao.stop_stream()
    transmissao.close()

def iniciar_cliente():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(("127.0.0.1", 9999))

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
        print("Música encontrada no cache local.")
    elif cache_status.decode() == "404":
        print("Música não encontrada no cache local. Buscando no servidor...")

    # Iniciar a reprodução da música em uma thread separada
    musica_thread = threading.Thread(target=reproduzir_musica, args=(cliente_socket,))
    musica_thread.start()

    while True:
        comando = input("Comando (pausar, prox, ant): ")

        if comando == "pausar":
            cliente_socket.send(comando.encode())
        elif comando == "prox":
            cliente_socket.send(comando.encode())
            break
        elif comando == "ant":
            cliente_socket.send(comando.encode())
            break

    # Aguardar a reprodução da música
    musica_thread.join()

    # Fechar a conexão com o servidor
    cliente_socket.close()

iniciar_cliente()
