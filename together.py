from downloader import Downloader
from threading import Timer
import socket
import json

port = 1111
sleepTime = 10
checkTime = 2

# GLOBAL
sock = {}
newDownload = {}

def requestDownload():
    global newDownload
    global sock

    print 'newDownload called!'

    # Send data
    message = json.dumps({
        'request': 'imReady'
    })
    sock.sendall(message)

    data = sock.recv(1000000000)
    print data
    data = json.loads(data)

    if data['type'] == 'noNeed':
        Timer( checkTime, checkStatus ).start()
    elif data['type'] == 'download':
        newDownload = Downloader( data['url'], data['startRange'], data['endRange'], data['partNum'] )
        newDownload.start()
        Timer( checkTime, checkStatus ).start()
    else:
        print 'error!'

def checkStatus():
    global newDownload
    print 'checkStatus called!'
    status = newDownload.status()
    print json.dumps(status)

    if status['inDownload'] == True:
        Timer( checkTime, checkStatus ).start()
    else:
        requestDownload()

def main():

    global sock

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', port)
    print 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    requestDownload()



if __name__ == "__main__":
    main()
