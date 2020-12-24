# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/workspace_py/jankflix-python/jankflixmodules/cli/cli.py
# Compiled at: 2013-01-14 02:15:10
from jankflixmodules.site.linksite.onechannel import OneChannel
from jankflixmodules.utils import downloadmanager
from jankflixmodules.site.hostsite import hostsitepicker
import argparse, atexit, os, subprocess, time

def main():
    parser = argparse.ArgumentParser(description='Jankflix - A jankier way to watch things!')
    parser.add_argument('query', type=str, help='A show you want to watch', nargs='?')
    parser.add_argument('-s', dest='season', type=int, help='season to watch')
    parser.add_argument('-e', dest='episode', type=int, help='episode to watch')
    parser.add_argument('-c', dest='command', type=str, help='command to run when the video starts downloading')
    args = parser.parse_args()
    query = args.query
    season = args.season
    episode = args.episode
    command = args.command
    while True:
        if not query:
            query = raw_input('What show do you want to watch: ')
        searchResult = OneChannel.searchSite(query)
        if len(searchResult) == 0:
            print 'Search did not return any results.'
            query = None
        else:
            break

    for i in range(len(searchResult)):
        title, link = searchResult[i]
        print '%i : %s    (%s)' % (i, title, link)

    if len(searchResult) > 1:
        selnum = getIntInput('Which one do you want to watch: ', 0, len(searchResult) - 1)
    else:
        print 'Automatically choosing %s' % searchResult[0][0]
        selnum = 0
    title, link = searchResult[selnum]
    print 'Accessing show page'
    oc = OneChannel(link)
    seasons = oc.getSeasons()
    if season and season not in seasons:
        print 'Season does not exist. Please choose another.'
        season = None
    if not season:
        print 'Seasons: ', str(seasons)[1:-1]
        season = getIntInput('Which season do you want to watch: ', int(min(seasons)), int(max(seasons)))
    print 'Selecting season %d' % season
    episodes = oc.getEpisodes(season)
    names = oc.getEpisodeNames(season)
    if episode and episode not in episodes:
        print 'Episode does not exist. Please choose another.'
        episode = None
    if not episode:
        for i in range(len(episodes)):
            print episodes[i], ':', names[i]

        episode = getIntInput('Which episode do you want to watch: ', int(min(episodes)), int(max(episodes)))
    print 'Selecting episode %d' % episode
    if not command:
        saveOrRun = getIntInput('Do you want to (0) save or (1) run the episode: ', 0, 1)
        if saveOrRun == 1:
            command = raw_input('Run with which program? (vlc): ')
            if command == '':
                command = 'vlc'
    print 'Getting host site'
    hostSite = hostsitepicker.pickFromLinkSite(oc, season, episode)
    metadata = hostSite.getMetadata()
    videoURL = hostSite.getVideo()
    filename = '%sS%sE%s.%s' % (query, str(season).zfill(2), str(episode).zfill(2), metadata['extension'])
    if command:
        processs, status = downloadmanager.startDownloads([(videoURL, filename)])
        atexit.register(onexit, proc=processs[0], rmFile=filename)
        for i in range(30):
            if os.path.isfile(filename) and os.stat(filename).st_size > 1000:
                break
            else:
                time.sleep(0.2)

        subprocess.call([command, filename])
        processs[0].terminate()
    else:
        processs, status = downloadmanager.startDownloads([(videoURL, filename)])
        atexit.register(onexit, proc=processs[0])
        while processs[0].is_alive:
            print status[0].get(True)

    return


def getIntInput(query, minimum, maximum):
    while True:
        sel = raw_input(query)
        if sel.isdigit():
            selnum = int(sel)
            if selnum >= minimum and selnum <= maximum:
                return selnum
        print 'Invalid selection'


def onexit(proc, rmFile=None):
    proc.terminate()
    if rmFile:
        os.remove(rmFile)


if __name__ == '__main__':
    main()