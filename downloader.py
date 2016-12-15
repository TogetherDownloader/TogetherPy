import requests
import thread
import os
import time

chunkSize = 1024

class Downloader:

    fileName = ""
    response = {}
    totalLength = 0
    dl = 0

    def __call__(self):
        print "hi!"

    def __init__(self, _url, startRange, endRange, partNum=-1):
        headers = {'Range': "bytes=" + str(startRange) + "-" + str(endRange) }
        self.response = requests.get(_url, stream=True, headers=headers)
        self.totalLength = int(self.response.headers.get('content-length'))
        # generate name for save file
        if partNum == -1:
            self.fileName = "Downloads/" + _url.split('/')[-1]
        else:
            self.fileName = "Downloads/" + _url.split('/')[-1] + ".part" + str(partNum)

    def check(self):
        return True if (self.totalLength != 0) else False;

    def start(self):
        if self.check():
            # make directory
            if not os.path.exists("Downloads"):
                os.makedirs("Downloads")

            # run downloader thread
            try:
                # TODO: add other thread for more speed!
                thread.start_new_thread( self.startDownload, () )
            except:
               print "Error: unable to start thread"

    def startDownload(self):
        with open(self.fileName, "wb") as f:
            for data in self.response.iter_content(chunk_size=chunkSize):
                self.dl += len(data)
                f.write(data)

    def status(self):
        return {
            'size': self.totalLength,
            'dl': self.dl,
            'fileName': self.fileName
            }
