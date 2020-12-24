# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/torrenthelper/__init__.py
# Compiled at: 2012-09-15 11:02:20
""" torrenthelper - a module for classifying and cleaning up of downloaded media files. """
__version__ = '0.6'
import actions, classify

class Config:
    """
    Example of a config class, providing the minimal amount of
    necesary variables and methods.
    """
    verbose = True
    pretend = True
    incomingdir = '/mount/incoming/'
    folders = {'music': '/data/music/', 'movies': '/data/movies/', 
       'tvshows': '/data/tvshows/'}
    _map = {classify.Movie: 'movies', classify.TVShow: 'tvshows', 
       classify.TVShowSeason: 'tvshows', 
       classify.MusicAlbum: 'music'}

    def get_folder(self, which):
        if which in self.folders:
            return self.folders[which]
        return '/tmp/'

    def get_actions(self, cls):
        """ Given a class, return a list of actions of what to do."""
        todo = []
        target = self.get_folder(self._map[cls.__class__])
        files = [ cls.sourcefolder + f for f in cls.files ]
        a = actions.CopyAction(self.incomingdir, files, target + cls.getPrefixFolder())
        a.pretend = self.pretend
        a.verbose = self.verbose
        todo.append(a)
        return todo