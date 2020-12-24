# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/factory.py
# Compiled at: 2011-01-23 19:08:22
__all__ = [
 'Factory', 'register', 'gettype', 'parse']
import stat, os, sys, struct, urlparse, urllib, logging, kaa.utils, core
log = logging.getLogger('metadata')
_factory = None
TIME_DEBUG = False
R_MIMETYPE = 0
R_EXTENSION = 1
R_CLASS = 2

def register(mimetype, extensions, c, magic=None):
    """
    Register a parser to the factory.
    """
    return Factory().register(mimetype, extensions, c, magic)


def gettype(mimetype, extensions):
    """
    Return parser for mimetype / extensions
    """
    return Factory().get(mimetype, extensions)


def parse(filename, force=True):
    """
    parse a file
    """
    result = Factory().create(filename, force)
    if result:
        result._finalize()
    return result


class NullParser(object):

    def __init__(self, file):
        raise core.ParseError


class File(file):

    def read(self, bytes=-1):
        """
        If the size argument is negative or omitted, read until EOF is
        reached. If more than 5MB is requested, an IOError is
        raised. This should not mappen for kaa.metadata parsers.
        """
        if bytes > 5000000 or bytes < 0 and os.stat(self.name)[stat.ST_SIZE] - self.tell() > 1000000:
            raise IOError('trying to read %s bytes' % bytes)
        return super(File, self).read(bytes)


class _Factory():
    """
    Abstract Factory for the creation of Media instances. The different
    Methods create Media objects by parsing the given medium.
    """

    def __init__(self):
        self.extmap = {}
        self.mimemap = {}
        self.classmap = {}
        self.magicmap = {}
        self.types = []
        self.device_types = []
        self.directory_types = []
        self.stream_types = []

    def get_class(self, name):
        if name not in self.classmap:
            try:
                exec 'from %s import Parser' % name
                self.classmap[name] = Parser
            except Exception:
                log.exception('Error importing parser %s' % name)
                self.classmap[name] = NullParser

        return self.classmap[name]

    def get_scheme_from_info(self, info):
        if info.__class__.__name__ == 'DVDInfo':
            return 'dvd'
        else:
            return 'file'

    def create_from_file(self, file, force=True):
        """
        create based on the file stream 'file
        """
        e = os.path.splitext(file.name)[1].lower()
        parser = None
        if e and e.startswith('.') and e[1:] in self.extmap:
            log.debug('trying ext %s on file %s', e[1:], file.name)
            parsers = self.extmap[e[1:]]
            for info in parsers:
                file.seek(0, 0)
                try:
                    parser = self.get_class(info[R_CLASS])
                    return parser(file)
                except core.ParseError:
                    pass
                except Exception:
                    log.exception('parse error')

        file.seek(0, 0)
        magic = file.read(10)
        for length, magicmap in self.magicmap.items():
            if magic[:length] in magicmap:
                for p in magicmap[magic[:length]]:
                    log.info('Trying %s by magic header', p[R_CLASS])
                    file.seek(0, 0)
                    try:
                        parser = self.get_class(p[R_CLASS])
                        return parser(file)
                    except core.ParseError:
                        pass
                    except Exception:
                        log.exception('parse error')

                log.info('Magic header found but parser failed')
                return

        if not force:
            log.info('No Type found by Extension (%s). Giving up.' % e)
            return
        else:
            log.info('No Type found by Extension (%s). Trying all parsers.' % e)
            for e in self.types:
                if self.get_class(e[R_CLASS]) == parser:
                    continue
                log.debug('trying %s' % e[R_MIMETYPE])
                file.seek(0, 0)
                try:
                    return self.get_class(e[R_CLASS])(file)
                except core.ParseError:
                    pass
                except Exception:
                    log.exception('parser error')

            return

    def create_from_url(self, url, force=True):
        """
        Create information for urls. This includes file:// and cd://
        """
        split = urlparse.urlsplit(url)
        scheme = split[0]
        if scheme == 'file':
            scheme, location, path, query, fragment = split
            return self.create_from_filename(location + path, force)
        if scheme == 'cdda':
            r = self.create_from_filename(split[4], force)
            if r:
                r._set_url(url)
            return r
        if scheme == 'http' and False:
            for e in self.stream_types:
                log.debug('Trying %s' % e[R_MIMETYPE])
                try:
                    return self.get_class(e[R_CLASS])(url)
                except core.ParseError:
                    pass

        else:
            if scheme == 'dvd':
                path = split[2]
                if not path.replace('/', ''):
                    return self.create_from_device('/dev/dvd')
                return self.create_from_filename(split[2])
            scheme, location, path, query, fragment = split
            try:
                uhandle = urllib.urlopen(url)
            except IOError:
                return

        mime = uhandle.info().gettype()
        log.debug('Trying %s' % mime)
        if self.mimemap.has_key(mime):
            try:
                return self.get_class(self.mimemap[mime][R_CLASS])(file)
            except core.ParseError:
                pass

    def create_from_filename(self, filename, force=True):
        """
        Create information for the given filename
        """
        if os.path.isdir(filename):
            return
        else:
            if os.path.isfile(filename):
                try:
                    f = File(filename, 'rb')
                except (IOError, OSError) as e:
                    log.info('error reading %s: %s' % (filename, e))
                    return

                result = self.create_from_file(f, force)
                qwsize = struct.calcsize('q')
                filehash = filesize = os.path.getsize(filename)
                for fpos in (0, max(0, filesize - 65536)):
                    f.seek(fpos)
                    buf = f.read(65536)
                    for qw in struct.unpack('%dq' % (len(buf) / qwsize), buf[:len(buf) & -8]):
                        filehash = filehash + qw & 18446744073709551615

                filehash = '%016x' % filehash
                f.close()
                if result:
                    result._set_url('%s://%s' % (self.get_scheme_from_info(result), os.path.abspath(filename)))
                    result.hash = filehash
                    return result
            return

    def create_from_device(self, devicename):
        """
        Create information from the device. Currently only rom drives
        are supported.
        """
        for e in self.device_types:
            log.debug('Trying %s' % e[R_MIMETYPE])
            try:
                t = self.get_class(e[R_CLASS])(devicename)
                t._set_url('%s://%s' % (self.get_scheme_from_info(t), os.path.abspath(devicename)))
                return t
            except core.ParseError:
                pass

        return

    def create_from_directory(self, dirname):
        """
        Create information from the directory.
        """
        for e in self.directory_types:
            log.debug('Trying %s' % e[R_MIMETYPE])
            try:
                return self.get_class(e[R_CLASS])(dirname)
            except core.ParseError:
                pass

        return

    def create(self, name, force=True):
        """
        Global 'create' function. This function calls the different
        'create_from_'-functions.
        """
        try:
            if name.find('://') > 0:
                return self.create_from_url(name)
            else:
                if not os.path.exists(name):
                    return
                if os.uname()[0] == 'FreeBSD' and stat.S_ISCHR(os.stat(name)[stat.ST_MODE]) or stat.S_ISBLK(os.stat(name)[stat.ST_MODE]):
                    return self.create_from_device(name)
                if os.path.isdir(name):
                    return self.create_from_directory(name)
                return self.create_from_filename(name, force)

        except Exception:
            log.exception('kaa.metadata.create error')
            log.warning('Please report this bug to the Freevo mailing list')
            return

        return

    def register(self, mimetype, extensions, c, magic=None):
        """
        register the parser to kaa.metadata
        """
        log.debug('%s registered' % mimetype)
        tuple = (mimetype, extensions, c)
        if extensions == core.EXTENSION_DEVICE:
            self.device_types.append(tuple)
        elif extensions == core.EXTENSION_DIRECTORY:
            self.directory_types.append(tuple)
        elif extensions == core.EXTENSION_STREAM:
            self.stream_types.append(tuple)
        else:
            self.types.append(tuple)
            for e in (x.lower() for x in extensions):
                if e not in self.extmap:
                    self.extmap[e] = []
                self.extmap[e].append(tuple)

            self.mimemap[mimetype] = tuple
        if magic is not None:
            if len(magic) not in self.magicmap:
                self.magicmap[len(magic)] = {}
            if magic not in self.magicmap[len(magic)]:
                self.magicmap[len(magic)][magic] = []
            self.magicmap[len(magic)][magic].append(tuple)
        return

    def get(self, mimetype, extensions):
        """
        return the object for mimetype/extensions or None
        """
        if extensions == core.EXTENSION_DEVICE:
            l = self.device_types
        else:
            if extensions == core.EXTENSION_DIRECTORY:
                l = self.directory_types
            elif extensions == core.EXTENSION_STREAM:
                l = self.stream_types
            else:
                l = self.types
            for info in l:
                if info[R_MIMETYPE] == mimetype and info[R_EXTENSION] == extensions:
                    return self.get_class(info[R_CLASS])

        return


Factory = kaa.utils.Singleton(_Factory)