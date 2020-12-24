# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dzhoshkun/ws/GiftGrab/src/tests/target/conftest.py
# Compiled at: 2016-12-08 05:54:41
# Size of source mod 2**32: 1390 bytes
from pygiftgrab import Codec, ColourSpace

def pytest_addoption(parser):
    parser.addoption('--codec', action='store', help='Codec (HEVC, Xvid, or VP9)')
    parser.addoption('--colour-space', action='store', help='Colour space specification (BGRA or I420)')


def pytest_generate_tests(metafunc):
    if 'codec' in metafunc.fixturenames:
        codec_str = str(metafunc.config.option.codec)
        case_insensitive = codec_str.lower()
        if case_insensitive == 'hevc':
            codec = Codec.HEVC
    else:
        if case_insensitive == 'xvid':
            codec = Codec.Xvid
        else:
            if case_insensitive == 'vp9':
                codec = Codec.VP9
            else:
                raise RuntimeError('Could not recognise codec ' + codec_str)
            metafunc.parametrize('codec', [codec])
        if 'colour_space' in metafunc.fixturenames:
            colour_space_str = str(metafunc.config.option.colour_space)
            case_insensitive = colour_space_str.lower()
            if case_insensitive == 'bgra':
                colour_space = ColourSpace.BGRA
            else:
                if case_insensitive == 'i420':
                    colour_space = ColourSpace.I420
                else:
                    raise RuntimeError('Could not recognise colour space ' + colour_space_str)
            metafunc.parametrize('colour_space', [colour_space])