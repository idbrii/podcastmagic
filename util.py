def printStep(msg):
    print
    print '==', msg, '=='

def printStatus(msg):
    print msg
printWarning = printStatus
printDebug = printStatus


def ensure_folders():
    ###
    # Make sure all of our folders exist
    for f in cfg.folders:
        try:
            os.makedirs(f)
        except OSError:
            # Folder probably already exists, that's good
            pass


