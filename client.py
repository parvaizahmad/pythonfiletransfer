import socket

def main():
    host = '127.0.0.1'
    port = 5003 
    loop = True 
    while loop:
        s = socket.socket()
        s.connect((host, port))
        print("#"*50)
        print("Available Files: ")
        print("")
        while True:
            data = s.recv(1024)
            data = data.decode()
            if 'sent' in data:
                break
            else:
                print(data)
                data = ""
        print("#"*50)
        print("")
        filename = input("Enter Filename: ->")
        if filename != 'q':
            filename = filename.encode()
            s.send(filename)
            data = s.recv(1024)
            data = data.decode()
            if data[:6] == 'EXISTS':
                filesize = float(data[6:])
                message = input("File exists, " + str(filesize) + " Bytes, download? (Y/N) ->")

                if message == 'Y' or message == 'y':
                    ok = 'OK'
                    ok = ok.encode()
                    s.send(ok)
                    filetosave = input("Enter the Save As file Name: ->")
                    f = open(filetosave, 'wb')
                    data = s.recv(1024)

                    totalrecv = len(data)
                    f.write(data)

                    while totalrecv < filesize:
                        data = s.recv(1024)

                        totalrecv += len(data)
                        f.write(data)
                        print('\r' + "{0:.2f}".format((totalrecv/float(filesize))*100) + "% Done")

                    print("Download Completed.")
                    f.close()
                    newfile = input("Want to download another file (Y/N) -> ")

                    if newfile == 'N' or newfile == 'n':
                        loop = False
                        s.close()
                        print("Connection Terminated.")

                else:
                    print("Download Aborted.")
            else:
                print("File does not exists.")

        else:
            s.close()
            print("Thanks for using.")
            loop = False

if __name__ == "__main__":
    main()
                
