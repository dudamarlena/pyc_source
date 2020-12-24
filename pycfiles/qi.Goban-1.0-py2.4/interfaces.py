# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/Goban/interfaces.py
# Compiled at: 2008-05-05 04:21:57
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope import schema
from qi.Goban import GobanMessageFactory as _

class IGoGame(Interface):
    """
        """
    __module__ = __name__
    blackPlayer = schema.TextLine(title=_('label_blackPlayer', default='Black'))
    blackRating = schema.TextLine(title=_('label_blackRating', default='Black rating'))
    whitePlayer = schema.TextLine(title=_('label_whitePlayer', default='White'))
    whiteRating = schema.TextLine(title=_('label_whiteRating', default='White rating'))
    komi = schema.Float(title=_('label_komi', default='Komi'), default=0.5, required=True)
    handicap = schema.Int(title=_('label_handicap', default='Handicap'), default=0, min=0, required=True)
    event = schema.TextLine(title=_('label_event', default='Event'))
    place = schema.TextLine(title=_('label_place', default='Place'))
    round = schema.TextLine(title=_('label_round', default='Round'))
    datePlayed = schema.Date(title=_('label_datePlayed', default='Date played'))
    dateFinished = schema.Date(title=_('label_dateFinished', default='Date finished'))
    result = schema.TextLine(title=_('label_result', default='Result'))


class IPDFDiagram(Interface):
    """
        """
    __module__ = __name__
    movesPerDiagram = schema.Int(title=_('label_movesPerDiagram', default='Moves per diagram'), description=_('help_movesPerDiagram', default='The number of moves displayed in each of the diagrams.'), required=True, default=50, min=10)
    ignoreVariations = schema.Bool(title=_('label_ignoreVariations', default='Ignore variations'), description=_('help_ignoreVariations', default="Check here if you don't want variations to be included."), default=False)
    ignoreLetters = schema.Bool(title=_('label_ignoreLetters', default='Ignore letters'), description=_('help_ignoreLetters', default="Check here if you don't want letter markings to be printed."), default=False)
    ignoreMarks = schema.Bool(title=_('label_ignoreMarks', default='Ignore marks'), description=_('help_ignoreMarks', default="Check here if you don't want marks to be printed."), default=False)


class IAddVariation(Interface):
    """
        """
    __module__ = __name__
    varSgf = schema.Bytes(title=_('label_sgf', default='Sgf'), description=_('help_variationSgf', default='the sgf file containing the new variation(s)'), required=True)