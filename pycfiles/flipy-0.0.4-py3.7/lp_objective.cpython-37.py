# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flipy/lp_objective.py
# Compiled at: 2020-03-11 10:59:56
# Size of source mod 2**32: 1945 bytes
from typing import Optional, Mapping, Union, Type
from flipy.lp_variable import LpVariable
from flipy.lp_expression import LpExpression
from flipy.utils import Numeric

class Minimize:
    __doc__ = ' A class representing a minimization problem '


class Maximize:
    __doc__ = ' A class representing a maximization problem '


ObjectiveType = Type[Union[(Minimize, Maximize)]]

class LpObjective(LpExpression):
    __doc__ = ' A class representing an objective function '

    def __init__(self, name='', expression=None, constant=0, sense=Minimize):
        """ Initialize the objective

        Parameters
        ----------
        name:
            The name of the objective
        expression:
            Dictionary representing variables and their coefficients
        constant:
            The constant term of the objective
        sense:
            Whether to minimize or maximize the objective
        """
        super(LpObjective, self).__init__(name, expression, constant)
        self._sense = None
        self.sense = sense

    @property
    def sense(self) -> ObjectiveType:
        """ Getter for the sense of the objective

        Returns
        -------
        flipy.lp_objective.ObjectiveType
        """
        return self._sense

    @sense.setter
    def sense(self, sense: ObjectiveType) -> None:
        """ Setter for the sens eof the objective. Raises error if not valid sense.

        Raises
        ------
        ValueError
            If `sense` is not one of `flipy.lp_objective.Minimize` or `flipy.lp_objective.Maximize`

        Parameters
        ----------
        sense: flipy.lp_objective.Minimize or flipy.lp_objective.Maximize
        """
        if sense not in [Minimize, Maximize]:
            raise ValueError('Sense must be one of %s, %s not %s' % (Minimize, Maximize, sense))
        self._sense = sense