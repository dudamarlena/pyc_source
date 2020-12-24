# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/constants/basic.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 7128 bytes
from __future__ import absolute_import, division, print_function
import six
from collections import namedtuple
import functools, os, logging
logger = logging.getLogger(__name__)
data_dir = os.path.join(os.path.dirname(__file__), 'data')
element = namedtuple('element', [
 'Z', 'sym', 'name', 'atomic_radius',
 'covalent_radius', 'mass', 'bp', 'mp', 'density',
 'atomic_volume', 'coherent_scattering_length',
 'incoherent_crosssection', 'absorption', 'debye_temp',
 'thermal_conductivity'])

def read_atomic_constants():
    """Returns a dictionary of atomic constants

    Returns
    -------
    constants : dict
        keys: ['Z'. 'sym', 'name', 'atomic_radius', 'covalent_radius', 'mass',
               'bp', 'mp', 'density', 'atomic_volume',
               'coherent_scattering_length', 'incoherent_crosssection',
               'absorption', 'debye_temp', 'thermal_conductivity']
    """
    basic = {}
    field_desc = []
    with open(os.path.join(data_dir, 'AtomicConstants.dat'), 'r') as (infile):
        for line in infile:
            if line.split()[0] == '#S':
                s = line.split()
                abbrev = s[2]
                Z = int(s[1])
                if Z == 1000:
                    break
            elif not field_desc and line.split()[0] == '#L':
                field_desc = [
                 'Atomic number',
                 'Element symbol (Fe, Cr, etc.)',
                 'Full element name (Iron, Chromium, etc.']
                field_desc += line.split()[1:]
            elif line.startswith('#UNAME'):
                elem_name = line.split()[1]
            elif line[0] == '#':
                continue
            else:
                data = [float(item) for item in line.split()]
                data = [Z, abbrev, elem_name] + data
                elem = element(*data)
                basic[abbrev.lower()] = elem

    return (
     basic, field_desc)


basic, field_descriptors = read_atomic_constants()
basic.update({elm.Z:elm for elm in six.itervalues(basic)})
basic.update({elm.name.lower():elm for elm in six.itervalues(basic)})
basic.update({elm.sym.lower():elm for elm in six.itervalues(basic)})
doc_title = '\n    Object to return basic elemental information\n    '
doc_params = "\n    element : str or int\n        Element symbol, name or atomic number ('Zinc', 'Zn' or 30)\n    "
fields = ['Z : int', 'sym : str', 'name : str'] + ['{} : float'.format(field) for field in element._fields[3:]]
fields = ['{}\n        {}'.format(field, field_desc) for field, field_desc in zip(fields, field_descriptors)]
doc_attrs = '\n    ' + '\n    '.join(fields)
doc_ex = "\n    >>> # Create an `Element` object\n    >>> e = Element('Zn') # or e = Element(30)\n    >>> # get the atomic mass\n    >>> e.mass\n    65.37\n    >>> # get the density in grams / cm^3\n    >>> e.density\n    7.14\n    "

@functools.total_ordering
class BasicElement(object):
    __doc__ = '{}\n    Parameters\n    ----------{}\n    Attributes\n    ----------{}\n\n    Examples\n    --------{}\n    '.format(doc_title, doc_params, doc_attrs, doc_ex)

    def __init__(self, Z, *args, **kwargs):
        super(BasicElement, self).__init__(*args, **kwargs)
        if isinstance(Z, six.string_types):
            Z = Z.lower()
        self._element = basic[Z]
        for e in element._fields:
            setattr(self, e, getattr(basic[Z], e))

    def __getitem__(self, item):
        return getattr(self, item)

    def __repr__(self):
        return six.text_type('BasicElement({})'.format(self.Z))

    def __str__(self):
        desc = self.name + '\n' + '=' * len(self.name)
        for d in dir(self):
            if d.startswith('_'):
                pass
            else:
                desc += '\n{}: {}'.format(d, getattr(self, d))

        return desc

    def __eq__(self, other):
        return self.Z == other.Z

    def __lt__(self, other):
        return self.Z < other.Z