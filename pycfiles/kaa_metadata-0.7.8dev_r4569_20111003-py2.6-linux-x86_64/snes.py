# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/games/snes.py
# Compiled at: 2009-05-22 11:00:08
__all__ = [
 'Parser']
import logging, sys
from struct import unpack
from re import match
import core
log = logging.getLogger('metadata')
snesromFileOffset = [
 33216, 32704, 65472, 65984]

class SNES(core.Game):

    def __init__(self, file):
        core.Game.__init__(self)
        self.mime = 'games/snes'
        self.type = 'SuperNintendo game'
        for offset in snesromFileOffset:
            log.debug('Checking for rom header at offset: %d' % offset)
            file.seek(offset)
            romHeader = file.read(32)
            try:
                romName, romHL, rom_type, romROM, romSRAM, romCountry, romLic, romVer, romICHK, romCHK = unpack('21sBBcccccHH', romHeader)
            except Exception as e:
                continue

            if rom_type not in (0, 1, 2, 3, 4, 5, 19, 227, 246):
                continue
            if not match('[a-zA-Z0-9 ]{21}', romName):
                continue
            log.debug('ROM NAME: "%s"' % romName)
            if romICHK | romCHK == 65535:
                log.debug('SNES rom header detected at offset : %d!!!!' % offset)
                break
            break
        else:
            raise core.ParseError()

        self.title = romName.strip()


Parser = SNES