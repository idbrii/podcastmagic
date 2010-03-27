podcastmagic is intended to be a simple and highly automatic podcast manager

Motivation  {{{

    I like to listen to a lot of podcasts. I have a second generation iPod Shuffle
that I use exclusively for podcasts. podcastmagic suits those requirements very
well.

    Previously, I used iTunes on my aging Mac, but I found it slow and
difficult to use AppleScript to automate trimming the intro songs off of
podcasts and copying to my iPod. When I bought a new PC and put ubuntu on it, I
decided that I'd develop my perfect solution. It's not perfect yet, but I'm
pretty happy.

}}}

Dependencies    {{{

    As with most great software, podcastmagic builds on the work of others. It
    calls two programs directly and runs on Python. Below are the programs, the
    containing package and version I use, and some information about them in
    Ubuntu.

    podget -- podget_0.5.8  -- http://packages.ubuntu.com/search?keywords=podget
    mp3cut -- poc-streamer_0.4.2  -- http://packages.ubuntu.com/search?keywords=poc-streamer
    python -- python_2.6.4    -- http://packages.ubuntu.com/search?keywords=python

}}}

Configuration   {{{

    First, you need to setup podget. Man podget for details. In short, run podget once to create sample config files. Edit ~/.podget/podgetrc to set dir_library to your podcast destination. Then add your rss feeds to ~/.podget/serverlist. Make sure the category for all podcasts is "New". For example:
    http://feeds.tvo.org/tvo/searchengine New SearchEngine
Now, when you run podget, it should download podcasts. podcastmagic doesn't have any special interaction with podget, it just calls it to download new podcasts.

    Next, you should copy the rebuild_db.py script onto your iPod. Copy it into the root directory.

    Edit podcastmagic's config.py file to match your local settings. Setup your iPod's name and your trim times. The name used is the same as the last name used. In my above example, the name is SearchEngine.

    Now you should be ready to give it a run.

}}}

Usage   {{{

    There are several primary scripts:
        download.py -- Checks that some folders exist and downloads the podcasts.
        manage.py   -- Runs download.py in another thread and starts working on
            the files we already have. Trims and copies the files to the iPod and
            rebuilds the database.
        trim.py     -- Removes the introduction of the podcast as specified in
            config.py. Generally, you don't run this manually.
        retrim.sh   -- Manually trim your podcasts from your iPod.

    Generally, you'll be doing two things: manage or retrim.

    Manage
    >> Downloads and copies podcasts onto your iPod.
    -- Connect your iPod.
    -- Run manage.py
        -- If you don't have any podcasts downloaded, you'll get an error and
            then the program will stall while it downloads podcasts. Currently,
            you don't get any output until the download completes.
        -- If you have processed podcasts, it moves them to Listening and
            prepends any embedded dates (for sorting). It begins copying the
            podcasts. Once the copy is complete, it rebuilds the database (using
            the rebuild_db.py on the iPod).
        -- Concurrently, it starts downloading podcasts. Once podcasts are
            downloaded, it trims from the beginning of the file the amount
            specified in config.py.
        -- podcastmagic will wait for both the download/trim and copy process
            to complete before exiting.

    Retrim
    >> Manually remove beginning of podcasts. Generally useful if you started
        listening to a podcast and lost your position. (My iPod shuffle doesn't
        keep position after a power off and it is easy to accidentally skip to the
        next podcasts.)
    -- Connect your iPod.
    -- Browse the podcasts on your iPod
    -- Determine the desired new beginning (example: I stopped listening to giantbombcast-081809.mp3 after almost an hour and a half -- at 1:26:09)
    -- Add a section to retrim.sh with the filename and desired start time.
        name=giantbombcast-081809.mp3
        start=1:26:09
        cutFile $name $start
    -- Once you've done this for all of your podcasts, run retrim.sh. It will
        copy the files locally, trim them, and copy them back.
    -- NOTE: retrim.sh will NOT rebuild your iPod database. I typically run
        this before manage.py.

}}}

# vim:set fdm=marker:
