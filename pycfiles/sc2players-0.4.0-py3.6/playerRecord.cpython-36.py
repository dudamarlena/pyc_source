# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2players\playerRecord.py
# Compiled at: 2018-09-29 00:51:05
# Size of source mod 2**32: 13185 bytes
"""
PURPOSE: manage records of all known players, both local and remote
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six import iteritems
import json, os, re, time
from sc2players import constants as c

class PlayerRecord(object):
    __doc__ = 'manage the out-of-game meta data of a given player'
    AVAILABLE_KEYS = [
     'name',
     'type',
     'difficulty',
     'initCmd',
     'initOptions',
     'raceDefault',
     'rating']

    def __init__(self, source=None, **override):
        self.name = ''
        self.type = c.PlayerDesigns(c.HUMAN)
        self.difficulty = c.ComputerDifficulties(None)
        self.initCmd = ''
        self.initOptions = {}
        self.rating = c.DEFAULT_RATING
        self.created = time.time()
        self.raceDefault = c.RANDOM
        self._matches = []
        if isinstance(source, str):
            self.load(source)
        else:
            if isinstance(source, dict):
                self.update(source)
            else:
                if isinstance(source, PlayerRecord):
                    self.update(source.__dict__)
        self.update(override)
        if not self.name:
            raise ValueError("must define 'name' parameter as part of %s source settings" % self.__class__.__name__)
        if self.type in [c.BOT, c.AI]:
            if not self.initCmd:
                raise ValueError('must provide initCmd attribute when specifying type=%s' % self.type)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.isComputer:
            diff = '-%s' % self.difficulty.type
        else:
            if self.rating:
                diff = '-%d' % self.rating
            else:
                diff = ''
        return '<%s %s %s%s>' % (self.__class__.__name__, self.name, self.type.type, diff)

    def __call__(self, attrs, **kwargs):
        """update internals according to parameters"""
        self.update(attrs)
        self.update(kwargs)
        return self

    @property
    def initOptStr(self):
        return ' '.join(['%s=%s' % (k, v) for k, v in self.initOptions.items()])

    @property
    def isAI(self):
        return self.type == c.AI

    @property
    def isBot(self):
        return self.type == c.BOT

    @property
    def isHuman(self):
        return self.type == c.HUMAN

    @property
    def isComputer(self):
        return self.type == c.COMPUTER

    @property
    def isMulti(self):
        return self.type == c.ARCHON

    @property
    def isStoredLocal(self):
        """determine whether this player can be run locally"""
        raise NotImplementedError('TODO -- determine whether this player is an already known player')

    @property
    def filename(self):
        """return the absolute path to the object's filename"""
        return os.path.join(c.PLAYERS_FOLDER, 'player_%s.json' % self.name)

    @property
    def attrs(self):
        """provide a copy of this player's attributes as a dictionary"""
        ret = dict(self.__dict__)
        del ret['_matches']
        if self.type != c.COMPUTER:
            del ret['difficulty']
        return ret

    @property
    def simpleAttrs(self):
        """provide a copy of this player's attributes as a dictionary, but with objects flattened into a string representation of the object"""
        simpleAttrs = {}
        for k, v in iteritems(self.attrs):
            if k in ('_matches', ):
                pass
            else:
                try:
                    simpleAttrs[k] = v.type
                except:
                    simpleAttrs[k] = v

        return simpleAttrs

    @property
    def matches(self):
        """retrieve the match history for this player from the matchHistory repo and cache the result"""
        return []

    def _validateAttrs(self, keys):
        """prove that all attributes are defined appropriately"""
        badAttrs = []
        for k in keys:
            if k not in self.__dict__:
                badAttrs.append("Attribute key '%s' is not a valid attribute" % k)

        badAttrsMsg = os.linesep.join(badAttrs)
        if not keys:
            return
        if badAttrsMsg:
            raise ValueError('Encountered invalid attributes.  ALLOWED: %s%s%s' % (
             list(self.__dict__), os.linesep, badAttrsMsg))

    @property
    def control(self):
        """the type of control this player exhibits"""
        if self.isComputer:
            value = c.COMPUTER
        else:
            value = c.PARTICIPANT
        return c.PlayerControls(value)

    def load(self, playerName=None):
        """retrieve the PlayerRecord settings from saved disk file"""
        if playerName:
            self.name = playerName
        try:
            with open(self.filename, 'rb') as (f):
                data = f.read()
        except Exception:
            raise ValueError("invalid profile, '%s'. file does not exist: %s" % (self.name, self.filename))

        self.update(json.loads(data))
        self._matches = []

    def save(self):
        """save PlayerRecord settings to disk"""
        data = str.encode(json.dumps((self.simpleAttrs), indent=4, sort_keys=True))
        with open(self.filename, 'wb') as (f):
            f.write(data)

    def update(self, attrs):
        """update attributes initialized with the proper type"""

        def convertStrToDict(strVal):
            if isinstance(strVal, dict):
                return strVal
            else:
                strVal = re.sub('[\\{\\}]+', '', str(strVal))
                regexCol = re.compile(':')
                terms = re.split('[,\\s]+', strVal)
                keyvals = [re.split(regexCol, t) for t in terms]
                x = re.compile('[\'"]')
                ret = {}
                boolTrue = re.compile('true', flags=(re.IGNORECASE))
                boolFalse = re.compile('false', flags=(re.IGNORECASE))
                for k, v in keyvals:
                    k = re.sub(x, '', k)
                    v = re.sub(x, '', v)
                    if re.search(boolTrue, v):
                        v = True
                    else:
                        if re.search(boolFalse, v):
                            v = False
                        else:
                            if '.' in v:
                                try:
                                    v = float(v)
                                except:
                                    pass

                            else:
                                try:
                                    v = int(v)
                                except:
                                    pass

                    ret[k] = v

                return ret

        self._validateAttrs(attrs)
        for k, v in iteritems(attrs):
            typecast = type(getattr(self, k))
            if typecast == bool:
                if v == 'False':
                    newval = False
            if issubclass(typecast, c.RestrictedType):
                newval = typecast(v)
            else:
                if '<' in str(v) or v == None:
                    newval = typecast(v)
                else:
                    if k == 'initCmd':
                        newval = str(v)
                    else:
                        if k == 'initOptions':
                            newval = convertStrToDict(v)
                        else:
                            newval = typecast(str(v).lower())
            setattr(self, k, newval)

        if self.isComputer:
            pass
        elif 'difficulty' in attrs:
            if attrs['difficulty'] != None:
                raise ValueError('%s type %s=%s does not have a difficulty' % (
                 self.__class__.__name__, self.type.__class__.__name__, self.type.type))
        else:
            self.difficulty = c.ComputerDifficulties(None)

    def matchSubset(**kwargs):
        """extract matches from player's entire match history given matching criteria kwargs"""
        ret = []
        for m in self.matches:
            allMatched = True
            for k, v in iteritems(kwargs):
                mVal = getattr(m, k)
                try:
                    if v == mVal or v in mVal:
                        continue
                except Exception:
                    pass

                allMatched = False
                break

            if allMatched:
                ret.append(m)

        return ret

    def apmRecent(self, maxMatches=c.RECENT_MATCHES, **criteria):
        """collect recent match history's apm data to report player's calculated MMR"""
        if not self.matches:
            return 0
        else:
            apms = [m.apm(self) for m in (self.recentMatches)(maxMatches=maxMatches, **criteria)]
            return sum(apms) / len(apms)

    def apmAggregate(self, **criteria):
        """collect all match history's apm data to report player's calculated MMR"""
        apms = [m.apm(self) for m in (self.matchSubset)(**criteria)]
        if not apms:
            return 0
        else:
            return sum(apms) / len(apms)

    def recentMatches(self, **criteria):
        """identify all recent matches for player given optional, additional criteria"""
        if not self.matches:
            return []
        else:
            try:
                maxMatches = criteria['maxMatches']
                del criteria['maxMatches']
            except AttributeError:
                maxMatches = c.RECENT_MATCHES

            alLMatches = (self.matchSubset)(**criteria)
            matchTimes = [(m.endTime, m) for m in matches]
            selMatches = sorted(matchTimes)[:maxMatches]
            retMatches = [m for endTime, m in selMatches]
            return retMatches