# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\musicbutler\locators.py
# Compiled at: 2008-08-18 16:04:36
import tempfile, os

class FileSearcher(object):

    @staticmethod
    def FileSearcher(location):
        if '@' in location:
            return SshFileSearcher(location)
        elif location.startswith('\\\\'):
            return NetworkFileSearcher(location)
        else:
            return NormalFileSearcher(location)


class NormalLocator(object):
    """Doesn't do anything fancy, just hands back the filename."""
    __slots__ = '_filename'

    def __init__(self, filename):
        self._filename = filename

    def filename_for_tagging(self):
        return self._filename

    def filename(self):
        return self._filename


class NormalFileSearcher(FileSearcher):

    def __init__(self, location):
        self.location = location

    def search(self):
        for (dirname, dirs, files) in os.walk(self.location):
            for filename in files:
                if filename.lower().endswith('.mp3'):
                    yield self.make_locator(dirname + '/' + filename)

    def make_locator(self, path):
        return NormalLocator(path)


class NetworkLocator(object):

    def __init__(self, filename):
        self._filename = filename
        self._cachedfilename = None
        return

    def filename(self):
        if not self._cachedfilename:
            self._cachedfilename = self._fetch()
        return self._cachedfilename

    def filename_for_tagging(self):
        return self._filename

    def _fetch(self):
        (fd, tmpname) = tempfile.mkstemp()
        os.close(fd)
        file(tmpname, 'wb').write(file(self._filename, 'rb').read())
        return tmpname


class NetworkFileSearcher(NormalFileSearcher):

    def __init__(self, location):
        self.location = location

    def make_locator(self, path):
        return NetworkLocator(path)


class SshFileSearcher(FileSearcher):

    def __init__(self, location):
        try:
            self.userAndHost = location[0:location.index(':')]
        except ValueError:
            raise Exception('SshFileSearcher expects a ":" in the location.')

        self.location = location
        self._password = None
        return

    def _getPassword(self):
        while not self._password:
            password = raw_input('Enter the password for %s: ' % self.userAndHost)
            try:
                self.ssh(password, '')
            except Exception:
                print 'Not the correct password.'
                raise
            else:
                self._password = password

    def search(self):
        """Get a password, connect, build all the file envelopes,
        store them locally.  Yield SshLocators for each file.
        """
        self._getPassword()
        sh_program = '\n            #!/bin/bash\n\n            # Script to print the names and envelopes of all mp3s\n            # found on a system.  Used over ssh to gather tag info\n            # from a remote host.\n\n            filenames=/tmp/filenames.$$\n            halfoffile=512\n\n            # Find all mp3 files, and put their names in $filenames.\n            find music -iname \'*.mp3\' > $filenames\n\n            # Print out the number of files found.\n            cat $filenames | wc -l\n\n            # For each file,\n            cat $filenames | while read file; do\n                # Print out the name,\n                echo "$file"\n\n                # and the first and last 512 bytes.  This is where the ID3 tags\n                # hide, so we only need this part of the file.  Note that we\n                # don\'t print a newline, so we can later read exactly 1024\n                # bytes and be ready to read the next filename.\n                head -c $halfoffile "$file"\n                tail -c $halfoffile "$file"\n            done\n            '
        output_file = self.ssh(self._password, sh_program)
        for (mp3file, artist, album, title) in self.getTagInfo(output_file):
            yield SshLocator(self, mp3file)

    def ssh(self, password, command):
        """Run the command on the remote host and return the output pipe."""
        (fd, tmpname) = tempfile.mkstemp()
        os.close(fd)
        file(tmpname, 'w').write(command)
        cmd = 'cat %s | ssh %s' % (tmpname, self.userAndHost)
        print cmd
        return os.popen(cmd)

    def getTagInfo(self, f):
        """
        Format of the file f that this reads:

        <Number of mp3s in this file, eg 3 in this example>
        <mp3 #1 filename>
        <1024 bytes of mp3, no newline><mp3 #2 filename>
        <1024 bytes of mp3, no newline><mp3 #3 filename>
        <1024 bytes of mp3, no newline>

        Yields (filename, artist, album, title) tuples as it reads them.
        """
        count = int(f.readline().rstrip())
        result = []
        tmpfile = '_taginfo_.tmp'
        for i in range(count):
            filename = f.readline().rstrip()
            file(tmpfile, 'wb').write(f.read(1024))
            tags = eval(repr(EasyID3(tmpfile)))
            os.remove(tmpfile)
            yield (filename,
             tags['artist'][0], tags['album'][0], tags['title'][0])