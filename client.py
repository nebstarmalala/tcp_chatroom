import socket
import threading
import config

PORT = 5050
HOST = config.host
ADDR = (HOST, PORT)
FORMAT = 'ascii'

nickname = input('Input your nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# def server_connect():
#     client.send('CONNECT'.encode(FORMAT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message =='NICK':
                client.send(nickname.encode(FORMAT))
            else:
                print(message)
        except:
            print('An error occurred')
            client.close()
            break

def write():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode(FORMAT))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()