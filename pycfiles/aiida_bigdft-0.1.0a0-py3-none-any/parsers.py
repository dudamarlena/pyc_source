# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ad254919/aiida_plugin/aiida-bigdft/aiida_bigdft/parsers.py
# Compiled at: 2019-07-03 08:53:39
"""
Parsers provided by aiida_bigdft.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from __future__ import absolute_import
from aiida import orm
from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory
from aiida.plugins import DataFactory
from BigDFT import Logfiles
BigDFTCalculation = CalculationFactory('bigdft')
BigDFTCalcJob = CalculationFactory('bigdft_calcjob')
BigDFTLogfile = DataFactory('bigdft_logfile')

class BigDFTParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a BigDFTCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.ProcessNode`
        """
        from aiida.common import exceptions
        super(BigDFTParser, self).__init__(node)
        if not (issubclass(node.process_class, BigDFTCalculation) or issubclass(node.process_class, BigDFTCalcJob)):
            raise exceptions.ParsingError('Can only parse BigDFTCalculation or BigDFTCalcJob')

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        from aiida.orm import SinglefileData
        output_filename = self.node.get_option('output_filename')
        jobname = self.node.get_option('jobname')
        if jobname != '':
            output_filename = 'log-' + jobname + '.yaml'
        else:
            output_filename = 'log.yaml'
        files_retrieved = self.retrieved.list_object_names()
        print files_retrieved
        files_expected = [output_filename]
        print output_filename
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error(("Found files '{}', expected to find '{}'").format(files_retrieved, files_expected))
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES
        self.logger.info(("Parsing '{}'").format(output_filename))
        output = BigDFTLogfile(self.retrieved._repository._get_base_folder().get_abs_path(output_filename))
        self.out('bigdft_logfile', output)
        return ExitCode(0)