import socket
import requests
import json
import thread
from mixer import Mixer

PORT = 1111
CHUNKSIZE = 1048576
BUFF = 1000000000

# GLOBAL variables! TODO:move inside functions
needToDownload = 0
lastPart = 0


def handler( url, connection, addr):
    global needToDownload
    global lastPart

    try:
        print 'client connected: ', addr
        while True:
            data = connection.recv(BUFF)

            if data != "":  # if client alive
                data = json.loads(data)
                if data['request'] == 'imReady':
                    packetSize = CHUNKSIZE if needToDownload>CHUNKSIZE else needToDownload
                    print needToDownload

                    if needToDownload != 0:
                        res = json.dumps({
                            'type': 'download',
                            'url': url,
                            'startRange': lastPart * CHUNKSIZE,
                            'endRange': (lastPart) * CHUNKSIZE + packetSize - (1 if needToDownload>CHUNKSIZE else 0),
                            'partNum': lastPart
                        })
                        needToDownload -= packetSize
                        lastPart = lastPart + 1
                    else:
                        res = json.dumps({
                            'type': 'noNeed',
                        })
                else:
                    res = json.dumps({
                        'type': 'error',
                        'message': 'badRequest'
                    })
                connection.sendall(res)
            else:
                print 'client die! ', addr
                exit()
                # TODO: do some thing

    finally:
        connection.close()


def main():
    global needToDownload
    global lastPart
    global url

    url = "http://cdn.download.ir/?b=dlir-mac&f=Audirvana.Plus.2.6.1.www.download.ir.rar"
    response = requests.get(url, stream=True)
    totalLength = int(response.headers.get('content-length'))

    if totalLength:
        print 'total size is ' + str( round(float(totalLength)/1048576, 1) ) + 'Mb'
        print totalLength
    else:
        print 'Not support!'
        exit()

    needToDownload = totalLength
    lastPart = 0

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', PORT)

    print 'Server is runnig on port ' + str(PORT)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        print 'waiting for a connection...'
        connection, addr = sock.accept()
        thread.start_new_thread(handler, (url, connection, addr))



if __name__ == "__main__":
    main()
