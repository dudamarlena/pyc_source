# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/wangwenpei/Codes/nextoa/cabric/cabric/components/mini.py
# Compiled at: 2017-02-24 23:53:33
import os
from cliez.component import Component

class MiniComponent(Component):

    def check(self):
        rtn = os.system('pyminifier --version > /dev/null')
        if rtn == 0:
            return True
        return False

    def minifier(self, infile):
        outfile = self.options.outdir + infile.replace(self.options.indir, '')
        outdir = os.path.dirname(outfile)
        _, infile_extension = os.path.splitext(infile)
        if self.options.dry_run:
            self.warn(outfile, prefix='[dry-run]: ', suffix='')
            return
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        if infile_extension in self.options.extension:
            cmd = ('pyminifier {} > {}').format(infile, outfile)
            if self.options.prepend:
                cmd = cmd.replace('pyminifier', 'pyminifier --prepend=%s' % self.options.prepend)
            if self.options.debug:
                self.logger.debug(cmd)
            os.system(cmd)
        else:
            with open(outfile, 'wb') as (fw):
                with open(infile, 'rb') as (fr):
                    fw.write(fr.read())

    def run(self, options):
        """
        :param options:
        :return:
        """
        if not self.check():
            self.error('please make sure you have installed pyminifier.')
        options.indir = os.path.abspath(options.indir)
        compare_dirs = []
        for v in options.exclude_dir:
            compare_dirs.append('/' + v)
            compare_dirs.append('/' + v + '/')

        for path, subdirs, files in os.walk(options.indir):
            skip_path = [ True for d in compare_dirs if d in path ]
            if skip_path:
                continue
            for name in files:
                self.minifier(os.path.join(path, name))

        if self.options.with_release:
            os.chdir(self.options.outdir)
            if os.path.exists('setup.py'):
                cmd = 'python setup.py sdist upload -r %s' % self.options.with_release
                if self.options.debug:
                    self.print_message(cmd)
                os.system(cmd)
            else:
                self.warn('no setup.py found,skip release')

    @classmethod
    def add_arguments(cls):
        """
        python web project deploy tool
        """
        return [
         (
          ('indir', ),
          dict(help='minifier root,default is current directory')),
         (
          ('outdir', ),
          dict(help='minifier root,default is current directory')),
         (
          ('--with-release', ),
          dict(help='release package to pypi server')),
         (
          ('--extension', ),
          dict(nargs='+', default=['.py'], help='file extension')),
         (
          ('--exclude-dir', ),
          dict(nargs='+', default=['.git', 'build', '.idea', 'dist'], help='directory to exclude')),
         (
          ('--prepend', ),
          dict(help='add license to minifier file')),
         (
          ('--dry-run', ),
          dict(action='store_true', help='show file list instead filter it'))]