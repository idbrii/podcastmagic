import os
import subprocess
from multiprocessing import Process

def _internal_download_trim_clean():
    p = ''
    devnull = open(os.devnull, 'w')
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
    devnull.close()

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
    dl.wait_for_download(dl.download_trim_clean())




def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()
