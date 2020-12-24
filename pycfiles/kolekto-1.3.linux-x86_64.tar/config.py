# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/kolekto/config.py
# Compiled at: 2014-06-16 16:12:17
""" Kolekto configuration parsers.
"""
import pkg_resources
from confiture import Confiture
from confiture.schema import ValidationError
from confiture.schema.containers import Section, Value, List
from confiture.schema.types import String
from .profiles.movies import Movies

class Profile(String):
    """ Type for Kolekto profiles.

    This type load know profiles using distutils entry-points.
    """

    def validate(self, value):
        value = super(Profile, self).validate(value)
        profile = next(pkg_resources.iter_entry_points('kolekto.profiles', str(value)), None)
        if profile is None:
            raise ValidationError('Unknown profile')
        return (
         profile.name, profile.load())

    def cast(self, value):
        raise NotImplementedError()


class ViewKolektoConfig(Section):
    _meta = {'args': Value(String()), 'unique': True, 
       'repeat': (0, None)}
    pattern = List(String())


class DatasourceKolektoConfig(Section):
    _meta = {'args': Value(String()), 'unique': True, 
       'repeat': (0, None), 
       'allow_unknown': True}


class ListingKolektoConfig(Section):
    _meta = {'args': Value(String()), 'unique': True, 
       'repeat': (0, None)}
    pattern = Value(String())
    order = List(String(), default=['title', 'year'])


class RootKolektoConfig(Section):
    profile = Value(Profile(), default=('movies', Movies))
    view = ViewKolektoConfig()
    datasource = DatasourceKolektoConfig()
    listing = ListingKolektoConfig()


def parse_config(filename):
    conf = Confiture.from_filename(filename, schema=RootKolektoConfig())
    return conf.parse()