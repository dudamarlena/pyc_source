# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raildecom/workspace/webitup/roxee/puke/puke/Compress.py
# Compiled at: 2012-01-03 06:16:01
import tarfile, zipfile, datetime, time

class Compress:

    @staticmethod
    def open(file, mode):
        ext = file.split('.')[(-1)]
        if ext == 'zip':
            i = CompressZip()
        elif ext == 'bz2':
            mode += ':bz2'
            i = CompressTar()
        else:
            mode += ':gz'
            i = CompressTar()
        i.open(file, mode)
        return i

    @staticmethod
    def check(file):
        if CompressTar.check(file):
            return True
        if CompressZip.check(file):
            return True
        return False


class CompressInterface:

    def __init__(self):
        """Init"""
        raise NotImplemented()

    def open(self, file, mode):
        """init compress instance"""
        raise NotImplemented()

    def add(self, file):
        """ add file"""
        raise NotImplemented()

    def close(self):
        """close it"""
        raise NotImplemented()

    @staticmethod
    def check(file):
        """validate pack format"""
        raise NotImplemented()

    def extract(self, file):
        """uncompress file"""
        raise NotImplemented()

    def __iter__(self):
        raise NotImplemented()


class CompressInfo:
    mode = 0
    mtime = 0


class CompressTar(CompressInterface):

    def __init__(self):
        self.__instance = None
        return

    def open(self, file, mode):
        self.__instance = tarfile.open(file, mode)

    def add(self, file):
        self.__instance.add(file)

    @staticmethod
    def check(file):
        return tarfile.is_tarfile(file)

    def extract(self, file):
        res = self.__instance.extractfile(file)
        if not res:
            return (None, None)
        else:
            infos = CompressInfo()
            tarinfo = self.__instance.getmember(file)
            infos.mode = int('%o' % tarinfo.mode)
            infos.mtime = tarinfo.mtime
            return (
             res.read(), infos)

    def __iter__(self):
        return iter(self.__instance.getnames())

    def close(self):
        self.__instance.close()


class CompressZip(CompressInterface):

    def __init__(self):
        self.__instance = None
        return

    def open(self, file, mode):
        self.__instance = zipfile.ZipFile(file, mode)

    def add(self, file):
        self.__instance.write(file)

    @staticmethod
    def check(file):
        return zipfile.is_zipfile(file)

    def extract(self, file):
        infos = CompressInfo()
        infos.mode = int('%o' % (self.__instance.getinfo(file).external_attr >> 16 & 511))
        infos.mtime = time.mktime(datetime.datetime(*self.__instance.getinfo(file).date_time[0:6]).timetuple())
        return (self.__instance.read(file), infos)

    def __iter__(self):
        for item in self.__instance.namelist():
            if item.endswith('/'):
                continue
            yield item

    def close(self):
        self.__instance.close()