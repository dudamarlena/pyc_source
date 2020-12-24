# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_no_two_neurons_in_set_of_compilation_units.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2220 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.utils.ast_utils import ASTUtils
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages

class CoCoNoTwoNeuronsInSetOfCompilationUnits(CoCo):
    __doc__ = '\n    This Coco checks that for a handed over list of compilation units, not two neurons have the same name.\n    '

    @classmethod
    def check_co_co(cls, list_of_compilation_units):
        """
        Checks the coco.
        :param list_of_compilation_units: a list of compilation units.
        :type list_of_compilation_units: list(ASTNestMLCompilationUnit)
        """
        list_of_neurons = ASTUtils.get_all_neurons(list_of_compilation_units)
        conflicting_neurons = list()
        checked = list()
        for neuronA in list_of_neurons:
            for neuronB in list_of_neurons:
                if neuronA is not neuronB and neuronA.get_name() == neuronB.get_name():
                    code, message = Messages.get_compilation_unit_name_collision(neuronA.get_name(), neuronA.get_artifact_name(), neuronB.get_artifact_name())
                    Logger.log_message(code=code, message=message, log_level=LoggingLevel.ERROR)
                conflicting_neurons.append(neuronB)

            checked.append(neuronA)

        return conflicting_neurons