import socket
import requests
import sys
import json

port = 1111
chunkSize = 1048576
# chunkSize = 1000000

def main():

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
    server_address = ('localhost', port)
    print 'Server is runnig on port ' + str(port)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        print 'waiting for a connection...'
        connection, client_address = sock.accept()

        try:
            print 'client connected: ', client_address
            while True:
                data = connection.recv(1000000000)

                if data != "":  # if client alive
                    data = json.loads(data)
                    if data['request'] == 'imReady':
                        packetSize = chunkSize if needToDownload>chunkSize else needToDownload
                        print needToDownload

                        if needToDownload != 0:
                            res = json.dumps({
                                'type': 'download',
                                'url': url,
                                'startRange': lastPart * chunkSize,
                                'endRange': (lastPart) * chunkSize + packetSize - (1 if needToDownload>chunkSize else 0),
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
                    pass
                    # print 'client die!'
                    # TODO: do some thing

        finally:
            connection.close()

if __name__ == "__main__":
    main()
