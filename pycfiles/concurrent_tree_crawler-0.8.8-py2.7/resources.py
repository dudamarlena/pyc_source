# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/common/resources.py
# Compiled at: 2011-09-28 13:52:18
import os.path, urllib
from pkg_resources import resource_stream

class Resources:

    @staticmethod
    def open(_name_, relative_file_path):
        """
                Safe way of accessing the resource file (it will work even in
                code enclosed in *.egg/*.zip package)
                
                @param _name_: C{__name__} variable (of the calling module)
                @return: file-like object
                """
        return resource_stream(_name_, relative_file_path)

    @staticmethod
    def path(_file_, relative_path, convert_to_url=False):
        """
                *Unsafe* way of getting path to a resource (dir/file) - it won't 
                work inside code enclosed in *.egg/*.zip package
                        
                @param _file_: C{__file__} variable of calling module
                @param relative_path: current module-relative path
                @param convert_to_url: if True, the returned path is converted to 
                        an URL format, e.g. "C:\x0coo\x08ar" is converted to "///C:/foo/bar"
                @return: absolute-like path to given resource
                """
        path = os.path.join(os.path.dirname(_file_), relative_path)
        if convert_to_url:
            return urllib.pathname2url(path)
        return path