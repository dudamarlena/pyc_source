# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/configmanager/configurations.py
# Compiled at: 2019-12-05 09:47:28
# Size of source mod 2**32: 18567 bytes
""" This module implements the definition of the different configuration.
    NOTE: Make sure to run the function 'save_common_default_template'
        to save the default config after altering CompleteConfiguration.
        Write the default raw configuration template
            >>> import muteria.configmanager.configurations as mcc
            >>> mcc.save_common_default_template()

    We have a class defined for each configuration type. namely:
        - `ExecutionConfig`: Execution Configuration.
        - `ReportingConfig`: Reporting Configuration.
        - `ProjectConfig`: Project Configuration.
        - `TestcaseToolsConfig`: Testcase Tools Configuration.
        - `CodecoverageToolsConfig`: Codecoverage Tools Configuration.
        - `MutationToolsConfig`: Mutation Tools Configuration.

    TODO: Implement the restriction in adding extra element after creation
    TODO: Implement the verification of the parameters of each config
    TODO: Implement loading the values of the parameters from files... and 
            Checking
"""
from __future__ import print_function
import os, logging, muteria.common.mix as common_mix
from muteria.drivers.testgeneration import TestToolType
ERROR_HANDLER = common_mix.ErrorHandler

class SessionMode(common_mix.EnumAutoName):
    EXECUTE_MODE = 0
    VIEW_MODE = 1
    INTERNAL_MODE = 2
    RESTORE_REPOS_MODE = 3


class ConfigClasses(common_mix.EnumAutoName):
    CONTROLLER_CONF = 'CONTROLLER_CONF'
    PROJECT_CONF = 'PROJECT_CONF'
    TESTCASES_CONF = 'TESTCASES_CONF'
    CRITERIA_CONF = 'CRITERIA_CONF'
    OTHER_CONF = 'OTHER_CONF'


class ConfigElement(object):

    def __init__(self, val=None, desc=None, val_range=None, conf_class=None):
        self.val = val
        self.desc = desc
        self.val_range = val_range
        self.conf_class = conf_class

    def set_val(self, new_val):
        self.val = new_val

    def get_val(self):
        return self.val

    def set_desc(self, new_desc):
        self.desc = new_desc

    def get_desc(self):
        return self.desc

    def set_val_range(self, new_val_range):
        self.val_range = new_val_range

    def get_val_range(self):
        return self.val_range

    def set_conf_class(self, new_conf_class):
        self.conf_class = new_conf_class

    def get_conf_class(self):
        return self.conf_class


class CompleteConfiguration(object):
    EXECUTION_CLEANSTART = False
    RUN_MODE = None
    ENABLED_CRITERIA = []
    GET_PASSFAIL_OUTPUT_SUMMARY = True
    CRITERIA_WITH_OUTPUT_SUMMARY = []
    SINGLE_REPO_PARALLELISM = 1
    EXECUTE_ONLY_CURENT_CHECKPOINT_META_TASK = False
    RESTART_CURRENT_EXECUTING_META_TASKS = False
    RE_EXECUTE_FROM_CHECKPOINT_META_TASKS = []
    OUTPUT_ROOT_DIR = None
    LOG_DEBUG = False
    GENERATE_HTML_REPORT = True
    OUTPUT_CRITERIA_SCORES = True
    CRITERIA_SCORE_BY_TOOL = True
    OUTPUT_CRITERIA_SUBSUMPTION_SCORE = True
    OUTPUT_CRITERIA_COVERED_ELEMENTS = False
    OUTPUT_CRITERIA_UNCOVERED_ELEMENTS = True
    DETAILED_ELEMENTS_OUTPUT = False
    OUTPUT_CRITERIA_SUBSUMING_ELEM_NUM = True
    OUTPUT_STATS_HISTORY = True
    PROGRAMMING_LANGUAGE = None
    REPOSITORY_ROOT_DIR = None
    REPO_EXECUTABLE_RELATIVE_PATHS = None
    TARGET_SOURCE_INTERMEDIATE_CODE_MAP = None
    TARGET_CLASSES_NAMES = None
    TARGET_METHODS_BY_TARGET_CLASSES = None
    DEVELOPER_TESTS_LIST = None
    CUSTOM_DEV_TEST_RUNNER_FUNCTION = None
    CUSTOM_DEV_TEST_PROGRAM_WRAPPER_CLASS = None
    CUSTOM_DEV_TEST_RUNNER_MODULE = None
    CODE_BUILDER_FUNCTION = None
    CODE_BUILDER_MODULE = None
    DEVELOPER_TESTS_ENABLED = True
    GENERATED_TESTS_ENABLED = True
    STOP_TESTS_EXECUTION_ON_FAILURE = False
    DISCARD_FLAKY_TESTS = True
    TEST_TOOL_TYPES_SCHEDULING = [
     (
      TestToolType.USE_ONLY_CODE,),
     (
      TestToolType.USE_CODE_AND_TESTS,)]
    TESTCASE_TOOLS_CONFIGS = []
    REPORT_NUMBER_OF_TESTS_GENERATED = True
    REPORT_NUMBER_OF_DUPLICATED_TESTS = True
    CRITERIA_TOOLS_CONFIGS_BY_CRITERIA = {}
    CRITERIA_SEQUENCE = None
    CRITERIA_REQUIRING_OUTDIFF_WITH_PROGRAM = None
    RUN_FAILING_TESTS_WITH_CRITERIA = []
    RUN_PASSING_TESTS_WITH_CRITERIA = []
    CRITERIA_RESTRICTION_ENABLED = True
    CRITERIA_ELEM_SELECTIONS = {}
    ONLY_EXECUTE_SELECTED_CRITERIA_ELEM = True
    MAX_CRITERIA_ELEM_SELECTION_NUM_PERCENT = '100%'
    CRITERIA_TESTGEN_GUIDANCE = {}
    CRITERIA_EXECUTION_OPTIMIZERS = {}
    COVER_CRITERIA_ELEMENTS_ONCE = False


class BaseToolConfig(dict):
    __doc__ = '\n    :param criteria_on: (list) alternate way to represent criteria of a tool (TODO)\n    '

    def __init__(self, tooltype=None, toolname=None, config_id=None, criteria_on=None, tool_user_custom=None):
        self.tooltype = tooltype
        self.toolname = toolname
        self.config_id = config_id
        self.criteria_on = criteria_on
        self.tool_user_custom = tool_user_custom
        if self.config_id is None:
            self.toolalias = self.toolname
        else:
            self.toolalias = toolname + '_' + str(self.config_id)

    def __eq__(self, value):
        return self.__dict__ == value.__dict__

    def get_tool_name(self):
        return self.toolname

    def get_tool_config_alias(self):
        return self.toolalias

    def get_tool_type(self):
        return self.tooltype

    def get_tool_criteria_on(self):
        return self.criteria_on

    def get_tool_user_custom(self):
        return self.tool_user_custom


class ToolUserCustom(dict):
    __doc__ = '\n    This config file is helpful to specify tool specific configurations\n    For example:\n    >>> conf = ToolUserCustom(         PATH_TO_TOOL_EXECUTABLE=\'/fullpath/to/tool/dir\',         ENV_VARS_DICT={\'var1\': \'value1\'},         PRE_TARGET_CMD_ORDERED_FLAGS_LIST=[(\'-solver\', \'stp\'),                     (\'-mutation-scope\', os.path.abspath("scopefile"))],         POST_TARGET_CMD_ORDERED_FLAGS_LIST=[(\'-sym-args\', \'0\', \'2\', \'3\')]\n    )\n\n    Note: It is possibled to only specify a subset of the values.\n    '
    PATH_TO_TOOL_BINARY_DIR = None
    ENV_VARS_DICT = None
    PRE_TARGET_CMD_ORDERED_FLAGS_LIST = None
    POST_TARGET_CMD_ORDERED_FLAGS_LIST = None

    def __init__(self, **kwargs):
        for k in kwargs:
            ERROR_HANDLER.assert_true(k.isupper() and k in dir(self), 'invalid parameter passed: ' + k, __file__)
            setattr(self, k, kwargs[k])

    def __eq__(self, value):
        return self.__dict__ == value.__dict__


class TestcaseToolsConfig(BaseToolConfig):
    TESTS_ORACLE_TESTS = True
    TESTS_ORACLE_OTHER_VERSION = None
    TESTS_ORACLE_OTHER_EXECUTABLE = None
    TEST_GENERATION_MAXTIME = 7200.0
    ONE_TEST_EXECUTION_TIMEOUT = 60.0

    def set_test_gen_maxtime(self, max_time):
        self.TEST_GENERATION_MAXTIME = max_time

    def set_one_test_execution_timeout(self, timeout):
        self.ONE_TEST_EXECUTION_TIMEOUT = timeout

    def set_test_oracle_test(self, value):
        self.TESTS_ORACLE_TESTS = value


class CriteriaToolsConfig(BaseToolConfig):
    SEPARATED_TEST_EXECUTION_EXTRA_TIMEOUT_TIMES = 1.5
    META_TEST_EXECUTION_EXTRA_TIMEOUT_TIMES = 100.0


def get_full_rawconf_template():
    """ Computes the defaul raw configuration template as string list
    """
    thisfile = os.path.abspath(__file__)
    with open(thisfile) as (f):
        row_list = []
        active = False
        for line in f:
            stripped_line = line.strip()
            if not active:
                if stripped_line == 'class CompleteConfiguration(object):':
                    active = True
                else:
                    if stripped_line == '#~ class CompleteConfiguration':
                        active = False
                    else:
                        row_list.append(stripped_line)

    if len(row_list) < 1:
        ERROR_HANDLER.error_exit('complete configuration class was not found', __file__)
    ERROR_HANDLER.assert_true(not active, 'did not find end of configuration class', __file__)
    return row_list


def save_common_default_template(filename=None):
    """ Write the default raw configuration template
        >>> import muteria.configmanager.configurations as mcc
        >>> mcc.save_common_default_template()
    """
    if filename is None:
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'defaults', 'common_defaults.py')
    row_list = get_full_rawconf_template()
    if os.path.isfile(filename):
        if not common_mix.confirm_execution('The filename to save configuration template exists. Do you want to override it?'):
            return
    header = '""" Defaults parameters that are common to all languages\n' + '"""\n'
    header += 'from __future__ import print_function\n\n'
    header += '{} {}\n'.format('from muteria.configmanager.configurations', 'import SessionMode')
    header += '{} {}\n'.format('from muteria.configmanager.configurations', 'import TestcaseToolsConfig')
    header += '{} {}\n'.format('from muteria.configmanager.configurations', 'import CriteriaToolsConfig')
    header += '{} {}\n'.format('from muteria.configmanager.configurations', 'import ToolUserCustom')
    header += '\n{} {}\n'.format('from muteria.drivers.criteria', 'import TestCriteria')
    header += '{} {}\n'.format('from muteria.drivers.criteria', 'import CriteriaToolType')
    header += '\n{} {}\n'.format('from muteria.drivers.testgeneration', 'import TestToolType')
    with open(filename, 'w') as (f):
        f.write(header + '\n')
        for row in row_list:
            f.write(row + '\n')


if __name__ == '__main__':
    save_common_default_template()