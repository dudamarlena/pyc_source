# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/datamaestro/download/single.py
# Compiled at: 2020-02-25 07:34:23
# Size of source mod 2**32: 3689 bytes
import logging, shutil, tarfile, io, tempfile, gzip, os.path as op, os, urllib3
from pathlib import Path
from tempfile import NamedTemporaryFile
import re
from docstring_parser import parse
from datamaestro.utils import rm_rf
from datamaestro.stream import Transform
from datamaestro.download import Download

def open_ext(*args, **kwargs):
    """Opens a file according to its extension"""
    name = args[0]
    if name.endswith('.gz'):
        return (gzip.open)(*args, *kwargs)
    else:
        return (io.open)(*args, **kwargs)


class SingleDownload(Download):

    def __init__(self, filename):
        super().__init__(re.sub('\\..*$', '', filename))
        self.name = filename

    @property
    def path(self):
        return self.definition.datapath / self.name

    def prepare(self):
        return self.path

    def download(self, force=False):
        if not self.path.is_file():
            self._download(self.path)


class filedownloader(SingleDownload):

    def __init__(self, filename, url, transforms=None):
        """Downloads a file given by a URL

        Args:
            filename: The filename within the data folder; the variable name corresponds to the filename without the extension
            url: The URL to download
            transforms: Transform the file before storing it
        """
        super().__init__(filename)
        self.url = url
        p = urllib3.util.parse_url(self.url)
        path = Path(Path(p.path).name)
        self.transforms = transforms if transforms else Transform.createFromPath(path)

    def _download(self, destination):
        logging.info('Downloading %s into %s', self.url, destination)
        dir = op.dirname(destination)
        os.makedirs(dir, exist_ok=True)
        with self.context.downloadURL(self.url) as (file):
            if self.transforms:
                logging.info('Transforming file')
                with self.transforms(file.path.open('rb')) as (stream):
                    with destination.open('wb') as (out):
                        shutil.copyfileobj(stream, out)
            else:
                logging.info('Keeping original downloaded file %s', file.path)
                shutil.copy if file.keep else shutil.move(file.path, destination)
        logging.info('Created file %s' % destination)


class concatdownload(SingleDownload):
    __doc__ = 'Concatenate all files in an archive'

    def __init__(self, filename, url, transforms=None):
        """Concat the files in an archive

        Args:
            filename: The filename within the data folder; the variable name corresponds to the filename without the extension
            url: The URL to download
            transforms: Transform the file before storing it
        """
        super().__init__(filename)
        self.url = url
        self.transforms = transforms

    def _download(self, destination):
        with self.context.downloadURL(self.url) as (dl):
            with tarfile.open(dl.path) as (archive):
                destination.parent.mkdir(parents=True, exist_ok=True)
                with open(destination, 'wb') as (out):
                    for tarinfo in archive:
                        if tarinfo.isreg():
                            transforms = self.transforms or Transform.createFromPath(Path(tarinfo.name))
                            logging.debug('Processing file %s', tarinfo.name)
                            with transforms(archive.fileobject(archive, tarinfo)) as (fp):
                                shutil.copyfileobj(fp, out)