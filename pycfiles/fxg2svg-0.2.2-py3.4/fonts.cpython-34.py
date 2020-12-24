# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fxg2svg/utils/fonts.py
# Compiled at: 2016-07-20 10:53:08
# Size of source mod 2**32: 1669 bytes
import logging, os
from PIL import ImageFont
import re
logger = logging.getLogger(__name__)
insensitive_re = re.compile(re.escape('Regular'), re.IGNORECASE)

def insensitive_eq(s1, s2):
    return s1.replace(' ', '').lower() == s2.replace(' ', '').lower()


class FontNotFoundError(Exception):
    pass


def get_filepaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


def camelcased(pattern, splitters=' '):
    return ' '.join(map(lambda s: s.capitalize(), pattern.split(splitters)))


def get_font_alias(font):
    fontname = ' '.join(font.getname())
    return insensitive_re.sub('', camelcased(fontname)).strip()


def get_font_file(name, f, fontdir):
    for filepath in get_filepaths(fontdir):
        try:
            try:
                font = ImageFont.truetype(filepath)
            except OSError:
                logger.debug('%s is not a font' % filepath)
            else:
                alias = get_font_alias(font)
                if insensitive_eq(alias, camelcased(name)):
                    return filepath
        finally:
            del font


def get_font(name, f='ttf', fontdir=None, size=None):
    if fontdir is None:
        raise FontNotFoundError("Font '%s' not found." % name)
    fontpath = get_font_file(name, f, fontdir)
    if fontpath is None:
        raise FontNotFoundError("Font '%s' not found." % name)
    if size is None:
        font = ImageFont.truetype(fontpath)
    else:
        font = ImageFont.truetype(fontpath, size=size)
    return font