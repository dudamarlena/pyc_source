# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/constants/xrf.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 17828 bytes
from __future__ import absolute_import, division, print_function
from collections import Mapping
import logging, numpy as np, six
from ..utils import NotInstalledError
from ..constants.basic import BasicElement, doc_title, doc_params, doc_attrs, doc_ex
from ..utils import verbosedict
logger = logging.getLogger(__name__)
line_name = [
 'Ka1', 'Ka2', 'Kb1', 'Kb2', 'La1', 'La2', 'Lb1', 'Lb2',
 'Lb3', 'Lb4', 'Lb5', 'Lg1', 'Lg2', 'Lg3', 'Lg4', 'Ll',
 'Ln', 'Ma1', 'Ma2', 'Mb', 'Mg']
bindingE = [
 'K', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5', 'N1',
 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'O1', 'O2', 'O3',
 'O4', 'O5', 'P1', 'P2', 'P3']

class XraylibNotInstalledError(NotInstalledError):
    message_post = 'xraylib is not installed. Please see https://github.com/tschoonj/xraylib or https://binstar.org/tacaswell/xraylib for help on installing xraylib'

    def __init__(self, caller, *args, **kwargs):
        message = 'The call to {} cannot be completed because {}'.format(caller, self.message_post)
        super(XraylibNotInstalledError, self).__init__(message, *args, **kwargs)


try:
    import xraylib
except ImportError:
    logger.warning('Xraylib is not installed on your machine. ' + XraylibNotInstalledError.message_post)
    xraylib = None

if xraylib is None:
    pass
else:
    xraylib.XRayInit()
    xraylib.SetErrorMessages(0)
    line_list = [
     xraylib.KA1_LINE, xraylib.KA2_LINE, xraylib.KB1_LINE,
     xraylib.KB2_LINE, xraylib.LA1_LINE, xraylib.LA2_LINE,
     xraylib.LB1_LINE, xraylib.LB2_LINE, xraylib.LB3_LINE,
     xraylib.LB4_LINE, xraylib.LB5_LINE, xraylib.LG1_LINE,
     xraylib.LG2_LINE, xraylib.LG3_LINE, xraylib.LG4_LINE,
     xraylib.LL_LINE, xraylib.LE_LINE, xraylib.MA1_LINE,
     xraylib.MA2_LINE, xraylib.MB_LINE, xraylib.MG_LINE]
    shell_list = [
     xraylib.K_SHELL, xraylib.L1_SHELL, xraylib.L2_SHELL,
     xraylib.L3_SHELL, xraylib.M1_SHELL, xraylib.M2_SHELL,
     xraylib.M3_SHELL, xraylib.M4_SHELL, xraylib.M5_SHELL,
     xraylib.N1_SHELL, xraylib.N2_SHELL, xraylib.N3_SHELL,
     xraylib.N4_SHELL, xraylib.N5_SHELL, xraylib.N6_SHELL,
     xraylib.N7_SHELL, xraylib.O1_SHELL, xraylib.O2_SHELL,
     xraylib.O3_SHELL, xraylib.O4_SHELL, xraylib.O5_SHELL,
     xraylib.P1_SHELL, xraylib.P2_SHELL, xraylib.P3_SHELL]
    line_dict = verbosedict((k.lower(), v) for k, v in zip(line_name, line_list))
    shell_dict = verbosedict((k.lower(), v) for k, v in zip(bindingE, shell_list))
    XRAYLIB_MAP = verbosedict({'lines': (line_dict, xraylib.LineEnergy), 
     'cs': (line_dict, xraylib.CS_FluorLine_Kissel), 
     'binding_e': (shell_dict, xraylib.EdgeEnergy), 
     'jump': (shell_dict, xraylib.JumpFactor), 
     'yield': (shell_dict, xraylib.FluorYield)})

class XrayLibWrap(Mapping):
    __doc__ = "High-level interface to xraylib.\n\n    This class exposes various functions in xraylib\n\n    This is an interface to wrap xraylib to perform calculation related\n    to xray fluorescence.\n\n    The code does one to one map between user options,\n    such as emission line, or binding energy, to xraylib function calls.\n\n    Parameters\n    ----------\n    element : int\n        atomic number\n    info_type : {'lines',  'binding_e', 'jump', 'yield'}\n        option to choose which physics quantity to calculate as follows:\n        :lines: emission lines\n        :binding_e: binding energy\n        :jump: absorption jump factor\n        :yield: fluorescence yield\n\n    Attributes\n    ----------\n    info_type : str\n\n\n    Examples\n    --------\n    Access the lines for zinc\n\n    >>> x = XrayLibWrap(30, 'lines') # 30 is atomic number for element Zn\n\n    Access the energy of the Kα1 line.\n\n    >>> x['Ka1'] # energy of emission line Ka1\n    8.047800064086914\n\n    List all of the lines and their energies\n\n    >>> x.all  # list energy of all the lines\n    [(u'ka1', 8.047800064086914),\n     (u'ka2', 8.027899742126465),\n     (u'kb1', 8.90530014038086),\n     (u'kb2', 0.0),\n     (u'la1', 0.9294999837875366),\n     (u'la2', 0.9294999837875366),\n     (u'lb1', 0.949400007724762),\n     (u'lb2', 0.0),\n     (u'lb3', 1.0225000381469727),\n     (u'lb4', 1.0225000381469727),\n     (u'lb5', 0.0),\n     (u'lg1', 0.0),\n     (u'lg2', 0.0),\n     (u'lg3', 0.0),\n     (u'lg4', 0.0),\n     (u'll', 0.8112999796867371),\n     (u'ln', 0.8312000036239624),\n     (u'ma1', 0.0),\n     (u'ma2', 0.0),\n     (u'mb', 0.0),\n     (u'mg', 0.0)]\n    "
    opts_info_type = [
     'lines', 'binding_e', 'jump', 'yield']

    def __init__(self, element, info_type, energy=None):
        if xraylib is None:
            raise XraylibNotInstalledError(self.__class__)
        self._element = element
        self._map, self._func = XRAYLIB_MAP[info_type]
        self._keys = sorted(list(six.iterkeys(self._map)))
        self._info_type = info_type

    @property
    def all(self):
        """List the physics quantity for all the lines or shells.
        """
        return list(six.iteritems(self))

    def __getitem__(self, key):
        """
        Call xraylib function to calculate physics quantity.  A return
        value of 0 means that the quantity not valid.

        Parameters
        ----------
        key : str
            Define which physics quantity to calculate.
        """
        return self._func(self._element, self._map[key.lower()])

    def __iter__(self):
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)

    @property
    def info_type(self):
        """
        option to choose which physics quantity to calculate as follows:

        """
        return self._info_type


class XrayLibWrap_Energy(XrayLibWrap):
    __doc__ = "\n    This is an interface to wrap xraylib\n    to perform calculation on fluorescence\n    cross section, or other incident energy\n    related quantity.\n\n    Attributes\n    ----------\n    incident_energy : float\n    info_type : str\n\n    Parameters\n    ----------\n    element : int\n        atomic number\n    info_type : {'cs'}, optional\n        option to calculate physics quantities which depend on\n        incident energy.\n        See Class attribute `opts_info_type` for valid options\n\n        :cs: cross section, unit in cm2/g\n\n    incident_energy : float\n        incident energy for fluorescence in KeV\n\n    Examples\n    --------\n    >>> # Cross section of zinc with an incident X-ray at 12 KeV\n    >>> x = XrayLibWrap_Energy(30, 'cs', 12)\n    >>> # Compute the cross section of the Kα1 line.\n    >>> x['Ka1'] # cross section for Ka1, unit in cm2/g\n    34.44424057006836\n    "
    opts_info_type = ['cs']

    def __init__(self, element, info_type, incident_energy):
        if xraylib is None:
            raise XraylibNotInstalledError(self.__class__)
        super(XrayLibWrap_Energy, self).__init__(element, info_type)
        self._incident_energy = incident_energy

    @property
    def incident_energy(self):
        """
        Incident x-ray energy in keV, float
        """
        return self._incident_energy

    @incident_energy.setter
    def incident_energy(self, val):
        """
        Parameters
        ----------
        val : float
            new incident x-ray energy in keV
        """
        self._incident_energy = float(val)

    def __getitem__(self, key):
        """
        Call xraylib function to calculate physics quantity.

        Parameters
        ----------
        key : str
            defines which physics quantity to calculate
        """
        return self._func(self._element, self._map[key.lower()], self._incident_energy)


doc_title = '\n    Object to return all the elemental information related to fluorescence\n    '
doc_params = doc_params
doc_attrs += '    emission_line : `XrayLibWrap`\n    cs : function\n    bind_energy : `XrayLibWrap`\n    jump_factor : `XrayLibWrap`\n    fluor_yield : `XrayLibWrap`\n    '
doc_ex += ">>> # Get the emission energy for the Kα1 line.\n    >>> e.emission_line['Ka1'] #\n    8.638900756835938\n\n    >>> Cross section for emission line Kα1 with 10 keV incident energy\n    >>> e.cs(10)['Ka1']\n    54.756561279296875\n\n    >>> # fluorescence yield for K shell\n    >>> e.fluor_yield['K']\n    0.46936899423599243\n\n    >>> # Find all emission lines within with in the range [9.5, 10.5]\n    >>> # keV with an incident energy of 12 KeV.\n    >>> e.find(10, 0.5, 12)\n    {'kb1': 9.571999549865723}\n\n    >>> # List all of the known emission lines\n    >>> e.emission_line.all # list all the emission lines\n    [('ka1', 8.638900756835938),\n     ('ka2', 8.615799903869629),\n     ('kb1', 9.571999549865723),\n     ('kb2', 0.0),\n     ('la1', 1.0116000175476074),\n     ('la2', 1.0116000175476074),\n     ('lb1', 1.0346999168395996),\n     ('lb2', 0.0),\n     ('lb3', 1.1069999933242798),\n     ('lb4', 1.1069999933242798),\n     ('lb5', 0.0),\n     ('lg1', 0.0),\n     ('lg2', 0.0),\n     ('lg3', 0.0),\n     ('lg4', 0.0),\n     ('ll', 0.8837999701499939),\n     ('ln', 0.9069000482559204),\n     ('ma1', 0.0),\n     ('ma2', 0.0),\n     ('mb', 0.0),\n     ('mg', 0.0)]\n\n    >>> # List all of the known cross sections\n    >>> e.cs(10).all\n    [('ka1', 54.756561279296875),\n     ('ka2', 28.13692855834961),\n     ('kb1', 7.509212970733643),\n     ('kb2', 0.0),\n     ('la1', 0.13898827135562897),\n     ('la2', 0.01567710004746914),\n     ('lb1', 0.0791187509894371),\n     ('lb2', 0.0),\n     ('lb3', 0.004138986114412546),\n     ('lb4', 0.002259803470224142),\n     ('lb5', 0.0),\n     ('lg1', 0.0),\n     ('lg2', 0.0),\n     ('lg3', 0.0),\n     ('lg4', 0.0),\n     ('ll', 0.008727769367396832),\n     ('ln', 0.00407258840277791),\n     ('ma1', 0.0),\n     ('ma2', 0.0),\n     ('mb', 0.0),\n     ('mg', 0.0)]\n    "

class XrfElement(BasicElement):
    __doc__ = '{}\n    Parameters\n    ----------{}\n    Attributes\n    ----------{}\n    Examples\n    --------{}\n    '.format(doc_title, doc_params, doc_attrs, doc_ex)

    def __init__(self, element):
        if xraylib is None:
            raise XraylibNotInstalledError(self.__class__)
        super(XrfElement, self).__init__(element)
        self._emission_line = XrayLibWrap(self.Z, 'lines')
        self._bind_energy = XrayLibWrap(self.Z, 'binding_e')
        self._jump_factor = XrayLibWrap(self.Z, 'jump')
        self._fluor_yield = XrayLibWrap(self.Z, 'yield')

    @property
    def emission_line(self):
        """Emission line information, `XrayLibWrap`

        Emission line can be used as a unique characteristic
        for qualitative identification of the element.
        line is string type and defined as 'Ka1', 'Kb1'.
        unit in KeV
        """
        return self._emission_line

    @property
    def cs(self):
        """Fluorescence cross section function, `function`

        Returns a function of energy which returns the
        elemental cross section in cm2/g

        The signature of the function is ::

           x_section = func(enery)

        where `energy` in in keV and `x_section` is in
        cm²/g
        """

        def myfunc(incident_energy):
            return XrayLibWrap_Energy(self.Z, 'cs', incident_energy)

        return myfunc

    @property
    def bind_energy(self):
        """Binding energy, `XrayLibWrap`

        Binding energy is a measure of the energy required
        to free electrons from their atomic orbits.
        shell is string type and defined as "K", "L1".
        unit in KeV
        """
        return self._bind_energy

    @property
    def jump_factor(self):
        """Jump Factor, `XrayLibWrap`

        Absorption jump factor is defined as the fraction
        of the total absorption that is associated with
        a given shell rather than for any other shell.
        shell is string type and defined as "K", "L1".
        """
        return self._jump_factor

    @property
    def fluor_yield(self):
        """fluorescence quantum yield, `XrayLibWrap`

        The fluorescence quantum yield gives the efficiency
        of the fluorescence process, and is defined as the ratio of the
        number of photons emitted to the number of photons absorbed.
        shell is string type and defined as "K", "L1".
        """
        return self._fluor_yield

    def line_near(self, energy, delta_e, incident_energy):
        """
        Find possible emission lines given the element.

        Parameters
        ----------
        energy : float
            Energy value to search for
        delta_e : float
            Define search range (energy - delta_e, energy + delta_e)
        incident_energy : float
            incident energy of x-ray in KeV

        Returns
        -------
        dict
            all possible emission lines
        """
        out_dict = dict()
        for k, v in six.iteritems(self.emission_line):
            if self.cs(incident_energy)[k] == 0:
                pass
            elif np.abs(v - energy) < delta_e:
                out_dict[k] = v

        return out_dict


def emission_line_search(line_e, delta_e, incident_energy, element_list=None):
    """Find elements which have an emission line near an energy

    This function returns a dict keyed on element type of all
    elements that have an emission line with in `delta_e` of
    `line_e` at the given x-ray energy.

    Parameters
    ----------
    line_e : float
         energy value to search for in KeV
    delta_e : float
         difference compared to energy in KeV
    incident_energy : float
        incident x-ray energy in KeV
    element_list : list, optional
         List of elements to restrict search to. If no list is present,
         search on all elements.
         Element abbreviations can be any mix of upper and
         lower case, e.g., Hg, hG, hg, HG

    Returns
    -------
    lines_dict : dict
        element and associate emission lines

    """
    if xraylib is None:
        raise XraylibNotInstalledError(__name__)
    if element_list is None:
        element_list = range(1, 101)
    search_list = [XrfElement(item) for item in element_list]
    cand_lines = [e.line_near(line_e, delta_e, incident_energy) for e in search_list]
    out_dict = dict()
    for e, lines in zip(search_list, cand_lines):
        if lines:
            out_dict[e.sym] = lines

    return out_dict