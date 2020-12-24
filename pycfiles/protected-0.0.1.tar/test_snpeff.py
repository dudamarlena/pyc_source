# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/protect/test/unit/test_snpeff.py
# Compiled at: 2018-05-07 13:54:25
__doc__ = '\nAuthor : Arjun Arkal Rao\nAffiliation : UCSC BME, UCSC Genomics Institute\nFile : protect/test/test_snpeff.py\n'
from __future__ import print_function
from protect.mutation_annotation.snpeff import run_snpeff
from protect.pipeline.ProTECT import _parse_config_file
from protect.test import ProtectTest
from toil.job import Job
import os, subprocess

class TestSnpeff(ProtectTest):

    def setUp(self):
        super(TestSnpeff, self).setUp()
        test_dir = self._createTempDir()
        self.options = Job.Runner.getDefaultOptions(self._getTestJobStorePath())
        self.options.logLevel = 'INFO'
        self.options.workDir = test_dir
        self.options.clean = 'always'

    def test_snpeff(self):
        """
        Test the functionality of run_transgene
        """
        univ_options = self._getTestUnivOptions()
        univ_options['output_folder'] = '/mnt/ephemeral/done'
        config_file = os.path.join(self._projectRootPath(), 'src/protect/test/test_inputs/ci_parameters.yaml')
        test_src_folder = os.path.join(self._projectRootPath(), 'src', 'protect', 'test')
        a = Job.wrapJobFn(self._get_test_mutation_vcf)
        b = Job.wrapJobFn(self._get_all_tools, config_file).encapsulate()
        c = Job.wrapJobFn(self._get_tool, b.rv(), 'snpeff')
        d = Job.wrapJobFn(run_snpeff, a.rv(), univ_options, c.rv(), disk='100M', memory='100M', cores=1).encapsulate()
        a.addChild(b)
        b.addChild(c)
        a.addChild(d)
        c.addChild(d)
        Job.Runner.startToil(a, self.options)

    @staticmethod
    def _get_all_tools(job, config_file):
        sample_set, univ_options, tool_options = _parse_config_file(job, config_file, max_cores=None)
        return tool_options

    @staticmethod
    def _get_tool(job, all_tools, tool):
        return all_tools[tool]

    @staticmethod
    def _get_test_mutation_vcf(job):
        """
        Get the test mutation vcf file and write to jobstore

        :return: FSID for the mutations vcf
        """
        base_call = 's3am download s3://cgl-pipeline-inputs/protect/unit_results/mutations/merged/'
        filename = 'all_merged.vcf'
        call = (base_call + '%s ' % filename * 2).strip().split(' ')
        subprocess.check_call(call)
        return job.fileStore.writeGlobalFile(filename)


_get_all_tools = TestSnpeff._get_all_tools
_get_tool = TestSnpeff._get_tool
_get_test_mutation_vcf = TestSnpeff._get_test_mutation_vcf