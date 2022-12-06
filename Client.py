from socket import *
import threading
import time
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

drift = driftTotal = [0] * 50 


# Starts the client. Connects to the server
def runClient(numThread):
    print('Attempting to connect to server...')
    server_name = ''
    server_port = 12000
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    threading.Thread(target=clockDrift, args=[numThread]).start()
    if (numThread == 0):
        threading.Thread(target=sendDrift, args=[client_socket]).start()
    recvMsg(client_socket)
    client_socket.close()


# Sends drift to server
def sendDrift(client_socket):
    while True:
        time.sleep(0.1)
        msg = ""
        for x in drift:
            msg += str(x) + ", "
        client_socket.send(str.encode(msg))


def recvMsg(client_socket):  
    global drift
    while True:
        try:
            recvdMsg = client_socket.recv(1024)
            newDrift = int(recvdMsg.decode())
            if (newDrift):
                # print('Old Drift:', drift)
                drift = [int(newDrift)] * len(drift)
                # print('New Drift:', drift)
        except:
            continue


# Adds drift to time
def clockDrift(numThread):
    global drift
    global driftTotal
    while True:
        time.sleep(0.25)
        r = random.randint(0,10)
        drift[numThread] += r
        driftTotal[numThread] += r


# Returns the time in ms plus the artificial drift
def getTimeBerk(numThread):
    return round(time.time(), 2) + drift[numThread]


# Returns the time in ms without using the berkeley algorithm
def getTime(numThread):
    return round(time.time(), 2) + driftTotal[numThread]
    

if __name__ == "__main__":
    print('Thomas Cazort') 
    for i in range(50):
        print(i, ':')
        threading.Thread(target=runClient, args=[i]).start()
    A, B = random.randint(0, 49), random.randint(0, 49)
    graph1Vals = [[], [], [], []]
    graph2Vals = [[], []]
    start = round(time.time(), 2)
    for i in range(100):
        time.sleep(0.1)
        graph1Vals[0].append(getTime(A) - start)        # A
        graph1Vals[1].append(getTime(B) - start)        # B
        graph1Vals[2].append(getTimeBerk(A) - start)    # A-Berkeley
        graph1Vals[3].append(getTimeBerk(B) - start)    # B-Berkeley

        # totalAvg = (driftTotal[A] + driftTotal[B]) / 2
        graph2Vals[0].append(graph1Vals[0][i] - graph1Vals[1][i])      # delta
        # berkAvg = (drift[A] + drift[B]) / 2
        graph2Vals[1].append(graph1Vals[2][i] - graph1Vals[3][i])       # delta-Berkeley

    d = {'A': graph1Vals[0], 'B': graph1Vals[1], 'A-Berkeley': graph1Vals[2], 'B-Berkeley': graph1Vals[3]}
    df = pd.DataFrame(data=d)
    print(df)
    print(drift)
    print(driftTotal)
    g1 = sns.lineplot(data=df)
    g1.set(xticklabels=['1', '0', '2000', '4000', '6000', '8000', '10000'], ylabel='Local Clock Value / ms', xlabel='Time / ms')
    plt.show()

    d = {'delta': graph2Vals[0], 'delta-Berkeley': graph2Vals[1]}
    df = pd.DataFrame(data=d)
    g2 = sns.lineplot(data=df)
    g2.set(xticklabels=['1', '0', '2000', '4000', '6000', '8000', '10000'], ylabel='Local Clock Difference / ms', xlabel='Time / ms')
    g2.axhline(0, c='black', ls='-')
    plt.show()


    
