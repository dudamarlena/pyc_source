# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/probabilities/models/R3models.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 7512 bytes
from mvc.models.properties import BoolProperty, FloatProperty
from pyxrd.generic.mathtext_support import mt_range
from pyxrd.generic.io import storables
from pyxrd.generic.utils import not_none
from pyxrd.generic.models.properties import InheritableMixin
from pyxrd.refinement.refinables.properties import RefinableMixin
from .base_models import _AbstractProbability
from mvc.models.properties.action_mixins import SetActionMixin
__all__ = [
 'R3G2Model']

@storables.register()
class R3G2Model(_AbstractProbability):
    __doc__ = "\n    (Restricted) probability model for Reichweite 3 with 2 components.\n    \n    The (due to restrictions only) 2 independent variables are:\n    \n    .. math::\n        :nowrap:\n        \n        \\begin{align*}\n            & W_1\n            & P_{1111} \\text{(if $\\nicefrac{2}{3} \\leq W_1 < \\nicefrac{3}{4}$) or} P_{2112} \\text{(if $\\nicefrac{3}{4} \\leq W_1 \\leq 1)$} \\\\\n        \\end{align*}\n    \n    This model can only describe mixed layers with more than \n    :math:`\\nicefrac{2}{3}` of the layers being of the first type, no two layers\n    of the second type occur after each other, and in which the probability of\n    finding a layer of the first type in between two layers of the second type\n    is zero. This translates to the following conditions:\n    \n    .. math::\n        :nowrap:\n        \n        \\begin{align*}\n\t        & \\nicefrac{2}{3} <= W_1 <= 1 \\\\\n\t        & P_{22} = 0  \\\\\n\t        & P_{212} = 0 \\\\\n\t        & \\\\\n\t        & \\text{Since $P_{22} = 0$ and $P_{212} = 0$:} \\\\\n            & P_{1122} = P_{1212} = 0 \\\\\n            & \\text{And thus:} \\\\\n            & P_{1121} = P_{1211} = 1 \\\\\n        \\end{align*} \n        \n    The following probabilities are undefined, but are set to zero or one to\n    make the validation correct. This doesn't matter much, since the weight\n    fractions these probabilities are multiplied with, equal zero anyway\n    (e.g. :math:`W_{2211} = W_{22} * P_{221} * P_{2211}` and :math:`W_{22}` \n    is zero since :math:`P_{22}` is zero):\n        \n    .. math::\n        :nowrap:\n        \n        \\begin{align*}\n            & P_{1121} &= P_{1211} &= P_{2211} \n            &= P_{2121} &= P_{2221} &= P_{1221} = 0 \\\\\n            & P_{1122} &= P_{1212} &= P_{2212} \n            &= P_{2122} &= P_{2222} &= P_{1222} = 1 \\\\\n        \\end{align*}  \n\n    The remaining probabilities and weight fractions can be calculated as \n    follows:\n    \n   .. math::\n        :nowrap:\n        \n        \\begin{align*}\n            & W_2 = 1 - W_1 \\\\\n            & \\\\\n            & \\text{if $W_1 < \\nicefrac{3}{4}$:} \\\\\n            & \\quad \\text{$P_{1111}$ is given}\\\\\n            & \\quad P_{1112} = 1 - P_{1111} \\\\\n            & \\quad P_{2111} = P_{1112} * \\frac{W_1 - 2 \\cdot W_2}{W_2} \\\\\n            & \\quad P_{2112} = 1 - P_{2111} \\\\  \n            & \\\\\n            & \\text{if $W_1 \\geq \\nicefrac{3}{4}$:} \\\\\n            & \\quad \\text{$P_{2112}$ is given}\\\\\n            & \\quad P_{2111} = 1 - P_{2112} \\\\\n            & \\quad P_{1111} = P_{2111} * \\frac{W_2}{W_1 - 2 \\cdot W_2} \\\\\n            & \\quad P_{1112} = 1 - P_{1111} \\\\  \n            & \\\\\n            & W_{111} = 3 \\cdot W_1 - 2 \\\\\n            & W_{212} = W_{221} = W_{222} = W_{122} = 0 \\\\\n            & W_{211} = W_{121} = W_{112} = 1 - W_1 \\\\\n        \\end{align*}\n\t\n\t"

    class Meta(_AbstractProbability.Meta):
        store_id = 'R3G2Model'

    _G = 2
    inherit_W1 = BoolProperty(default=False,
      text='Inherit flag for W1',
      persistent=True,
      visible=True,
      set_action_name='update',
      mix_with=(
     SetActionMixin,))
    W1 = FloatProperty(default=0.85,
      text='W1 (> 2/3)',
      math_text='$W_1 (> \\frac{2}{3})$',
      persistent=True,
      visible=True,
      refinable=True,
      store_private=True,
      minimum=0.6666666666666666,
      maximum=1.0,
      is_independent=True,
      inheritable=True,
      inherit_flag='inherit_W1',
      inherit_from='parent.based_on.probabilities.W1',
      set_action_name='update',
      mix_with=(
     SetActionMixin, RefinableMixin, InheritableMixin))
    inherit_P1111_or_P2112 = BoolProperty(default=False,
      text='Inherit flag for P1111_or_P2112',
      persistent=True,
      visible=True,
      set_action_name='update',
      mix_with=(
     SetActionMixin,))
    P1111_or_P2112 = FloatProperty(default=0.75,
      text='P1111 (W1 < 3/4) or\nP2112 (W1 > 3/4)',
      math_text=('$P_{1111} %s$ or $\\newline P_{2112} %s$' % (
     mt_range(0.6666666666666666, 'W_1', 0.75),
     mt_range(0.75, 'W_1', 1.0))),
      persistent=True,
      visible=True,
      refinable=True,
      store_private=True,
      minimum=0.0,
      maximum=1.0,
      is_independent=True,
      inheritable=True,
      inherit_flag='inherit_P1111_or_P2112',
      inherit_from='parent.based_on.probabilities.P1111_or_P2112',
      set_action_name='update',
      mix_with=(
     SetActionMixin, RefinableMixin, InheritableMixin))

    def __init__(self, W1=0.85, P1111_or_P2112=0.75, *args, **kwargs):
        (super(R3G2Model, self).__init__)(args, R=3, **kwargs)
        with self.data_changed.hold():
            self.W1 = not_none(W1, 0.85)
            self.P1111_or_P2112 = not_none(P1111_or_P2112, 0.75)
            self.update()

    def update(self):
        with self.monitor_changes():
            self.mW[0] = self.W1
            self.mW[1] = 1.0 - self.W1
            if self.mW[0] <= 0.75:
                self.mP[(0, 0, 0, 0)] = self.P1111_or_P2112
                self.mP[(0, 0, 0, 1)] = max(min(1.0 - self.mP[(0, 0, 0, 0)], 1.0), 0.0)
                self.mP[(1, 0, 0, 0)] = max(min(self.mP[(0, 0, 0, 1)] * (self.mW[0] - 2 * self.mW[1]) / self.mW[1], 1.0), 0.0)
                self.mP[(1, 0, 0, 1)] = max(min(1.0 - self.mP[(1, 0, 0, 0)], 1.0), 0.0)
            else:
                self.mP[(1, 0, 0, 1)] = self.P1111_or_P2112
                self.mP[(1, 0, 0, 0)] = max(min(1.0 - self.mP[(1, 0, 0, 1)], 1.0), 0.0)
                self.mP[(0, 0, 0, 0)] = max(min(1.0 - self.mP[(1, 0, 0, 0)] * self.mW[1] / (self.mW[0] - 2 * self.mW[1]), 1.0), 0.0)
                self.mP[(0, 0, 0, 1)] = max(min(1.0 - self.mP[(0, 0, 0, 0)], 1.0), 0.0)
            self.mP[(0, 0, 1, 0)] = 1.0
            self.mP[(0, 0, 1, 1)] = 0.0
            self.mP[(0, 1, 0, 0)] = 1.0
            self.mP[(0, 1, 0, 1)] = 0.0
            self.mP[(0, 1, 1, 0)] = 1.0
            self.mP[(0, 1, 1, 1)] = 0.0
            self.mP[(1, 0, 1, 0)] = 1.0
            self.mP[(1, 0, 1, 1)] = 0.0
            self.mP[(1, 1, 0, 0)] = 1.0
            self.mP[(1, 1, 0, 1)] = 0.0
            self.mP[(1, 1, 1, 0)] = 1.0
            self.mP[(1, 1, 1, 1)] = 0.0
            self.mW[(0, 0, 0)] = max(min(3 * self.mW[0] - 2, 1.0), 0.0)
            self.mW[(1, 0, 1)] = self.mW[(1, 1, 0)] = self.mW[(1, 1, 1)] = self.mW[(0,
                                                                                    1,
                                                                                    1)] = 0.0
            self.mW[(1, 0, 0)] = self.mW[(0, 1, 0)] = self.mW[(0, 0, 1)] = max(min(1 - self.mW[0], 1.0), 0.0)
            self.solve()
            self.validate()