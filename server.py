import socket
import os
import threading
import time

path = '.\\'

def RetFile(name, sock):
    files = os.listdir(path)
    for i in range(len(files)):
        sock.send(files[i].encode())
        time.sleep(0.7)

    sock.send("sent".encode())
    filename = sock.recv(1024)
    filename = filename.decode()

    if os.path.isfile(filename):
        var = "EXISTS " + str(os.path.getsize(filename))
        var = var.encode()
        sock.send(var)

        userResp = sock.recv(1024)
        userResp = userResp.decode()
        if userResp[:2] == 'OK':
            with open(filename, 'rb') as f:
                dataToSend = f.read(1024)
                sock.send(dataToSend)
                while dataToSend != "":
                    dataToSend = f.read(1024)
                    sock.send(dataToSend)
            
    else:
        sock.send("ERR".encode())

    sock.close()
    print("Port Closed in Thread.")

def main():
    host = '127.0.0.1'
    port = 5003

    s = socket.socket()
    s.bind((host, port))

    s.listen(5)
    print("Server Started.")
    print("Waiting for the connections...")
    while True:
        c, addr = s.accept()
        print("Client Conencted. IP: (" + str(addr) + ")")
        thread = threading.Thread(target=RetFile, args=("RetThread", c))
        thread.start()

    s.close()
    print("Connection closed.")
    
if __name__ == "__main__":
    main()