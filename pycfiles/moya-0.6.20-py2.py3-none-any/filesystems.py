# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/filesystems.py
# Compiled at: 2017-08-10 15:51:42
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from fs.errors import FSError
from fs.info import Info
from .console import Cell
from .compat import text_type, implements_to_string
from .interface import AttributeExposer
from .reader import DataReader
from .context.expressiontime import ExpressionDateTime
import weakref, re
_re_fs_path = re.compile(b'^(?:\\{(.*?)\\})*(.*$)')

def parse_fs_path(path):
    fs_name, fs_path = _re_fs_path.match(path).groups()
    return (fs_name or None, fs_path)


class FSContainer(dict):

    def __moyaconsole__(self, console):
        table = [
         [
          Cell(b'Name', bold=True),
          Cell(b'Type', bold=True),
          Cell(b'Location', bold=True)]]
        for name, fs in sorted(self.items()):
            syspath = fs.getsyspath(b'/', allow_none=True)
            if syspath is not None:
                location = syspath
                fg = b'green'
            else:
                try:
                    location = fs.desc(b'/')
                except FSError as e:
                    location = text_type(e)
                    fg = b'red'
                else:
                    fg = b'blue'

            table.append([
             Cell(name),
             Cell(fs.get_type_name()),
             Cell(b'%s' % location, bold=True, fg=fg)])

        console.table(table, header=True)
        return

    def close_all(self):
        for fs in self.items():
            try:
                fs.close()
            except:
                pass

        self.clear()


class _FSInfoProxy(Info, AttributeExposer):
    __moya_exposed_attributes__ = [
     b'raw',
     b'namespaces',
     b'name',
     b'path',
     b'is_dir',
     b'accessed',
     b'modified',
     b'created',
     b'metadata_changed',
     b'permissions',
     b'size',
     b'target']


class FSInfo(object):
    """Custom info class that return Moya datetime objects."""

    @classmethod
    def _from_epoch(cls, epoch):
        if epoch is None:
            return
        else:
            return ExpressionDateTime.from_epoch(epoch)

    def __init__(self, info):
        self._info = Info.copy(info, to_datetime=self._from_epoch)

    def __moyarepr__(self, context):
        return repr(self._info)

    def __repr__(self):
        return repr(self._info)

    @property
    def raw(self):
        return self._info.raw

    @property
    def namespaces(self):
        return self._info.namespaces

    @property
    def name(self):
        return self._info.name

    @property
    def is_dir(self):
        return self._info.is_dir

    @property
    def accessed(self):
        return self._info.accessed

    @property
    def modified(self):
        return self._info.modified

    @property
    def created(self):
        return self._info.created

    @property
    def metadata_changed(self):
        return self._info.metadata_changed

    @property
    def permissions(self):
        return self._info.permissions

    @property
    def size(self):
        return self._info.size

    @property
    def type(self):
        return self._info.type

    @property
    def group(self):
        return self._info.group

    @property
    def user(self):
        return self._info.user

    @property
    def target(self):
        return self._info.target


@implements_to_string
class FSWrapper(object):

    def __init__(self, fs, ref=False):
        self._fs = weakref.ref(fs)
        if ref:
            self.ref = self.fs

    @property
    def fs(self):
        return self._fs()

    def get_type_name(self):
        return type(self.fs).__name__

    def __str__(self):
        return self.fs.desc(b'/')

    def __repr__(self):
        return repr(self.fs)

    def __moyarepr__(self, context):
        return text_type(self.fs)

    def __contains__(self, path):
        return self.fs.isfile(path)

    def __getitem__(self, path):
        if self.fs.isfile(path):
            return self.fs.getbytes(path)
        return self.__class__(self.fs.opendir(path), ref=True)

    def __getattr__(self, name):
        return getattr(self.fs, name)

    def __moyaconsole__(self, console):
        console(self.fs.desc(b'.')).nl()
        self.fs.tree(max_levels=1)

    def keys(self):
        return self.fs.listdir()

    def values(self):
        return [ self.fs.desc(p) for p in self.fs.listdir() ]

    def items(self):
        return [ (p, self.fs.desc(p)) for p in self.fs.listdir() ]

    @property
    def reader(self):
        return DataReader(self.fs)


if __name__ == b'__main__':
    print(parse_fs_path(b'{templates}/widgets/posts.html'))
    print(parse_fs_path(b'/media/css/blog.css'))
    print(parse_fs_path(b'{}/media/css/blog.css'))