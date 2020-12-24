# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/adapters/reference_number.py
# Compiled at: 2019-02-15 13:51:23
from emrt.necd.content.observation import IObservation
from plone.app.content.interfaces import INameFromTitle
from plone.app.content.namechooser import NormalizingNameChooser
from zope.component import adapts
from zope.interface import implements
ATTEMPTS = 100

class INameFromData(INameFromTitle):
    pass


class ReferenceNumberCreator(NormalizingNameChooser):
    """A name chooser for a Zope object manager.

    If the object is adaptable to or provides INameFromTitle, use the
    title to generate a name.
    """
    adapts(IObservation)
    implements(INameFromData)

    def chooseName(self, name, object):
        parent = self.context
        items = []
        items.append(object.country.upper())
        items.append(object.nfr_code)
        items.append(str(object.review_year))
        prename = ('-').join(items)
        number = 1
        observations = [ k for k in parent.keys() if k.startswith(prename) ]
        if observations:
            observations.sort()
            last_observation = observations[(-1)]
            number = int(last_observation.split('-')[(-1)])
            number = number + 1
        last_part = '%04d' % number
        name = prename + '-' + last_part
        return str(name)