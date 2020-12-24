# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galleryremote/multipart.py
# Compiled at: 2011-06-09 07:24:08
import mimetypes

def multipart(boundary, arguments, file_info):
    """
    Generates the body of a multipart data.
    """
    parts = []
    for key, value in arguments.iteritems():
        parts.append('--%s' % boundary)
        parts.append('Content-disposition: form-data; name="%s"' % key)
        parts.append('')
        parts.append(value)

    if file_info is not None:
        content_type = mimetypes.guess_type(file_info[1])[0] or 'application/octet-stream'
        parts.append('--%s' % boundary)
        parts.append('Content-disposition: form-data; ' + 'name="%s"; filename="%s"' % (
         file_info[0], file_info[1]))
        parts.append('Content-Type: %s' % content_type)
        parts.append('Content-Transfer-Encoding: base64')
        parts.append('')
        image = file(file_info[1], 'rb')
        contents = image.read()
        image.close()
        parts.append(contents)
    parts.append('--%s--' % boundary)
    return ('\r\n').join(parts)