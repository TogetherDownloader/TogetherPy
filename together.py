from downloader import Downloader
from threading import Timer
import socket
import json

PORT = 1111
CHECKTIME = 5
BUFF = 1000000000

# GLOBAL TODO: make this call in functions!
sock = {}
newDownload = {}

def requestDownload():
    global newDownload
    global sock

    # Send data
    message = json.dumps({
        'request': 'imReady'
    })
    sock.sendall(message)

    data = sock.recv(BUFF)
    print data
    data = json.loads(data)

    if data['type'] == 'noNeed':
        Timer( CHECKTIME, checkStatus ).start()
    elif data['type'] == 'download':
        newDownload = Downloader( data['url'], data['startRange'], data['endRange'], data['partNum'] )
        newDownload.start()
        Timer( CHECKTIME, checkStatus ).start()
    else:
        print 'error!'

def checkStatus():
    global newDownload
    status = newDownload.status()
    print json.dumps(status)

    if status['inDownload'] == True:
        Timer( CHECKTIME, checkStatus ).start()
    else:
        requestDownload()

def main():

    global sock

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', PORT)
    print 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    requestDownload()



if __name__ == "__main__":
    main()
