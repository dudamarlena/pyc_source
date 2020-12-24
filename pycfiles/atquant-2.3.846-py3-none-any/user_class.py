# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\utils\user_class.py
# Compiled at: 2018-08-27 20:45:27
# Size of source mod 2**32: 1943 bytes
import os, shutil, tempfile

class dotdict(dict):

    def __init__(self, _dict=None):
        _dict = _dict if _dict else {}
        super(dotdict, self).__init__(_dict)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            return super(dotdict, self).__getattribute__(item)


class OutputFileManager:
    __doc__ = '\n    输出文件管理，默认位置在：User/用户名/AppData/Local/Temp/Bitpower/Log\n    '
    _OutputFileManager__root_dir = os.path.normpath(os.path.join(tempfile.gettempdir(), 'Bitpower'))
    _OutputFileManager__root_sub = ['', 'record', 'mat', 'test', 'Log']

    @classmethod
    def root_sub_dir(cls, sub=''):
        """
        获取数据文件夹路径
        :param sub: '','record','mat','test','Log' 
        :return: 当为''时，返回文件夹目录的根目录，否则返回rootdir/sub
        """
        if sub in cls._OutputFileManager__root_sub:
            return os.path.normpath(os.path.join(cls._OutputFileManager__root_dir, sub))
        else:
            return

    @classmethod
    def rm_root_sub_dir(cls, sub):
        _path = cls.root_sub_dir(sub)
        if _path and os.path.exists(_path):
            try:
                shutil.rmtree(_path)
            except Exception:
                pass

        return _path

    @classmethod
    def mk_root_sub_dir(cls, sub):
        _path = cls.root_sub_dir(sub)
        if _path and not os.path.exists(_path):
            try:
                os.makedirs(_path)
            except Exception:
                pass

        return _path

    @classmethod
    def cls_root_sub_dir(cls, sub):
        cls.rm_root_sub_dir(sub)
        _path = cls.mk_root_sub_dir(sub)
        return _path