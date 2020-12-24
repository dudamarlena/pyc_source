# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/src/eb.py
# Compiled at: 2008-10-29 17:02:15
"""Encylopaedia Britannica (11th ed) material.
"""
from shakespeare.cache import default as cache
import os, time

class Wikimedia(object):
    """Extract EB shakespeare related material from wikimedia.
    """

    def __init__(self, verbose=False):
        self.verbose = verbose

    def execute(self):
        """Do the work."""
        for ii in range(28):
            pagenum = 772 + ii
            self.download(pagenum)

    def download(self, page_number):
        url = self.make_url(page_number)
        if self.verbose:
            print 'Downloading: ', url

        def download_success(url):
            expected_min_file_size = 100000
            local_path = cache.path(url)
            out = os.path.exists(local_path) and os.stat(local_path).st_size > expected_min_file_size
            return out

        cache.download_url(url)
        if not download_success(url):
            print 'ERROR: failed to download %s successfully' % url

    def make_url(self, page_number):
        """Generate urls for wikimedia diffs.

        @param page_number: EB page number you want from volume 24.

        """
        base_path = 'http://upload.wikimedia.org/wikipedia/commons/scans/EB1911_tiff/'
        volume = 'VOL24%20SAINTE-CLAIRE%20DEVILLE-SHUTTLE/'
        urlnum = page_number + 28
        urlnum = str(urlnum)
        fn = 'ED4A' + urlnum + '.TIF'
        return base_path + volume + fn


import os, shutil

class BasicCommand(object):

    def __init__(self):
        self.verbose = True

    def _p(self, msg, force=False):
        if self.verbose or force:
            print msg

    def _run(self, system_cmd):
        self._p(system_cmd)
        os.system(system_cmd)

    def execute(self):
        """Stub method: To be implemented in inheriting classes"""
        pass


class OcrEbCommand(BasicCommand):
    """Convert Encyclopaedia Britannica scans to plain text

    This requires ImageMagick convert utility to be installed.
    """

    def __init__(self, src_dir, dest_dir):
        """
        @param src_dir: directory where source tifs are located.
        @param dest_dir: where to put out text files (named after tifs).
        """
        super(OcrEbCommand, self).__init__()
        self.src_dir = src_dir
        self.dest_dir = dest_dir

    def chop(self, fn, out):
        chop_cmd = 'convert +gravity -crop 50x100% ' + fn + ' ' + out
        self._run(chop_cmd)

    def ocr(self, scan, out_file_path):
        cmd = 'tesseract %s %s' % (scan, out_file_path)
        self._run(cmd)

    def ocr_all(self):
        import tempfile
        tmpdir = tempfile.mkdtemp()
        try:
            for fn in os.listdir(self.src_dir):
                print fn
                src = os.path.join(self.src_dir, fn)
                (base, ext) = text_file = os.path.splitext(fn)
                intermediate_tif = os.path.join(tmpdir, base + '_%d.tif')
                self.chop(src, intermediate_tif)
                for extra in ['0', '1']:
                    tif_fn = base + '_' + extra + '.tif'
                    tif_fp = os.path.join(tmpdir, tif_fn)
                    dest = os.path.join(self.dest_dir, tif_fn)
                    self.ocr(tif_fp, dest)

        finally:
            shutil.rmtree(tmpdir)

    def put_text_files_together(self, out_file_path):
        outfo = file(out_file_path, 'w')
        for fn in os.listdir(self.dest_dir):
            if fn.startswith('ED4A'):
                srcpath = os.path.join(self.dest_dir, fn)
                srcurl = 'http://upload.wikimedia.org/wikipedia/commons/scans/EB1911_tiff/VOL24%20SAINTE-CLAIRE%20DEVILLE-SHUTTLE/' + fn[:-10] + '.TIF'
                startmsg = '### START: %s ###\n' % fn
                startmsg += '#### Source: %s \n\n' % srcurl
                endmsg = '### END: %s ###\n\n' % fn
                outfo.write(startmsg)
                outfo.write(file(srcpath).read())
                outfo.write(endmsg)

        outfo.close()

    def execute(self):
        self.ocr_all()


if __name__ == '__main__':
    print 'Starting ...'
    src_dir = '/Users/rgrp/svk/shakespeare/trunk/cache/upload.wikimedia.org/wikipedia/commons/scans/EB1911_tiff/VOL24%20SAINTE-CLAIRE%20DEVILLE-SHUTTLE'
    dest_dir = '/Users/rgrp/svk/shakespeare/trunk/ocr/processed'
    ocrcmd = OcrEbCommand(src_dir, dest_dir)
    ocrcmd.put_text_files_together('here.txt')