#! /bin/bash

# Given a list of files and times for each file, will trim the length off the
# beginning of the paired file.
#
# Used to retrim files after partial listens.
#

#####
# Config
ipod=/media/YITHIAN/podcasts
common=$PWD/tempfiles
in=$common/input
out=$common/out


#####
# Use mp3cut to trim the beginning off of a file.
#
# name - the name of the file, no path
# start - the start time of the file in the same format as mp3cut: [[nn:]nn:]nn
function cutFile()
{
    name=$1
    start=$2

    echo
    echo 'Moving file from ipod...'
    mv $ipod/$name $in/$name
    echo
    echo 'Cutting file...'
    mp3cut -o $out/$name -T $name -t $start $in/$name
    echo
    echo 'Moving file to ipod...'
    mv $out/$name $ipod/$name

    # remove if successful (TODO: test this)
    if [ $? -eq 0 ] ; then
        echo
        echo 'Removing old file...'
        rm $in/$name
    fi
}

#####
# What files to trim
mkdir -p $in $out 2> /dev/null

#####
# What files to trim
name=giantbombcast-081809.mp3
start=1:26:09
cutFile $name $start

name=giantbombcast-081806.mp3
start=1:26:09
cutFile $name $start



