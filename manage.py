#!/usr/bin/python
# -*- coding: utf-8 -*-

import shutil
import sys
import os
import os.path as path
import subprocess
from multiprocessing import Process

import config as cfg

# TODO:
    # FIX listening. it's not being emptied when files are copied
    # TEST pod downloading and processing at the same time
    # copy a minimum of one of each podcast
    # TEST interrupts during copying and interpret as a skip the copy step
    ## And interaction with downloading
    # print more of what's going on
    # run download and trim
    # copy oldest files first

def printStep(msg):
    print
    print '==', msg, '=='

def printStatus(msg):
    print msg
printWarning = printStatus
printDebug = printStatus

# Wrap shutil so I can have debug output
def _shutilFunc(func, src, dst):
    printDebug( 'shutil.'+ func.func_name +'('+ src +', '+ dst +')' )
    func(src, dst)

def moveFile(src, dst):
    _shutilFunc(shutil.move, src, dst)

def copyFile(src, dst):
    _shutilFunc(shutil.copy, src, dst)

def removeFile(src):
    func = os.remove
    printDebug( 'os.remove('+ src +')' )
    func(src)


def ensure_folders():
    ###
    # Make sure all of our folders exist
    for f in cfg.folders:
        try:
            os.makedirs(f)
        except OSError:
            # Folder probably already exists, that's good
            pass


def select_and_move():
    printStep( 'Find files to copy' )

    desiredFiles = []
    
    # find files in Processed
    fileNames = os.listdir(cfg.trimCastFolder)
    # filter out files that aren't mp3s
    fileNames = [f for f in fileNames if f.endswith('.mp3')]
    
    fData = {}
    for f in fileNames:
        p = path.join(cfg.trimCastFolder, f)
        statinfo = os.stat(p)
        fData[statinfo.st_ctime] = f
    
    
    #   find oldest files
    n = cfg.maxFilesToCopy
    for k in fData.keys():
        desiredFiles.append( fData[k] )
        n -= 1
        if n is 0:
            break

    printStatus('Found %d files to copy' % len(desiredFiles))
    
    
    #   move to Listening folder
    for f in desiredFiles:
        src = path.join(cfg.trimCastFolder, f)
        dst = path.join(cfg.listeningFolder, f)
        moveFile(src, dst)


def _internal_download_trim_clean():
    p = ''
    devnull = open(os.devnull, 'w')
    try:
        p = 'podget'
        subprocess.check_call([p], stderr=devnull, stdout=devnull)
        p = path.normpath('./trim.py')
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


def copy_to_ipod():
    ###
    # Copy files from Listening folder to iPod
    printStep('Begin copy')
    
    # reserve some space
    desiredFiles = os.listdir(cfg.listeningFolder)
    printStatus( 'Making buffer space' )
    try:
        copyFile(path.join(cfg.listeningFolder, desiredFiles[0]), cfg.freeSpaceMagic)
    except IOError, ex:
        printWarning("No space on device. Cannot copy any files (%s)" % ex)
        raise ex
    except KeyboardInterrupt, ex:
        printWarning('Interrupt caught, skipping copying step')
        return      ####### Early Return
    
    for f in desiredFiles:
        printStatus( 'Copying: %s' % f )
        src = path.join(cfg.listeningFolder, f)
        dst = path.join(cfg.iPodCastFolder, f)
        try:
            # copy out of listening folder
            copyFile(src, dst)
            # if successful, then remove from listening folder
            removeFile(src)
        except IOError, ex:
            printWarning( "Warning: Out of space on device (%s)" % ex )
            # failure means it will stay in listening folder for the next iPod sync
        except KeyboardInterrupt, ex:
            printWarning('Interrupt caught, not copying any more files')
    
    # free up junk space
    printStatus( 'Clearing buffer space' )
    removeFile(cfg.freeSpaceMagic)


def rebuild_ipod():
    ###
    printStep( 'Rebuild the database' )
    p = path.normpath(cfg.rebuild_db)
    os.system(p)





def main():
    ensure_folders()
    select_and_move()
    p = download_trim_clean()
    try:
        copy_to_ipod()
        rebuild_ipod()
    except IOError:
        # When we get an io error, it's probably already been reported. We just
        # need to skip everything else except waiting for our external process
        pass
    wait_for_download(p)



def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()

