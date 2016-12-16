from downloader import Downloader
import socket
import sys
import json

port = 2222

def main():
    # a = Downloader("http://cdn.download.ir/?b=dlir-mac&f=Audirvana.Plus.2.6.1.www.download.ir.rar", 0, 1000000000)
    # print a.check()
    # a.start()

    # tmpStatus = a.status()
    # while( tmpStatus['dl'] != tmpStatus['size'] ):
    #     tmpStatus = a.status()
    #     print a.status()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', port)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    try:

        while True:
            # Send data
            message = json.dumps({
                'request': 'imReady'
            })

            print 'sending "%s"' % message
            sock.sendall(message)

            data = sock.recv(1000000000)
            print data
            data = json.loads(data)

            if data['type'] == 'noNeed':
                break

    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()




if __name__ == "__main__":
    main()
