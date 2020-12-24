# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\phaseshifts\leed.py
# Compiled at: 2014-09-04 17:03:27
"""
Provides CLEED validator and Converter classes.

The CLEED_validator() class provides a method for checking 
the input files for errors, whereas the Converter.import_CLEED()
method allows importing CLEED input files as a MTZ_model class 

"""
import os, sys
from phaseshifts import model
from phaseshifts.elements import ELEMENTS
try:
    from io import IOBase
except ImportError:
    from io import iobase as IOBase

from math import sqrt, pow
from glob import glob

class CLEED_validator(object):
    """
    Class for validation of CLEED input files
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    @staticmethod
    def is_CLEED_file(filename):
        """
        Determine if file is a CLEED input file
        
        Returns
        -------
        True
            if a valid filename ending in any of .bul, .inp, .bsr, .bmin
            
        False
            otherwise 
        """
        try:
            filename = glob(os.path.expanduser(os.path.expandvars(filename)))[0]
        except IndexError:
            raise IOError("filename '%s' not found" % filename)

        if not os.path.isfile(filename):
            return False
        else:
            ext = os.path.splitext(filename)[1]
            if ext not in ('.bmin', '.bul', '.inp', '.pmin'):
                if ext != '.i':
                    sys.stderr.write('Warning: %s is not a valid CLEED extension\n' % filename)
                    sys.stderr.flush()
                return False
            return True

    def validate(self, filename, aoi=False):
        r"""
        Checks CLEED input file for errors
        
        Parameters
        ----------
        filename : str
            Path to input file. Should be \*.bul , \*.ctr, \*.inp or \*.bmin
        aoi : bool
            Check for angle of incidence parameters

        """
        filename = glob(os.path.expanduser(os.path.expandvars(filename)))[0]
        basename, ext = os.path.splitext(filename)
        if isinstance(ext, int):
            aoi = True
            basename, ext = os.path.splitext(basename)
        if ext in ('.bul', '.bmin', '.bsr'):
            filetype = 'bulk'
        else:
            if ext in ('.inp', '.pmin', '.par'):
                filetype = 'surface'
            else:
                if ext == '.ctr':
                    filetype = 'control'
                else:
                    if ext == '.mkiv':
                        filetype = 'make_iv'
                    else:
                        with open(filename, 'r') as (f):
                            lines = ('').join([ line.lstrip() for line in f if not line.lstrip().startswith('#')
                                              ])
                            if 'ef=' in lines and 'ti=' in lines and 'id=' in lines and 'wt=' in lines:
                                filetype = 'control'
                            elif 'pb:' in lines and ('ei:' in lines or 'ef:' in lines or 'es:' in lines or 'ep:' in lines or 'vi:' in lines or 'vr:' in lines or 'lm:' in lines or 'm1:' in lines or 'm2:' in lines):
                                filetype = 'bulk'
                            elif 'po:' in lines and ('a1:' in lines or 'a2:' in lines or 'm1:' in lines or 'm2:' in lines):
                                filetype = 'surface'
                            elif 'po:' in lines and not ('a1:' in lines or 'a2:' in lines or 'm1:' in lines or 'm2:' in lines):
                                filetype = 'parameter'
                            else:
                                raise IOError("unknown CLEED format for file '%s'" % filename)
                    with open(filename, 'r') as (f):
                        lines = [ line for line in f ]
                    with open(filename, 'w') as (f):
                        for i, line in enumerate(lines):
                            line = line.lstrip().rstrip()
                            if not line.startswith('#') or line.startswith(''):
                                if line.startswith('po:'):
                                    if filetype not in ('surface', 'parameter'):
                                        sys.stderr.write('warning: commented out line %i\n' % i)
                                        sys.stderr.flush()
                                        line = '#' + line
                                else:
                                    sys.stderr.write('warning: commented out line %i\n' % i)
                                    sys.stderr.flush()
                                    line = '#' + line
                                if filetype == 'bulk' or filetype == 'surface':
                                    pass
                            f.write(line + '\r\n')
                            sys.stderr.flush()

                    try:
                        basis = [ line for line in lines if line.startswith('a') and int(line[1]) <= 3 and int(line[1]) > 0
                                ]
                    except ValueError:
                        raise ValueError("'%s' is not a valid basis vector" % line[:2])

                    try:
                        minimum_radii = [ ('').join(line.split(':')[1].split()[:4]) for line in lines if line.startswith('rm:')
                                        ]
                    except ValueError:
                        raise ValueError("'%s' is not a valid minimum radius input" % line[:2])

                    radii_dict = {}
                    for radius in minimum_radii:
                        tag, value = zip((str, float), radius.split()[:2])
                        radii_dict[tag] = value

                try:
                    overlayer_atoms = [ ('').join(line.split(':')[1].split()[:4]) for line in lines if line.startswith('po:') ]
                except ValueError:
                    raise ValueError("'%s' is not a valid overlayer atom input" % line[:2])

            try:
                bulk_atoms = [ ('').join(line.split(':')[1].split()[:4]) for line in lines if line.startswith('pb:')
                             ]
            except ValueError:
                raise ValueError("'%s' is not a valid overlayer atom input" % line[:2])


class Converter(object):
    """
    Convert different input into phaseshift compatible input
    
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    @staticmethod
    def import_CLEED(filename, **kwargs):
        """
        Imports CLEED input file and converts model to muffin-tin input.
         
        It assumes the following:
          * the basis vectors :math:`a_1`, :math:`a_2`, & :math:`a_3` are 
            :math:`x`,:math:`y`,:math:`z` cartezian coordinates
          * if no :math:`a_3` is found, the maximum :math:`z` distance between 
          atoms multiplied by four is given.
          * the unitcell is converted from cartezian to fractional coordinates
          * atom sites are converted from Angstrom to Bohr units
          * additional info from the phase shift filename is provided by 
            splitting the '_' chars:
              1. First string segment is element or symbol, e.g. Ni
              2. Second string segment is the oxidation (valence), e.g. +2
          * lines with :code:`rm:` provide the radii dictionary of the 
            individual phase shifts, whereas lines starting with 
            :code:`lmax:` provide the lmax dictionary for individual phase 
            shifts. Additionally, the valency can be given in lines 
            starting with :code:`ox:`. Both bulk and surface input files 
            will be searched for these.
          * if no :code:`rm:` found for that species, the atomic radius is used 
            for zero valence, otherwise the covalent radius is used.
          * if no lmax values are found for the specific phase shift, then the
            global value will be used instead.
          * if no valence values are found for the specific phase shift, then 
            the guessed oxidation value from the phase shift filename is used 
            instead. However, if the oxidation state cannot be parsed using 
            the filename then a default oxidation state of zero is used.
           
        Additional information can, however, be provided using 'phs:' at the 
        start of a line within the input file and may have the following 
        formats:
          1. "**phs:** c *<float>* nh *<int>* nform *<int>* exchange *<float>*"
          2. "**phs:** *<phase_shift>* valence *<float>* radius *<float>*"
          
        The identifiers ``exchange``, ``nform``, ``valence`` and ``radius`` may 
        be abbreviated to ``exc``, ``nf``, ``val`` and ``rad``, respectively.
        
        Information given in this manner overrides any other input.
         
        
        Parameters
        ----------
        filename : str
            Path to input file.
            
        Returns
        -------
        phaseshifts.model.MTZ_model
        
        Raises
        ------
        IOError : filename invalid
        ValueError : bad formatting of input

        """
        try:
            verbose = kwargs['verbose']
        except KeyError:
            verbose = False

        if not isinstance(filename, str):
            raise IOError("'%s' is not a string" % filename)
        filename = glob(os.path.expanduser(os.path.expandvars(filename)))[0]
        if os.path.isdir(filename):
            raise IOError("'%s' is a directory, not a file" % filename)
        else:
            if os.path.isfile(filename):
                name, ext = os.path.splitext(filename)
                if ext in ('.bul', '.bmin'):
                    other_input = name + '.inp'
                else:
                    if ext in ('.inp', '.pmin', '.par'):
                        other_input = name + '.bul'
                    try:
                        with open(other_input, 'r') as (f):
                            other_lines = [ line for line in f ]
                    except IOError:
                        other_lines = []

            else:
                raise IOError("cannot open '%s'" % filename)
            with open(filename, 'r') as (f):
                lines = [ line.lstrip() for line in f if not line.lstrip().startswith('#')
                        ]
            atoms = []
            radii_dict = {}
            lmax_dict = {}
            oxidation_dict = {}
            unitcell = model.Unitcell(1, 2, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            z_dist = 4.0
            z_min = sys.float_info.max
            z_max = sys.float_info.min
            try:
                alpha = float([ line.split(':')[1] for line in lines if line.startswith('alpha:') or line.startswith('exchange:') or line.startswith('exc:')
                              ][0])
            except (ValueError, IndexError):
                alpha = None

            basis = [ line for line in lines if line.startswith('a') and int(line[1]) <= 3 and int(line[1]) > 0
                    ]
            a1 = a2 = a3 = [
             0.0, 0.0, 0.0]
            for vector_line in basis:
                line = (' ').join(vector_line.replace(':', '').split()[:4])
                try:
                    vector_str, x, y, z = [ t(s) for t, s in zip((
                     str, float, float, float), line.split())
                                          ]
                except ValueError:
                    raise ValueError("'%s' is not a valid basis vector" % vector_line.replace('\n', ''))

                exec '%s = [%f, %f, %f]' % (vector_str, x, y, z)

            zmin = sys.float_info.max
            a = zmax = sys.float_info.min
            for vector in [a1, a2, a3]:
                len_a = sqrt(pow(vector[0], 2) + pow(vector[1], 2))
                if len_a > a:
                    a = len_a
                if vector[2] < zmin:
                    zmin = vector[2]
                if vector[2] > zmax:
                    zmax = vector[2]

            try:
                minimum_radii = [ (' ').join(line.split(':')[1].split()[:4]) for line in lines + other_lines if line.startswith('rm:')
                                ]
                for radius in minimum_radii:
                    tag, value = zip((str, float), radius.split()[:2])
                    radii_dict[tag] = value

            except ValueError:
                raise ValueError("'%s' is not a valid minimum radius input" % line[:2])

            try:
                lmax_values = [ (' ').join(line.split(':')[1].split()[:4]) for line in lines + other_lines if line.startswith('lmax:')
                              ]
                for lmax_str in lmax_values:
                    tag, value = [ t(s) for t, s in zip((str, int), lmax_str.split()[:2])
                                 ]
                    lmax_dict[tag] = value

            except ValueError:
                raise ValueError("'%s' is not a valid lmax input" % line[:2])

            try:
                oxidation_values = [ (' ').join(line.split(':')[1].split()[:4]) for line in lines + other_lines if line.startswith('val:')
                                   ]
                for oxi_str in oxidation_values:
                    tag, value = [ t(s) for t, s in zip((str, float), oxi_str.split()[:2])
                                 ]
                    oxidation_dict[tag] = value

            except ValueError:
                raise ValueError("'%s' is not a valid valency (oxidation state)" % line[:2])

            overlayer_atoms = [ (' ').join(line.split(':')[1].split()[:4]) for line in lines if line.startswith('po:')
                              ]
            for overlayer_atom in overlayer_atoms:
                try:
                    id_str, x, y, z = [ t(s) for t, s in zip((str, float,
                     float, float), overlayer_atom.split())
                                      ]
                except ValueError:
                    raise ValueError("'%s' line input is invalid")

                id_str = os.path.basename(os.path.expanduser(os.path.expandvars(id_str)))
                element = id_str.split('_')[0]
                element = ('').join([ ch for ch in element if ch.isalpha() ])
                if element not in ELEMENTS:
                    raise NameError("Unknown element '%s' from phase shift name'%s'" % (
                     element, id_str))
                oxidation = None
                if id_str in oxidation_dict:
                    oxidation = oxidation_dict[id_str]
                else:
                    try:
                        try:
                            oxidation = str(id_str.split('_')[1])
                            if oxidation.startswith('-') or oxidation.startswith('+'):
                                oxidation = float(oxidation)
                            elif oxidation.endswith('-') or oxidation.endswith('+'):
                                if oxidation.endswith('-'):
                                    oxidation = float(oxidation.rstrip('-'))
                                else:
                                    oxidation = float(oxidation.rstrip('+'))
                            else:
                                oxidation = 0.0
                        except (IndexError, ValueError):
                            pass

                    finally:
                        if oxidation is None:
                            oxidation = 0.0

                rm = None
                try:
                    rm = radii_dict[id_str]
                except KeyError:
                    pass

                lmax = None
                try:
                    lmax = lmax_dict[id_str]
                except KeyError:
                    pass

                if lmax is None:
                    try:
                        substrings = [ s for s in id_str.lower().split('_') if s.startswith('lmax')
                                     ]
                        if substrings:
                            lmax = int(('').join([ s for s in substrings[0] if s.isdigit()
                                                 ]))
                    except ValueError:
                        pass

                if rm and lmax:
                    atom = model.Atom(element, [x, y, z], tag=id_str, valence=oxidation, radius=rm, lmax=lmax)
                elif rm and not lmax:
                    atom = model.Atom(element, [x, y, z], tag=id_str, valence=oxidation, radius=rm)
                elif not rm and lmax:
                    atom = model.Atom(element, [x, y, z], tag=id_str, valence=oxidation, lmax=lmax)
                else:
                    atom = model.Atom(element, [x, y, z], tag=id_str, valence=oxidation)
                if z < z_min:
                    z_min = z
                if z > z_max:
                    z_max = z
                atoms.append(atom)

            bulk_atoms = [ (' ').join(line.split(':')[1].split()[:4]) for line in lines if line.startswith('pb:')
                         ]
            if verbose:
                print 'CLEED model'
                print '\tbulk atoms: %s' % [ s for s in bulk_atoms ]
            for bulk_atom in bulk_atoms:
                try:
                    id_str, x, y, z = [ t(s) for t, s in zip((
                     str, float, float, float), bulk_atom.split())
                                      ]
                    id_str = os.path.basename(os.path.expanduser(os.path.expandvars(id_str)))
                    element = id_str.split('_')[0]
                    element = ('').join([ ch for ch in element if ch.isalpha() ])
                    if element not in ELEMENTS:
                        raise NameError("Unknown element '%s' from phase shift name'%s'" % (
                         element, id_str))
                except ValueError:
                    print "'%s' line input is invalid"
                    raise ValueError("'%s' line input is invalid")

                oxidation = None
                if id_str in oxidation_dict:
                    oxidation = oxidation_dict[id_str]
                else:
                    try:
                        try:
                            oxidation = str(id_str.split('_')[1])
                            if oxidation.startswith('-') or oxidation.startswith('+'):
                                oxidation = float(oxidation)
                            elif oxidation.endswith('-') or oxidation.endswith('+'):
                                if oxidation.endswith('-'):
                                    oxidation = float(oxidation.rstrip('-'))
                                else:
                                    oxidation = float(oxidation.rstrip('+'))
                            else:
                                oxidation = 0.0
                        except (IndexError, ValueError):
                            pass

                    finally:
                        if oxidation is None:
                            oxidation = 0.0

                rm = None
                if id_str in radii_dict:
                    rm = radii_dict[id_str]
                lmax = None
                if id_str in lmax_dict:
                    lmax = lmax_dict[id_str]
                if rm and lmax:
                    atom = model.Atom(element, [x, y, z], tag=id_str, valence=oxidation, radius=rm, lmax=lmax)
                elif rm and not lmax:
                    atom = model.Atom(element, [x, y, z], tag=id_str, valence=oxidation, radius=rm)
                elif not rm and lmax:
                    atom = model.Atom(element, [x, y, z], tag=id_str, valence=oxidation, lmax=lmax)
                else:
                    atom = model.Atom(element, [x, y, z], tag=id_str, valence=oxidation)
                if z < z_min:
                    z_min = z
                if z > z_max:
                    z_max = z
                atoms.append(atom)

            for vector in [a1, a2, a3]:
                vector = [ x / a for x in vector ]

            if a3 == [0.0, 0.0, 0.0]:
                z_dist = (z_max - z_min) / float(a) / 0.529
                c = z_dist * 5
                a3[2] = c
            else:
                c = a3[2] / float(a) / 0.529
            unitcell = model.Unitcell(a, c, [a1, a2, a3])
            mtz_model = model.MTZ_model(unitcell, atoms)
            if alpha:
                mtz_model.set_exchange(alpha)
            phs_lines = [ line.lower().lstrip('phs:').rstrip('#') for line in lines if line.lower().startswith('phs:')
                        ]
            for line in phs_lines:
                strings = line.split()
                phase_shift = strings[0]
                phs_atoms = [ atom.tag for atom in mtz_model.atoms if atom.tag == phase_shift
                            ]
                if phase_shift not in phs_atoms:
                    for i in range(len(strings)):
                        try:
                            if strings[i] == 'c':
                                c = strings[i] / float(a) / 0.529
                                mtz_model.unitcell.set_c(c)
                            elif strings[i] == 'nh':
                                mtz_model.set_nh(strings[(i + 1)])
                            elif strings[i] == 'exc' or strings[i] == 'exchange':
                                mtz_model.set_exchange(strings[(i + 1)])
                            elif strings[i] == 'nf' or strings[i] == 'nform':
                                mtz_model.set_nform(strings[(i + 1)])
                        except IndexError:
                            break

                else:
                    for i in range(1, len(strings)):
                        try:
                            if strings[i] == 'val' or strings[i] == 'valence':
                                for atom in phs_atoms:
                                    atom.valence = float(strings[(i + 1)])

                            elif strings[i] == 'rad' or strings[i] == 'radius':
                                for atom in phs_atoms:
                                    atom.radius = float(strings[(i + 1)])

                        except IndexError:
                            break

        return mtz_model


class CSearch(object):
    """class for csearch related data exchange"""

    def __init__(self, model_name, leed_command=None):
        self.set_Model(model_name)
        self._getResults()

    def setModel(self, name):
        """sets the model name"""
        self.model = str(name)

    def getIteration(self, iteration):
        try:
            with open(self.model + '.log', 'r') as (f):
                return [ line for line in f if line.startswith('#') and 'par' in line ][int(iteration)]
        except (IndexError, ValueError, IOError):
            return

        return

    def getRFactor(self, iteration):
        pass

    def getTimeStamp(self, iteration):
        pass

    def _getResults(self):
        pass