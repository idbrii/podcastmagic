#!/usr/bin/python
# -*- coding: utf-8 -*-

import shutil
import sys
import os
import os.path as path

import config as cfg
import download as dl
import util as u
import namemanip

# TODO:
    # FIX listening. it's not being emptied when files are copied
    # TEST pod downloading and processing at the same time
    # copy a minimum of one of each podcast
    # TEST interrupts during copying and interpret as a skip the copy step
    ## And interaction with downloading
    # print more of what's going on
    # run download and trim
    # copy oldest files first

# Wrap shutil so I can have debug output
def _shutilFunc(func, src, dst):
    u.printDebug( 'shutil.'+ func.func_name +'('+ src +', '+ dst +')' )
    func(src, dst)

def moveFile(src, dst):
    _shutilFunc(shutil.move, src, dst)

def copyFile(src, dst):
    _shutilFunc(shutil.copy, src, dst)

def removeFile(src):
    u.printDebug( 'os.remove('+ src +')' )
    os.remove(src)


def select_and_move():
    u.printStep( 'Find files to copy' )

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

    u.printStatus('Found %d files to copy' % len(desiredFiles))
    
    
    #   move to Listening folder
    for f in desiredFiles:
        src = path.join(cfg.trimCastFolder, f)
        dst = path.join(cfg.listeningFolder, namemanip.find_date(f)+'_'+f)
        moveFile(src, dst)


def copy_to_ipod():
    ###
    # Copy files from Listening folder to iPod
    u.printStep('Begin copy')
    
    # reserve some space
    desiredFiles = os.listdir(cfg.listeningFolder)
    u.printStatus( 'Making buffer space' )
    try:
        copyFile(path.join(cfg.listeningFolder, desiredFiles[0]), cfg.freeSpaceMagic)
    except IOError, ex:
        u.printWarning("No space on device. Cannot copy any files (%s)" % ex)
        raise ex
    except KeyboardInterrupt, ex:
        u.printWarning('Interrupt caught, skipping copying step')
        return      ####### Early Return
    
    for f in desiredFiles:
        u.printStatus( 'Copying: %s' % f )
        src = path.join(cfg.listeningFolder, f)
        dst = path.join(cfg.iPodCastFolder, f)
        try:
            # move out of listening folder to ipod
            # hopefully, the move will only occur if there's space
            moveFile(src, dst)
        except IOError, ex:
            u.printWarning( "Warning: Out of space on device (%s)" % ex )
            # failure means it will stay in listening folder for the next iPod sync
        except KeyboardInterrupt, ex:
            u.printWarning('Interrupt caught, not copying any more files')
    
    # free up junk space
    u.printStatus( 'Clearing buffer space' )
    removeFile(cfg.freeSpaceMagic)


def rebuild_ipod():
    ###
    u.printStep( 'Rebuild the database' )
    p = path.normpath(cfg.rebuild_db)
    os.system(p)





def main():
    u.ensure_folders()
    select_and_move()
    p = dl.download_trim_clean()
    try:
        copy_to_ipod()
    except IOError:
        # When we get an io error, it's probably already been reported. We just
        # need to skip everything else except waiting for our external process
        pass
    try:
        rebuild_ipod()
    except IOError:
        u.printWarning("Failed to rebuild ipod database!")

    dl.wait_for_download(p)



def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()

