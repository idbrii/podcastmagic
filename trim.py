#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import os.path as path
import shutil

import config as cfg


# TODO:
    # deal with files after copying. move, delete?
    # display more progress

def require_mp3cut():
    """
    Aborts if mp3cut isn't installed
    """
    # pipe to null so user can't see output
    installed = os.system("which mp3cut > /dev/null") == 0
    if not installed:
        print "Error: mp3cut is not installed."
        print "\t We use mp3cut to trim files and this program is useless without it."
        print "\t Install with:\n\t sudo apt-get install mp3cut"
        sys.exit(-1)


def mp3cut(infile, min, sec, outfile, title, artist):
    """
    mp3cut_command(str, int, int, str, str, str) --> None
    Run mp3cut on the specified files

    outfile - the file to output to
    infile  - the source file
    min,sec - where to start the song
    title,artist    - id3 tag data
    """
    command = "mp3cut -o '%s' -T '%s' -A '%s' -t %d:%d '%s'" % (outfile, title, artist, min, sec, infile)
    print command
    os.system(command)


def seconds_to_min_sec(seconds):
    """
    seconds_to_min_sec(int) --> int,int
    Converts seconds to minutes and seconds

    >>> seconds_to_min_sec(5)
    (0, 5)
    >>> seconds_to_min_sec(60)
    (1, 0)
    >>> seconds_to_min_sec(125)
    (2, 5)
    """
    sec = seconds % 60
    min = seconds / 60
    return min,sec
    

def get_start_time(podcast):
    """
    get_start_time(path) --> int,int
    Returns the minutes and seconds for the current podcast path
    """
    try:
        min, sec = seconds_to_min_sec(cfg.startTime[podcast])
    except KeyError:
        print "Warning: No start time set for", podcast
        min,sec = 0,0

    return min,sec


def cut_and_replace_files(paths, min, sec):
    for f in paths.fileNames:
        sourceFilePath = path.join(paths.source, f)
        targetFilePath = path.join(paths.target, f)
        #print 'source:', sourceFilePath
        #print 'target:', targetFilePath
        title = f
        artist = paths.podcast

        #os.makedirs( cfg.trimCastFolder )

        # skip no-ops
        if min + sec > 0:
            mp3cut(
                path.abspath(sourceFilePath)
                , min, sec
                , path.abspath(targetFilePath)
                , title, artist
            )
        else:
            os.link(
                path.abspath(sourceFilePath)
                , path.abspath(targetFilePath)
            )

#        shutil.move(
#            path.abspath(sourceFilePath)
#            , 'Trash/.'
#        )


class Paths():
    """ Struct for several path elements."""

    'The location of the files to be processed'
    source = ''
    'The destination for the processed files'
    target = ''
    'The short name of the podcast'
    podcast = ''
    'The files (no path) to be processed.'
    fileNames = []


def main():
    # abort if we have to
    require_mp3cut()

    # create a path walker
    walker = os.walk(cfg.newCastFolder)
    # discard podcast-free parent directory
    walker.next()

    # cut stuff up
    p = Paths()
    for podPath, dn, fileNames in walker:
        p.source = podPath
        p.target = cfg.trimCastFolder
        p.podcast = path.basename(podPath)
        p.fileNames = fileNames

        print p.podcast
        min,sec = get_start_time(p.podcast)
        cut_and_replace_files(p, min, sec)
        print



def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    #_test()
    main()

