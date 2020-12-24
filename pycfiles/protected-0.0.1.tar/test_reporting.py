# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/protect/test/unit/test_reporting.py
# Compiled at: 2018-05-07 13:54:25
__doc__ = '\nAuthor : Arjun Arkal Rao\nAffiliation : UCSC BME, UCSC Genomics Institute\nFile : protect/test/test_reporting.py\n'
from __future__ import print_function
import os
from toil.job import Job
from protect.addons.assess_car_t_validity import assess_car_t_validity
from protect.addons.assess_immunotherapy_resistance import assess_itx_resistance
from protect.addons.assess_mhc_pathway import assess_mhc_genes
from protect.common import get_file_from_s3, untargz
from protect.pipeline.ProTECT import _parse_config_file
from protect.test import ProtectTest

class TestReporting(ProtectTest):

    def setUp(self):
        super(TestReporting, self).setUp()
        test_dir = self._createTempDir()
        self.options = Job.Runner.getDefaultOptions(self._getTestJobStorePath())
        self.options.logLevel = 'INFO'
        self.options.workDir = test_dir
        self.options.clean = 'always'

    def test_mhc_assessment(self):
        """
        Test the functionality of assess_mhc_genes
        """
        univ_options = self._getTestUnivOptions()
        config_file = os.path.join(self._projectRootPath(), 'src/protect/test/test_inputs/ci_parameters.yaml')
        test_src_folder = os.path.join(self._projectRootPath(), 'src', 'protect', 'test')
        a = Job.wrapJobFn(self._get_test_rsem_file, test_src_folder)
        b = Job.wrapJobFn(self._get_all_tools, config_file).encapsulate()
        c = Job.wrapJobFn(self._get_tool, b.rv(), 'reports')
        d = Job.wrapJobFn(self._get_test_haplotype_file, test_src_folder)
        e = Job.wrapJobFn(assess_mhc_genes, a.rv(), d.rv(), univ_options, c.rv())
        f = Job.wrapJobFn(self._test_mhc_assessment_output, e.rv(), univ_options)
        a.addChild(b)
        a.addChild(d)
        b.addChild(c)
        c.addChild(e)
        d.addChild(e)
        Job.Runner.startToil(a, self.options)

    def test_itx_resistance(self):
        """
        Test the functionality of assess_mhc_genes
        """
        univ_options = self._getTestUnivOptions()
        config_file = os.path.join(self._projectRootPath(), 'src/protect/test/test_inputs/ci_parameters.yaml')
        test_src_folder = os.path.join(self._projectRootPath(), 'src', 'protect', 'test')
        a = Job.wrapJobFn(self._get_test_rsem_file, test_src_folder)
        b = Job.wrapJobFn(self._get_all_tools, config_file).encapsulate()
        c = Job.wrapJobFn(self._get_tool, b.rv(), 'reports')
        d = Job.wrapJobFn(assess_itx_resistance, a.rv(), univ_options, c.rv(), disk='100M', memory='100M', cores=1)
        a.addChild(b)
        b.addChild(c)
        c.addChild(d)
        Job.Runner.startToil(a, self.options)

    def test_car_t_validity(self):
        """
        Test the functionality of assess_mhc_genes
        """
        univ_options = self._getTestUnivOptions()
        config_file = os.path.join(self._projectRootPath(), 'src/protect/test/test_inputs/ci_parameters.yaml')
        test_src_folder = os.path.join(self._projectRootPath(), 'src', 'protect', 'test')
        a = Job.wrapJobFn(self._get_test_rsem_file, test_src_folder)
        b = Job.wrapJobFn(self._get_all_tools, config_file).encapsulate()
        c = Job.wrapJobFn(self._get_tool, b.rv(), 'reports')
        d = Job.wrapJobFn(assess_car_t_validity, a.rv(), univ_options, c.rv(), disk='100M', memory='100M', cores=1)
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
    def _get_test_rsem_file(job, test_src_folder):
        """
        Get the test rsem file and write to jobstore

        :return: FSID for the rsem file
        """
        rsem_file = get_file_from_s3(job, 'S3://cgl-pipeline-inputs/protect/unit_results/expression/rsem.genes.results', write_to_jobstore=False)
        return job.fileStore.writeGlobalFile(rsem_file)

    @staticmethod
    def _get_test_haplotype_file(job, test_src_folder):
        """
        Get the test haplotype file and write to jobstore

        :return: FSID for the MHC file
        """
        rna_haplotype = os.path.join(test_src_folder, 'test_inputs/test_mhc_haplotype.sum.tar.gz')
        rna_haplotype = untargz(rna_haplotype, os.getcwd())
        return job.fileStore.writeGlobalFile(rna_haplotype)

    @staticmethod
    def _test_mhc_assessment_output(job, output_file, univ_options):
        """
        Test the results of the assessment

        :param output_file: The file created by assess_mhc_genes
        """
        outfile = job.fileStore.readGlobalFile(output_file, 'mhc_report.txt')
        print(os.listdir(os.path.join(univ_options['output_folder'], 'test/reports')))
        assert os.path.exists(os.path.join(univ_options['output_folder'], 'test/reports', 'mhc_pathway_report.txt'))
        outdict = {}
        with open(outfile) as (o_f):
            for line in o_f:
                line = line.strip().split()
                if len(line) == 0 or line[0] in ('Gene', 'TAP', 'MHC', 'MHCI', 'MHCII'):
                    continue
                else:
                    outdict[line[0]] = line[3]

        lows = {x for x in outdict if outdict[x] == 'LOW'}
        fails = {x for x in outdict if outdict[x] == 'FAIL'}
        passes = {x for x in outdict if outdict[x] == 'PASS'}
        expectedlows = {
         'TNF', 'HLA_A', 'HLA_B', 'HLA_DRA'}
        expectedfails = {'HLA_DQA'}
        expectedpasses = {'CTSL', 'HLA_C', 'HLA_DRB', 'HLA_DQB'}
        assert expectedlows.difference(lows) == set([])
        assert expectedfails.difference(fails) == set([])
        assert expectedpasses.difference(passes) == set([])


_get_test_rsem_file = TestReporting._get_test_rsem_file
_test_output = TestReporting._test_mhc_assessment_output
_get_test_haplotype_file = TestReporting._get_test_haplotype_file
_get_all_tools = TestReporting._get_all_tools
_get_tool = TestReporting._get_tool