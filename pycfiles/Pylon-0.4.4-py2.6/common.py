# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\io\common.py
# Compiled at: 2010-12-26 13:36:33
""" Defines common components for reading/writing cases.
"""
import logging
logger = logging.getLogger(__name__)
BUS_ATTRS = [
 'name', 'type', 'v_base', 'v_magnitude',
 'v_angle', 'v_max', 'v_min', 'p_demand', 'q_demand',
 'g_shunt', 'b_shunt', 'p_lmbda', 'q_lmbda', 'mu_vmin', 'mu_vmax',
 'position']
BRANCH_ATTRS = [
 'name', 'online', 'r', 'x', 'b', 'rate_a', 'rate_b', 'rate_c',
 'ratio', 'phase_shift', 'ang_min', 'ang_max', 'p_from', 'p_to',
 'q_from', 'q_to', 'mu_s_from', 'mu_s_to', 'mu_angmin', 'mu_angmax']
GENERATOR_ATTRS = [
 'name', 'online', 'base_mva', 'p', 'p_max', 'p_min',
 'v_magnitude', 'q', 'q_max', 'q_min', 'c_startup', 'c_shutdown',
 'pcost_model', 'p_cost', 'qcost_model', 'q_cost', 'mu_pmin', 'mu_pmax']

class _CaseWriter(object):
    """ Defines a base class for writers of case data.
    """

    def __init__(self, case):
        """ Initialises a new _CaseWriter instance.
        """
        self.case = case

    def write(self, file_or_filename):
        """ Writes the case data to file.
        """
        if isinstance(file_or_filename, basestring):
            file = None
            try:
                try:
                    file = open(file_or_filename, 'wb')
                except Exception, detail:
                    logger.error('Error opening %s.' % detail)

            finally:
                if file is not None:
                    self._write_data(file)
                    file.close()

        else:
            file = file_or_filename
            self._write_data(file)
        return file

    def _write_data(self, file):
        self.write_case_data(file)
        self.write_bus_data(file)
        self.write_branch_data(file)
        self.write_generator_data(file)
        self.write_generator_cost_data(file)

    def write_case_data(self, file):
        """ Writes case data to file.
        """
        pass

    def write_bus_data(self, file):
        """ Writes bus data to file.
        """
        pass

    def write_branch_data(self, file):
        """ Writes branch data to file.
        """
        pass

    def write_generator_data(self, file):
        """ Writes generator data to file.
        """
        pass

    def write_generator_cost_data(self, file):
        """ Writes generator cost data to file.
        """
        pass


class _CaseReader(object):
    """ Defines a base class for case readers.
    """

    def read(self, file_or_filename):
        """ Reads the data file and returns a case.
        """
        raise NotImplementedError