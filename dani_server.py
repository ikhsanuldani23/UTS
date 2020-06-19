import socket
import select
from threading import *
import sys


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
Argumen pertama AF_INET adalah domain alamat soket. Ini digunakan ketika kita memiliki Domain Internet dengan dua host
Argumen kedua adalah jenis soket. SOCK_STREAM berarti bahwa data atau karakter dibaca dalam aliran yang berkelanjutan.
"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 3:
    print("Penggunaan benar: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port)) 
#binds the server to an entered IP address and at the specified port number. The client must be aware of these parameters
server.listen(100)
#listens for 100 active connections. This number can be increased as per convenience
list_of_clients=[]

def clientthread(conn, addr):
    conn.send("Selamat datang di chatroom!")
    #sends a message to the client whose user object is conn
    while True:
            try:     
                message = conn.recv(2048)    
                if message:
                    print("<" + addr[0] + "> " + message)
                    message_to_send = "<" + addr[0] + "> " + message
                    broadcast(message_to_send,conn)
                    #prints the message and address of the user who just sent the message on the server terminal
                else:
                    remove(conn)
            except:
                continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    """
    Argumen pertama AF_INET adalah domain alamat soket. Ini digunakan ketika kita memiliki Domain Internet dengan dua host
    Argumen kedua adalah jenis soket. SOCK_STREAM berarti bahwa data atau karakter dibaca dalam aliran yang berkelanjutan.
    
    """
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    #Prints the address of the person who just connected
    start_new_thread(clientthread,(conn,addr))
    #creates and individual thread for every user that connects

conn.close()
server.close()
