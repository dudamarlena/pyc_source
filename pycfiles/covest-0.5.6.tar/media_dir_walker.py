# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/cover_grabber/os/media_dir_walker.py
# Compiled at: 2012-07-05 18:18:49
import os, urllib
from cover_grabber.handler.handler_factory import HandlerFactory
from cover_grabber.downloader.lastfm_downloader import LastFMDownloader
from cover_grabber.logging.config import logger

class MediaDirWalker(object):

    def __init__(self, path, overwrite=False):
        """ Initialize Media directory walker object"""
        self.path = path
        self.overwrite = overwrite

    def do_walk_path(self):
        """ Walk specified directory recursively.  Call self.process_dir() on each directory """
        logger.info(('Scanning {path}').format(path=self.path))
        os.path.walk(self.path, self.process_dir, None)
        return

    def process_dir(self, args, dirname, filenames):
        """ callback for each directory encourted by os.path.walk.
            If directory contains audio files, attempt to extract it's metatags, then search and download it's cover art"""
        album_name = ''
        artist_name = ''
        filehandler = None
        if filenames:
            filehandler = HandlerFactory.get_handler(dirname, filenames)
            if filehandler:
                if filehandler.audio_files:
                    album_name, artist_name = filehandler.get_album_and_artist()
                    if album_name:
                        cover_exists = self.check_cover_image_existence(dirname)
                        if cover_exists == False:
                            image_url = self.get_image_url(album_name, artist_name)
                        else:
                            logger.warning(('cover image for "{artist_name} - {album_name}" already exists, moving on to the next one').format(artist_name=artist_name, album_name=album_name))
                            image_url = None
                        if image_url:
                            logger.info(('Downloading album cover image for "{artist_name} - {album_name}"').format(artist_name=artist_name, album_name=album_name))
                            self.download_image(dirname, image_url)
        return

    def check_cover_image_existence(self, dirname):
        """ Check if cover image already exists in the specified directory """
        possible_covers = [
         'cover.png', 'cover.jpg', 'cover.gif', 'cover.tiff', 'cover.svg']
        for cover_name in possible_covers:
            if os.path.exists(os.path.join(dirname, cover_name)):
                return True

        return False

    def get_image_url(self, album_name, artist_name):
        """ Retrieve URL for cover image """
        image_url = None
        try:
            downloader = LastFMDownloader(album_name, artist_name)
            image_url = downloader.search_for_image()
        except KeyboardInterrupt as e:
            raise
        except Exception as e:
            logger.error(('SOMETHING VERY BAD HAPPENED during processing of "{artist_name} - {album_name}"').format(artist_name=artist_name, album_name=album_name))

        return image_url

    def download_image(self, dirname, image_url):
        """ Check if overwrite is enabled.  Check if album cover already exists
        Call method to download album cover art image to specified directory"""
        if '.png' in image_url.lower():
            cover_name = 'cover.png'
        elif '.jpg' in image_url.lower():
            cover_name = 'cover.jpg'
        elif '.jpeg' in image_url.lower():
            cover_name = 'cover.jpg'
        elif '.gif' in image_url.lower():
            cover_name = 'cover.gif'
        elif '.tif' in image_url.lower():
            cover_name = 'cover.tiff'
        elif '.tiff' in image_url.lower():
            cover_name = 'cover.tiff'
        elif '.svg' in image_url.lower():
            cover_name = 'cover.svg'
        else:
            return
        if os.path.exists(os.path.join(dirname, cover_name)):
            if self.overwrite:
                self.do_download(dirname, image_url, cover_name)
            else:
                logger.warning(('Cover ({covername}) already exists in {dir_name}').format(covername=cover_name, dir_name=dirname))
        else:
            self.do_download(dirname, image_url, cover_name)

    def do_download(self, dirname, image_url, cover_name):
        """ Download album cover art and save as cover.(png|jpg|gif|tiff|svg)"""
        image_data = urllib.urlopen(image_url).read()
        f = open(os.path.join(dirname, cover_name), 'w')
        f.write(image_data)
        f.close()