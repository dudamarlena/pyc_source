# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/protect/test/unit/test_alignments.py
# Compiled at: 2018-05-07 13:54:25
__doc__ = '\nAuthor : Arjun Arkal Rao\nAffiliation : UCSC BME, UCSC Genomics Institute\nFile : protect/test/test_file_downloads.py\n'
from __future__ import print_function
import os, subprocess
from protect.alignment.dna import align_dna
from protect.alignment.rna import align_rna
from protect.pipeline.ProTECT import _parse_config_file
from protect.test import ProtectTest
from toil.job import Job

class TestAlignments(ProtectTest):

    def setUp(self):
        super(TestAlignments, self).setUp()
        test_dir = self._createTempDir()
        self.options = Job.Runner.getDefaultOptions(self._getTestJobStorePath())
        self.options.logLevel = 'INFO'
        self.options.workDir = test_dir
        self.options.clean = 'always'

    def test_bwa(self):
        """
        Test the functionality of align_dna
        """
        univ_options = self._getTestUnivOptions()
        config_file = os.path.join(self._projectRootPath(), 'src/protect/test/test_inputs/ci_parameters.yaml')
        test_src_folder = os.path.join(self._projectRootPath(), 'src', 'protect', 'test')
        a = Job.wrapJobFn(self._get_test_bwa_files)
        b = Job.wrapJobFn(self._get_all_tools, config_file).encapsulate()
        c = Job.wrapJobFn(self._get_tool, b.rv(), 'bwa')
        d = Job.wrapJobFn(align_dna, a.rv(), 'tumor_dna', univ_options, c.rv()).encapsulate()
        a.addChild(b)
        b.addChild(c)
        c.addChild(d)
        Job.Runner.startToil(a, self.options)

    @staticmethod
    def _get_all_tools(job, config_file):
        sample_set, univ_options, tool_options = _parse_config_file(job, config_file, max_cores=None)
        return tool_options

    @staticmethod
    def _get_tool(job, all_tools, tool):
        all_tools[tool]['n'] = 2
        return all_tools[tool]

    @staticmethod
    def _get_test_bwa_files(job):
        """
        Get the test rsem file and write to jobstore

        :return: FSID for the rsem file
        """
        base_call = 's3am download s3://cgl-pipeline-inputs/protect/ci_references/'
        subprocess.check_call((base_call + 'Tum_1.fq.gz Tum_1.fq.gz').split(' '))
        subprocess.check_call((base_call + 'Tum_2.fq.gz Tum_2.fq.gz').split(' '))
        return [
         job.fileStore.writeGlobalFile('Tum_1.fq.gz'),
         job.fileStore.writeGlobalFile('Tum_2.fq.gz')]

    def test_star(self):
        """
        Test the functionality of align_dna
        """
        univ_options = self._getTestUnivOptions()
        config_file = os.path.join(self._projectRootPath(), 'src/protect/test/test_inputs/ci_parameters.yaml')
        test_src_folder = os.path.join(self._projectRootPath(), 'src', 'protect', 'test')
        a = Job.wrapJobFn(self._get_test_star_files)
        b = Job.wrapJobFn(self._get_all_tools, config_file).encapsulate()
        c = Job.wrapJobFn(self._get_tool, b.rv(), 'star')
        d = Job.wrapJobFn(align_rna, a.rv(), univ_options, c.rv()).encapsulate()
        a.addChild(b)
        b.addChild(c)
        c.addChild(d)
        Job.Runner.startToil(a, self.options)

    @staticmethod
    def _get_test_star_files(job):
        """
        Get the test rsem file and write to jobstore

        :return: FSID for the rsem file
        """
        base_call = 's3am download s3://cgl-pipeline-inputs/protect/ci_references/'
        subprocess.check_call((base_call + 'Rna_1.fq.gz Rna_1.fq.gz').split(' '))
        subprocess.check_call((base_call + 'Rna_2.fq.gz Rna_2.fq.gz').split(' '))
        return [
         job.fileStore.writeGlobalFile('Rna_1.fq.gz'),
         job.fileStore.writeGlobalFile('Rna_2.fq.gz')]


_get_all_tools = TestAlignments._get_all_tools
_get_tool = TestAlignments._get_tool
_get_test_bwa_files = TestAlignments._get_test_bwa_files
_get_test_star_files = TestAlignments._get_test_star_files