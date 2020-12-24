# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/WarriorCore/ironclaw_driver.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 2851 bytes
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
import os
from warrior.WarriorCore.Classes.ironclaw_class import IronClaw
from warrior.Framework.Utils.print_Utils import print_info, print_error
from warrior.Framework.Utils import xml_Utils, file_Utils, testcase_Utils
from xml.etree import ElementTree

def iron_claw_warrior_xml_files(filepath):
    """Validate Warrior xml files (Testcase/Testsuite/Project) against
    their xsd schema files """
    try:
        root = xml_Utils.getRoot(filepath)
    except ElementTree.ParseError as err:
        print_error('PARSING ERROR:{0}'.format(err))
        return False

    ironclaw_object = IronClaw()
    if root.tag == 'Testcase':
        result = ironclaw_object.testcase_prerun(filepath)
    if root.tag == 'TestSuite':
        result = ironclaw_object.testsuite_prerun(filepath, root)
    if root.tag == 'Project':
        result = ironclaw_object.project_prerun(filepath, root)
    return result


def main(parameter_list):
    """Check the validity of testcase/testuite/project xml files """
    valid = True
    print_info('==========' + 'PRE-RUN XML VALIDATION' + '==========' + '\n')
    if len(parameter_list) > 0:
        for parameter in parameter_list:
            if file_Utils.get_extension_from_path(parameter) == '.xml':
                filepath = parameter
                abs_filepath = file_Utils.getAbsPath(filepath, os.curdir)
                res = iron_claw_warrior_xml_files(abs_filepath)
                result = testcase_Utils.convertLogic(res)
                valid &= res
                print_info("File '{0}' '{1}ED' Warrior prerunvalidation".format(abs_filepath, result))
            else:
                print_error("Provided file '{0}' is not an xml file".format(parameter))

    else:
        print_error('No input files provided to be validated')
        valid = False
    print_info('\n')
    print_info('Validation Completed:')
    if valid:
        print_info('Files are compatible with WARRIOR \n')
    else:
        print_error('Files failed Warrior Ironclaw validation\n')
    return valid