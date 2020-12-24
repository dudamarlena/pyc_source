# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cw12401/code/work/isambard/src/isambard/optimisation/mmc_optimizer.py
# Compiled at: 2018-04-18 05:35:22
# Size of source mod 2**32: 11394 bytes
"""Provides optimisation of structure using Metropolis Monte Carlo."""
import copy, enum, math, random, sys, numpy

def float_f(f):
    """Formats a float for printing to std out."""
    return '{:.0f}'.format(f)


class MMCParameterType(enum.Enum):
    __doc__ = 'Defines the types of parameters that can be used for Monte Carlo.'
    STATIC_VALUE = 1
    DISCRETE_RANGE = 2
    LIST = 3
    UNIFORM_DIST = 4
    NORMAL_DIST = 5


class MMCParameter:
    __doc__ = 'Defines parameters used in the MMC optimizer.\n\n    Parameters\n    ----------\n    label : str\n        The name of the parameter.\n    parameter_type : MMCParameterType\n        The type of the parameter.\n    static_dist_or_list\n        The values used to create the parameter. For example, if the\n        parameter types is "STATIC_VALUE" then this can be any object,\n        if it is "LIST" then it should be a list of values and if it\n        is "UNIFORM_DIST" then it should be (mu, sigma) etc.\n    starting_value, optional\n        The initial value of the parameter.\n\n    Attributes\n    ----------\n    label : str\n        The name of the parameter.\n    parameter_type : MMCParameterType\n        The type of the parameter.\n    static_dist_or_list\n        The values used to create the parameter. For example, if the\n        parameter types is "STATIC_VALUE" then this can be any object,\n        if it is "LIST" then it should be a list of values and if it\n        is "UNIFORM_DIST" then it should be (mu, sigma) etc.\n    starting_value\n        The initial value of the parameter.\n    current_value\n        The currently accepted value for the parameter.\n    proposed_value\n        A new value proposed for the parameter that has not been\n        accepted.\n    '

    def __init__(self, label, parameter_type, static_dist_or_list, starting_value=None):
        self.label = label
        self.parameter_type = parameter_type
        self.current_value = None
        self.static_dist_or_list = static_dist_or_list
        if starting_value is None:
            if self.parameter_type is MMCParameterType.STATIC_VALUE:
                self.starting_value = static_dist_or_list
                self.current_value = self.starting_value
            else:
                self.randomise_proposed_value()
                self.starting_value = self.proposed_value
                self.accept_proposed_value()
        else:
            self.starting_value = starting_value
            self.current_value = self.starting_value
        self.proposed_value = None

    def randomise_proposed_value(self):
        """Creates a randomly the proposed value.

        Raises
        ------
        TypeError
            Raised if this method is called on a static value.
        TypeError
            Raised if the parameter type is unknown.
        """
        if self.parameter_type is MMCParameterType.UNIFORM_DIST:
            a, b = self.static_dist_or_list
            self.proposed_value = random.uniform(a, b)
        else:
            if self.parameter_type is MMCParameterType.NORMAL_DIST:
                mu, sigma = self.static_dist_or_list
                self.proposed_value = random.normalvariate(mu, sigma)
            else:
                if self.parameter_type is MMCParameterType.DISCRETE_RANGE:
                    min_v, max_v, step = self.static_dist_or_list
                    self.proposed_value = random.choice(numpy.arange(min_v, max_v, step))
                else:
                    if self.parameter_type is MMCParameterType.LIST:
                        self.proposed_value = random.choice(self.static_dist_or_list)
                    else:
                        if self.parameter_type is MMCParameterType.STATIC_VALUE:
                            raise TypeError('This value is static, it cannot be mutated.')
                        else:
                            raise TypeError('Cannot randomise this parameter, unknown parameter type.')

    def accept_proposed_value(self):
        """Changes the current value to the proposed value."""
        if self.proposed_value is not None:
            self.current_value = self.proposed_value
            self.proposed_value = None

    def reject_proposed_value(self):
        """Removes the proposed value."""
        self.proposed_value = None

    def __repr__(self):
        return '<MMCParameter: {}, {}, {}, {}>'.format(self.label, self.parameter_type, self.static_dist_or_list, self.current_value)


class MMCParameterOptimisation:
    __doc__ = 'Performs Metropolis Monte Carlo opimisation on a specification.\n\n    References\n    ----------\n    .. [0] Metropolis N, Rosenbluth AW, Rosenbluth MN, Teller AH and\n       Teller E (1953) Equations of State Calculations by Fast\n       Computing Machines, Journal of Chemical Physics. 21 (6),\n       1087-1092.\n\n    Parameters\n    ----------\n    specification : isambard.Specification\n        Any ISAMBARD specification. This will be used to create models\n        during the optimisation.\n    parameters : [MMCParameter]\n        Parameters to be optimised. The order of the parameters should\n        match the init signiture of the specification.\n    sequences : [str]\n        The sequences to be used during the optimisation.\n    eval_function : f(ampal) -> float\n        A function that takes an AMPAL object as an input and returns\n        a float. By default the `buff_interaction_energy` will be\n        used to evaluate the structure.\n\n    Attributes\n    ----------\n    specification : isambard.Specification\n        Any ISAMBARD specification. This will be used to create models\n        during the optimisation.\n    parameters : [MMCParameter]\n        Parameters to be optimised. The order of the parameters should\n        match the init signiture of the specification.\n    sequences : [str]\n        The sequences to be used during the optimisation.\n    eval_function : f(ampal) -> float\n        A function that takes an AMPAL object as an input and returns\n        a float. By default the `buff_interaction_energy` will be\n        used to evaluate the structure.\n    current_energy : float\n        The energy of the current structure.\n    best_energy : float\n        The best energy observed for any model.\n    best_parameters : [MMCParameter]\n        The parameters associated with the `best_energy`.\n    best_model : AMPAL Object\n        The model associated with the `best_energy`.\n    '
    current_energy = None
    best_energy = None
    best_parameters = None
    best_model = None

    def __init__(self, specification, parameters, sequences, eval_function):
        self.specification = specification
        self.current_parameters = copy.deepcopy(parameters)
        self.sequences = sequences
        self.eval_function = eval_function

    def start_optimisation(self, rounds, temp=298.15):
        """Begin the optimisation run.

        Parameters
        ----------
        rounds : int
            The number of rounds of optimisation to perform.
        temp : float, optional
            The temperature (in K) used during the optimisation.
        """
        self._generate_initial_model()
        self._mmc_loop(rounds, temp=temp)

    def _generate_initial_model(self):
        """Creates the initial model for the optimistation.

        Raises
        ------
        TypeError
            Raised if the model failed to build. This could be due to
            parameters being passed to the specification in the wrong
            format.
        """
        initial_parameters = [p.current_value for p in self.current_parameters]
        try:
            initial_model = (self.specification)(*initial_parameters)
        except TypeError:
            raise TypeError('Failed to build initial model. Make sure that the input parameters match the number and order of arguements expected by the input specification.')

        initial_model.pack_new_sequences(self.sequences)
        self.current_energy = self.eval_function(initial_model)
        self.best_energy = copy.deepcopy(self.current_energy)
        self.best_parameters = copy.deepcopy(self.current_parameters)
        self.best_model = initial_model

    def _mmc_loop(self, rounds, temp=298.15, verbose=True):
        """The main MMC loop.

        Parameters
        ----------
        rounds : int
            The number of rounds of optimisation to perform.
        temp : float, optional
            The temperature (in K) used during the optimisation.
        verbose : bool, optional
            If true, prints information about the run to std out.
        """
        current_round = 0
        while current_round < rounds:
            modifiable = list(filter(lambda p: p.parameter_type is not MMCParameterType.STATIC_VALUE, self.current_parameters))
            chosen_parameter = random.choice(modifiable)
            if chosen_parameter.parameter_type is MMCParameterType.UNIFORM_DIST:
                chosen_parameter.randomise_proposed_value()
            else:
                chosen_parameter.randomise_proposed_value()
            proposed_parameters = [p.current_value if p.proposed_value is None else p.proposed_value for p in self.current_parameters]
            model = (self.specification)(*proposed_parameters)
            model.pack_new_sequences(self.sequences)
            proposed_energy = self.eval_function(model)
            if verbose:
                sys.stdout.write('\rRound: {}, Current energy: {}, Proposed energy: {} (best {}), {}.       '.format(current_round, float_f(self.current_energy), float_f(proposed_energy), float_f(self.best_energy), 'ACCEPTED' if self.check_move(proposed_energy,
                  (self.current_energy), t=temp) else 'DECLINED'))
                sys.stdout.flush()
            if self.check_move(proposed_energy, (self.current_energy), t=temp):
                for p in self.current_parameters:
                    p.accept_proposed_value()

                self.current_energy = proposed_energy
                if self.current_energy < self.best_energy:
                    self.best_energy = copy.deepcopy(self.current_energy)
                    self.best_parameters = copy.deepcopy(self.current_parameters)
                    self.best_model = model
            else:
                for p in self.current_parameters:
                    p.reject_proposed_value()

            current_round += 1

    @staticmethod
    def check_move(new, old, t):
        """Determines if a model will be accepted.

        Uses Boltzmann distribution scaled by temperature in Kelvin."""
        if t <= 0 or numpy.isclose(t, 0.0):
            return False
        else:
            K_BOLTZ = 0.0083144621
            if new < old:
                return True
            move_prob = math.exp(-(new - old) / (K_BOLTZ * t))
            if move_prob > random.uniform(0, 1):
                return True
            return False


__author__ = 'Christopher W. Wood'