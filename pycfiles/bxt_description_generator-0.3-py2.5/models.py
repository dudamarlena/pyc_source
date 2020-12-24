# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bxt_description_generator/models.py
# Compiled at: 2009-09-28 17:22:38
import os
imageFileExtensions = [
 'jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG']
ignoreFileExtensions = [
 'mood', 'sfv', 'txt', 'nfo', 'm3u', 'ini', 'lnk', 'md5']

def deduce_name(path):
    """
        Deduce a file/directory name from a path
        """
    (head, tail) = os.path.split(path)
    return tail if tail else head


def folder_sort(x, y):
    return cmp(x.name, y.name)


class ImageFileException:
    pass


class UnknownFileException:
    pass


class Folder:
    """
        Representation of a folder

        name: folder name
        path: full path (absolute or relative) to the file from current directory
        folders: a list of Folders directly under this one
        files: a list of Files directly under this one
        numScans: number of files in this folder that are scans
        artists: list of artists
        """

    def __init__(self, path, name=None):
        self.name = name if name else deduce_name(path)
        self.path = path
        self.folders = []
        self.files = {'music': [], 'scans': [], 'unknown': []}
        self.bitrate = None
        self.artists = []
        self.extensions = []
        return

    def __str__(self):
        return self.name

    def scan(self):
        for name in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, name)):
                self.folders.append(Folder(os.path.join(self.path, name)))
            elif os.path.isfile(os.path.join(self.path, name)):
                newFile = File(os.path.join(self.path, name))
                try:
                    newFile.scan()
                    self.files['music'].append(newFile)
                except ImageFileException:
                    self.files['scans'].append(newFile)
                except UnknownFileException:
                    self.files['unknown'].append(newFile)

        for folder in self.folders:
            folder.scan()

        self.calcBitrate()
        self.calcExtensions()
        self.calcArtists()
        self.files['music'].sort(lambda x, y: cmp(x.track, y.track))
        self.folders.sort(folder_sort)

    def calcBitrate(self):
        aggregator = 0
        count = 0
        for file in self.files['music']:
            if file.bitrate:
                aggregator += file.bitrate
                count += 1

        self.bitrate = aggregator / count if aggregator != 0 else None
        return

    def calcArtists(self):
        for file in self.files['music']:
            if file.artist not in self.artists:
                self.artists.append(file.artist)

    def calcExtensions(self):
        for file in self.files['music']:
            if file.extension not in self.extensions:
                self.extensions.append(file.extension)


class File:
    """
        Representation of a file

        name: filename
        path: full path (absolute or relative) to the file from current directory
        extension: file extension
        artist:
        album:
        title:
        track:
        """

    def __init__(self, path, name=None):
        self.name = name if name else deduce_name(path)
        self.path = path
        try:
            self.extension = os.path.splitext(self.name)[1][1:]
        except IndexError:
            self.extension = None

        self.bitrate = None
        return

    def __str__(self):
        return self.name

    def scan(self):
        global ignoreFileExtensions
        global imageFileExtensions
        if self.extension in imageFileExtensions:
            raise ImageFileException
        elif self.extension in ignoreFileExtensions:
            raise UnknownFileException
        else:
            import mutagen.mp3
            try:
                tags = mutagen.File(self.path)
            except mutagen.mp3.HeaderNotFoundError:
                import sys
                sys.stderr.write('I can\'t pull information out of "%s"!\n' % self.path)

            if not tags:
                import sys
                sys.stderr.write('I don\'t know what to do with "%s"!\n' % self.path)
                raise UnknownFileException
            else:
                if isinstance(tags, mutagen.mp3.MP3):
                    self.bitrate = tags.info.bitrate / 1000
                    import mutagen.easyid3
                    tags = mutagen.easyid3.EasyID3(self.path)
                self.artist = tags['artist'][0] if 'artist' in tags else None
                self.album = tags['album'][0] if 'album' in tags else None
                self.title = tags['title'][0] if 'title' in tags else self.name.rsplit('.', 1)[0].decode('utf-8')
                self.track = tags['tracknumber'][0] if 'tracknumber' in tags else None
        return