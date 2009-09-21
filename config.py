#!/usr/bin/python
# -*- coding: utf-8 -*-

# Where your iPod is mounted
iPod = '/media/YITHIAN/'

# Where your rebuild_db script is located
rebuild_db = iPod +'/rebuild_db.py'

# folders
newCastFolder = '/home/dbriscoe/data/podcasts/New'
trimCastFolder = '/home/dbriscoe/data/podcasts/Processed'
listeningFolder = '/home/dbriscoe/data/podcasts/Listening'
iPodCastFolder = iPod +'podcasts'
freeSpaceMagic = iPod +'magic'

# trim times
startTime = {}
startTime["ALifeWellWasted"] = 0
startTime["Geekbox"] = 10
startTime["GiantBombCast"] = 22
startTime["ListenUp"] = 22
startTime["MobCast"] = 0
# TODO: figure out rebel since there is game club
startTime["RebelFM"] = 0
startTime["SearchEngine"] = 13


# manage.py
nFiles = 3
