# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\game.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'ThorN'
__version__ = '1.6'

class Game(object):
    _mapName = None
    _mapTimeStart = None
    _roundTimeStart = None
    captureLimit = None
    fragLimit = None
    timeLimit = None
    gameName = None
    gameType = None
    modName = None
    rounds = 0

    def __init__(self, console, gameName):
        """
        Object constructor.
        :param console: Console class instance
        :param gameName: The current game name
        """
        self.console = console
        self.gameName = gameName
        self.startRound()

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            return

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        return self.__dict__[key]

    def _get_mapName(self):
        if not self._mapName:
            try:
                mapname = self.console.getMap()
            except Exception:
                self._mapName = None
            else:
                self._set_mapName(mapname)

        return self._mapName

    def _set_mapName(self, newmap):
        if self._mapName != newmap:
            event = self.console.getEvent('EVT_GAME_MAP_CHANGE', data={'old': self._mapName, 'new': newmap})
            self.console.queueEvent(event)
        self._mapName = newmap

    mapName = property(_get_mapName, _set_mapName)

    def mapTime(self):
        """
        Return the time elapsed since map start.
        """
        if self._mapTimeStart:
            return self.console.time() - self._mapTimeStart
        else:
            return

    def roundTime(self):
        """
        Return the time elapsed since round start
        """
        return self.console.time() - self._roundTimeStart

    def startRound(self):
        """
        Set variables to mark round start.
        """
        if not self._mapTimeStart:
            self.startMap()
        self._roundTimeStart = self.console.time()
        self.rounds += 1

    def startMap(self, mapName=None):
        """
        Set variables to mark map start.
        """
        if mapName:
            self.mapName = mapName
        self._mapTimeStart = self.console.time()

    def mapEnd(self):
        """
        Set variables to mark map end.
        """
        self._mapTimeStart = None
        return