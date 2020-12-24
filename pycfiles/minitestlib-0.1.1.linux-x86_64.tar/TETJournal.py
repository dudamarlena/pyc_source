# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/minitestlib/TETJournal.py
# Compiled at: 2009-01-22 06:18:57
"""
TetJournal - interpret TET journal file
"""
__author__ = 'Andy Shevchenko <andy.shevchenko@gmail.com>'
__revision__ = '$Id$'
__all__ = [
 'TETJournal']
import os
from minitestlib.Log import logger
from minitestlib.TestObject import TestObject

class TETJournalTP(TestObject):
    """ Representation of Test Purpose """

    def parse(self):
        """ Find result of execution """
        result = 'NORESULT'
        for line in self.lines:
            if line.split('|')[0] == '220':
                result = line.split('|')[2].strip('\n')

        self.dbg('Result is %s' % result)
        self.results[result] = 1
        self.amount = 1
        self.name = 'TP'


class TETJournalIC(TestObject):
    """ Representation of Invocation Case """

    def parse(self):
        """ Parse TPs for IC """
        flag = False
        key = 0
        new_tp = TETJournalTP(self, key)
        for line in self.lines:
            code = line.split('|')[0]
            if code in ('200', '410'):
                if flag:
                    new_tp.parse()
                    self.objects[key] = new_tp
                    key += 1
                    new_tp = TETJournalTP(self, key)
                    if code == '410':
                        flag = False
                elif code == '200':
                    flag = True
            if flag:
                new_tp.append(line)

        self.dbg('%d TPs were parsed' % key)
        self.name = 'IC'


class TETJournalBlock(TestObject):
    """ Representation of TET journal common block"""

    def __init__(self, parent, key):
        TestObject.__init__(self, parent, key)
        self.btype = 'empty'
        self.output = []
        self.parsed = False

    def get_output(self):
        """ Return output, parse block if needed """
        if not self.parsed:
            self.parse()
        return self.output

    def get_btype(self):
        """ Return block type, parse block if needed """
        if not self.parsed:
            self.parse()
        return self.btype

    def parse(self):
        """ Parse block to the logical sections """
        if self.parsed or len(self.lines) == 0:
            return
        try:
            custom_parse = getattr(self, '_parse')
            custom_parse()
        except AttributeError:
            self.dbg('_parse() is absent')

        self.name = '%s block' % self.btype
        for line in self.lines:
            if line.split('|')[0] in ('50', '100', '510'):
                self.output.append(line)

        self.parsed = True


class TETJournalHeaderBlock(TETJournalBlock):
    """ Header block in TET journal """

    def _parse(self):
        """ Custom parser """
        self.btype = 'header'


class TETJournalTextBlock(TETJournalBlock):
    """ Text block in TET journal """

    def _parse(self):
        """ Custom parser """
        self.btype = 'scenario'


class TETJournalNormalBlock(TETJournalBlock):
    """ Normal block representation """

    def __init__(self, parent, key):
        TETJournalBlock.__init__(self, parent, key)
        self.tc_name = ''

    def _parse(self):
        """ Custom parser """
        block_types = {'110': 'build', 
           '10': 'TC', 
           '300': 'clean'}
        (code, info, dummy) = self.lines[0].split('|', 2)
        self.btype = block_types.get(code, 'unknown')
        if code in ('110', '10', '300'):
            self.tc_name = info.split()[1]
        flag = False
        for line in self.lines:
            (code, info, dummy) = line.split('|', 2)
            if code == '400':
                key = info.split()[1]
                self.objects[key] = TETJournalIC(self, key)
                flag = True
            elif code == '410':
                key = info.split()[1]
                self.objects[key].append(line)
                flag = False
            if flag:
                self.objects[key].append(line)

        for key in self.objects.keys():
            self.objects[key].parse()

        self.dbg('%d ICs were parsed' % len(self.objects))


class TETJournal(TestObject):
    """ Parse TET journal file """

    def __init__(self, parent, key):
        TestObject.__init__(self, parent, key)
        self.arc_file = None
        self.start_time = 'unknown'
        self.end_time = 'unknown'
        self.tcc_cmd = None
        self.sys_info = 'unknown'
        self.parsed = False
        return

    def _create_block(self, xtype, key=None):
        """ Create block by its type """
        if key is None:
            key = len(self.objects)
        if xtype == 'normal':
            block = TETJournalNormalBlock(self, key)
        elif xtype == 'text':
            block = TETJournalTextBlock(self, key)
        elif xtype == 'header':
            block = TETJournalHeaderBlock(self, key)
        else:
            block = TETJournalBlock(self, key)
        self.objects[key] = block
        return block

    def _append_line(self, block, line, new_block_required):
        """ Append line to a (new) normal block """
        if new_block_required:
            block = self._create_block('normal', line.split('|')[1].split()[0])
        block.append(line)
        return block

    def read(self, arch_dir, arc_file):
        """ Open and read journal file """
        tc_name = arc_file['path']
        try:
            journal_file = os.path.join(arch_dir, tc_name, arc_file['file'])
            self.lines = open(journal_file).read().splitlines()
            self.dbg('File: %s' % os.path.join(tc_name, arc_file['file']))
        except IOError, err:
            logger.warning(str(err))

        self.arc_file = arc_file
        self.name = '%s journal' % tc_name

    def parse(self):
        """ Break journal file into header and logical blocks """
        if self.parsed or len(self.lines) == 0:
            return
        header = self._create_block('header')
        block = None
        new_block_required = True
        lastcode = ''
        for line in self.lines:
            (code, info, msg) = line.strip('\n').split('|', 2)
            if code in ('0', '5', '20', '30', '40'):
                if code == '0':
                    self.start_time = info.split()[1]
                    if self.tcc_cmd is None:
                        self.tcc_cmd = msg.split('Command line: ')[1]
                elif code == '5':
                    self.sys_info = info
                header.append(line)
            elif code == '900':
                self.end_time = info
            elif code in ('50', '70'):
                if lastcode not in ('50', '70'):
                    text = self._create_block('text')
                text.append(msg)
            elif code in ('110', '10', '300'):
                block = self._append_line(block, line, new_block_required)
                new_block_required = False
            elif code in ('130', '80', '320'):
                block = self._append_line(block, line, new_block_required)
                new_block_required = True
            else:
                block = self._append_line(block, line, new_block_required)
                new_block_required = False
            lastcode = code

        for obj_key in self.objects.keys():
            self.objects[obj_key].parse()

        self.dbg('%d blocks were parsed' % len(self.objects))
        self.parsed = True
        return