# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Transformers/TypeChecking/Transform.py
# Compiled at: 2019-09-09 15:48:17
from RoboticsLanguage.Tools import Semantic

def transform(code, parameters):
    if parameters['Transformers']['TypeChecking']['ignoreSemanticErrors']:
        return (code, parameters)
    code, parameters = Semantic.Checker(code, parameters)
    return (
     code, parameters)