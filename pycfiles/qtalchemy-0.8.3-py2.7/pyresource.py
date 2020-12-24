# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtalchemy/xplatform/pyresource.py
# Compiled at: 2012-06-23 09:45:18
"""
This module contains a python zip file extractor that works with py2exe.

It is not perfect, but it is a proof-of-concept that I'd rather not lose.
"""
from pkg_resources import resource_stream
resource_temp_dir = None

def resource_to_tempfile(module, resource):
    """
    Read a pkg_resources stream and dump it to a temp file.
    Return the file name of the new temp file.

    TODO:  get smart about cacheing files and temp dir management!
    """
    global resource_temp_dir
    import tempfile, os
    if resource_temp_dir is None:
        resource_temp_dir = tempfile.mkdtemp()
    file_name = os.path.join(resource_temp_dir, module, resource)
    if not os.path.exists(file_name):
        my_stream = resource_stream(module, resource)
        if not os.path.exists(os.path.join(resource_temp_dir, module)):
            os.mkdir(os.path.join(resource_temp_dir, module))
        f = open(file_name, 'wb')
        f.write(my_stream.read())
        f.close()
    return file_name