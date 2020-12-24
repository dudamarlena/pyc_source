# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/bin/build_fs_tree.py
# Compiled at: 2008-10-23 05:55:16
"""
Export FileSystemStorage tree in a site like tree
"""
__version__ = '$Revision: 1.31 $'
__docformat__ = 'restructuredtext'
import re, os, sys, getopt
from StringIO import StringIO
MAN = 'python build_fs_tree.py SOURCE_PATH DEST_PATH LIB_PATH\n\nSOURCE_PATH\n    Path where fss and rdf files are stored.\n\nDEST_PATH\n    Path where filesystem tree are built.\n\nLIB_PATH\n    Path where FileSystemStorage is installed.\n'

def usage():
    print MAN


SEARCH_RDF = '^(?P<uid>.{32})_(?P<field>[^.]*).rdf$'
SEARCH_RDF_RE = re.compile(SEARCH_RDF)

def build_fs_tree(src_path, dst_path, lib_path):
    """Build FS tree"""
    sys.path.append(lib_path)
    from rdf import RDFReader
    from utils import copy_file
    print 'Build filesystem data in %s from %s' % (src_path, dst_path)
    sys_encoding = sys.getfilesystemencoding()
    rdf_files = []
    for (root, dirs, files) in os.walk(src_path):
        if root == src_path:
            for item in files:
                match = SEARCH_RDF_RE.match(item)
                if match is None:
                    continue
                uid = match.group('uid')
                field = match.group('field')
                rdf_files.append({'uid': uid, 'field': field})

    print 'Processing %s rdf files' % str(len(rdf_files))
    file_paths = []
    for rdf_file in rdf_files:
        uid = rdf_file['uid']
        field = rdf_file['field']
        rdf_filename = '%s_%s.rdf' % (uid, field)
        rdf_path = os.path.join(src_path, rdf_filename)
        rdf_file = StringIO()
        rdf_text = ''
        try:
            copy_file(rdf_path, rdf_file)
            rdf_file.seek(0)
            rdf_text = rdf_file.getvalue()
        finally:
            rdf_file.close()
        try:
            rdf_reader = RDFReader(rdf_text)
        except:
            try:
                rdf_text = rdf_text.replace('&', '&amp;')
                rdf_reader = RDFReader(rdf_text)
            except:
                print rdf_path
                print rdf_text
                raise

        field_url = rdf_reader.getFieldUrl()
        field_url = field_url.encode(sys_encoding, 'replace')
        content_path_array = field_url.split('/')[:-2]
        content_path = dst_path
        for content_dir in content_path_array:
            content_path = os.path.join(content_path, content_dir)
            if os.path.exists(content_path):
                continue
            print 'Create path: %s' % content_path
            os.mkdir(content_path)

        src_filename = '%s_%s' % (uid, field)
        src_file_path = os.path.join(src_path, src_filename)
        if not os.path.exists(src_file_path):
            print "Source file doesn't exist, we continue: %s" % src_file_path
            continue
        dst_filename = field
        dst_filenames = rdf_reader.getFieldProperty('fss:filename')
        if dst_filenames:
            dst_filename = dst_filenames[0]
            if not dst_filename:
                dst_filename = field
            else:
                dst_filename = dst_filename.encode(sys_encoding, 'replace')
        dst_file_path = os.path.join(content_path, dst_filename)
        orig_dst_filename = dst_filename
        dst_file_path_ok = False
        index = 0
        while not dst_file_path_ok:
            if dst_file_path not in file_paths:
                dst_file_path_ok = True
                file_paths.append(dst_file_path)
            else:
                index += 1
                dst_filename = '%s-%s' % (str(index), orig_dst_filename)
                print dst_filename
                dst_file_path = os.path.join(content_path, dst_filename)

        print 'Create file: %s' % dst_file_path
        copy_file(src_file_path, dst_file_path)
        print 'Create RDF file: %s.rdf' % dst_file_path
        copy_file(rdf_path, dst_file_path + '.rdf')

    print 'Filesystem data built complete'
    return


def main():
    """Build FS tree"""
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'h', ['help'])
    except getopt.error, msg:
        print msg
        print 'for help use --help'
        sys.exit(2)

    for (o, a) in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(0)

    if len(args) != 3:
        print 'for help use --help'
        usage()
        sys.exit(2)
    src_path = args[0]
    dst_path = args[1]
    lib_path = args[2]
    if not os.path.exists(src_path):
        print 'source path is not valid: %s' % src_path
        sys.exit(2)
    if not os.path.exists(src_path):
        print 'destination path is not valid: %s' % dst_path
        sys.exit(2)
    if not os.path.exists(lib_path):
        print 'lib path is not valid: %s' % lib_path
        sys.exit(2)
    build_fs_tree(src_path, dst_path, lib_path)


if __name__ == '__main__':
    main()