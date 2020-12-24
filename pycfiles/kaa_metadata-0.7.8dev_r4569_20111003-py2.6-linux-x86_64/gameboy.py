# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/games/gameboy.py
# Compiled at: 2008-10-26 20:23:09
__all__ = [
 'Parser']
import logging, core
log = logging.getLogger('metadata')
GBA_LOGOCODE = b"$\xff\xaeQi\x9a\xa2!=\x84\x82\n\x84\xe4\t\xad\x11$\x8b\x98\xc0\x81\x7f!\xa3R\xbe\x19\x93\t\xce \x10FJJ\xf8'1\xecX\xc7\xe83\x82\xe3\xce\xbf\x85\xf4\xdf\x94\xceK\t\xc1\x94V\x8a\xc0\x13r\xa7\xfc\x9f\x84Ms\xa3\xca\x9aaX\x97\xa3'\xfc\x03\x98v#\x1d\xc7a\x03\x04\xaeV\xbf8\x84\x00@\xa7\x0e\xfd\xffR\xfe\x03o\x950\xf1\x97\xfb\xc0\x85`\xd6\x80%\xa9c\xbe\x03\x01N8\xe2\xf9\xa24\xff\xbb>\x03Dx\x00\x90\xcb\x88\x11:\x94e\xc0|c\x87\xf0<\xaf\xd6%\xe4\x8b8\n\xacr!\xd4\xf8\x07"
GB_LOGOCODE = b'\xce\xedff\xcc\r\x00\x0b\x03s\x00\x83\x00\x0c\x00\r\x00\x08\x11\x1f\x88\x89\x00\x0e\xdc\xccn\xe6\xdd\xdd\xd9\x99\xbb\xbbgcn\x0e\xec\xcc\xdd\xdc\x99\x9f\xbb\xb93>'

class Gameboy(core.Game):

    def __init__(self, file):
        core.Game.__init__(self)
        file.seek(4)
        if file.read(156) != GBA_LOGOCODE:
            file.seek(260)
            if file.read(len(GB_LOGOCODE)) != GB_LOGOCODE:
                raise core.ParseError()
            game_title = file.read(15)
            self.title = game_title
            if file.read(1) == b'\x80':
                self.mime = 'games/gbc'
                self.type = 'GameBoyColour game'
            else:
                self.mime = 'games/gb'
                self.type = 'GameBoy game'
        else:
            self.mime = 'games/gba'
            self.type = 'GameBoyAdvance game'
            game_title = file.read(12)
            self.title = game_title
            game_code = file.read(4)
            maker_code = file.read(2)
            log.debug('MAKER CODE: %s' % maker_code)
            if file.read(1) != b'\x96':
                raise core.ParseError()


Parser = Gameboy