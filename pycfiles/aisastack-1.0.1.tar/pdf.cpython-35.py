# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/AIS/pdf.py
# Compiled at: 2018-10-22 10:39:31
# Size of source mod 2**32: 3299 bytes
__doc__ = '\nAIS.py - A Python interface for the Swisscom All-in Signing Service.\n\n:copyright: (c) 2016 by Camptocamp\n:license: AGPLv3, see README and LICENSE for more details\n\n'
import base64, codecs, hashlib, shutil, subprocess, tempfile, PyPDF2
from pkg_resources import resource_filename
from . import exceptions
from . import helpers

class PDF(object):
    """PDF"""

    def __init__(self, in_filename, prepared=False):
        self.in_filename = in_filename
        _out_fp, _out_filename = tempfile.mkstemp(suffix='.pdf')
        self.out_filename = _out_filename
        shutil.copy(self.in_filename, self.out_filename)
        self.prepared = prepared

    @staticmethod
    def _java_command():
        java_dir = resource_filename(__name__, 'empty_signer')
        return [
         'java',
         '-cp', '.:vendor/itextpdf-5.5.9.jar',
         '-Duser.dir={}'.format(java_dir),
         'EmptySigner']

    @classmethod
    def prepare_batch(cls, pdfs):
        """Add an empty signature to each of pdfs with only one java call."""
        pdfs_to_prepare = filter(lambda p: not p.prepared, pdfs)
        subprocess.check_call(cls._java_command() + [pdf.out_filename for pdf in pdfs_to_prepare])
        for pdf in pdfs_to_prepare:
            pdf.prepared = True

    def prepare(self):
        """Add an empty signature to self.out_filename."""
        if not self.prepared:
            subprocess.check_call(self._java_command() + [self.out_filename])
            self.prepared = True

    def digest(self):
        reader = PyPDF2.PdfFileReader(self.out_filename)
        sig_obj = None
        for generation, idnums in reader.xref.items():
            for idnum in idnums:
                if idnum == 0:
                    break
                pdf_obj = PyPDF2.generic.IndirectObject(idnum, generation, reader).getObject()
                if isinstance(pdf_obj, PyPDF2.generic.DictionaryObject) and pdf_obj.get('/Type') == '/Sig':
                    sig_obj = pdf_obj
                    break

        if sig_obj is None:
            raise exceptions.MissingPreparedSignature
        self.byte_range = sig_obj['/ByteRange']
        h = hashlib.sha256()
        with open(self.out_filename, 'rb') as (fp):
            for start, length in (self.byte_range[:2], self.byte_range[2:]):
                fp.seek(start)
                h.update(fp.read(length))

        result = base64.b64encode(h.digest())
        if helpers.PY3:
            result = result.decode('ascii')
        return result

    def write_signature(self, signature):
        """ Write the signature in the pdf file

        :type signature: Signature
        """
        with open(self.out_filename, 'rb+') as (fp):
            fp.seek(self.byte_range[1] + 1)
            fp.write(codecs.encode(signature.contents, 'hex'))