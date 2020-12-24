# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/symbols/predefined_functions.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 18132 bytes
from pynestml.symbols.function_symbol import FunctionSymbol
from pynestml.symbols.predefined_types import PredefinedTypes

class PredefinedFunctions(object):
    __doc__ = '\n    This class is used to represent all predefined functions of NESTML.\n\n    Attributes:\n        TIME_RESOLUTION       The callee name of the resolution function.\n        TIME_STEPS            The callee name of the time-steps function.\n        EMIT_SPIKE            The callee name of the emit-spike function.\n        PRINT                 The callee name of the print function.\n        PRINTLN               The callee name of the println function.\n        EXP                   The callee name of the exponent function.\n        LN                    The callee name of the natural logarithm function, i.e. the logarithm function of base :math:`e`.\n        LOG10                 The callee name of the logarithm function of base 10.\n        COSH                  The callee name of the hyperbolic cosine.\n        SINH                  The callee name of the hyperbolic sine.\n        TANH                  The callee name of the hyperbolic tangent.\n        LOGGER_INFO           The callee name of the logger-info function.\n        LOGGER_WARNING        The callee name of the logger-warning function.\n        RANDOM_NORMAL         The callee name of the function used to generate a random normal (Gaussian) distributed variable with parameters `mean` and `var` (variance).\n        RANDOM_UNIFORM        The callee name of the function used to generate a random sample from a uniform distribution in the interval `[offset, offset + scale)`.\n        EXPM1                 The callee name of the exponent (alternative) function.\n        DELTA                 The callee name of the delta function.\n        CLIP                  The callee name of the clip function.\n        MAX                   The callee name of the max function.\n        MIN                   The callee name of the min function.\n        INTEGRATE_ODES        The callee name of the integrate-ode function.\n        CURR_SUM              The callee name of the curr-sum function.\n        COND_SUM              The callee name of the cond-sum function.\n        CONVOLVE              The callee name of the convolve function.\n        name2function         A dict of function symbols as currently defined.\n    '
    TIME_RESOLUTION = 'resolution'
    TIME_STEPS = 'steps'
    EMIT_SPIKE = 'emit_spike'
    PRINT = 'print'
    PRINTLN = 'println'
    EXP = 'exp'
    LN = 'ln'
    LOG10 = 'log10'
    COSH = 'cosh'
    SINH = 'sinh'
    TANH = 'tanh'
    LOGGER_INFO = 'info'
    LOGGER_WARNING = 'warning'
    RANDOM_NORMAL = 'random_normal'
    RANDOM_UNIFORM = 'random_uniform'
    EXPM1 = 'expm1'
    DELTA = 'delta'
    CLIP = 'clip'
    MAX = 'max'
    MIN = 'min'
    INTEGRATE_ODES = 'integrate_odes'
    CURR_SUM = 'curr_sum'
    COND_SUM = 'cond_sum'
    CONVOLVE = 'convolve'
    name2function = {}

    @classmethod
    def register_functions(cls):
        """
        Registers all predefined functions.
        """
        cls.name2function = {}
        cls._PredefinedFunctions__register_time_resolution_function()
        cls._PredefinedFunctions__register_time_steps_function()
        cls._PredefinedFunctions__register_emit_spike_function()
        cls._PredefinedFunctions__register_print_function()
        cls._PredefinedFunctions__register_print_ln_function()
        cls._PredefinedFunctions__register_exponent_function()
        cls._PredefinedFunctions__register_ln_function()
        cls._PredefinedFunctions__register_log10_function()
        cls._PredefinedFunctions__register_cosh_function()
        cls._PredefinedFunctions__register_sinh_function()
        cls._PredefinedFunctions__register_tanh_function()
        cls._PredefinedFunctions__register_logger_info_function()
        cls._PredefinedFunctions__register_logger_warning_function()
        cls._PredefinedFunctions__register_random_normal_function()
        cls._PredefinedFunctions__register_random_uniform_function()
        cls._PredefinedFunctions__register_exp1_function()
        cls._PredefinedFunctions__register_delta_function()
        cls._PredefinedFunctions__register_clip_function()
        cls._PredefinedFunctions__register_max_function()
        cls._PredefinedFunctions__register_min_function()
        cls._PredefinedFunctions__register_integrated_odes_function()
        cls._PredefinedFunctions__register_curr_sum_function()
        cls._PredefinedFunctions__register_cond_sum_function()
        cls._PredefinedFunctions__register_convolve()

    @classmethod
    def __register_time_steps_function(cls):
        """
        Registers the time-resolution.
        """
        params = list()
        params.append(PredefinedTypes.get_type('ms'))
        symbol = FunctionSymbol(name=cls.TIME_STEPS, param_types=params, return_type=PredefinedTypes.get_integer_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.TIME_STEPS] = symbol

    @classmethod
    def __register_emit_spike_function(cls):
        """
        Registers the emit-spike function.
        """
        symbol = FunctionSymbol(name=cls.EMIT_SPIKE, param_types=list(), return_type=PredefinedTypes.get_real_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.EMIT_SPIKE] = symbol

    @classmethod
    def __register_print_function(cls):
        """
        Registers the print function.
        """
        params = list()
        params.append(PredefinedTypes.get_string_type())
        symbol = FunctionSymbol(name=cls.PRINT, param_types=params, return_type=PredefinedTypes.get_void_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.PRINT] = symbol

    @classmethod
    def __register_print_ln_function(cls):
        """
        Registers the print-line function.
        """
        symbol = FunctionSymbol(name=cls.PRINTLN, param_types=list(), return_type=PredefinedTypes.get_void_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.PRINTLN] = symbol

    @classmethod
    def __register_exponent_function(cls):
        """
        Registers the exponent (e(X)) function.
        """
        params = list()
        params.append(PredefinedTypes.get_real_type())
        symbol = FunctionSymbol(name=cls.EXP, param_types=params, return_type=PredefinedTypes.get_real_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.EXP] = symbol

    @classmethod
    def __register_ln_function(cls):
        """
        Registers the natural logarithm function, i.e. the logarithm function of base :math:`e`.
        """
        params = list()
        params.append(PredefinedTypes.get_real_type())
        symbol = FunctionSymbol(name=cls.LN, param_types=params, return_type=PredefinedTypes.get_real_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.LN] = symbol

    @classmethod
    def __register_log10_function(cls):
        """
        Registers the logarithm function of base 10.
        """
        params = list()
        params.append(PredefinedTypes.get_real_type())
        symbol = FunctionSymbol(name=cls.LOG10, param_types=params, return_type=PredefinedTypes.get_real_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.LOG10] = symbol

    @classmethod
    def __register_cosh_function(cls):
        """
        Registers the hyperbolic cosine function.
        """
        params = list()
        params.append(PredefinedTypes.get_real_type())
        symbol = FunctionSymbol(name=cls.COSH, param_types=params, return_type=PredefinedTypes.get_real_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.COSH] = symbol

    @classmethod
    def __register_sinh_function(cls):
        """
        Registers the hyperbolic sine function.
        """
        params = list()
        params.append(PredefinedTypes.get_real_type())
        symbol = FunctionSymbol(name=cls.SINH, param_types=params, return_type=PredefinedTypes.get_real_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.SINH] = symbol

    @classmethod
    def __register_tanh_function(cls):
        """
        Registers the hyperbolic tangent function.
        """
        params = list()
        params.append(PredefinedTypes.get_real_type())
        symbol = FunctionSymbol(name=cls.TANH, param_types=params, return_type=PredefinedTypes.get_real_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.TANH] = symbol

    @classmethod
    def __register_logger_info_function(cls):
        """
        Registers the logger info method into the scope.
        """
        params = list()
        params.append(PredefinedTypes.get_string_type())
        symbol = FunctionSymbol(name=cls.LOGGER_INFO, param_types=params, return_type=PredefinedTypes.get_void_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.LOGGER_INFO] = symbol

    @classmethod
    def __register_logger_warning_function(cls):
        """
        Registers the logger warning method.
        """
        params = list()
        params.append(PredefinedTypes.get_string_type())
        symbol = FunctionSymbol(name=cls.LOGGER_WARNING, param_types=params, return_type=PredefinedTypes.get_void_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.LOGGER_WARNING] = symbol

    @classmethod
    def __register_random_normal_function(cls):
        """
        Registers the random method as used to generate a random normal (Gaussian) distributed variable with first parameter "mean" and second parameter "standard deviation".
        """
        symbol = FunctionSymbol(name=cls.RANDOM_NORMAL, param_types=[PredefinedTypes.get_template_type(0), PredefinedTypes.get_template_type(0)], return_type=PredefinedTypes.get_template_type(0), element_reference=None, is_predefined=True)
        cls.name2function[cls.RANDOM_NORMAL] = symbol

    @classmethod
    def __register_random_uniform_function(cls):
        """
        Registers the random method as used to generate a random sample from a uniform distribution in the interval [offset, offset + scale).
        """
        symbol = FunctionSymbol(name=cls.RANDOM_UNIFORM, param_types=[PredefinedTypes.get_template_type(0), PredefinedTypes.get_template_type(0)], return_type=PredefinedTypes.get_template_type(0), element_reference=None, is_predefined=True)
        cls.name2function[cls.RANDOM_UNIFORM] = symbol

    @classmethod
    def __register_time_resolution_function(cls):
        """
        Registers the time resolution function.
        """
        symbol = FunctionSymbol(name=cls.TIME_RESOLUTION, param_types=list(), return_type=PredefinedTypes.get_type('ms'), element_reference=None, is_predefined=True, scope=None)
        cls.name2function[cls.TIME_RESOLUTION] = symbol

    @classmethod
    def __register_exp1_function(cls):
        """
        Registers the alternative version of the exponent function, exp1.
        """
        params = list()
        params.append(PredefinedTypes.get_real_type())
        symbol = FunctionSymbol(name=cls.EXPM1, param_types=params, return_type=PredefinedTypes.get_real_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.EXPM1] = symbol

    @classmethod
    def __register_delta_function(cls):
        """
        Registers the delta function.
        """
        params = list()
        params.append(PredefinedTypes.get_type('ms'))
        params.append(PredefinedTypes.get_type('ms'))
        symbol = FunctionSymbol(name=cls.DELTA, param_types=params, return_type=PredefinedTypes.get_real_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.DELTA] = symbol

    @classmethod
    def __register_clip_function(cls):
        """
        Registers the clip function (bound a number between a minimum and a
        maximum value).
        """
        params = list()
        params.append(PredefinedTypes.get_template_type(0))
        params.append(PredefinedTypes.get_template_type(0))
        params.append(PredefinedTypes.get_template_type(0))
        symbol = FunctionSymbol(name=cls.CLIP, param_types=params, return_type=PredefinedTypes.get_template_type(0), element_reference=None, is_predefined=True)
        cls.name2function[cls.CLIP] = symbol

    @classmethod
    def __register_max_function(cls):
        """
        Registers the maximum function.
        """
        params = list()
        params.append(PredefinedTypes.get_template_type(0))
        params.append(PredefinedTypes.get_template_type(0))
        symbol = FunctionSymbol(name=cls.MAX, param_types=params, return_type=PredefinedTypes.get_template_type(0), element_reference=None, is_predefined=True)
        cls.name2function[cls.MAX] = symbol

    @classmethod
    def __register_min_function(cls):
        """
        Registers the minimum function.
        """
        params = list()
        params.append(PredefinedTypes.get_template_type(0))
        params.append(PredefinedTypes.get_template_type(0))
        symbol = FunctionSymbol(name=cls.MIN, param_types=params, return_type=PredefinedTypes.get_template_type(0), element_reference=None, is_predefined=True)
        cls.name2function[cls.MIN] = symbol

    @classmethod
    def __register_integrated_odes_function(cls):
        """
        Registers the integrate-odes function.
        """
        params = list()
        symbol = FunctionSymbol(name=cls.INTEGRATE_ODES, param_types=params, return_type=PredefinedTypes.get_void_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.INTEGRATE_ODES] = symbol

    @classmethod
    def __register_curr_sum_function(cls):
        """
        Registers the curr_sum function into scope.
        """
        params = list()
        params.append(PredefinedTypes.get_type('pA'))
        params.append(PredefinedTypes.get_real_type())
        symbol = FunctionSymbol(name=cls.CURR_SUM, param_types=params, return_type=PredefinedTypes.get_type('pA'), element_reference=None, is_predefined=True)
        cls.name2function[cls.CURR_SUM] = symbol

    @classmethod
    def __register_cond_sum_function(cls):
        """
        Registers the cond_sum function into scope.
        """
        params = list()
        params.append(PredefinedTypes.get_type('nS'))
        params.append(PredefinedTypes.get_real_type())
        symbol = FunctionSymbol(name=cls.COND_SUM, param_types=params, return_type=PredefinedTypes.get_type('nS'), element_reference=None, is_predefined=True)
        cls.name2function[cls.COND_SUM] = symbol

    @classmethod
    def __register_convolve(cls):
        """
        Registers the convolve function into the system.
        """
        params = list()
        params.append(PredefinedTypes.get_real_type())
        params.append(PredefinedTypes.get_real_type())
        symbol = FunctionSymbol(name=cls.CONVOLVE, param_types=params, return_type=PredefinedTypes.get_real_type(), element_reference=None, is_predefined=True)
        cls.name2function[cls.CONVOLVE] = symbol

    @classmethod
    def get_function_symbols(cls):
        """
        Returns a copy of the dict containing all predefined functions symbols.
        :return: a copy of the dict containing the functions symbols
        :rtype: dict(FunctionSymbol)
        """
        return cls.name2function

    @classmethod
    def get_function(cls, name):
        """
        Returns a copy of a element in the set of defined functions if one exists, otherwise None
        :param name: the name of the function symbol
        :type name: str
        :return: a copy of the element if such exists in the dict, otherwise None
        :rtype: None or FunctionSymbol
        """
        assert name is not None and isinstance(name, str), '(PyNestML.SymbolTable.PredefinedFunctions) No or wrong type of name provided (%s)!' % type(name)
        if name in cls.name2function.keys():
            return cls.name2function[name]
        else:
            return