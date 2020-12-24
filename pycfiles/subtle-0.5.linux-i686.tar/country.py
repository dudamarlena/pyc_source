# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/country.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import UnicodeMixin, base_text_type, u
from guessit.fileutils import load_file_in_same_dir
import logging
__all__ = [
 b'Country']
log = logging.getLogger(__name__)
_iso3166_contents = load_file_in_same_dir(__file__, b'ISO-3166-1_utf8.txt')
country_matrix = [ l.strip().split(b'|') for l in _iso3166_contents.strip().split(b'\n')
                 ]
country_matrix += [[b'Unknown', b'un', b'unk', b'', b''],
 [
  b'Latin America', b'', b'lat', b'', b'']]
country_to_alpha3 = dict((c[0].lower(), c[2].lower()) for c in country_matrix)
country_to_alpha3.update(dict((c[1].lower(), c[2].lower()) for c in country_matrix))
country_to_alpha3.update(dict((c[2].lower(), c[2].lower()) for c in country_matrix))
country_to_alpha3.update({b'latinoamérica': b'lat', b'brazilian': b'bra', 
   b'españa': b'esp', 
   b'uk': b'gbr'})
country_alpha3_to_en_name = dict((c[2].lower(), c[0]) for c in country_matrix)
country_alpha3_to_alpha2 = dict((c[2].lower(), c[1].lower()) for c in country_matrix)

class Country(UnicodeMixin):
    """This class represents a country.

    You can initialize it with pretty much anything, as it knows conversion
    from ISO-3166 2-letter and 3-letter codes, and an English name.
    """

    def __init__(self, country, strict=False):
        country = u(country.strip().lower())
        self.alpha3 = country_to_alpha3.get(country)
        if self.alpha3 is None and strict:
            msg = b'The given string "%s" could not be identified as a country'
            raise ValueError(msg % country)
        if self.alpha3 is None:
            self.alpha3 = b'unk'
        return

    @property
    def alpha2(self):
        return country_alpha3_to_alpha2[self.alpha3]

    @property
    def english_name(self):
        return country_alpha3_to_en_name[self.alpha3]

    def __hash__(self):
        return hash(self.alpha3)

    def __eq__(self, other):
        if isinstance(other, Country):
            return self.alpha3 == other.alpha3
        if isinstance(other, base_text_type):
            try:
                return self == Country(other)
            except ValueError:
                return False

        return False

    def __ne__(self, other):
        return not self == other

    def __unicode__(self):
        return self.english_name

    def __repr__(self):
        return b'Country(%s)' % self.english_name