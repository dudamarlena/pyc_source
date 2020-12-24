# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/madiolahb/chardesc.py
# Compiled at: 2011-12-07 22:55:37
from core import in_prof_range, in_spot_range, SPOTS

def playing(self, subject=None, name='', **kwargs):
    exists = Character.all().ancestor(self.game).filter('name =', name).count(1)
    if exists:
        self.errors.append('Character name exists: %s' % name)
        return False
    else:
        owner = self.sender
        if subject is not None:
            if isinstance(subject, basestring):
                self.warnings.append('The subject of "is playing" should be a player.')
            elif subject.type == 'Addr':
                owner = subject.value
        if owner not in self.game.players:
            self.game.players.append(owner)
            self.gameupdated = True
        self.char = self.game.new_char(owner, name)
        self.char.put()
        self.charcache[self.char.key()] = self.char
        self.updated.append(self.char.key())
        return


def advanced(self, subject=None, prof1=None, prof2=None, prof3=None, **kwargs):
    if not self._char(subject):
        return False
    else:
        for prof, value in (('job1', prof1), ('job2', prof2), ('job3', prof3)):
            if value is not None:
                if in_prof_range(value):
                    setattr(self.char, prof, value)
                    if self.char.key() not in self.updated:
                        self.updated.append(self.char.key())
                else:
                    self.warnings.append('%s is out of range for a profession' % value)

        return


def has(lifewheel, **kwargs):
    """
    Set a Lifewheel spot to a given count.
    """
    for spot in SPOTS:
        if spot in kwargs:
            if in_spot_range[spot](kwargs[spot]):
                lifewheel[spot] = kwargs[spot]
            else:
                lifewheel['warnings'].append('%s is out of range for %s' % (
                 kwargs[spot], spot))


def _register_has(subp):
    parser = subp.add_parser('has')
    for spot in SPOTS:
        parser.add_argument('--%s' % spot, type=int)

    parser.set_defaults(func=has)


def check(lifewheel, **kwargs):
    """
    Check a Lifewheel for general consistency.
    """
    for spot in SPOTS:
        if not in_spot_range[spot](lifewheel[spot]):
            lifewheel['warnings'].append('%s is out of range for %s' % (
             lifewheel[spot], spot))


def _register_check(subp):
    parser = subp.add_parser('check')
    parser.set_defaults(func=check)


def register_commands(subp):
    _register_has(subp)
    _register_check(subp)