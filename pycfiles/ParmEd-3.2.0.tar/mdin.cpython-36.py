# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/amber/mdin/mdin.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 18893 bytes
"""
This module will create an amber mdin file for either sander or      
pmemd (or others). The program specification loads the appropriate   
dictionaries with default values, etc. It can read and write mdins. 

                           GPL LICENSE INFO                             

Copyright (C) 2009 - 2014 Dwight Mcgee, Bill Miller III, and Jason Swails

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
from parmed.amber.mdin.cntrl import cntrl
from parmed.amber.mdin.ewald import ewald
from parmed.amber.mdin.pb import pb
from parmed.amber.mdin.qmmm import qmmm
from parmed.exceptions import InputError
from parmed.utils.six import string_types
from parmed.utils.six.moves import range

def addOn(line, string, file):
    if len(line.strip()) == 0:
        return line + string
    else:
        if len(line) + len(string) > 40:
            file.write(line + '\n')
            return ' ' + string
        return line + string


class Mdin(object):

    def __init__(self, program='sander', verbosity=1):
        self.program = program
        self.cntrl_obj = cntrl()
        self.ewald_obj = ewald()
        self.pb_obj = pb()
        self.qmmm_obj = qmmm()
        self.verbosity = 0
        self.cards = []
        self.cntrl_nml = {}
        self.cntrl_nml_defaults = {}
        self.ewald_nml = {}
        self.ewald_nml_defaults = {}
        self.pb_nml = {}
        self.pb_nml_defaults = {}
        self.qmmm_nml = {}
        self.qmmm_nml_defaults = {}
        self.valid_namelists = []
        self.title = 'mdin prepared by mdin.py'
        if self.program == 'sander':
            self.cntrl_nml = self.cntrl_obj.sander
            self.ewald_nml = self.ewald_obj.sander
            self.pb_nml = self.pb_obj.sander
            self.qmmm_nml = self.qmmm_obj.sander
            self.valid_namelists = ['cntrl', 'ewald', 'qmmm', 'pb']
        else:
            if self.program == 'sander.APBS':
                self.cntrl_nml = self.cntrl_obj.sander
                self.pb_nml = self.pb_obj.sanderAPBS
                self.valid_namelists = ['cntrl', 'apbs']
            else:
                if self.program == 'pmemd':
                    self.cntrl_nml = self.cntrl_obj.pmemd
                    self.ewald_nml = self.ewald_obj.pmemd
                    self.valid_namelists = ['cntrl', 'ewald']
                else:
                    raise InputError('Error: program (%s) unrecognized!' % self.program)
        self.cntrl_nml_defaults = self.cntrl_nml.copy()
        self.ewald_nml_defaults = self.ewald_nml.copy()
        self.pb_nml_defaults = self.pb_nml.copy()
        self.qmmm_nml_defaults = self.qmmm_nml.copy()

    def write(self, filename='mdin'):
        file = open(filename, 'w')
        file.write(self.title + '\n')
        file.write('&cntrl\n')
        line = ' '
        for var in self.cntrl_nml.keys():
            if self.cntrl_nml[var] == self.cntrl_nml_defaults[var]:
                pass
            else:
                if isinstance(self.cntrl_nml[var], string_types):
                    line = addOn(line, "%s='%s', " % (var, self.cntrl_nml[var]), file)
                else:
                    line = addOn(line, '%s=%s, ' % (var, self.cntrl_nml[var]), file)

        if len(line.strip()) != 0:
            file.write(line + '\n')
        file.write('/\n')
        line = ' '
        has_been_printed = False
        for var in self.ewald_nml.keys():
            if self.ewald_nml[var] == self.ewald_nml_defaults[var]:
                pass
            else:
                if not has_been_printed:
                    file.write('&ewald\n')
                    has_been_printed = True
                if isinstance(self.ewald_nml_defaults[var], string_types):
                    line = addOn(line, "%s='%s', " % (var, self.ewald_nml[var]), file)
                else:
                    line = addOn(line, "%s='%s', " % (var, self.ewald_nml[var]), file)

        if len(line.strip()) != 0:
            file.write(line + '\n')
        if has_been_printed:
            file.write('/\n')
        line = ' '
        has_been_printed = False
        for var in self.pb_nml.keys():
            if self.pb_nml[var] == self.pb_nml_defaults[var]:
                continue
            else:
                if not has_been_printed:
                    if self.program == 'sander.APBS':
                        file.write('&apbs\n')
                    else:
                        file.write('&pb\n')
                    has_been_printed = True
                if isinstance(self.pb_nml[var], string_types):
                    line = addOn(line, "%s='%s', " % (var, self.pb_nml[var]), file)
                else:
                    line = addOn(line, '%s=%s, ' % (var, self.pb_nml[var]), file)

        if len(line.strip()) != 0:
            file.write(line + '\n')
        if has_been_printed:
            file.write('/\n')
        line = ' '
        has_been_printed = False
        if self.cntrl_nml['ifqnt'] == 1:
            for var in self.qmmm_nml.keys():
                if self.qmmm_nml[var] == self.qmmm_nml_defaults[var]:
                    pass
                elif not has_been_printed:
                    file.write('&qmmm\n')
                    has_been_printed = True
                else:
                    if isinstance(self.qmmm_nml_defaults[var], string_types):
                        line = addOn(line, "%s='%s', " % (var, self.qmmm_nml[var]), file)
                    else:
                        line = addOn(line, '%s=%s, ' % (var, self.qmmm_nml[var]), file)

            if len(line.strip()) != 0:
                file.write(line + '\n')
            if has_been_printed:
                file.write('/\n')
        for i in range(len(self.cards)):
            file.write(self.cards[i].strip() + '\n')

        if len(self.cards) != 0:
            file.write('END\n')
        file.close()

    def read(self, filename='mdin'):
        lines = open(filename, 'r').readlines()
        blocks = []
        block_fields = []
        inblock = False
        lead_comment = True
        for i in range(len(lines)):
            if not inblock:
                if not lines[i].strip().startswith('&'):
                    if lead_comment:
                        continue
            if not inblock and not lines[i].strip().startswith('&') and not lead_comment:
                final_ended = True
                for j in range(i, len(lines)):
                    if lines[j].strip().startswith('&'):
                        final_ended = False

                if final_ended:
                    if len(lines[i].strip()) != 0:
                        self.cards.append(lines[i])
            else:
                if not inblock and lines[i].strip().startswith('&'):
                    lead_comment = False
                    inblock = True
                    block = lines[i].strip()[1:].lower()
                    blocks.append(block)
                    block_fields.append([])
                    if block not in self.valid_namelists:
                        raise InputError('Invalid namelist (%s) in input file (%s) for %s' % (
                         lines[i].strip(), filename,
                         self.program))
                    else:
                        if inblock:
                            if lines[i].strip() == '/' or lines[i].strip() == '&end':
                                inblock = False
                        if inblock:
                            if lines[i].strip().startswith('&'):
                                raise InputError('Invalid input file (%s). Terminate each namelist before another is started' % filename)
                        if inblock:
                            items = lines[i].strip().split(',')
                            j = 0
                            while j < len(items):
                                items[j] = items[j].strip()
                                if len(items[j]) == 0:
                                    items.pop(j)
                                else:
                                    j += 1

                            block_fields[(len(block_fields) - 1)].extend(items)

        if len(self.cards) != 0:
            if self.cards[(len(self.cards) - 1)].strip().upper() == 'END':
                self.cards.pop()
        begin_field = -1
        for i in range(len(block_fields)):
            for j in range(len(block_fields[i])):
                if '=' not in block_fields[i][j]:
                    if begin_field == -1:
                        raise InputError('Invalid input file (%s).' % filename)
                    else:
                        block_fields[i][begin_field] += ',' + block_fields[i][j]
                else:
                    begin_field = j

        for i in range(len(block_fields)):
            for j in range(len(block_fields[i])):
                if '=' not in block_fields[i][j]:
                    continue
                else:
                    var = block_fields[i][j].split('=')
                    self.change(blocks[i], var[0].strip(), var[1].strip())

    def change(self, namelist, variable, value):
        """ Change the value of a variable without adding a new key-pair """
        variable = variable.lower()
        if isinstance(value, string_types):
            if value.startswith('"') and value.endswith('"') or value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
        else:
            if namelist == 'cntrl':
                if variable in self.cntrl_nml.keys():
                    mytype = type(self.cntrl_nml_defaults[variable])
                    self.cntrl_nml[variable] = mytype(value)
                else:
                    raise InputError('Unknown variable (%s) in &cntrl!' % variable)
            else:
                if namelist == 'ewald':
                    if variable in self.ewald_nml.keys():
                        mytype = type(self.ewald_nml_defaults[variable])
                        self.ewald_nml[variable] = mytype(value)
                    else:
                        raise InputError('Unknown variable (%s) in &ewald!' % variable)
                else:
                    if namelist == 'pb' or namelist == 'apbs':
                        if variable in self.pb_nml.keys():
                            mytype = type(self.pb_nml_defaults[variable])
                            self.pb_nml[variable] = mytype(value)
                        else:
                            raise InputError('Unknown variable (%s) in &%s!' % (
                             variable, namelist))
                    else:
                        if namelist == 'qmmm':
                            if variable in self.qmmm_nml.keys():
                                mytype = type(self.qmmm_nml_defaults[variable])
                                self.qmmm_nml[variable] = mytype(value)
                            else:
                                raise InputError('Unknown variable (%s) in &qmmm' % variable)
                        else:
                            raise InputError('Unknown namelist (%s)!' % namelist)

    def check(self):
        return True

    def SHAKE(self):
        self.change('cntrl', 'ntf', 2)
        self.change('cntrl', 'ntc', 2)
        self.change('cntrl', 'dt', 0.002)

    def constPressure(self, press=1.0, taup=1.0):
        self.change('cntrl', 'ntb', 2)
        self.change('cntrl', 'ntp', 1)
        self.change('cntrl', 'pres0', press)
        self.change('cntrl', 'taup', taup)

    def constVolume(self):
        self.change('cntrl', 'ntb', 1)
        self.change('cntrl', 'ntp', 0)

    def constTemp(self, ntt=3, temp=300.0, gamma_ln=2.0, ig=-1, tautp=1.0):
        self.change('cntrl', 'ntt', ntt)
        self.change('cntrl', 'temp0', temp)
        self.change('cntrl', 'tempi', temp)
        self.change('cntrl', 'gamma_ln', gamma_ln if ntt == 3 else 0)
        self.change('cntrl', 'ig', ig)
        self.change('cntrl', 'tautp', tautp)

    def constpH(self, solvph=7.0, igb=2, ntcnstph=10):
        self.change('cntrl', 'icnstph', 1)
        self.change('cntrl', 'solvph', solvph)
        self.change('cntrl', 'ntcnstph', ntcnstph)
        self.change('cntrl', 'igb', igb)
        self.change('cntrl', 'ntb', 0)
        self.change('cntrl', 'saltcon', 0.1)

    def restrainHeavyAtoms(self, restraint_wt=0.0):
        self.change('cntrl', 'ntr', 1)
        self.change('cntrl', 'restraint_wt', restraint_wt)
        self.change('cntrl', 'restraintmask', '!@H=')

    def restrainBackbone(self, restraint_wt=0.0):
        self.change('cntrl', 'ntr', 1)
        self.change('cntrl', 'restraint_wt', restraint_wt)
        self.change('cntrl', 'restraintmask', '@N,CA,C')

    def genBorn(self, igb=5, rgbmax=25.0):
        self.change('cntrl', 'igb', igb)
        self.change('cntrl', 'ntb', 0)
        self.change('cntrl', 'ntp', 0)
        self.change('cntrl', 'rgbmax', rgbmax)

    def time(self, time=1000.0, dt=-1):
        if dt == -1:
            if self.cntrl_nml['ntc'] == 2:
                if self.cntrl_nml['ntf'] == 2:
                    dt = 0.002
            else:
                dt = 0.001
        time = int(time / dt)
        self.change('cntrl', 'dt', dt)
        self.change('cntrl', 'nstlim', time)
        self.change('cntrl', 'imin', 0)

    def heat(self, tempi=0.0, temp0=300.0, ntt=3, tautp=5.0, ig=-1, gamma_ln=5.0):
        self.constVolume()
        self.change('cntrl', 'tempi', tempi)
        self.change('cntrl', 'temp0', temp0)
        self.change('cntrl', 'ntt', ntt)
        self.change('cntrl', 'tautp', tautp)
        self.change('cntrl', 'ig', ig)
        self.change('cntrl', 'gamma_ln', gamma_ln if ntt == 3 else 0)

    def restart(self, ntx=5):
        self.change('cntrl', 'irest', 1)
        self.change('cntrl', 'ntx', ntx)

    def TI(self, clambda=0.0):
        self.change('cntrl', 'clambda', clambda)
        self.change('cntrl', 'icfe', 1)

    def softcore_TI(self, scalpha=0.5, scmask='', crgmask='', logdvdl=0):
        self.change('cntrl', 'icfe', 1)
        self.change('cntrl', 'ifsc', 1)
        self.change('cntrl', 'scalpha', scalpha)
        self.change('cntrl', 'scmask', scmask)
        self.change('cntrl', 'crgmask', crgmask)
        self.change('cntrl', 'logdvdl', logdvdl)

    def minimization(self, imin=1, maxcyc=1, ncyc=10, ntmin=1):
        self.change('cntrl', 'imin', imin)
        self.change('cntrl', 'maxcyc', maxcyc)
        self.change('cntrl', 'ncyc', ncyc)
        self.change('cntrl', 'ntmin', ntmin)

    def AddCard(self, title='Residues in card', cardString='RES 1'):
        self.cards.append('%s\n%s\nEND' % (title, cardString))