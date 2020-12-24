# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\works4xtowordpythonconverter\__init__.py
# Compiled at: 2013-01-04 18:54:44
from read_works import *
from create import create_docx
import os
from os.path import join
import zipfile, shutil, optparse, sys
from send2trash import send2trash

def parse():
    """Parse any command arguments"""
    parser = optparse.OptionParser()
    parser.add_option('-S', '--sourcePath', action='store', type='string', default='', dest='sourcePath', help='Set the source path to process, if unset defaults to location from which program is run')
    parser.add_option('-D', '--destPath', action='store', type='string', default='', dest='destPath', help='Set the destination path to save processed files to, if unset defaults to saving beside the existing files')
    parser.add_option('--delete', action='store_true', dest='delete', help='Deletes the source files after processing - ARE YOU SURE YOU WANT TO DO THIS?!')
    parser.add_option('-A', '--archive', action='store_true', dest='archive', help="Archive the source files after processing - but doesn't delete them, consider using with the dangerous --delete flag")
    parser.add_option('-d', '--debug', action='store_true', dest='debug', help='If called with the --debug flag instead of just warning that a file failed will raise the error so that you can debug it properly - or send problematic file to nick.wilde.90@gmail.com')
    (opts, e) = parser.parse_args()
    if len(e) > 0:
        parser.print_help()
    return (
     opts, e)


def convert(opts):
    filelist = []
    sourcePath = opts.sourcePath
    if not sourcePath:
        sourcePath = os.path.dirname(__file__)
    srclen = len(sourcePath)
    print 'Works-4x-to-Word-Python-Converter running with source path of: %s' % sourcePath
    if opts.destPath:
        if not os.path.isabs(opts.destPath):
            destPath = join(sourcePath, opts.destPath)
        else:
            destPath = opts.destPath
    else:
        destPath = sourcePath
    if opts.archive:
        archive = zipfile.ZipFile(join(sourcePath, 'archive.zip'), mode='w', compression=zipfile.ZIP_DEFLATED)
    else:
        archive = None
    if opts.delete:
        if not opts.archive:
            confirm = raw_input('WARNING: you have selected the delete source files option, are you sure you want to do this? (enter Y, Yes to continue with delete option active)\n-->')
            if confirm and confirm.lower() in ('y', 'yes'):
                delete = True
            else:
                delete = False
        else:
            delete = True
    else:
        delete = False
    for (dir, folders, files) in os.walk(sourcePath):
        for file in files:
            if file.endswith('.wps'):
                filelist.append([dir, file])

    for file in filelist:
        src = join(file[0], file[1])
        newfile = join(destPath, file[0][srclen + 1:], file[1][:-3] + 'docx')
        text = read_ms_works_file(src)
        props = {}
        for (i, line) in enumerate(text):
            line = line.replace(b'\x92', "'")
            line = line.replace(b'\x93', '"')
            line = line.replace(b'\x94', '"')
            line = line.replace(b'\xbe', '~')
            line = line.replace(b'\x85', '...')
            line = line.replace(b'\xe2', '~')
            line = line.replace(b'\xa9', '(c)')
            line = line.replace(b'\x99', '*')
            line = line.replace(b'\x98', '*')
            line = line.replace(b'\x97', '&')
            line = line.replace(b'\x96', '-')
            line = line.replace('\x0b', ' ')
            line = line.replace('\x07', ' * ')
            line = line.replace(b'\xb7', '*')
            line = line.replace(b'\xe8', 'e')
            line = line.replace(b'\xeb', 'e')
            line = line.replace('\x0c', '')
            if line.find('\x00') != -1:
                line = line.split('\x00')[0]
            text[i] = line

        try:
            try:
                os.makedirs(os.path.dirname(newfile))
            except:
                pass

            create_docx(text, newfile, props)
        except:
            print 'Error creating file: ', newfile
            if opts.debug:
                if archive:
                    archive.close()
                raise
            continue

        tmpdir = os.path.join(os.environ['TMP'], 'works_to_word')
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
        with zipfile.ZipFile(newfile) as (mydoc):
            mydoc.extractall(tmpdir)
        with open(os.path.join(tmpdir, 'word/document.xml')) as (f):
            content = f.read()
            content = content.replace('<ns0:t>', '<ns0:t xml:space="preserve">')
            content = content.replace('(c)', b'\xa9')
        with open(os.path.join(tmpdir, 'word/document.xml'), 'w') as (f):
            f.write(content)
        with zipfile.ZipFile(newfile, mode='w', compression=zipfile.ZIP_DEFLATED) as (docxfile):
            i = len(tmpdir) + 1
            for (dirpath, dirnames, filenames) in os.walk(tmpdir):
                for filename in filenames:
                    templatefile = join(dirpath, filename)
                    archivename = templatefile[i:]
                    docxfile.write(templatefile, archivename)

        shutil.rmtree(tmpdir)
        os.utime(newfile, (os.path.getatime(src), os.path.getmtime(src)))
        if archive:
            archive.write(src, src[srclen + 1:])
        if delete:
            send2trash(src)

    if archive:
        archive.close()
    print 'Found %i files to process' % len(filelist)
    return


if __name__ == '__main__':
    (opts, extra) = parse()