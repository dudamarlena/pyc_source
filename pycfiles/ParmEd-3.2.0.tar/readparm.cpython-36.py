# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/amber/readparm.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 3611 bytes
"""
This module is simply a namespace for all Amber topology-like classes. There are
different variants; for instance the standard Amber topology, the chamber-made
topology, and the tinker_to_amber-made topology. These classes are all defined
in their own private modules, but imported here to simplify the API.

Copyright (C) 2010 - 2014  Jason Swails

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
   
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""
from parmed.amber.amberformat import AmberFormat
from parmed.amber._amberparm import AmberParm, Rst7
from parmed.amber._chamberparm import ChamberParm, ConvertFromPSF
from parmed.amber._tinkerparm import AmoebaParm, BeemanRestart
from parmed.utils.six import string_types
assert BeemanRestart and ConvertFromPSF
__all__ = [
 'AmberFormat', 'AmberParm', 'ChamberParm', 'LoadParm', 'Rst7']

def LoadParm(parmname, xyz=None, box=None):
    """
    Loads a topology file using the correct class.

    Parameters
    ----------
    parmname : ``str``
        The name of the topology file to load
    xyz : str or array, optional
        If provided, the coordinates and unit cell dimensions from the provided
        Amber inpcrd/restart file will be loaded into the molecule, or the
        coordinates will be loaded from the coordinate array
    box : array, optional
        If provided, the unit cell information will be set from the provided
        unit cell dimensions (a, b, c, alpha, beta, and gamma, respectively)

    Returns
    -------
    parm : :class:`AmberParm` (or subclass)
        This function parses the topology file, determines if it is an
        Amber-style (i.e., *traditional* Amber force field), Chamber-style
        (i.e., CHARMM force field), or Amoeba-style (i.e., Amoeba force field),
        and then returns an instance of the appropriate type.
    """
    from parmed import load_file
    from parmed.constants import IFBOX
    parm = AmberFormat(parmname)
    if 'CTITLE' in parm.flag_list:
        parm = parm.view_as(ChamberParm)
    else:
        if 'AMOEBA_FORCEFIELD' in parm.flag_list:
            parm = parm.view_as(AmoebaParm)
        else:
            parm = parm.view_as(AmberParm)
        if isinstance(xyz, string_types):
            f = load_file(xyz)
            if not hasattr(f, 'coordinates') or f.coordinates is None:
                raise TypeError('%s does not have coordinates' % xyz)
            parm.coordinates = f.coordinates
            if hasattr(f, 'box'):
                if f.box is not None:
                    if box is None:
                        parm.box = f.box
        else:
            parm.coordinates = xyz
    if box is not None:
        parm.box = box
    if parm.parm_data['POINTERS'][IFBOX] > 0 and parm.box is None:
        box = parm.parm_data['BOX_DIMENSIONS']
        parm.box = list(box[1:]) + [box[0], box[0], box[0]]
    parm.hasbox = parm.box is not None
    return parm