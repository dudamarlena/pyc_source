# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/pipeline/compilers/less.py
# Compiled at: 2019-06-12 01:17:17
"""A specialization of pipeline's LessCompiler."""
from __future__ import unicode_literals
import logging, os.path
from shutil import rmtree
from tempfile import mkdtemp
from pipeline.compilers.less import LessCompiler as PipelineLessCompiler
from pipeline.conf import settings as pipeline_settings

class LessCompiler(PipelineLessCompiler):
    """A LESS compiler which doesn't redirect the output.

    Pipeline's LESS compiler outputs to stdout and redirects that output to the
    target file, because of some bug in old versions of lessc. We don't want to
    do that, because it interferes with the generation of sourcemaps.

    To use this, add the path to this class to
    ``settings.PIPELINE['COMPILERS']``.
    """

    def compile_file(self, infile, outfile, outdated=False, force=False):
        """Compile a given file.

        Args:
            infile (unicode):
                The input filename.

            outfile (unicode):
                The output filename.

            outdated (bool):
                Whether the file is outdated.

            force (bool):
                Whether the compilation should proceed, regardless of whether
                the file is out of date.
        """
        if outdated or force:
            self.execute_command((
             pipeline_settings.LESS_BINARY,
             pipeline_settings.LESS_ARGUMENTS,
             infile,
             outfile))

    def is_outdated(self, infile, outfile):
        """Check to see if the given file is outdated.

        This will compare the timestamps of the ``infile`` and ``outfile``, but
        also compare the timestamp of ``outfile`` against any import
        depedencies that exist.

        Args:
            infile (unicode):
                The path to the input file.

            outfile (unicode):
                The path to the output file.

        Returns:
            bool:
            True if the file is out of date and needs to be recompiled.
        """
        if pipeline_settings.get(b'_DJBLETS_LESS_ALWAYS_REBUILD', False) or super(LessCompiler, self).is_outdated(infile, outfile):
            return True
        tempdir = mkdtemp()
        command = (
         os.path.join(os.path.dirname(__file__), b'less-imports.js'),
         pipeline_settings.LESS_ARGUMENTS,
         infile)
        imports_file = os.path.join(tempdir, os.path.basename(outfile))
        self.execute_command(command, stdout_captured=imports_file)
        with open(imports_file) as (f):
            files = f.read().splitlines()
            for dep in files:
                if super(LessCompiler, self).is_outdated(dep, outfile):
                    logging.info(b'Recompiling %s because dependency %s is out of date', infile, dep)
                    return True

        rmtree(tempdir)
        return False