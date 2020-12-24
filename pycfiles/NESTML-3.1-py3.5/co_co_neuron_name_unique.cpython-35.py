# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_neuron_name_unique.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2217 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages

class CoCoNeuronNameUnique(CoCo):
    __doc__ = '\n    This coco ensures that for all elements in a single compile units, the names of all neurons are pairwise \n    distinct.\n    Allowed:\n        neuron a:\n            ...\n        end\n        ...\n        neuron b:\n            ...\n        end\n    Not allowed:\n        neuron a:\n            ...\n        end\n        ...\n        neuron a: <- neuron with the same name\n            ...\n        end\n    '

    @classmethod
    def check_co_co(cls, compilation_unit):
        """
        Checks the coco for the handed over compilation unit.
        :param compilation_unit: a single compilation unit.
        :type compilation_unit: ASTCompilationUnit
        """
        checked = list()
        for neuronA in compilation_unit.get_neuron_list():
            for neuronB in compilation_unit.get_neuron_list():
                if neuronA is not neuronB and neuronA.get_name() == neuronB.get_name() and neuronB not in checked:
                    code, message = Messages.get_neuron_redeclared(neuronB.get_name())
                    Logger.log_message(error_position=neuronB.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)

            checked.append(neuronA)