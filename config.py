#!/usr/bin/python
# -*- coding: utf-8 -*-

# trim times (in seconds)
startTime = {}
startTime["ALifeWellWasted"] = 0
startTime["Geekbox"] = 10
startTime["GiantBombCast"] = 22
startTime["ListenUp"] = 35
startTime["MobCast"] = 50
# both rebel and game club have long intros
startTime["RebelFM"] = 29
# TODO: figure out SearchEngine. it's outputting bad files. I used to cut at 13
startTime["SearchEngine"] = 0

# manage.py
maxFilesToCopy = 10

# Where your iPod is mounted
iPod = '/media/YITHIAN/'





# Where your rebuild_db script is located
rebuild_db = iPod +'/rebuild_db.py'

# folders
trashFolder = '/home/dbriscoe/data/podcasts/Trash'
newCastFolder = '/home/dbriscoe/data/podcasts/New'
trimCastFolder = '/home/dbriscoe/data/podcasts/Processed'
listeningFolder = '/home/dbriscoe/data/podcasts/Listening'
folders = [ trashFolder, newCastFolder, trimCastFolder, listeningFolder ]
iPodCastFolder = iPod +'podcasts'
freeSpaceMagic = iPod +'magic'
