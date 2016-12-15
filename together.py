from downloader import Downloader

def main():
    a = Downloader("http://cdn.download.ir/?b=dlir-mac&f=Audirvana.Plus.2.6.1.www.download.ir.rar", 0, 1000000000)
    print a.check()
    a.start()

    tmpStatus = a.status()
    while( tmpStatus['dl'] != tmpStatus['size'] ):
        tmpStatus = a.status()
        print a.status()


if __name__ == "__main__":
    main()
