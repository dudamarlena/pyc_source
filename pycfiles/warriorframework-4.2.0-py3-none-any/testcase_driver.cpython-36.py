# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/WarriorCore/testcase_driver.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 45120 bytes
"""
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys, os, time, shutil, ast, xml.etree.ElementTree as et
from json import loads, dumps
from warrior.WarriorCore.defects_driver import DefectsDriver
from warrior.WarriorCore import custom_sequential_kw_driver, custom_parallel_kw_driver
from warrior.WarriorCore import iterative_sequential_kw_driver, iterative_parallel_kw_driver, common_execution_utils, framework_detail
from warrior.WarriorCore.Classes import execution_files_class, junit_class, hybrid_driver_class
from warrior.Framework import Utils
from warrior.Framework.Utils.testcase_Utils import convertLogic
from warrior.Framework.Utils.print_Utils import print_info, print_warning, print_error, print_debug, print_exception
from warrior.Framework.ClassUtils.kafka_utils_class import WarriorKafkaProducer
from warrior.Framework.Utils.data_Utils import getSystemData, _get_system_or_subsystem
import warrior.Framework.Utils.email_utils as email

def get_testcase_details(testcase_filepath, data_repository, jiraproj):
    """Gets all the details of the Testcase
    (like title, resultsfolder, logsfolder, datafile, default on_error
    action/value etc) from its xml file,for details that are not provided
    by user assigns default values.
    """
    Utils.config_Utils.set_datarepository(data_repository)
    name = Utils.xml_Utils.getChildTextbyParentTag(testcase_filepath, 'Details', 'Name')
    title = Utils.xml_Utils.getChildTextbyParentTag(testcase_filepath, 'Details', 'Title')
    expResults = Utils.xml_Utils.getChildTextbyParentTag(testcase_filepath, 'Details', 'ExpectedResults')
    category = Utils.xml_Utils.getChildTextbyParentTag(testcase_filepath, 'Details', 'Category')
    def_on_error_action = Utils.testcase_Utils.get_defonerror_fromxml_file(testcase_filepath)
    def_on_error_value = Utils.xml_Utils.getChildAttributebyParentTag(testcase_filepath, 'Details', 'default_onError', 'value')
    filename = os.path.basename(testcase_filepath)
    filedir = os.path.dirname(testcase_filepath)
    nameonly = Utils.file_Utils.getNameOnly(filename)
    operating_system = sys.platform
    if name is None or name is False:
        name = nameonly
    else:
        name = name.strip()
    if name != nameonly:
        print_warning('<Name> tag in xml file should match the filename')
        name = nameonly
    else:
        if title is None or title is False:
            print_warning('title is missing, please provide a title for the testcase')
            title = 'None'
        else:
            title = str(title).strip()
    if expResults is None or expResults is False:
        expResults = 'None'
    elif def_on_error_value is None or def_on_error_value is False:
        def_on_error_value = None
    elif 'wt_results_execdir' not in data_repository:
        if 'ow_resultdir' in data_repository:
            data_repository['wt_results_execdir'] = data_repository['ow_resultdir']
        else:
            data_repository['wt_results_execdir'] = None
    else:
        if 'wt_logs_execdir' not in data_repository:
            if 'ow_logdir' in data_repository:
                data_repository['wt_logs_execdir'] = data_repository['ow_logdir']
            else:
                data_repository['wt_logs_execdir'] = None
        res_startdir = data_repository['wt_results_execdir']
        logs_startdir = data_repository['wt_logs_execdir']
        efile_obj = execution_files_class.ExecFilesClass(testcase_filepath, 'tc', res_startdir, logs_startdir)
        resultfile = efile_obj.resultfile
        resultsdir = efile_obj.resultsdir
        logfile = efile_obj.logfile
        logsdir = efile_obj.logsdir
        defectsdir = efile_obj.get_defect_files()
        if 'ow_datafile' in data_repository:
            datafile = data_repository['ow_datafile']
            data_type = efile_obj.check_get_datatype(datafile)
        else:
            if testcase_filepath in data_repository:
                datafile = data_repository[testcase_filepath]
                data_type = efile_obj.check_get_datatype(datafile)
            else:
                if 'suite_data_file' in data_repository:
                    datafile = data_repository['suite_data_file']
                    data_type = efile_obj.check_get_datatype(datafile)
                else:
                    datafile, data_type = efile_obj.get_data_files()
    if datafile:
        if datafile is not 'NO_DATA':
            Utils.xml_Utils.getRoot(datafile)
    kw_results_dir = Utils.file_Utils.createDir(resultsdir, 'Keyword_Results')
    console_logfile = Utils.file_Utils.getCustomLogFile(filename, logsdir, 'consoleLogs')
    Utils.config_Utils.debug_file(console_logfile)
    to_strip_list = [
     name, title, category, datafile, data_type, logsdir,
     resultsdir, defectsdir, expResults]
    stripped_list = Utils.string_Utils.strip_white_spaces(to_strip_list)
    name = stripped_list[0]
    title = stripped_list[1]
    category = stripped_list[2]
    datafile = stripped_list[3]
    data_type = stripped_list[4]
    logsdir = stripped_list[5]
    resultsdir = stripped_list[6]
    defectsdir = stripped_list[7]
    expResults = stripped_list[8]
    data_repository['wt_name'] = name
    data_repository['wt_testcase_filepath'] = testcase_filepath
    data_repository['wt_title'] = title
    data_repository['wt_filename'] = filename
    data_repository['wt_filedir'] = filedir
    data_repository['wt_datafile'] = datafile
    data_repository['wt_data_type'] = data_type.upper()
    data_repository['wt_resultsdir'] = resultsdir
    data_repository['wt_resultfile'] = resultfile
    data_repository['wt_logsdir'] = logsdir
    data_repository['wt_kw_results_dir'] = kw_results_dir
    data_repository['wt_defectsdir'] = defectsdir
    data_repository['wt_console_logfile'] = console_logfile
    data_repository['wt_expResults'] = expResults
    data_repository['wt_operating_system'] = operating_system.upper()
    data_repository['wt_def_on_error_action'] = def_on_error_action.upper()
    data_repository['wt_def_on_error_value'] = def_on_error_value
    if 'jiraproj' not in data_repository:
        data_repository['jiraproj'] = jiraproj
    Utils.config_Utils.set_resultfile(resultfile)
    Utils.config_Utils.set_datafile(datafile)
    Utils.config_Utils.set_logsdir(logsdir)
    Utils.config_Utils.set_filename(filename)
    Utils.config_Utils.set_logfile(logfile)
    Utils.config_Utils.set_testcase_path(filedir)
    Utils.testcase_Utils.pTestcase()
    Utils.testcase_Utils.pCustomTag('Title', title)
    Utils.testcase_Utils.pCustomTag('TC_Location', testcase_filepath)
    Utils.testcase_Utils.pCustomTag('Datafile', datafile)
    Utils.testcase_Utils.pCustomTag('Logsdir', logsdir)
    Utils.testcase_Utils.pCustomTag('Defectsdir', defectsdir)
    Utils.testcase_Utils.pCustomTag('Resultfile', resultfile)
    Utils.testcase_Utils.pCustomTag('Operating_System', operating_system)
    exec_dir = os.path.dirname(data_repository['wt_resultsdir'])
    shutil.copy2(testcase_filepath, exec_dir)
    return data_repository


def report_testcase_requirements(testcase_filepath):
    """Reports the requirements of the testcase to the result file """
    req_id_list = Utils.testcase_Utils.get_requirement_id_list(testcase_filepath)
    if req_id_list is not None:
        for req_id in req_id_list:
            Utils.testcase_Utils.pReportRequirements(req_id)


def junit_requirements(testcase_filepath, tc_junit_object, timestamp):
    """ Takes the location of any Testcase xml file as input and add a new requirement when
    called"""
    req_id_list = Utils.testcase_Utils.get_requirement_id_list(testcase_filepath)
    if req_id_list is not None:
        for req_id in req_id_list:
            tc_junit_object.add_requirement(req_id, timestamp)


def compute_testcase_status(step_status, tc_status):
    """Compute the status of the testcase based on the step_status and the impact value of the step

    Arguments:
    1. step_status    = (bool) status of the executed step
    2. tc_status      = (bool) status of the testcase
    3. data_repository= (dict) data_repository of the testcase
    """
    if step_status is None:
        return tc_status
    else:
        return tc_status and step_status


def report_testcase_result(tc_status, data_repository, tag='Steps'):
    """Report the testcase result to the result file

    :Arguments:
        1. tc_status (bool) = status of the executed testcase
        2. data_repository (dict) = data_repository of the executed  testcase
    """
    print_info('\n**** Testcase Result ***')
    print_info('TESTCASE:{0}  STATUS:{1}'.format(data_repository['wt_name'], convertLogic(tc_status)))
    print_info('\n')
    Utils.testcase_Utils.pTestResult(tc_status, data_repository['wt_resultfile'])
    root = Utils.xml_Utils.getRoot(data_repository['wt_resultfile'])
    fail_count = 0
    for value in root.findall('Keyword'):
        kw_status = value.find('KeywordStatus').text
        if kw_status != 'PASS' and kw_status != 'RAN':
            fail_count += 1
            kw_name = value.find('Name').text
            get_step_value = list(value.attrib.values())
            step_num = ','.join(get_step_value)
            if fail_count == 1:
                print_info('++++++++++++++++++++++++ Summary of Failed Keywords ++++++++++++++++++++++++')
                print_info('{0:15} {1:45} {2:10}'.format('StepNumber', 'KeywordName', 'Status'))
                print_info('{0:15} {1:45} {2:10}'.format(str(step_num), tag + '-' + str(kw_name), str(kw_status)))
            elif fail_count > 1:
                print_info('{0:15} {1:45} {2:10}'.format(str(step_num), tag + '-' + str(kw_name), str(kw_status)))

    print_info('=================== END OF TESTCASE ===========================')


def get_system_list(datafile, node_req=False, iter_req=False):
    """Get the list of systems from the datafile
    :Arguments:
        1. datafile(string) - path of the input data file
        2. node_req(boolean) :
            If True, returns system_node_list(system xml objects) along
            with system_list(name of the systems)
        3. iter_req(boolean) :
             If True, picks systems only with 'iter' value other than 'no'
             If False, picks all systems from the data file
    :Returns:
        1. system_list(list) - name of the systems in the datafile
        2. system_node_list(list) - xml objects of the systems in the
                                    datafile(when node_req is True)
    """
    root = Utils.xml_Utils.getRoot(datafile)
    temp_systems = root.findall('system')
    systems = []
    system_list = []
    system_node_list = []
    if iter_req is True:
        for system in temp_systems:
            iter_flag = system.get('iter')
            if iter_flag:
                if str(iter_flag).lower() != 'no':
                    systems.append(system)
            else:
                systems.append(system)

    else:
        systems = temp_systems
    for system in systems:
        subsystems = system.findall('subsystem')
        if subsystems != []:
            first_subsystem = True
            for subsystem in subsystems:
                default = subsystem.get('default')
                if default == 'yes':
                    subsystem_name = subsystem.get('name')
                    system_name = system.get('name') + '[' + subsystem_name + ']'
                    break
                else:
                    if first_subsystem == True:
                        subsystem_name = subsystem.get('name')
                        system_name = system.get('name') + '[' + subsystem_name + ']'
                        first_subsystem = False

        else:
            system_name = system.get('name')
            system_node = system
        system_list.append(system_name)
        system_node_list.append(system_node)

    if node_req:
        return (system_list, system_node_list)
    else:
        return system_list


def print_testcase_details_to_console(testcase_filepath, data_repository, steps_tag='Steps'):
    """Prints the testcase details to the console """
    framework_detail.warrior_framework_details()
    print_info('\n===============================  TC-DETAILS  ==================================================')
    print_info('Title: %s' % data_repository['wt_title'])
    print_info('Results directory: %s' % data_repository['wt_resultsdir'])
    print_info('Logs directory: %s' % data_repository['wt_logsdir'])
    print_info('Defects directory: {0}'.format(data_repository['wt_defectsdir']))
    print_info('Datafile: %s' % data_repository['wt_datafile'])
    if data_repository['wt_testwrapperfile']:
        print_info('Testwrapperfile: %s' % data_repository['wt_testwrapperfile'])
    print_info('Expected Results: %s' % data_repository['wt_expResults'])
    if steps_tag == 'Steps':
        report_testcase_requirements(testcase_filepath)
    print_info('================================================================================================')
    time.sleep(2)


def create_defects(auto_defects, data_repository):
    """Creates the defects json files for the testcase executed
    If auto_defects = True create bugs in jira for the associated project provided in jira
    config file
    """
    defect_obj = DefectsDriver(data_repository)
    json_status = defect_obj.create_failing_kw_json()
    if json_status:
        if auto_defects:
            print_info('auto-create defects ')
            defects_json_list = defect_obj.get_defect_json_list()
            if len(defects_json_list) == 0:
                print_warning("No defect json files found in defects directory '{0}' of this testcase".format(data_repository['wt_defectsdir']))
            elif len(defects_json_list) > 0:
                connect = defect_obj.connect_warrior_jira()
                if connect is True:
                    defect_obj.create_jira_issues(defects_json_list)
        else:
            print_info('auto-create defects was Not requested')


def check_and_create_defects(tc_status, auto_defects, data_repository, tc_junit_object):
    """Check tc_status and create defects if tc_status is fail/error/exception
    update testcase junit with error/failures accordingly """
    if tc_status is True:
        pass
    else:
        if tc_status is False:
            create_defects(auto_defects, data_repository)
        elif tc_status == 'EXCEPTION' or tc_status == 'ERROR':
            create_defects(auto_defects, data_repository)


def execute_steps(data_type, runtype, data_repository, step_list, tc_junit_object, iter_ts_sys):
    """executes steps based on given data_type and runtype"""
    tc_status = True
    if data_type.upper() == 'CUSTOM':
        if runtype.upper() == 'SEQUENTIAL_KEYWORDS':
            tc_status = execute_custom(data_type, runtype, custom_sequential_kw_driver, data_repository, step_list)
    if data_type.upper() == 'CUSTOM' and runtype.upper() == 'PARALLEL_KEYWORDS':
        tc_junit_object.remove_html_obj()
        data_repository['war_parallel'] = True
        tc_status = execute_custom(data_type, runtype, custom_parallel_kw_driver, data_repository, step_list)
    elif data_type.upper() == 'ITERATIVE' and runtype.upper() == 'SEQUENTIAL_KEYWORDS':
        print_info('iterative sequential')
        system_list = get_system_list((data_repository['wt_datafile']), iter_req=True) if iter_ts_sys is None else [iter_ts_sys]
        if len(system_list) == 0:
            print_warning('Datatype is iterative but no systems found in input datafile, when Datatype is iterative the InputDataFile should have system(s) to iterate upon')
            tc_status = False
        else:
            if len(system_list) > 0:
                tc_status = iterative_sequential_kw_driver.main(step_list, data_repository, tc_status, system_list)
    else:
        if data_type.upper() == 'ITERATIVE' and runtype.upper() == 'PARALLEL_KEYWORDS':
            tc_junit_object.remove_html_obj()
            data_repository['war_parallel'] = True
            print_info('iterative parallel')
            system_list = get_system_list((data_repository['wt_datafile']), iter_req=True) if iter_ts_sys is None else [iter_ts_sys]
            if len(system_list) == 0:
                print_warning('DataType is iterative but no systems found in input datafile, when DataType id iterative the InputDataFile should have system(s) to iterate upon')
                tc_status = False
            else:
                if len(system_list) > 0:
                    tc_status = iterative_parallel_kw_driver.main(step_list, data_repository, tc_status, system_list)
        else:
            if data_type.upper() == 'HYBRID':
                print_info('Hybrid')
                system_list, system_node_list = get_system_list((data_repository['wt_datafile']),
                  node_req=True)
                hyb_drv_obj = hybrid_driver_class.HybridDriver(step_list, data_repository, tc_status, system_list, system_node_list)
                tc_status = hyb_drv_obj.execute_hybrid_mode()
            else:
                print_warning('unsupported value provided for testcase data_type or testsuite runtype')
                tc_status = False
    return tc_status


def get_testwrapper_file_details(testcase_filepath, data_repository):
    """retuns testwrapperfile to use if specified, else returns False"""
    if 'ow_testwrapperfile' in data_repository:
        testwrapperfile = data_repository['ow_testwrapperfile']
    else:
        if 'suite_testwrapper_file' in data_repository:
            testwrapperfile = data_repository['suite_testwrapper_file']
        else:
            if Utils.xml_Utils.nodeExists(testcase_filepath, 'TestWrapperFile'):
                testwrapperfile = Utils.xml_Utils.getChildTextbyParentTag(testcase_filepath, 'Details', 'TestWrapperFile')
            else:
                return [
                 False, False, False, 'abort']
    abs_cur_dir = os.path.dirname(testcase_filepath)
    abs_testwrapperfile = Utils.file_Utils.getAbsPath(testwrapperfile, abs_cur_dir)
    Utils.xml_Utils.getRoot(abs_testwrapperfile)
    jfile_obj = execution_files_class.ExecFilesClass(abs_testwrapperfile, 'tc', None, None)
    j_data_type = jfile_obj.check_get_datatype(data_repository['wt_datafile'])
    j_runtype = jfile_obj.check_get_runtype()
    setup_on_error_action = Utils.testcase_Utils.get_setup_on_error(abs_testwrapperfile)
    return [abs_testwrapperfile, j_data_type, j_runtype, setup_on_error_action]


def execute_testcase(testcase_filepath, data_repository, tc_context, runtype, tc_parallel, queue, auto_defects, suite, jiraproj, tc_onError_action, iter_ts_sys, steps_tag='Steps'):
    """ Executes the testcase (provided as a xml file)
            - Takes a testcase xml file as input and executes each command in the testcase.
            - Computes the testcase status based on the stepstatus and the impact value of the step
            - Handles step failures as per the default/specific onError action/value
            - Calls the function to report the testcase status

    :Arguments:
        1. testcase_filepath (string) = the full path of the testcase xml file
        2. execution_dir (string) = the full path of the directory under which the
                                    testcase execution directory will be created
                                    (the results, logs for this testcase will be
                                    stored in this testcase execution directory.)
    """
    tc_status = True
    tc_start_time = Utils.datetime_utils.get_current_timestamp()
    tc_timestamp = str(tc_start_time)
    print_info('[{0}] Testcase execution starts'.format(tc_start_time))
    get_testcase_details(testcase_filepath, data_repository, jiraproj)
    testwrapperfile, j_data_type, j_runtype, setup_on_error_action = get_testwrapper_file_details(testcase_filepath, data_repository)
    data_repository['wt_testwrapperfile'] = testwrapperfile
    isRobotWrapperCase = check_robot_wrapper_case(testcase_filepath)
    from_ts = False
    pj_junit_display = 'False'
    if 'wt_junit_object' not in data_repository:
        tc_junit_object = junit_class.Junit(filename=(data_repository['wt_name']), timestamp=tc_timestamp,
          name='customProject_independant_testcase_execution',
          display=pj_junit_display)
        if 'jobid' in data_repository:
            tc_junit_object.add_jobid(data_repository['jobid'])
            del data_repository['jobid']
        tc_junit_object.create_testcase(location=(data_repository['wt_filedir']), timestamp=tc_timestamp,
          ts_timestamp=tc_timestamp,
          name=(data_repository['wt_name']),
          testcasefile_path=(data_repository['wt_testcase_filepath']))
        junit_requirements(testcase_filepath, tc_junit_object, tc_timestamp)
        data_repository['wt_ts_timestamp'] = tc_timestamp
    else:
        tag = 'testcase' if steps_tag == 'Steps' else steps_tag
        tc_junit_object = data_repository['wt_junit_object']
        tc_junit_object.create_testcase(location='from testsuite', timestamp=tc_timestamp, ts_timestamp=(data_repository['wt_ts_timestamp']),
          classname=(data_repository['wt_suite_name']),
          name=(data_repository['wt_name']),
          tag=tag,
          testcasefile_path=(data_repository['wt_testcase_filepath']))
        from_ts = True
        junit_requirements(testcase_filepath, tc_junit_object, data_repository['wt_ts_timestamp'])
    data_repository['wt_tc_timestamp'] = tc_timestamp
    data_repository['tc_parallel'] = tc_parallel
    data_type = data_repository['wt_data_type']
    if not from_ts:
        data_repository['war_parallel'] = False
    tc_junit_object.add_property('resultsdir', os.path.dirname(data_repository['wt_resultsdir']), 'tc', tc_timestamp)
    tc_junit_object.update_attr('console_logfile', data_repository['wt_console_logfile'], 'tc', tc_timestamp)
    tc_junit_object.update_attr('title', data_repository['wt_title'], 'tc', tc_timestamp)
    data_repository['wt_junit_object'] = tc_junit_object
    print_testcase_details_to_console(testcase_filepath, data_repository, steps_tag)
    if data_repository['war_file_type'] == 'Case':
        filename = os.path.basename(testcase_filepath)
        html_filepath = os.path.join(data_repository['wt_resultsdir'], Utils.file_Utils.getNameOnly(filename)) + '.html'
        print_info('HTML result file: {0}'.format(html_filepath))
    step_list = common_execution_utils.get_step_list(testcase_filepath, steps_tag, 'step')
    if not step_list:
        print_warning('Warning! cannot get steps for execution')
        tc_status = 'ERROR'
    if step_list:
        if not len(step_list):
            print_warning('step list is empty in {0} block'.format(steps_tag))
    tc_state = Utils.xml_Utils.getChildTextbyParentTag(testcase_filepath, 'Details', 'State')
    if tc_state is not False:
        if tc_state is not None:
            if tc_state.upper() == 'DRAFT':
                print_warning("Testcase is in 'Draft' state, it may have keywords that have not been developed yet. Skipping the testcase execution and it will be marked as 'ERROR'")
                tc_status = 'ERROR'
    if isRobotWrapperCase is True and from_ts is False:
        print_warning("Case which has robot_wrapper steps should be executed as part of a Suite. Skipping the case execution and it will be marked as 'ERROR'")
        tc_status = 'ERROR'
    else:
        if step_list:
            setup_tc_status, cleanup_tc_status = (True, True)
            if testwrapperfile and not from_ts or testwrapperfile and from_ts and 'suite_testwrapper_file' not in data_repository:
                setup_step_list = common_execution_utils.get_step_list(testwrapperfile, 'Setup', 'step')
                if not len(setup_step_list):
                    print_warning('step list is empty in {0} block'.format('Setup'))
                print_info('****** SETUP STEPS EXECUTION STARTS *******')
                data_repository['wt_step_type'] = 'setup'
                original_tc_filepath = data_repository['wt_testcase_filepath']
                data_repository['wt_testcase_filepath'] = testwrapperfile
                setup_tc_status = execute_steps(j_data_type, j_runtype, data_repository, setup_step_list, tc_junit_object, iter_ts_sys)
                data_repository['wt_testcase_filepath'] = original_tc_filepath
                data_repository['wt_step_type'] = 'step'
                print_info('setup_tc_status : {0}'.format(setup_tc_status))
                print_info('****** SETUP STEPS EXECUTION ENDS *******')
            if setup_on_error_action == 'next' or setup_on_error_action == 'abort' and isinstance(setup_tc_status, bool) and setup_tc_status:
                if steps_tag == 'Steps':
                    print_info('****** TEST STEPS EXECUTION STARTS *******')
                data_repository['wt_step_type'] = 'step'
                tc_status = execute_steps(data_type, runtype, data_repository, step_list, tc_junit_object, iter_ts_sys)
                if steps_tag == 'Steps':
                    print_info('****** TEST STEPS EXECUTION ENDS *******')
            else:
                print_error('Test steps are not executed as setup steps failed to execute,setup status : {0}'.format(setup_tc_status))
                print_error('Steps in cleanup will be executed on besteffort')
                tc_status = 'ERROR'
            if tc_context.upper() == 'NEGATIVE':
                if all([tc_status != 'EXCEPTION', tc_status != 'ERROR']):
                    print_debug("Test case status is: '{0}', flip status as context is negative".format(tc_status))
                    tc_status = not tc_status
            if not isinstance(tc_status, bool) or isinstance(tc_status, bool) and tc_status is False:
                tc_testwrapperfile = None
                if Utils.xml_Utils.nodeExists(testcase_filepath, 'TestWrapperFile'):
                    tc_testwrapperfile = Utils.xml_Utils.getChildTextbyParentTag(testcase_filepath, 'Details', 'TestWrapperFile')
                    abs_cur_dir = os.path.dirname(testcase_filepath)
                    tc_testwrapperfile = Utils.file_Utils.getAbsPath(tc_testwrapperfile, abs_cur_dir)
                tc_debug_step_list = None
                if tc_testwrapperfile:
                    if Utils.xml_Utils.nodeExists(tc_testwrapperfile, 'Debug'):
                        tc_debug_step_list = common_execution_utils.get_step_list(tc_testwrapperfile, 'Debug', 'step')
                if tc_debug_step_list:
                    print_info('****** DEBUG STEPS EXECUTION STARTS *******')
                    data_repository['wt_step_type'] = 'debug'
                    original_tc_filepath = data_repository['wt_testcase_filepath']
                    data_repository['wt_testcase_filepath'] = tc_testwrapperfile
                    debug_tc_status = execute_steps(j_data_type, j_runtype, data_repository, tc_debug_step_list, tc_junit_object, iter_ts_sys)
                    data_repository['wt_testcase_filepath'] = original_tc_filepath
                    data_repository['wt_step_type'] = 'step'
                    print_info('debug_tc_status : {0}'.format(debug_tc_status))
                    print_info('****** DEBUG STEPS EXECUTION ENDS *******')
            if testwrapperfile and not from_ts or testwrapperfile and from_ts and 'suite_testwrapper_file' not in data_repository:
                cleanup_step_list = common_execution_utils.get_step_list(testwrapperfile, 'Cleanup', 'step')
                if not len(cleanup_step_list):
                    print_warning('step list is empty in {0} block'.format('Cleanup'))
                print_info('****** CLEANUP STEPS EXECUTION STARTS *******')
                data_repository['wt_step_type'] = 'cleanup'
                original_tc_filepath = data_repository['wt_testcase_filepath']
                data_repository['wt_testcase_filepath'] = testwrapperfile
                cleanup_tc_status = execute_steps(j_data_type, j_runtype, data_repository, cleanup_step_list, tc_junit_object, iter_ts_sys)
                data_repository['wt_step_type'] = 'step'
                print_info('cleanup_tc_status : {0}'.format(cleanup_tc_status))
                print_info('****** CLEANUP STEPS EXECUTION ENDS *******')
    if step_list:
        if isinstance(tc_status, bool):
            if isinstance(cleanup_tc_status, bool):
                if tc_status:
                    if cleanup_tc_status:
                        tc_status = True
    if step_list:
        if isinstance(tc_status, bool):
            if tc_status:
                if cleanup_tc_status != True:
                    print_warning('setting tc status to WARN as cleanup failed')
                    tc_status = 'WARN'
    if step_list:
        if tc_status == False:
            if tc_onError_action:
                if tc_onError_action.upper() == 'ABORT_AS_ERROR':
                    print_info("Testcase status will be marked as ERROR as onError action is set to 'abort_as_error'")
                    tc_status = 'ERROR'
    defectsdir = data_repository['wt_defectsdir']
    check_and_create_defects(tc_status, auto_defects, data_repository, tc_junit_object)
    print_info('\n')
    tc_end_time = Utils.datetime_utils.get_current_timestamp()
    print_info('[{0}] Testcase execution completed'.format(tc_end_time))
    tc_duration = Utils.datetime_utils.get_time_delta(tc_start_time)
    hms = Utils.datetime_utils.get_hms_for_seconds(tc_duration)
    print_info('Testcase duration= {0}'.format(hms))
    tc_junit_object.update_count(tc_status, '1', 'ts', data_repository['wt_ts_timestamp'])
    tc_junit_object.update_count('tests', '1', 'ts', data_repository['wt_ts_timestamp'])
    tc_junit_object.update_count('tests', '1', 'pj', 'not appicable')
    tc_junit_object.update_attr('status', str(tc_status), 'tc', tc_timestamp)
    tc_junit_object.update_attr('time', str(tc_duration), 'tc', tc_timestamp)
    tc_junit_object.add_testcase_message(tc_timestamp, tc_status)
    if str(tc_status).upper() in ('FALSE', 'ERROR', 'EXCEPTION'):
        tc_junit_object.update_attr('defects', defectsdir, 'tc', tc_timestamp)
    tc_junit_object.update_attr('resultsdir', os.path.dirname(data_repository['wt_resultsdir']), 'tc', tc_timestamp)
    tc_junit_object.update_attr('logsdir', os.path.dirname(data_repository['wt_logsdir']), 'tc', tc_timestamp)
    data_file = data_repository['wt_datafile']
    system_name = ''
    try:
        tree = et.parse(data_file)
        for elem in tree.iter():
            if elem.tag == 'system':
                for key, value in elem.items():
                    if value == 'kafka_producer':
                        system_name = elem.get('name')
                        break

    except:
        pass

    if system_name:
        junit_file_obj = data_repository['wt_junit_object']
        root = junit_file_obj.root
        suite_details = root.findall('testsuite')[0]
        test_case_details = suite_details.findall('testcase')[0]
        print_info('kafka server is presented in Inputdata file..')
        system_details = _get_system_or_subsystem(data_file, system_name)
        data = {}
        for item in system_details.getchildren():
            if item.tag == 'kafka_port':
                ssh_port = item.text
            else:
                if item.tag == 'ip':
                    ip_address = item.text
                else:
                    try:
                        value = ast.literal_eval(item.text)
                    except ValueError:
                        value = item.text

                    data.update({item.tag: value})

        ip_port = [
         '{}:{}'.format(ip_address, ssh_port)]
        data.update({'bootstrap_servers': ip_port})
        data.update({'value_serializer': lambda x: dumps(x).encode('utf-8')})
        try:
            producer = WarriorKafkaProducer(**data)
            producer.send_messages('warrior_results', suite_details.items())
            producer.send_messages('warrior_results', test_case_details.items())
            print_info('message published to topic: warrior_results {}'.format(suite_details.items()))
            print_info('message published to topic: warrior_results {}'.format(test_case_details.items()))
        except:
            print_warning('Unable to connect kafka server !!')

    report_testcase_result(tc_status, data_repository, tag=steps_tag)
    if not from_ts:
        tc_junit_object.update_count(tc_status, '1', 'pj', 'not appicable')
        tc_junit_object.update_count('suites', '1', 'pj', 'not appicable')
        tc_junit_object.update_attr('status', str(tc_status), 'ts', data_repository['wt_ts_timestamp'])
        tc_junit_object.update_attr('status', str(tc_status), 'pj', 'not appicable')
        tc_junit_object.update_attr('time', str(tc_duration), 'ts', data_repository['wt_ts_timestamp'])
        tc_junit_object.update_attr('time', str(tc_duration), 'pj', 'not appicable')
        tc_junit_object.output_junit(data_repository['wt_resultsdir'])
        if data_repository.get('db_obj') is not False:
            tc_junit_xml = data_repository['wt_resultsdir'] + os.sep + tc_junit_object.filename + '_junit.xml'
            data_repository.get('db_obj').add_html_result_to_mongodb(tc_junit_xml)
    else:
        if str(tc_status).upper() in ('FALSE', 'ERROR', 'EXCEPTION'):
            email_setting = None
            if 'any_failures' not in data_repository:
                email_params = email.get_email_params('first_failure')
                if all(value != '' for value in email_params[:3]):
                    email_setting = 'first_failure'
                data_repository['any_failures'] = True
            if email_setting is None:
                email_params = email.get_email_params('every_failure')
                if all(value != '' for value in email_params[:3]):
                    email_setting = 'every_failure'
            if email_setting is not None:
                email.compose_send_email('Test Case: ', data_repository['wt_testcase_filepath'], data_repository['wt_logsdir'], data_repository['wt_resultsdir'], tc_status, email_setting)
    if not tc_parallel:
        if not data_repository['war_parallel']:
            if 'wp_results_execdir' in data_repository:
                tc_junit_object.output_junit((data_repository['wp_results_execdir']), print_summary=False)
            else:
                tc_junit_object.output_junit((data_repository['wt_results_execdir']), print_summary=False)
    if tc_parallel:
        tc_impact = data_repository['wt_tc_impact']
        if tc_impact.upper() == 'IMPACT':
            msg = 'Status of the executed test case impacts Testsuite result'
        else:
            if tc_impact.upper() == 'NOIMPACT':
                msg = 'Status of the executed test case does not impact Teststuie result'
        print_debug(msg)
        tc_name = Utils.file_Utils.getFileName(testcase_filepath)
        queue.put((tc_status, tc_name, tc_impact, tc_duration, tc_junit_object))
    if data_repository.get('db_obj') is not False:
        data_repository.get('db_obj').add_xml_result_to_mongodb(data_repository['wt_resultfile'])
    return (
     tc_status, data_repository)


def execute_custom(datatype, runtype, driver, data_repository, step_list):
    """
    Execute a custom testcase
    """
    print_info('{0} {1}'.format(datatype, runtype))
    tc_status = False
    if 'suite_exectype' in data_repository:
        if data_repository['suite_exectype'].upper() == 'ITERATIVE':
            print_info('Testsuite execute type=iterative but the testcase datatype=custom. All testcases in a iterative testsuite should have datatype=iterative, Hence this testcase will be marked as failure.')
    else:
        if runtype.upper() == 'SEQUENTIAL_KEYWORDS' or runtype.upper() == 'PARALLEL_KEYWORDS':
            tc_status = driver.main(step_list, data_repository, tc_status, system_name=None)
        else:
            print_error('Unsuppored runtype found, please check testcase file')
    return tc_status


def check_robot_wrapper_case(testcase_filepath):
    """
    Check if the case has any robot_wrapper steps in it.
    """
    steps = Utils.xml_Utils.getElementListWithSpecificXpath(testcase_filepath, './/step[@Driver]')
    isRobotWrapperCase = False
    for step in steps:
        if step.get('Plugin') == 'plugin_robot_wrapper':
            isRobotWrapperCase = True
            break

    return isRobotWrapperCase


def main(testcase_filepath, data_repository={}, tc_context='POSITIVE', runtype='SEQUENTIAL_KEYWORDS', tc_parallel=False, auto_defects=False, suite=None, tc_onError_action=None, iter_ts_sys=None, queue=None, jiraproj=None):
    """ Executes a testcase """
    tc_start_time = Utils.datetime_utils.get_current_timestamp()
    if Utils.file_Utils.fileExists(testcase_filepath):
        try:
            tc_status, data_repository = execute_testcase(testcase_filepath, data_repository, tc_context, runtype, tc_parallel, queue, auto_defects, suite, jiraproj, tc_onError_action, iter_ts_sys)
        except Exception as exception:
            print_exception(exception)
            tc_status = False

    else:
        print_error('Testcase xml file does not exist in provided path: {0}'.format(testcase_filepath))
        tc_status = False
        if tc_parallel:
            queue.put(('ERROR', str(testcase_filepath), 'IMPACT', '0'))
        tc_duration = Utils.datetime_utils.get_time_delta(tc_start_time)
        return (
         tc_status, tc_duration, data_repository)