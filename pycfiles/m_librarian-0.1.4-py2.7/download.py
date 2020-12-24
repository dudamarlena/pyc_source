# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.7/m_librarian/download.py
# Compiled at: 2018-06-11 09:54:59
from __future__ import print_function
import os
from time import mktime
from shutil import copyfileobj
from zipfile import ZipFile
from .config import get_config
__all__ = [
 'download']
format = '%f'
compile_format = True
compiled_format = '%(file)s'

def _compile_format():
    global compile_format
    global compiled_format
    global format
    if not compile_format:
        return
    compile_format = False
    format = get_config().get('download', 'format')
    if not format:
        return
    got_percent = False
    compiled = []
    for c in format:
        if c == '%':
            if got_percent:
                got_percent = False
                compiled.append('%')
            else:
                got_percent = True
        elif got_percent:
            got_percent = False
            if c == 'a':
                new_format = '%(author1)s'
            elif c == 'A':
                new_format = '%(authors)s'
            elif c == 'e':
                new_format = '%(extension)s'
            elif c == 'f':
                new_format = '%(file)s'
            elif c == 'G':
                new_format = '%(gname)s'
            elif c == 'g':
                new_format = '%(gtitle)s'
            elif c == 'J':
                new_format = '%(gname_list)s'
            elif c == 'j':
                new_format = '%(gtitle_list)s'
            elif c == 'l':
                new_format = '%(language)s'
            elif c == 'n':
                new_format = '%(ser_no)d'
            elif c == 's':
                new_format = '%(series)s'
            elif c == 't':
                new_format = '%(title)s'
            else:
                raise ValueError('Bad format specifier "%%%c"' % c)
            compiled.append(new_format)
        else:
            compiled.append(c)

    compiled_format = ('').join(compiled)


_library_path = None

def download(book, dest_path=None, lib_path=None, a_format=None):
    global _library_path
    global compile_format
    global compiled_format
    global format
    if lib_path is None:
        if _library_path is None:
            _library_path = get_config().getpath('library', 'path')
        lib_path = _library_path
    if a_format:
        compile_format = True
        format = a_format
    _compile_format()
    if compiled_format[(-1)] in ('\x00', '\\', '/'):
        raise ValueError('Bad format: "%s"' % compiled_format)
    bdict = {}
    bdict['author1'] = book.author1
    bdict['authors'] = book.author_list
    bdict['extension'] = book.extension.name
    bdict['file'] = book.file
    genre = book.genres[0]
    bdict['gname'] = genre.name
    bdict['gtitle'] = genre.title
    bdict['gname_list'] = book.genre_name_list
    bdict['gtitle_list'] = book.genre_title_list
    bdict['language'] = book.language.name
    bdict['ser_no'] = book.ser_no or 0
    bdict['series'] = book.series
    bdict['title'] = book.title
    if '%(extension)s' not in compiled_format:
        compiled_format += '.%(extension)s'
    filename = compiled_format % bdict
    full_path = os.path.join(dest_path, filename)
    try:
        os.makedirs(os.path.dirname(full_path))
    except OSError:
        pass

    zf = ZipFile(os.path.join(lib_path, book.archive), 'r')
    infile = zf.open('%s.%s' % (book.file, book.extension.name))
    outfile = open(full_path, 'wb')
    copyfileobj(infile, outfile)
    outfile.close()
    infile.close()
    zf.close()
    dt = mktime(book.date.timetuple())
    os.utime(full_path, (dt, dt))
    return


def test():
    _compile_format()
    print(compiled_format)


if __name__ == '__main__':
    test()