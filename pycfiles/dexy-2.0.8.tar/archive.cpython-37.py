# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/archive.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 3111 bytes
from dexy.filter import DexyFilter
import tarfile, zipfile, os

class UnprocessedDirectoryArchiveFilter(DexyFilter):
    __doc__ = '\n    Create a .tgz archive containing the unprocessed files in a directory.\n    '
    aliases = ['tgzdir']
    _settings = {'output':True, 
     'output-extensions':[
      '.tgz'], 
     'dir':('Directory in which to output the archive.', '')}

    def process(self):
        parent_dir = self.output_data.parent_dir()
        subdir = self.setting('dir')
        dir_to_archive = os.path.join(parent_dir, subdir)
        af = self.output_filepath()
        tar = tarfile.open(af, mode='w:gz')
        for fn in os.listdir(dir_to_archive):
            fp = os.path.join(dir_to_archive, fn)
            self.log_debug('Adding file %s to archive %s' % (fp, af))
            tar.add(fp, arcname=(os.path.join(subdir, fn)))

        tar.close()


class ArchiveFilter(DexyFilter):
    __doc__ = '\n    Creates a .tgz archive of all input documents.\n\n    The use-short-names option will store documents under their short\n    (canonical) filenames.\n    '
    aliases = ['archive', 'tgz']
    _settings = {'output':True, 
     'output-extensions':[
      '.tgz'], 
     'use-short-names':('Whether to use short, potentially non-unique names within the archive.', False)}

    def open_archive(self):
        self.archive = tarfile.open((self.output_filepath()), mode='w:gz')

    def add_to_archive(self, filepath, archivename):
        self.archive.add(filepath, arcname=archivename)

    def process(self):
        self.open_archive()
        dirname = self.output_data.baserootname()
        use_short_names = self.setting('use-short-names')
        for doc in self.doc.walk_input_docs():
            if not doc.output_data().is_cached():
                raise Exception('File not on disk.')
            elif use_short_names:
                arcname = doc.output_data().name
            else:
                arcname = doc.output_data().long_name()
            arcname = os.path.join(self.input_data.relative_path_to(arcname))
            arcname = os.path.join(dirname, arcname)
            self.add_to_archive(doc.output_data().storage.data_file(), arcname)

        self.archive.close()


class ZipArchiveFilter(ArchiveFilter):
    __doc__ = '\n    Creates a .zip archive of all input documents.\n\n    The use-short-names option will store documents under their short\n    (canonical) filenames.\n    '
    aliases = ['zip']
    _settings = {'output-extensions': ['.zip']}

    def open_archive(self):
        self.archive = zipfile.ZipFile((self.output_filepath()), mode='w')

    def add_to_archive(self, filepath, archivename):
        self.archive.write(filepath, arcname=archivename)