# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/HTTP/MimeTypes.py
# Compiled at: 2008-10-19 12:19:52
"""Mapping of common file extensions to their associated MIME types.
"""
import string
extensionToMimeType = {'png': 'image/png', 
   'gif': 'image/gif', 
   'jpg': 'image/jpeg', 
   'jpeg': 'image/jpeg', 
   'bmp': 'image/bmp', 
   'tif': 'image/tiff', 
   'tiff': 'image/tiff', 
   'ico': 'image/x-icon', 
   'c': 'text/plain', 
   'py': 'text/plain', 
   'cpp': 'text/plain', 
   'cc': 'text/plain', 
   'h': 'text/plain', 
   'hpp': 'text/plain', 
   'txt': 'text/plain', 
   'htm': 'text/html', 
   'html': 'text/html', 
   'css': 'text/css', 
   'zip': 'application/zip', 
   'gz': 'application/x-gzip', 
   'tar': 'application/x-tar', 
   'mid': 'audio/mid', 
   'mp3': 'audio/mpeg', 
   'wav': 'audio/x-wav', 
   'cool': 'text/cool'}

def workoutMimeType(filename):
    """Determine the MIME type of a file from its file extension"""
    fileextension = string.rsplit(filename, '.', 1)[(-1)]
    if extensionToMimeType.has_key(fileextension):
        return extensionToMimeType[fileextension]
    else:
        return 'application/octet-stream'