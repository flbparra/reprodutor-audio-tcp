## Projeto de Streaming de Música Cliente-Servidor

>Este projeto implementa um sistema de streaming de música cliente-servidor, onde os clientes podem conectar-se a um servidor para reproduzir músicas disponíveis em um cache local ou buscadas no servidor principal.

### Tecnologias Utilizadas:
- Python: A linguagem de programação principal usada para implementar tanto o cliente quanto o servidor.
- Socket Programming: As comunicações entre cliente e servidor são realizadas utilizando sockets TCP/IP.
- Threading: O uso de threads permite lidar com várias conexões de clientes simultaneamente, garantindo um serviço assíncrono.
- PyAudio: Uma biblioteca Python para lidar com entrada e saída de áudio, utilizada para reproduzir as músicas no cliente.

### Funcionalidades:
- Cliente:

  1. Conecta-se ao servidor para obter a lista de músicas disponíveis.
  2. Escolhe uma música para reproduzir.
  3. Verifica se a música está no cache local. Se não estiver, solicita ao servidor.
  4. Inicia a reprodução da música em uma thread separada para não bloquear outras operações.
  5. Encerra a conexão após a reprodução da música.

- Servidor:

  1. Aguarda conexões de clientes em um endereço IP e porta específicos.
  2. Envia a lista de músicas disponíveis quando um cliente se conecta.
  3. Recebe a escolha de música do cliente e verifica se está presente no cache local.
  4. Se a música estiver no cache, envia-a para o cliente. Caso contrário, busca-a no servidor principal.
  5. Utiliza threads para lidar com os clientes e suas interações, como escolha de cliente para enviar a música.

### Configuração:
- Certifique-se de ter as músicas desejadas na pasta de músicas do servidor.
- Os clientes devem ter acesso ao servidor utilizando o endereço IP e porta configurados.
- Certifique-se de que todas as bibliotecas Python necessárias, como PyAudio, estejam instaladas no ambiente.

### Execução:
- Execute o script server.py para iniciar o servidor.
- Execute o script client.py em um ou mais clientes para se conectar ao servidor e reproduzir músicas.

### Notas Adicionais:
- Cache Local: O servidor mantém um cache local de músicas para melhorar o desempenho, evitando acessos frequentes ao sistema de arquivos.
- Controle de Cliente: Implementa um comando de seleção de cliente, permitindo ao servidor escolher a quem enviar a música, se necessário.
- Espero que isso ajude! Se precisar de mais alguma coisa, estou aqui para ajudar.
