import socket
import threading
import logging


PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)
FORMAT = 'ascii'


logger = logging.getLogger('ROOT')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('logs.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(asctime)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
nicknames = []

# # Color Handler
# def prGreen(skk): print("\033[92m{}\033[00m".format(skk))
# def prYellow(skk): print("\033[93m{}\033[00m".format(skk))
# def prRed(skk): print("\033[91m{}\033[00m".format(skk))


def broadcast(messsage):
    for client in clients:
        client.send(messsage)


def handle_client(addr, client):
    connected = True
    while connected:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client.index(clients)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            print(f'{nickname} left the chat!'.encode(FORMAT))
            logger.info(f'{addr} left the chat!')
            break


def main():
    while True:
        server.listen()
        print(f"[*] {len(clients)} clients connected")
        logger.info(f"[*] {len(clients)} clients connected")
        print(f"[*] server is listening on {HOST}...")
        client, addr = server.accept()

        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)

        print(f'[*] {addr} connected as {nickname}')
        logger.info(f'[*] {addr} connected as {nickname}')
        broadcast(f'{nickname} joined the chat'.encode(FORMAT))
        client.send('You are connected to the server'.encode(FORMAT))

        thread = threading.Thread(target=handle_client, args=(addr, client))
        thread.start()


print('[*] Server is starting...')
logger.info("[*] Server is starting...")
print(f"[*] server is listening on {HOST}...")
logger.info(f"[*] server is listening on {HOST}")
main()