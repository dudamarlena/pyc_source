# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pathlib_mate-project/pathlib_mate/mate_tool_box_zip.py
# Compiled at: 2020-03-14 12:17:18
# Size of source mod 2**32: 6255 bytes
"""
Provide zip related functions.
"""
from __future__ import print_function
import os, random, string
from datetime import datetime
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from .mate_path_filters import all_true
from .helper import repr_data_size
alpha_digits = string.ascii_letters + string.digits

def rand_str(length):
    return ''.join([random.choice(alpha_digits) for _ in range(length)])


class ToolBoxZip(object):
    __doc__ = '\n    Provide zip related functions.\n    '

    def _auto_zip_archive_dst(self):
        surfix = '-{}-{}.zip'.format(datetime.now().strftime('%Y-%m-%d-%Hh-%Mm-%Ss'), rand_str(4))
        new_basename = self.basename + surfix
        return self.change(new_basename=new_basename)

    def make_zip_archive(self, dst=None, filters=all_true, compress=True, overwrite=False, makedirs=False, verbose=False):
        """
        Make a zip archive.

        :param dst: output file path. if not given, will be automatically assigned.
        :param filters: custom path filter. By default it allows any file.
        :param compress: compress or not.
        :param overwrite: overwrite exists or not.
        :param verbose: display log or not.
        :return:
        """
        self.assert_exists()
        if dst is None:
            dst = self._auto_zip_archive_dst()
        else:
            dst = self.change(new_abspath=dst)
        if not dst.basename.lower().endswith('.zip'):
            raise ValueError("zip archive name has to be endswith '.zip'!")
        else:
            if dst.exists():
                if not overwrite:
                    raise IOError("'%s' already exists!" % dst)
            if compress:
                compression = ZIP_DEFLATED
            else:
                compression = ZIP_STORED
        if not dst.parent.exists():
            if makedirs:
                os.makedirs(dst.parent.abspath)
        if verbose:
            msg = "Making zip archive for '%s' ..." % self
            print(msg)
        current_dir = os.getcwd()
        if self.is_dir():
            total_size = 0
            selected = list()
            for p in self.glob('**/*'):
                if filters(p):
                    selected.append(p)
                    total_size += p.size

            if verbose:
                msg = 'Got {} files, total size is {}, compressing ...'.format(len(selected), repr_data_size(total_size))
                print(msg)
            with ZipFile(dst.abspath, 'w', compression) as (f):
                os.chdir(self.abspath)
                for p in selected:
                    relpath = p.relative_to(self).__str__()
                    f.write(relpath)

        else:
            if self.is_file():
                with ZipFile(dst.abspath, 'w', compression) as (f):
                    os.chdir(self.parent.abspath)
                    f.write(self.basename)
            os.chdir(current_dir)
        if verbose:
            msg = 'Complete! Archive size is {}.'.format(dst.size_in_text)
            print(msg)

    def backup(self, dst=None, ignore=None, ignore_ext=None, ignore_pattern=None, ignore_size_smaller_than=None, ignore_size_larger_than=None, case_sensitive=False):
        """
        Create a compressed zip archive backup for a directory.

        :param dst: the output file path.
        :param ignore: file or directory defined in this list will be ignored.
        :param ignore_ext: file with extensions defined in this list will be ignored.
        :param ignore_pattern: any file or directory that contains this pattern
            will be ignored.
        :param ignore_size_smaller_than: any file size smaller than this
            will be ignored.
        :param ignore_size_larger_than: any file size larger than this
            will be ignored.

        **中文文档**

        为一个目录创建一个备份压缩包。可以通过过滤器选择你要备份的文件。
        """

        def preprocess_arg(arg):
            if arg is None:
                return []
            else:
                if isinstance(arg, (tuple, list)):
                    return list(arg)
                return [arg]

        self.assert_is_dir_and_exists()
        ignore = preprocess_arg(ignore)
        for i in ignore:
            if i.startswith('/') or i.startswith('\\'):
                raise ValueError

        ignore_ext = preprocess_arg(ignore_ext)
        for ext in ignore_ext:
            if not ext.startswith('.'):
                raise ValueError

        ignore_pattern = preprocess_arg(ignore_pattern)
        if case_sensitive:
            pass
        else:
            ignore = [i.lower() for i in ignore]
            ignore_ext = [i.lower() for i in ignore_ext]
            ignore_pattern = [i.lower() for i in ignore_pattern]

        def filters(p):
            relpath = p.relative_to(self).abspath
            if not case_sensitive:
                relpath = relpath.lower()
            else:
                for i in ignore:
                    if relpath.startswith(i):
                        return False

                if case_sensitive:
                    ext = p.ext
                else:
                    ext = p.ext.lower()
            if ext in ignore_ext:
                return False
            else:
                for pattern in ignore_pattern:
                    if pattern in relpath:
                        return False

                if ignore_size_smaller_than:
                    if p.size < ignore_size_smaller_than:
                        return False
                if ignore_size_larger_than:
                    if p.size > ignore_size_larger_than:
                        return False
                return True

        self.make_zip_archive(dst=dst,
          filters=filters,
          compress=True,
          overwrite=False,
          verbose=True)