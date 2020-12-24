# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/bandcampscrape/bandcampscrape.py
# Compiled at: 2014-11-23 15:40:22
import demjson, requests, sys, os, argparse
from clint.textui import colored, puts, progress
from mutagen.mp3 import EasyMP3

def get_album_metadata(url):
    request = requests.get(url)
    sloppy_json = request.text.split('var TralbumData = ')
    sloppy_json = sloppy_json[1].replace('" + "', '')
    sloppy_json = sloppy_json.replace("'", "'")
    sloppy_json = sloppy_json.split('};')[0] + '};'
    sloppy_json = sloppy_json.replace('};', '}')
    return demjson.decode(sloppy_json)


def download_file(url, path):
    r = requests.get(url, stream=url)
    with open(path, 'wb') as (f):
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=total_length / 1024 + 1):
            if chunk:
                f.write(chunk)
                f.flush()

    return path


def tag_file(filename, artist, title):
    try:
        song = EasyMP3(filename)
        song['artist'] = artist
        song['title'] = title
        song.save()
    except Exception as e:
        print e


def download_tracks(album_data):
    artist = album_data['artist'].replace(' ', '_')
    album_name = album_data['current']['title'].replace(' ', '_')
    directory = artist + ' - ' + album_name
    directory = directory.replace('/', ' - ')
    if not os.path.exists(directory):
        os.makedirs(directory)
    for track in album_data['trackinfo']:
        print colored.cyan('Downloading %s by %s.' % (track['title'], artist))
        track_name = track['title'].replace(' ', '_')
        track_number = str(track['track_num']).zfill(2)
        track_filename = '%s_%s.mp3' % (track_number, track_name)
        path = directory + '/' + track_filename
        download_file(track['file']['mp3-128'], path)
        tag_file(path, artist, track['title'])


def main():
    parser = argparse.ArgumentParser(description='BcampScrape. Scrape and download an artist album from BandCamp.\n')
    parser.add_argument('album_url', metavar='U', type=str, help='A BandCamp band album url')
    args = parser.parse_args()
    vargs = vars(args)
    if not any(vargs.values()):
        parser.error('Please supply a band albums url.')
    album_data = get_album_metadata(vargs['album_url'])
    download_tracks(album_data)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print e