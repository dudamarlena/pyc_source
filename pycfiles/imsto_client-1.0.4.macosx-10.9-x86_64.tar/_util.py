# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/imsto_client/_util.py
# Compiled at: 2013-12-17 23:31:21
import os
__all__ = [
 'encode_upload']
BOUNDARY = '----------bundary------'
CRLF = '\r\n'

def encode_upload(file=None, content=None, name=None, content_type=None, ext_data=[]):
    """encode a upload file form
                sea also: http://mancoosi.org/~abate/upload-file-using-httplib
        """
    body = []
    for key, value in ext_data:
        body.extend([
         '--' + BOUNDARY,
         'Content-Disposition: form-data; name="%s"' % key,
         '',
         str(value)])

    if content is None:
        if file is None:
            raise ValueError('need file or content argument')
        if hasattr(file, 'read'):
            content = file.read()
        else:
            name = os.path.basename(file)
            f = open(file, 'rb')
            content = f.read()
            f.close()
    if name is None:
        ext = guess_image_ext(content[:32])
        name = ('data.{}').format(ext)
    if content_type is None:
        content_type = guess_mimetype(name)
    body.extend([
     '--' + BOUNDARY,
     str('Content-Disposition: form-data; name="file"; filename="%s"' % name),
     str('Content-Type: %s' % content_type),
     '',
     content])
    body.extend(['--' + BOUNDARY + '--', ''])
    return ('multipart/form-data; boundary=%s' % BOUNDARY, CRLF.join(body))


sig_gif = 'GIF'
sig_jpg = b'\xff\xd8\xff'
sig_png = b'\x89PNG\r\n\x1a\n'

def guess_image_ext(data):
    if data[:3] == sig_gif:
        return 'gif'
    else:
        if data[:3] == sig_jpg:
            return 'jpg'
        else:
            if data[:8] == sig_png:
                return 'png'
            return

        return


def guess_mimetype(fn, default='application/octet-stream'):
    """Guess a mimetype from filename *fn*.

        >>> guess_mimetype("foo.txt")
        'text/plain'
        >>> guess_mimetype("foo")
        'application/octet-stream'
        """
    import mimetypes
    if '.' not in fn:
        return default
    bfn, ext = fn.lower().rsplit('.', 1)
    if ext == 'jpg':
        ext = 'jpeg'
    return mimetypes.guess_type(bfn + '.' + ext)[0] or default


def mime_to_ext(mime):
    import mimetypes
    ext = mimetypes.guess_extension(mime)
    if ext == '.jpe':
        return '.jpg'
    return ext