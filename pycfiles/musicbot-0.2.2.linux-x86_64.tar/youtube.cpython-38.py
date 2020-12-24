# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/commands/youtube.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 4136 bytes
import os, logging, click, acoustid, youtube_dl
from humanfriendly import format_timespan
from musicbot import helpers
from musicbot.music.file import File
from musicbot.music.fingerprint import acoustid_api_key_option
logger = logging.getLogger(__name__)

@click.group(help='Youtube tool', cls=(helpers.GroupWithHelp))
def cli():
    pass


@cli.command(help='Search a youtube link with artist and title')
@click.argument('artist')
@click.argument('title')
def search(artist, title):
    """Search a youtube link with artist and title"""
    ydl_opts = {'format':'bestaudio', 
     'skip_download':True, 
     'quiet':True, 
     'no_warnings':True}
    with youtube_dl.YoutubeDL(ydl_opts) as (ydl):
        infos = ydl.extract_info(f"ytsearch1:'{artist} {title}'", download=False)
        for entry in infos['entries']:
            print(entry['webpage_url'])


@cli.command(help='Download a youtube link with artist and title')
@click.argument('artist')
@click.argument('title')
@click.option('--path', default=None)
def download(artist, title, path):
    if not path:
        path = f"{artist} - {title}.mp3"
    ydl_opts = {'format':'bestaudio/best',  'postprocessors':[
      {'key':'FFmpegExtractAudio', 
       'preferredcodec':'mp3', 
       'preferredquality':'192'}], 
     'outtmpl':path}
    with youtube_dl.YoutubeDL(ydl_opts) as (ydl):
        ydl.extract_info(f"ytsearch1:'{artist} {title}'", download=True)


@cli.command(help='Search a youtube link with artist and title')
@click.argument('path')
@helpers.add_options(acoustid_api_key_option)
def find(path, acoustid_api_key):
    f = File(path)
    yt_path = f"{f.artist} - {f.title}.mp3"
    try:
        try:
            file_id = f.fingerprint(acoustid_api_key)
            print(f"Searching for artist {f.artist} and title {f.title}\xa0and duration {format_timespan(f.duration)}")
            ydl_opts = {'format':'bestaudio/best', 
             'quiet':True, 
             'no_warnings':True, 
             'postprocessors':[
              {'key':'FFmpegExtractAudio', 
               'preferredcodec':'mp3', 
               'preferredquality':'192'}], 
             'outtmpl':yt_path}
            with youtube_dl.YoutubeDL(ydl_opts) as (ydl):
                infos = ydl.extract_info(f"ytsearch1:'{f.artist} {f.title}'", download=True)
                url = None
                for entry in infos['entries']:
                    url = entry['webpage_url']
                    break
                else:
                    yt_ids = acoustid.match(acoustid_api_key, yt_path)
                    yt_id = None
                    for _, recording_id, _, _ in yt_ids:
                        yt_id = recording_id
                        break
                    else:
                        if file_id == yt_id:
                            print(f"Found: fingerprint {file_id} | url {url}")
                        else:
                            print(f"Not exactly found: fingerprint file: {file_id} | yt: {yt_id} | url {url}")
                            print(f"Based only on duration, maybe: {url}")

        except acoustid.WebServiceError as e:
            try:
                logger.error(e)
            finally:
                e = None
                del e

    finally:
        try:
            if yt_path:
                os.remove(yt_path)
        except FileNotFoundError:
            logger.warning(f"File not found: {yt_path}")


@cli.command(help='Fingerprint a youtube video')
@click.argument('url')
@helpers.add_options(acoustid_api_key_option)
def fingerprint(url, acoustid_api_key):
    yt_path = 'intermediate.mp3'
    ydl_opts = {'format':'bestaudio/best', 
     'quiet':True, 
     'no_warnings':True, 
     'postprocessors':[
      {'key':'FFmpegExtractAudio', 
       'preferredcodec':'mp3', 
       'preferredquality':'192'}], 
     'outtmpl':yt_path}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as (ydl):
            ydl.extract_info(url, download=True)
            yt_ids = acoustid.match(acoustid_api_key, yt_path)
            for _, recording_id, _, _ in yt_ids:
                print(recording_id)
                break

    except acoustid.WebServiceError as e:
        try:
            logger.error(e)
        finally:
            e = None
            del e