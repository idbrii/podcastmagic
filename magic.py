#!/usr/bin/python
# -*- coding: utf-8 -*-

import shutil
import sys
import os
import os.path as path

import config as cfg

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
    sec = seconds%60
    min = seconds / 60
    return min,sec
    

def get_start_time(podPath):
    """
    get_start_time(path) --> int,int
    Returns the minutes and seconds for the current podcast path
    """
    try:
        min, sec = seconds_to_min_sec(cfg.startTime[podPath])
    except KeyError:
        print "Warning: No start time set for", podPath
        min,sec = 0,0

    return min,sec


def replace_file(orig, new):
    shutil.move(new, orig)

def cut_and_replace_files(fileNames, podPath, min, sec):
    for f in fileNames:
        sourceFilePath = path.join(podPath, f)
        targetFilePath = path.join(os.getcwd(), f)
        title = f
        artist = path.basename(podPath)

        # skip no-ops
        if min + sec > 0:
            mp3cut(path.abspath(sourceFilePath), min, sec, path.abspath(targetFilePath), title, artist)
            replace_file(sourceFilePath, targetFilePath)


def main():
    # abort if we have to
    require_mp3cut()

    # create a path walker
    walker = os.walk("Podcasts")
    # discard podcast-free parent directory
    walker.next()

    # cut stuff up
    for podPath, dn, fileNames in walker:
        print podPath
        min,sec = get_start_time(podPath)
        cut_and_replace_files(fileNames, podPath, min, sec)
        print



def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    #_test()
    main()


