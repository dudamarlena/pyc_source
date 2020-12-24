# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ad254919/aiida_plugin/aiida-bigdft/aiida_bigdft/calculations.py
# Compiled at: 2019-07-03 08:44:44
"""
Calculations provided by aiida_bigdft.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
from __future__ import absolute_import
import six, os
from aiida import orm
from aiida.common import datastructures, exceptions
from aiida.engine import CalcJob
from aiida.orm.nodes.data import List, SinglefileData
from aiida.plugins import DataFactory
from BigDFT import Calculators as BigDFT_calc
from BigDFT import InputActions as BigDFT_input
from BigDFT import Inputfiles as BigDFT_files
BigDFTParameters = DataFactory('bigdft')
BigDFTLogfile = DataFactory('bigdft_logfile')

class BigDFTCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the BigDFT python interface.
    """
    _POSINP_FILE_NAME = 'posinp.xyz'
    _INPUT_FILE_NAME = 'input.yaml'
    _OUTPUT_FILE_NAME = 'log.yaml'
    _TIMING_FILE_NAME = 'time.yaml'

    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        super(BigDFTCalculation, cls).define(spec)
        spec.input('metadata.options.resources', valid_type=dict, default={'num_machines': 1, 'num_mpiprocs_per_machine': 1})
        spec.input('metadata.options.parser_name', valid_type=six.string_types, default='bigdft')
        spec.input('metadata.options.output_filename', valid_type=six.string_types, default=cls._OUTPUT_FILE_NAME)
        spec.input('metadata.options.jobname', valid_type=six.string_types)
        spec.input('parameters', valid_type=BigDFTParameters, help='Command line parameters for BigDFT')
        spec.input('structure', valid_type=orm.StructureData, help='StructureData struct')
        spec.input('structurefile', valid_type=orm.Str, help='xyz file', default=orm.Str(cls._POSINP_FILE_NAME))
        spec.input('pseudos', valid_type=List, help='')
        spec.output('bigdft_logfile', valid_type=BigDFTLogfile, help='')
        spec.exit_code(100, 'ERROR_MISSING_OUTPUT_FILES', message='Calculation did not produce all expected output files.')

    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files needed by
            the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        dico = BigDFT_files.Inputfile()
        dico.update(self.inputs.parameters.dict)
        bigdft_calc = BigDFT_calc.SystemCalculator()
        posinp_filename = self.inputs.structurefile.value
        if self.inputs.structure is not None:
            print 'writing input posinp file'
            posinp_string = self.inputs.structure._prepare_xyz()[0]
            if self.inputs.metadata.options.jobname is None:
                posinp_filename = self._POSINP_FILE_NAME
            else:
                posinp_filename = self.inputs.metadata.options.jobname + '.xyz'
            posinp_file = open(posinp_filename, 'w')
            posinp_file.write(posinp_string)
            posinp_file.close()
        posinp_filedata = SinglefileData(file=os.path.abspath(posinp_filename)).store()
        local_copy_list = [
         (
          posinp_filedata.uuid, posinp_filedata.filename, posinp_filedata.filename)]
        if self.inputs.pseudos is not None:
            for filename in self.inputs.pseudos:
                pseudo_filedata = SinglefileData(file=os.path.abspath(filename)).store()
                local_copy_list.append((pseudo_filedata.uuid, pseudo_filedata.filename, filename))

        if self.inputs.metadata.options.jobname is not None:
            bigdft_calc.update_global_options(name=self.inputs.metadata.options.jobname)
        bigdft_calc._run_options(input=dico)
        bigdft_calc.pre_processing()
        if self.inputs.metadata.options.jobname is None:
            input_filename = self._INPUT_FILE_NAME
        else:
            input_filename = self.inputs.metadata.options.jobname + '.yaml'
        input_filedata = SinglefileData(file=os.path.abspath(input_filename)).store()
        local_copy_list.append((input_filedata.uuid, input_filedata.filename, input_filename))
        codeinfo = datastructures.CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        outfile = self.inputs.metadata.options.output_filename
        timefile = self._TIMING_FILE_NAME
        if self.inputs.metadata.options.jobname is not None:
            outfile = 'log-' + self.inputs.metadata.options.jobname + '.yaml'
            timefile = 'time-' + self.inputs.metadata.options.jobname + '.yaml'
        codeinfo.withmpi = self.inputs.metadata.options.withmpi
        if self.inputs.metadata.options.jobname is not None:
            codeinfo.cmdline_params = [
             '--name=' + self.inputs.metadata.options.jobname]
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = local_copy_list
        calcinfo.retrieve_list = [outfile, timefile]
        return calcinfo