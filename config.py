#!/usr/bin/python
# -*- coding: utf-8 -*-

sourceFolder = '/home/dbriscoe/data/podcasts/New/'
targetFolder = '/home/dbriscoe/data/podcasts/Processed'

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
nFiles = 2
