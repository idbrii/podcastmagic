#! /usr/bin/env python

import sys
import os
import os.path as path
import subprocess
from multiprocessing import Process

import util as u
import config as cfg

class IoWrapper(object):
    """
    This class represents 
    """

    def __init__(self, io):
        """
        Constructor.
        
        io -- A file io object
        """
        assert io != None
        self._io = io
    
    def obj(self):
        """
        obj() --> file io object
        """
        return self._io
        
    def close(self):
        """
        close() --> None
        Closes the io object, if applicable
        """
        self._io.close()
        

class StdOutWrapper(IoWrapper):
    def __init__(self):
        IoWrapper.__init__(self, sys.stdout)
    def close(self):
        """ We don't close stdout """
        pass
class DevNullWrapper(IoWrapper):
    def __init__(self):
        IoWrapper.__init__(self, open(os.devnull, 'w'))


def _internal_download_trim_clean(silence=True):
    p = ''

    if silence:
        # We don't want to see output from our subprocess
        output = DevNullWrapper()
    else:
        output = StdOutWrapper()

    try:
        p = 'podget'
        subprocess.check_call([p], stderr=output.obj(), stdout=output.obj())

        p = path.join(os.getcwd(), 'trim.py')
        p = path.normpath(p)
        subprocess.check_call([p], stdout=output.obj())

    except subprocess.CalledProcessError, ex:
        printWarning('Failed to run %s (%s)' % (p, ex))
    except OSError, ex:
        printWarning('Cannot find application %s (%s)' % (p, ex))

    output.close()

def download_trim_clean():
    ###
    #printStep('Start download, trim, and cleanup in new thread')

    p = Process(target=_internal_download_trim_clean, args=())
    p.start()
    return p



def wait_for_download(p):
    # TODO: consider turning output back on (how?)
    print
    print
    print 'Waiting for download to complete...'
    print
    p.join()


def main():
    u.printStep('Initializing')
    u.ensure_folders()
    u.printStep('Beginning download')
    _internal_download_trim_clean(False)
    u.printStep('Done')




def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()
