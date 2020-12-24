# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/stepwise_param.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 3438 bytes
from federatedml.param.base_param import BaseParam
from federatedml.util import consts

class StepwiseParam(BaseParam):
    __doc__ = "\n    Define stepwise params\n\n    Parameters\n    ----------\n    score_name: str, default: 'AIC'\n        Specify which model selection criterion to be used\n\n    mode: str, default: 'Hetero'\n        Indicate what mode is current task\n\n    role: str, default: 'Guest'\n        Indicate what role is current party\n\n    direction: str, default: 'both'\n        Indicate which direction to go for stepwise.\n        'forward' means forward selection; 'backward' means elimination; 'both' means possible models of both directions are examined at each step.\n\n    max_step: int, default: '10'\n        Specify total number of steps to run before forced stop.\n\n    nvmin: int, default: '2'\n        Specify the min subset size of final model, cannot be lower than 2. When nvmin > 2, the final model size may be smaller than nvmin due to max_step limit.\n\n    nvmax: int, default: None\n        Specify the max subset size of final model, 2 <= nvmin <= nvmax. The final model size may be larger than nvmax due to max_step limit.\n\n    need_stepwise: bool, default False\n        Indicate if this module needed to be run\n\n    "

    def __init__(self, score_name='AIC', mode=consts.HETERO, role=consts.GUEST, direction='both', max_step=10, nvmin=2, nvmax=None, need_stepwise=False):
        super(StepwiseParam, self).__init__()
        self.score_name = score_name
        self.mode = mode
        self.role = role
        self.direction = direction
        self.max_step = max_step
        self.nvmin = nvmin
        self.nvmax = nvmax
        self.need_stepwise = need_stepwise

    def check(self):
        model_param_descr = "stepwise param's"
        self.score_name = self.check_and_change_lower(self.score_name, ['aic', 'bic'], model_param_descr)
        self.check_valid_value((self.mode), model_param_descr, valid_values=[consts.HOMO, consts.HETERO])
        self.check_valid_value((self.role), model_param_descr, valid_values=[consts.HOST, consts.GUEST, consts.ARBITER])
        self.direction = self.check_and_change_lower(self.direction, ['forward', 'backward', 'both'], model_param_descr)
        self.check_positive_integer(self.max_step, model_param_descr)
        self.check_positive_integer(self.nvmin, model_param_descr)
        if self.nvmin < 2:
            raise ValueError(model_param_descr + ' nvmin must be no less than 2.')
        if self.nvmax is not None:
            self.check_positive_integer(self.nvmax, model_param_descr)
            if self.nvmin > self.nvmax:
                raise ValueError(model_param_descr + ' nvmax must be greater than nvmin.')
        self.check_boolean(self.need_stepwise, model_param_descr)