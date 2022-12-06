import socket
from socket import *
import threading
import time
import pandas as pd



connections = []
curDrift = []

# Starts the server
def runServer():
    global runningThreads
    server_port = 12000
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen()
    print("The server is ready to receive...")
    threading.Thread(target=berkeley).start()
    while True:
        connection_socket, addr = server_socket.accept()
        connections.append(connection_socket)
        threading.Thread(target=recvMsg, args=[connection_socket]).start()
       

# Receives messages from clients
def recvMsg(connection_socket):
    global curDrift
    while True:
        try: 
            msg = connection_socket.recv(1024)
            if msg:
                drift = (msg.decode()).split(", ")
                drift.pop()
                drift = [eval(i) for i in drift]
                curDrift = drift
            else:
                break
        except:
            continue
    connection_socket.close()


# Computes the average delay of all of the clients and sends it back to them.
# This is equivalent to sending the clients the avg clock value, but it
# is much easier to implement in the code.
def berkeley():
    while True:
        if not curDrift:
            continue    
        time.sleep(1)
        avgDelay = sum(curDrift) / len(curDrift)
        print('avgDelay', avgDelay)
        sendMsg(avgDelay)

# Sends messages to clients
def sendMsg(msg):
    to_send = str.encode(str(round(msg)))
    connections[0].send(to_send)


# def compute(thread, connection_socket):
#     global runningThreads
#     total = 0
#     for i in range(900000):
#         total += i
#     msg = 'Thread {} Connected.'.format(thread)
#     connection_socket.send(str.encode(msg))
#     runningThreads -= 1
#     print('Running Threads:', runningThreads)
#     if thread == 100:
#         global t_end
#         t_end = time.time()
#         print('Total Time:', t_end - t_start)
    



if __name__ == "__main__":
    runServer()


