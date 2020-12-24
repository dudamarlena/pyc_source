# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benjaminweb/22_Projekte/Pareto/python/venv/lib/python3.6/site-packages/effectus/__init__.py
# Compiled at: 2017-01-31 19:12:20
# Size of source mod 2**32: 5067 bytes
"""
    effectus
    ~~~~~~~~

    effectus tells you which minority of causes provokes which
    majority of effects. You provide it with a series of numbers.
    It tells you whether a pareto distribution is present.

    :copyright: (c) 2017 by Benjamin Weber
    :license: MIT, see LICENSE for more details.
"""
from .core import make_summary, attain_effects, attain_causes, separate_causes, separate_effects
from .pareto import ratio
from .helpers import reduce_values, write_reduced_values, unfold_values, make_relations, sort_effects, format_summary
__all__ = [
 'make_summary', 'attain_effects', 'attain_causes',
 'separate_causes', 'separate_effects',
 'reduce_values', 'write_reduced_values', 'unfold_values',
 'ratio']

class Effects:
    __doc__ = 'Chief facility to assimilate and evaluate a series of effect values.\n\n    This class provides you all relevant information about the cause-\n    effect relationship in the given series of effect values. While\n    ``summary`` suffices in most cases, ``attain_effects`` and\n    ``attain_causes`` tell you which causes are required for the\n    given effects and vice versa. ``separate_effects`` and\n    ``separate_causes`` tell you the threshold you need to pick\n    values up to (including) to attain the given share of effects\n    or causes.\n\n    Args:\n        effect_values (List[number]): An iterable of effect values.\n        precision (int): Numbers of digits to round to.\n\n    Attributes:\n        summary (dict): Tells you which causes provoke which effects\n          in fractional notation.\n        summary_decimal (dict): Tells you which causes provoke which\n          effects in decimal notation.\n        ratio (float): entropy of ``effect_values`` in proportion\n          to ``control_limit``. If less or equal than one, a\n          pareto distribution is present.\n        pareto (bool): True if a pareto distribution is present.\n    '

    def __init__(self, effect_values, precision=3):
        """Assimilates series of effect values.

        Args:
            precision (int): Numbers of digits to round to.
        """
        self.relations = make_relations(effect_values)
        self.sorted_effects = sort_effects(effect_values)
        self.precision = precision
        self.ratio = ratio(effect_values, self.precision)
        self.pareto = self.ratio <= 1
        self.summary = make_summary(self.relations)

    def __repr__(self):
        causes, effects = format_summary(self.summary, self.precision)
        present_text = 'present'
        if self.pareto is False:
            present_text = 'not ' + present_text
        return '<pareto {0} [{1}]: {2} causes => {3} effects [total ∆: {4:.1f} %]>'.format(present_text, self.ratio, causes, effects, self.summary['variability'] * 100)

    def attain_effects(self, limit):
        """Tells you the causes required for the given share of effects.

        Args:
            limit (float): Share of effects between 0 and 1, including.

        Returns:
            Share of causes required for given share of effects as
            float value between 0 and 1.
        """
        return attain_effects(self.relations, limit, self.precision)

    def attain_causes(self, limit):
        """Tells you the effects required for the given share of causes.

        Args:
            limit (float): Share of causes between 0 and 1, including.

        Returns:
            Share of effects required for given share of causes as
            float value between 0 and 1.
        """
        return attain_causes(self.relations, limit, self.precision)

    def separate_effects(self, limit):
        """Tells you which effect values to pick for given share of effects.

        Args:
            limit (float): Share of effects between 0 and 1, including.

        Returns:
            Tuple like (5.4, 3, 4) telling you to pick all values less
            or equal 5.4 up to the third occurrence of 5.4 (including)
            to get the given share of effects. 4 tells you there are in
            total 4 values of 5.4 present.
        """
        return separate_effects(self.sorted_effects, limit, self.precision)

    def separate_causes(self, limit):
        """Tells you which effect values to pick for given share of causes.

        Args:
            limit (float): Share of causes between 0 and 1, including.

        Returns:
            Tuple like (5.4, 3, 4) telling you to pick all values less
            or equal 5.4 up to the third occurence of 5.4 (including)
            to get the given share of causes. 4 tells you there are in
            total 4 values of 5.4 present.
        """
        return separate_causes(self.sorted_effects, limit, self.precision)


__version__ = '1.0.0-dev4'
VERSION = __version__