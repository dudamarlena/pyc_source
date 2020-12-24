# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/utils/decompress.py
# Compiled at: 2016-06-05 22:18:17
import os, shutil, zipfile, tarfile, ConfigParser, rarfile, magic

class Decompress:
    """Decompress zip, rar and tar.gz

    filename: filename without path
    filetype: file type display in MIME type.
    filepath: filename with path

    """
    filename = None
    filetype = None
    filepath = None

    def __init__(self, filename):
        """
        :param filename: a file name without path.
        """
        config = ConfigParser.ConfigParser()
        config.read('config')
        self.upload_directory = config.get('cobra', 'upload_directory') + os.sep
        self.filename = filename
        self.filepath = self.upload_directory + filename
        self.filetype = magic.from_file(self.filepath, mime=True)
        self.dir_name = os.path.splitext(self.filename)[0]

    def decompress(self):
        """
        Decompress a file.
        :return: a dict.
            code: -1 -> error, 1-> success
            msg: None or error message
            dir_name: decompressed directory name. Usually, the directory name is the filename without file extension.
        """
        if self.filetype == 'application/zip':
            return self.__decompress_zip()
        else:
            if self.filetype == 'application/x-rar':
                return self.__decompress_rar()
            if self.filetype == 'application/x-gzip':
                return self.__decompress_tar_gz()
            return {'code': -1, 'msg': 'File type error, only zip, rar, tar.gz accepted.'}

    def get_file_type(self):
        return self.filetype

    def __decompress_zip(self):
        """unzip a file."""
        zip_file = zipfile.ZipFile(self.filepath)
        self.__check_filename_dir()
        os.mkdir(self.upload_directory + self.dir_name)
        zip_file.extractall(self.upload_directory + self.dir_name)
        zip_file.close()
        return {'code': 1, 'msg': 'Success', 'dir_name': self.dir_name}

    def __decompress_rar(self):
        """extract a rar file."""
        rar_file = rarfile.RarFile(self.filepath)
        self.__check_filename_dir()
        os.mkdir(self.upload_directory + self.dir_name)
        rar_file.extractall(self.upload_directory + self.dir_name)
        rar_file.close()
        return {'code': 1, 'msg': 'Success', 'dir_name': self.dir_name}

    def __decompress_tar_gz(self):
        """extract a tar.gz file"""
        tar_file = tarfile.open(self.filepath)
        self.__check_filename_dir()
        os.mkdir(self.upload_directory + self.dir_name)
        tar_file.extractall(self.upload_directory + self.dir_name)
        tar_file.close()
        return {'code': 1, 'msg': 'Success', 'dir_name': self.dir_name}

    def __check_filename_dir(self):
        if os.path.isdir(self.upload_directory + self.dir_name):
            shutil.rmtree(self.upload_directory + self.dir_name)

    def __repr__(self):
        return '<decompress - %r>' % self.filename