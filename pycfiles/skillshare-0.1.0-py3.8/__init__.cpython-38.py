# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skillshare/__init__.py
# Compiled at: 2020-05-10 11:43:43
# Size of source mod 2**32: 2559 bytes
__version__ = '0.1.0'
__title__ = 'skillshare'
__author__ = 'Technofab'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020 Technofab'
import logging, os, aiohttp, aiofiles, aiofiles.os
log = logging.getLogger(__name__)

async def download(url: str, destination: str):
    """
    Downloads all lessons from the given `url` into a folder at `destination`
    named after the course name

    Parameters
    ----------
    url: :class:`str`
        The URL of the Skillshare course
    destination: :class:`str`
        The path where the folder will be created and the lessons will be downloaded
    """
    data = parse_url(url)
    if not data:
        raise RuntimeError('URL is in the wrong format!')
    c_id, c_name = data
    endpoint = 'https://skillshare-flask.herokuapp.com/get_videos_list/' + c_id
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as resp:
            if resp.status == 200:
                videos = await resp.json()
                videos = videos['video_list']
                destination = os.path.abspath(destination) + '/' + c_name + '/'
                await aiofiles.os.mkdir(destination)
                for video in videos:
                    await download_video(video, destination)


def parse_url(url: str):
    """
    Gets the course id and name from the URL or returns `False` if the URL is not valid

    Parameters
    ----------
    url: :class:`str`
        The URL to parse
    """
    chunks = url.split('/')
    if chunks[2] == 'www.skillshare.com':
        if chunks[3] == 'classes':
            course_id = chunks[5].split('?')[0]
            course_name = chunks[4].replace('-', ' ')
            log.debug('URL parsed: ID={0} Name={1}'.format(course_id, course_name))
            return (
             course_id, course_name)
    return False


async def download_video(video, destination):
    """
    Downloads the video to the destination

    Parameters
    ----------
    video: :class:`dict`
        The video dict coming from `skillshare-flask.herokuapp.com`
    destination: :class:`str`
        The folder to download the file to
    """
    url = video['video_url']
    filename = video['file_name'] + '.' + video['type']
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open((destination + filename), mode='wb+')
                await f.write(await resp.read())
                await f.close()
                log.debug('Downloaded ' + filename)