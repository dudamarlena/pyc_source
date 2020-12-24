# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lazy_slides/download.py
# Compiled at: 2012-03-17 18:14:01
import contextlib, logging, os, urllib2, urlparse, uuid
log = logging.getLogger(__name__)

def download(url, directory):
    """Download a file specified by a URL to a local file.

    This generates a unique name for the downloaded file and saves
    into that.

    :param url: The URL to download.
    :param directory: The directory into which to save the file.
    """
    parsed = urlparse.urlparse(url)
    filename = os.path.split(parsed.path)[1]
    filename_comps = os.path.splitext(filename)
    filename = ('{}_{}{}').format(filename_comps[0], uuid.uuid4(), filename_comps[1])
    filename = os.path.join(directory, filename)
    log.info(('Downloading {} to {}').format(url, filename))
    with contextlib.closing(urllib2.urlopen(url)) as (infile):
        with open(filename, 'wb') as (outfile):
            outfile.write(infile.read())
    return filename