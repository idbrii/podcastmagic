#! /usr/bin/env python

import sys
import os
import os.path as path
import subprocess
from multiprocessing import Process

import util as u
import config as cfg

def _internal_download_trim_clean(silence=True):
    p = ''
    if silence:
        devnull = open(os.devnull, 'w')
    else:
        devnull = sys.stdout

    try:
        p = 'podget'
        subprocess.check_call([p], stderr=devnull, stdout=devnull)

        p = path.join(os.getcwd(), 'trim.py')
        p = path.normpath(p)
        subprocess.check_call([p], stdout=devnull)

    except subprocess.CalledProcessError, ex:
        printWarning('Failed to run %s (%s)' % (p, ex))
    except OSError, ex:
        printWarning('Cannot find application %s (%s)' % (p, ex))

    if silence:
        devnull.close()
    # else: don't close stdio

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
