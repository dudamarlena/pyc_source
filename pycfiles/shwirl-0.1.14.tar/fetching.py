# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/util/fetching.py
# Compiled at: 2016-11-03 01:40:19
"""Data downloading and reading functions
"""
from math import log
import os
from os import path as op
import sys, shutil, time
from ..ext.six.moves import urllib
from ..ext.six import string_types
from ..util.config import config

def load_data_file(fname, directory=None, force_download=False):
    """Get a standard vispy demo data file

    Parameters
    ----------
    fname : str
        The filename on the remote ``demo-data`` repository to download,
        e.g. ``'molecular_viewer/micelle.npy'``. These correspond to paths
        on ``https://github.com/vispy/demo-data/``.
    directory : str | None
        Directory to use to save the file. By default, the vispy
        configuration directory is used.
    force_download : bool | str
        If True, the file will be downloaded even if a local copy exists
        (and this copy will be overwritten). Can also be a YYYY-MM-DD date
        to ensure a file is up-to-date (modified date of a file on disk,
        if present, is checked).

    Returns
    -------
    fname : str
        The path to the file on the local system.
    """
    _url_root = 'http://github.com/vispy/demo-data/raw/master/'
    url = _url_root + fname
    if directory is None:
        directory = config['data_path']
        if directory is None:
            raise ValueError('config["data_path"] is not defined, so directory must be supplied')
    fname = op.join(directory, op.normcase(fname))
    if op.isfile(fname):
        if not force_download:
            return fname
        if isinstance(force_download, string_types):
            ntime = time.strptime(force_download, '%Y-%m-%d')
            ftime = time.gmtime(op.getctime(fname))
            if ftime >= ntime:
                return fname
            print 'File older than %s, updating...' % force_download
    if not op.isdir(op.dirname(fname)):
        os.makedirs(op.abspath(op.dirname(fname)))
    _fetch_file(url, fname)
    return fname


class ProgressBar(object):
    """Class for generating a command-line progressbar

    Parameters
    ----------
    max_value : int
        Maximum value of process (e.g. number of samples to process, bytes to
        download, etc.).
    initial_value : int
        Initial value of process, useful when resuming process from a specific
        value, defaults to 0.
    mesg : str
        Message to include at end of progress bar.
    max_chars : int
        Number of characters to use for progress bar (be sure to save some room
        for the message and % complete as well).
    progress_character : char
        Character in the progress bar that indicates the portion completed.
    spinner : bool
        Show a spinner.  Useful for long-running processes that may not
        increment the progress bar very often.  This provides the user with
        feedback that the progress has not stalled.
    """
    spinner_symbols = [
     '|', '/', '-', '\\']
    template = '\r[{0}{1}] {2:.05f} {3} {4}   '

    def __init__(self, max_value, initial_value=0, mesg='', max_chars=40, progress_character='.', spinner=False):
        self.cur_value = initial_value
        self.max_value = float(max_value)
        self.mesg = mesg
        self.max_chars = max_chars
        self.progress_character = progress_character
        self.spinner = spinner
        self.spinner_index = 0
        self.n_spinner = len(self.spinner_symbols)

    def update(self, cur_value, mesg=None):
        """Update progressbar with current value of process

        Parameters
        ----------
        cur_value : number
            Current value of process.  Should be <= max_value (but this is not
            enforced).  The percent of the progressbar will be computed as
            (cur_value / max_value) * 100
        mesg : str
            Message to display to the right of the progressbar.  If None, the
            last message provided will be used.  To clear the current message,
            pass a null string, ''.
        """
        self.cur_value = cur_value
        progress = float(self.cur_value) / self.max_value
        num_chars = int(progress * self.max_chars)
        num_left = self.max_chars - num_chars
        if mesg is not None:
            self.mesg = mesg
        bar = self.template.format(self.progress_character * num_chars, ' ' * num_left, progress * 100, self.spinner_symbols[self.spinner_index], self.mesg)
        sys.stdout.write(bar)
        if self.spinner:
            self.spinner_index = (self.spinner_index + 1) % self.n_spinner
        sys.stdout.flush()
        return

    def update_with_increment_value(self, increment_value, mesg=None):
        """Update progressbar with the value of the increment instead of the
        current value of process as in update()

        Parameters
        ----------
        increment_value : int
            Value of the increment of process.  The percent of the progressbar
            will be computed as
            (self.cur_value + increment_value / max_value) * 100
        mesg : str
            Message to display to the right of the progressbar.  If None, the
            last message provided will be used.  To clear the current message,
            pass a null string, ''.
        """
        self.cur_value += increment_value
        self.update(self.cur_value, mesg)


def _chunk_read(response, local_file, chunk_size=65536, initial_size=0):
    """Download a file chunk by chunk and show advancement

    Can also be used when resuming downloads over http.

    Parameters
    ----------
    response: urllib.response.addinfourl
        Response to the download request in order to get file size.
    local_file: file
        Hard disk file where data should be written.
    chunk_size: integer, optional
        Size of downloaded chunks. Default: 8192
    initial_size: int, optional
        If resuming, indicate the initial size of the file.
    """
    bytes_so_far = initial_size
    total_size = int(response.headers['Content-Length'].strip())
    total_size += initial_size
    progress = ProgressBar(total_size, initial_value=bytes_so_far, max_chars=40, spinner=True, mesg='downloading')
    while True:
        chunk = response.read(chunk_size)
        bytes_so_far += len(chunk)
        if not chunk:
            sys.stderr.write('\n')
            break
        _chunk_write(chunk, local_file, progress)


def _chunk_write(chunk, local_file, progress):
    """Write a chunk to file and update the progress bar"""
    local_file.write(chunk)
    progress.update_with_increment_value(len(chunk))


def _fetch_file(url, file_name, print_destination=True):
    """Load requested file, downloading it if needed or requested

    Parameters
    ----------
    url: string
        The url of file to be downloaded.
    file_name: string
        Name, along with the path, of where downloaded file will be saved.
    print_destination: bool, optional
        If true, destination of where file was saved will be printed after
        download finishes.
    """
    temp_file_name = file_name + '.part'
    local_file = None
    initial_size = 0
    n_try = 3
    for ii in range(n_try):
        try:
            data = urllib.request.urlopen(url, timeout=15.0)
        except Exception as e:
            if ii == n_try - 1:
                raise RuntimeError('Error while fetching file %s.\nDataset fetching aborted (%s)' % (
                 url, e))

    try:
        try:
            file_size = int(data.headers['Content-Length'].strip())
            print 'Downloading data from %s (%s)' % (url, sizeof_fmt(file_size))
            local_file = open(temp_file_name, 'wb')
            _chunk_read(data, local_file, initial_size=initial_size)
            if not local_file.closed:
                local_file.close()
            shutil.move(temp_file_name, file_name)
            if print_destination is True:
                sys.stdout.write('File saved as %s.\n' % file_name)
        except Exception as e:
            raise RuntimeError('Error while fetching file %s.\nDataset fetching aborted (%s)' % (
             url, e))

    finally:
        if local_file is not None:
            if not local_file.closed:
                local_file.close()

    return


def sizeof_fmt(num):
    """Turn number of bytes into human-readable str"""
    units = [
     'bytes', 'kB', 'MB', 'GB', 'TB', 'PB']
    decimals = [0, 0, 1, 2, 2, 2]
    if num > 1:
        exponent = min(int(log(num, 1024)), len(units) - 1)
        quotient = float(num) / 1024 ** exponent
        unit = units[exponent]
        num_decimals = decimals[exponent]
        format_string = '{0:.%sf} {1}' % num_decimals
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    return '1 byte'