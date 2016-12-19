import os

class Mixer:
    def MixFiles(self, inputPath, inputName, outputPath="", outputName="", partCount):

        if not self.checkFilesExist( inputPath, inputName, partCount )
            return False

        # if not set!
        outputPath = outputPath if outputPath != "" else inputPath
        outputName = outputName if outputName != "" else inputName

        with open( outputPath + '/' + outputName , "wb" ) as mainFile:
            for i in xrange(0, partCount-1):
                with open( inputPath + '/' + inputName + '.part' + srt(i) , "r") as partFile:
                    mainFile.write( partFile.read() )

        return True


    def checkFilesExist(self, inputPath, inputName, partCount)

        if not os.path.exists(inputPath):
            return False

        for i in xrange(0, partCount-1):
            if not os.path.isfile( inputPath + '/' + inputName + '.part' + srt(i) ):
                return False

        return True
