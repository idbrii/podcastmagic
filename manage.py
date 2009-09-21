import shutil
import os
import os.path as path

import config as cfg

# TODO:
    # copy a minimum of one of each podcast
    # catch interrupts during copying and interpret as a skip the copy step
    # print more of what's going on
    # run download and trim


def require_folders():
    ###
    # Make sure all of our folders exist
    for f in (cfg.newCastFolder, cfg.trimCastFolder, cfg.listeningFolder, cfg.iPodCastFolder):
        try:
            os.makedirs(f)
        except OSError:
            # Folder probably already exists, that's good
            pass


def select_and_move():
    ####
    # Find the files we want to copy
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
    n = cfg.nFiles
    for k in fData.keys():
        desiredFiles.append( fData[k] )
        n -= 1
        if n is 0:
            break
    
    
    #   move to Listening folder
    for f in desiredFiles:
        src = path.join(cfg.trimCastFolder, f)
        dst = path.join(cfg.listeningFolder, f)
        shutil.move(src, dst)
    
    return src, dst


def download_trim_clean():
    ###
    # Start download, trim, and cleanup in new thread
    #p = path.normpath('./trim.py')
    #os.system(p)
    pass


def copy_to_ipod():
    ###
    # Copy files from Listening folder to iPod
    
    # reserve some space
    desiredFiles = os.listdir(cfg.listeningFolder)
    print 'Making buffer space'
    shutil.copy(path.join(cfg.listeningFolder, desiredFiles[0]), cfg.freeSpaceMagic)
    
    lastFile = None
    for f in desiredFiles:
        print 'Copying:', f
        src = path.join(cfg.listeningFolder, f)
        dst = path.join(cfg.iPodCastFolder, f)
        try:
            shutil.copy(src, dst)
            lastFile = dst
        except IOError, ex:
            print "Warning: Out of space on device (%s)" % ex
    
    # free up junk space
    print 'Clearing buffer space'
    os.remove(cfg.freeSpaceMagic)


def rebuild_ipod():
    ###
    print 'Rebuild the database'
    p = path.normpath(cfg.rebuild_db)
    os.system(p)


#require_folders()
#src, dst = select_and_move()
#download_trim_clean()
copy_to_ipod()
rebuild_ipod()
