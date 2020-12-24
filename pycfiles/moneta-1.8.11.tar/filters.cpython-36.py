# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/repository/filters.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 6713 bytes
import bz2, gzip, hashlib, mimetypes, os, tarfile, zipfile
from moneta.archives import ArFile
from moneta.utils import mkdtemp
__author__ = 'flanker'
mimetypes.init()

def informations(element, open_file, filename, temp_files, uncompressed_path=None):
    size = 0
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    data = open_file.read(1024)
    while data:
        md5.update(data)
        sha1.update(data)
        sha256.update(data)
        size += len(data)
        data = open_file.read(1024)

    element.sha1 = sha1.hexdigest()
    element.sha256 = sha256.hexdigest()
    element.md5 = md5.hexdigest()
    element.filesize = size
    element.extension = os.path.splitext(filename)[1]
    element.mimetype = mimetypes.guess_type(filename, strict=False)[0]
    if element.mimetype is None:
        element.mimetype = 'application/octet-stream'
    element.filename = filename


def compressions(element, open_file, filename, temp_files, uncompressed_path=None):
    if uncompressed_path is not None:
        return
    else:
        extension = os.path.splitext(filename)[1]
        new_filename = filename[0:-len(extension)]
        result_file = None
        if extension == '.zip':
            result_file = mkdtemp()
            temp_files.add(result_file)
            obj = zipfile.ZipFile(open_file, 'r')
            members = filter(lambda x: os.path.abspath(os.path.join(result_file, x)).find(result_file) == 0, obj.namelist())
            obj.extractall(result_file, members)
            obj.close()
        else:
            if extension == '.gz':
                result_file = mkdtemp()
                temp_files.add(result_file)
                result_file = os.path.join(result_file, new_filename)
                with gzip.GzipFile(filename, 'rb', 9, open_file) as (obj):
                    with open(result_file, 'wb') as (fd):
                        data = obj.read(4096)
                        while data != '':
                            fd.write(data)
                            data = obj.read(4096)

                with open(result_file, 'rb') as (fd):
                    extra_compression = compressions(element, fd, new_filename, temp_files)
                if extra_compression is not None:
                    result_file = extra_compression
            else:
                if extension == '.bz2':
                    result_file = mkdtemp()
                    temp_files.add(result_file)
                    result_file = os.path.join(result_file, new_filename)
                    decompressor = bz2.BZ2Decompressor()
                    with open(result_file, 'wb') as (fd):
                        data = open_file.read(4096)
                        while data != '':
                            data = decompressor.decompress(data)
                            fd.write(data)
                            data = open_file.read(4096)

                    with open(result_file, 'rb') as (fd):
                        extra_compression = compressions(element, fd, new_filename, temp_files)
                    if extra_compression is not None:
                        result_file = extra_compression
                else:
                    if extension in ('.tgz', '.tbz', '.tar'):
                        result_file = mkdtemp()
                        temp_files.add(result_file)
                        obj = tarfile.TarFile(fileobj=open_file, mode='r')
                        members = filter(lambda x: x.type in (tarfile.REGTYPE, tarfile.DIRTYPE) and os.path.abspath(os.path.join(result_file, x.name)).find(result_file) == 0, obj.getmembers())
                        obj.extractall(result_file, members)
                        obj.close()
        if result_file:
            if os.path.isdir(result_file):
                if len(os.listdir(result_file)[0:2]) == 1:
                    result_file = os.path.join(result_file, os.listdir(result_file)[0])
                else:
                    tmp_dir = mkdtemp()
                    temp_files.add(tmp_dir)
                    tmp_dir = os.path.join(tmp_dir, new_filename)
                    os.makedirs(tmp_dir)
                    for name in os.listdir(result_file):
                        os.rename(os.path.join(result_file, name), os.path.join(tmp_dir, name))

                    result_file = tmp_dir
        return result_file


def deb_archive(element, open_file, filename, temp_files, uncompressed_path=None):
    """
    Uncompress files in a Debian .deb archive.
    A .deb is a .ar archive with control.tar.gz (metadata) and data.tar.gz (actual package files).
    :param element:
    :param open_file:
    :param filename:
    :param temp_files:
    :param uncompressed_path:
    :return:
    """
    if uncompressed_path is not None:
        return
    else:
        extension = os.path.splitext(filename)[1]
        if extension != '.deb':
            return
        new_filename = filename[0:-len(extension)]
        ar_file_obj = ArFile(name=new_filename, mode='r', fileobj=open_file)
        data_file_obj = ar_file_obj.extractfile('data.tar.gz') or ar_file_obj.extractfile('data.tar.gz/')
        if data_file_obj is None:
            return
        result_file = mkdtemp()
        temp_files.add(result_file)
        tar_file_obj = tarfile.open(name='data.tar.gz', fileobj=data_file_obj, mode='r:gz')
        members = filter(lambda x: x.type in (tarfile.REGTYPE, tarfile.DIRTYPE) and os.path.abspath(os.path.join(result_file, x.name)).find(result_file) == 0, tar_file_obj.getmembers())
        tar_file_obj.extractall(result_file, members)
        tar_file_obj.close()
        data_file_obj.close()
        ar_file_obj.close()
        if result_file and os.path.isdir(result_file):
            if len(os.listdir(result_file)[0:2]) == 1:
                result_file = os.path.join(result_file, os.listdir(result_file)[0])
            else:
                tmp_dir = mkdtemp()
                temp_files.add(tmp_dir)
                tmp_dir = os.path.join(tmp_dir, new_filename)
                os.makedirs(tmp_dir)
                for name in os.listdir(result_file):
                    os.rename(os.path.join(result_file, name), os.path.join(tmp_dir, name))

                result_file = tmp_dir
        return result_file


if __name__ == '__main__':
    import doctest
    doctest.testmod()