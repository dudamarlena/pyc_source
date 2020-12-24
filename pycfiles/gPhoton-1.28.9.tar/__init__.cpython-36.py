# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/c/Dropbox/gPhoton_v1289/gPhoton/gPhoton/cal/__init__.py
# Compiled at: 2018-08-16 11:08:00
# Size of source mod 2**32: 6567 bytes
from __future__ import absolute_import, division, print_function
from builtins import range
import sys, os as _os, numpy as np
from astropy.io import fits
from gPhoton.MCUtils import get_fits_data, get_fits_header, get_tbl_data
from gPhoton import cal_dir
cal_url = 'https://archive.stsci.edu/prepds/gphoton/cal/cal/'
if sys.version_info[0] == 3:
    from urllib.request import urlopen
    from urllib.error import HTTPError
    from urllib.parse import urlencode
    from io import BytesIO
else:
    from urllib2 import urlopen
    from urllib2 import HTTPError
    from urllib import urlencode
    from cStringIO import StringIO as BytesIO

def url_content_length(fhandle):
    if sys.version_info[0] == 3:
        length = dict(fhandle.info())['Content-Length']
    else:
        length = fhandle.info().getheader('Content-Length')
    return int(length.strip())


def bytes_to_string(nbytes):
    if nbytes < 1024:
        return '%ib' % nbytes
    else:
        nbytes /= 1024.0
        if nbytes < 1024:
            return '%.1fkb' % nbytes
        nbytes /= 1024.0
        if nbytes < 1024:
            return '%.2fMb' % nbytes
        nbytes /= 1024.0
        return '%.1fGb' % nbytes


def download_with_progress_bar(data_url, file_path):
    if not _os.path.exists(_os.path.dirname(file_path)):
        _os.makedirs(_os.path.dirname(file_path))
    num_units = 40
    fhandle = urlopen(data_url)
    content_length = url_content_length(fhandle)
    chunk_size = content_length // num_units
    print('Downloading {url} to {cal_dir}'.format(url=data_url,
      cal_dir=(_os.path.dirname(file_path))))
    nchunks = 0
    buf = BytesIO()
    content_length_str = bytes_to_string(content_length)
    while True:
        next_chunk = fhandle.read(chunk_size)
        nchunks += 1
        if next_chunk:
            buf.write(next_chunk)
            s = '[' + nchunks * '=' + (num_units - 1 - nchunks) * ' ' + ']  %s / %s   \r' % (bytes_to_string(buf.tell()),
             content_length_str)
        else:
            sys.stdout.write('\n')
            break
        sys.stdout.write(s)
        sys.stdout.flush()

    buf.seek(0)
    open(file_path, 'wb').write(buf.getvalue())


def check_band(band):
    if band not in ('NUV', 'FUV'):
        raise ValueError('Band must be NUV or FUV')
    return band


def check_xy(xy):
    if xy not in ('x', 'y'):
        raise ValueError('xy must be x or y.')
    return xy


def read_data(fn, dim=0):
    path = _os.path.join(cal_dir, fn)
    if not _os.path.exists(path):
        data_url = '{b}/{f}'.format(b=cal_url, f=fn)
        fitsdata = download_with_progress_bar(data_url, path)
    if '.fits' in fn:
        return (
         get_fits_data(path, dim=dim), get_fits_header(path))
    if '.tbl' in fn:
        return get_tbl_data(path)
    raise ValueError('Unrecognized data type: {ext}'.format(ext=(fn[-4:])))


def wiggle(band, xy):
    fn = '{b}_wiggle_{d}.fits'.format(b=(check_band(band)), d=(check_xy(xy)))
    return read_data(fn)


def wiggle2():
    """The post-CSP wiggle file."""
    return read_data('WIG2_Sep2010.fits', dim=1)


def avgwalk(band, xy):
    fn = '{b}_avgwalk_{d}.fits'.format(b=(check_band(band)),
      d=(check_xy(xy)))
    return read_data(fn)


def walk(band, xy):
    fn = '{b}_walk_{d}.fits'.format(b=(check_band(band)),
      d=(check_xy(xy)))
    return read_data(fn)


def walk2():
    """The post-CSP walk file."""
    return read_data('WLK2_Sep2010.fits', dim=1)


def clock2():
    """The post-CSP clock file."""
    return read_data('CLK2_Sep2010.fits', dim=1)


def linearity(band, xy):
    fn = '{b}_NLC_{d}_det2sky.fits'.format(b=(check_band(band)),
      d=(check_xy(xy)))
    return read_data(fn)


def addbuffer(fn):
    m, h = read_data(fn)
    ix = np.where(m == 0)
    for i in range(-1, 2):
        for j in range(-1, 2):
            try:
                m[(ix[0] + i, ix[1] + j)] = 0
            except IndexError:
                continue

    return (
     m, h)


def flat(band, buffer=False):
    fn = '{b}_flat.fits'.format(b=(check_band(band)))
    if buffer:
        return addbuffer(fn)
    else:
        return read_data(fn)


def distortion(band, xy, eclipse, raw_stimsep):
    index = ''
    if band == 'NUV':
        if eclipse > 37460:
            if raw_stimsep < 5136.3:
                index = 'a'
            else:
                if raw_stimsep < 5137.25:
                    index = 'b'
                else:
                    index = 'c'
    fn = '{b}_distortion_cube_d{d}{i}.fits'.format(b=(check_band(band).lower()),
      d=(check_xy(xy)),
      i=index)
    return read_data(fn)


def offset(xy):
    fn = 'fuv_d{d}_fdttdc_coef_0.tbl'.format(d=(check_xy(xy)))
    return read_data(fn)


def mask(band, buffer=False):
    fn = '{b}_mask.fits'.format(b=(check_band(band)))
    if buffer:
        return addbuffer(fn)
    else:
        return read_data(fn)