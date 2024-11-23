import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")
if nickname == "admin":
    password = input("Enter Password")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            global stop_thread
            if stop_thread:
                break
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode("ascii")
                if next_message == "PASS":
                    client.send(password.encode("ascii"))
                    if client.recv(1024).decode("ascii") == "REFUSE":
                        print("Connection was refused! Wrong password")
                        stop_thread = True
                elif next_message == "BAN":
                    print("Connection is refused because of ban!")
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


# Sending Messages To Server
def write():
    while True:
        if stop_thread:
            break
        message = '{}: {}'.format(nickname, input(''))
        if message[len(nickname) + 2:].startswith("/"):
            if nickname == "admin":
                if message[len(nickname) + 2:].startswith("/kick"):
                    client.send(f'KICK{message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname) + 2:].startswith("/ban"):
                    client.send(f'KICK{message[len(nickname) + 2 + 5:]}'.encode('ascii'))

            else:
                print("Commands can only be excecuted by the admin")
        else:
            client.send(message.encode('ascii'))


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()