# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DistExt\InstallMisc.py
# Compiled at: 2006-08-11 14:46:52
import os
from distutils import util
from distutils.core import Command
from distutils.filelist import FileList

class InstallMisc(Command):
    """
    Common base class for installing some files in a subdirectory.
    Currently used by install_data and install_localstate.
    """
    __module__ = __name__
    user_options = [
     (
      'force', 'f', 'force installation (overwrite existing files)')]

    def initialize_options(self):
        self.install_dir = None
        self.force = None
        self.allfiles = None
        self.filelists = None
        return
        return

    def finalize_options(self):
        self.set_undefined_options('install', (
         self.get_command_name(), 'install_dir'), (
         'force', 'force'))
        return

    def _get_distribution_filelists(self):
        raise NotImplementedError('subclass %s must override' % self.__class__)

    def run(self):
        for filelist in self.get_filelists():
            sources = filelist.files
            outputs = self.get_filelist_outputs(filelist)
            if not sources:
                assert len(outputs) == 1
                self.mkpath(outputs[0])
            else:
                assert len(sources) == len(outputs)
                for (src, dst) in zip(sources, outputs):
                    self.mkpath(os.path.dirname(dst))
                    self.copy_file(src, dst)

        return

    def process_filelist(self, filelist):
        assert isinstance(filelist, FileList)
        filelist.set_allfiles(self.distribution.get_allfiles())
        for source in tuple(filelist.sources):
            pattern = util.convert_path(source)
            if filelist.recursive:
                found = filelist.include_pattern(None, prefix=pattern)
            else:
                found = filelist.include_pattern(pattern, anchor=True)
            if not found:
                self.warn("no files found matching '%s'" % source)
                filelist.sources.remove(source)

        for exclude in filelist.excludes:
            pattern = util.convert_path(exclude)
            if filelist.recursive:
                found = filelist.exclude_pattern(None, prefix=pattern)
            else:
                found = filelist.exclude_pattern(pattern, anchor=True)
            if not found:
                self.warn("no previously included files found matching '%s'" % exclude)

        filelist.sort()
        filelist.remove_duplicates()
        return filelist
        return

    def get_filelists(self):
        if self.filelists is None:
            self.filelists = self._get_distribution_filelists()
            for filelist in self.filelists:
                self.process_filelist(filelist)

        return self.filelists
        return

    def get_filelist_outputs(self, filelist):
        outputs = []
        destdir = util.convert_path(filelist.dest)
        destdir = os.path.join(self.install_dir, destdir)
        if not filelist.sources:
            outputs.append(destdir)
        else:
            if filelist.recursive:
                for pattern in filelist.sources:
                    pattern = util.convert_path(pattern)
                    for filename in filelist.files:
                        assert filename.startswith(pattern)
                        source = filename[len(pattern):]
                        assert source.startswith(os.sep)
                        outputs.append(destdir + source)

            for filename in filelist.files:
                source = os.path.basename(filename)
                outputs.append(os.path.join(destdir, source))

        return outputs

    def get_source_files(self):
        sources = []
        for filelist in self.get_filelists():
            sources.extend(filelist.files)

        return sources

    def get_inputs(self):
        inputs = []
        for filelist in self.get_filelists():
            inputs.extend(filelist.files)

        return inputs

    def get_outputs(self):
        outputs = []
        for filelist in self.get_filelists():
            outputs.extend(self.get_filelist_outputs(filelist))

        return outputs