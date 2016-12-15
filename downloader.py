import requests
import os

class Downloader:

    fileName = ""
    response = {}
    totalLength = 0
    dl = 0
    chunkSize = 1024

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
            # start download
            with open(self.fileName, "wb") as f:
                for data in self.response.iter_content(chunk_size=self.chunkSize):
                    self.dl += len(data)
                    f.write(data)

    def status(self):
        return bool(self.dl/self.totalLength)
