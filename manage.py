import shutil
import os
import os.path as path

import config as cfg

# find the files we want to copy
desiredFiles = []

#   find files in Processed
fileNames = os.listdir(cfg.targetFolder)
# filter out files that aren't mp3s
fileNames = [f for f in fileNames if f.endswith('.mp3')]

fData = {}
for f in fileNames:
    p = path.join(cfg.targetFolder, f)
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
    print f

# start download and trim in new thread
#os.system()


# copy files from Listening  folder to iPod
#shutil.copy(cfg.sourceFolder)


# rebuild the database
#os.system()
