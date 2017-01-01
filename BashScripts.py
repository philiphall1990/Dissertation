import os
import subprocess
import glob

'''This class contains functions that execute bash scripts on behalf of the user. Specifically,
the class is responsible for downloading and compiling packages, as well as executing the Objdump program on all pbject files within a given folder.'''

class BashScripts:
    def find_and_compile(self, packages):
        for package in packages:
            subprocess.call(['sudo', 'apt-get', 'build-dep', '--assume-yes', package])
            subprocess.call(['sudo', 'apt-get', 'source', '--compile', package])

    def search(self, file):
        for infile in glob.glob(os.path.join(self.inputfolder, '*.o')):
            self.executeObjDump(self,infile)
        return 0

    def executeObjDump(self, infile):
        dirname = os.path.dirname(self.destination)
        if not (os.path.exists(dirname)):
            os.makedirs(dirname)
        destfile = dirname + "/" + os.path.basename(infile)
        if not(os.path.exists(destfile)):
            f = open('{0}.txt'.format(destfile), mode='x')
        else:
            f = open('{0}.txt'.format(destfile), mode='a')
        with f:
            subprocess.call(['objdump', '-d', '-l', '{0}'.format(infile)], stdout=f)