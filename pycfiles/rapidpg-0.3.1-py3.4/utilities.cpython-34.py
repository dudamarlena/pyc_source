# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rapidpg\utilities.py
# Compiled at: 2014-07-01 20:24:30
# Size of source mod 2**32: 3232 bytes
"""
Utilities for the library, not all of the functions are suppose to be used
externally
"""
from pygame import BLEND_RGBA_MIN

def parse_config(raw_config):

    def collision_reader(s):
        """
        The config must be in the format of e,e,e....
        where e is either a single character, or a range that
        looks like *start...end*
        the range is inclusive
        """
        as_list = s.split(',')
        as_list = [x.strip() for x in as_list]
        result = set()
        for e in as_list:
            if '...' in e:
                start, _, end = e.partition('...')
                for c in range(int(start), int(end) + 1):
                    result.add(str(c))

            else:
                result.add(e)

        return result

    def map_parser_builder(function, how_many):
        """
        Factory function for building parsers that just map
        a function over all the elements
        """

        def parser(s):
            t = tuple(map(function, s.strip().split(' ')))
            result = t[:how_many + 1]
            if len(result) == 1:
                return result[0]
            return result

        return parser

    dispatch = {'s': str,  'f': float,  'i': int}

    def parser_builder(format_):
        """
        Factory for complex parsers.
        :param str format_: ``"e+e+e..."`` where ``e = 's' | 'f' | 'i'``
        """
        look_up = tuple(map(dispatch.get, format_.split('+')))

        def parser(s):
            result = []
            elements = s.split(' ')
            for c in range(len(look_up)):
                result.append(look_up[c](elements[c]))

            return tuple(result)

        return parser

    def wrap_with_list(fn):
        return lambda s: [
         fn(s)]

    processors = {'collision': collision_reader,  'gravity': map_parser_builder(float, 1), 
     'resolution': map_parser_builder(int, 2), 
     'background': wrap_with_list(parser_builder('s+i')), 
     'exit': map_parser_builder(int, 4), 
     'spawn': map_parser_builder(int, 2), 
     'animations': wrap_with_list(parser_builder('s+i+i+i'))}
    config = []
    for config_line in raw_config:
        name, _, value = config_line.strip().partition(' ')
        config.append((name, value))

    processed_config = dict()
    for n, v in config:
        if n in processors:
            if n in processed_config:
                processed_config[n] = processed_config[n] + processors[n](v)
            else:
                processed_config[n] = processors[n](v)
                continue

    return processed_config


def set_alpha(surface, alpha):
    """
    Takes a surface with per-pixel transparency, then return a new one with
    a new alpha level. Setting a alpha higher than the original will not work.
    :param surface: original surface
    :param alpha: new alpha level
    :return: surface
    """
    new = surface.copy()
    new.fill((255, 255, 255, alpha), None, BLEND_RGBA_MIN)
    return new