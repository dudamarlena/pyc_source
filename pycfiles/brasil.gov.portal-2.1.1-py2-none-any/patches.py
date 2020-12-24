# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/patches.py
# Compiled at: 2018-10-18 17:35:14
from brasil.gov.portal.logger import logger
from plone.app.contenttypes.content import Link
from plone.outputfilters.filters import resolveuid_and_caption as base

def outputfilters():

    def patched_call(self, data):
        """ Patch original __call__ """
        data = data.replace('/>', ' />')
        return self.__orig_call__(data)

    setattr(base.ResolveUIDAndCaptionFilter, '__orig_call__', base.ResolveUIDAndCaptionFilter.__call__)
    setattr(base.ResolveUIDAndCaptionFilter, '__call__', patched_call)
    logger.info('Patched ResolveUIDAndCaptionFilter')


def link():

    def getRemoteUrl(self):
        return self.remoteUrl

    setattr(Link, 'getRemoteUrl', getRemoteUrl)
    logger.info('Patched Link content type')


def deselect(self):
    selecteditems = []
    notselecteditems = []
    for selecteditem in self.selectedItems:
        selecteditems.append(selecteditem['value'])

    for item in self.items:
        if item['value'] not in selecteditems:
            notselecteditems.append(item)

    return notselecteditems


def run():
    outputfilters()
    link()