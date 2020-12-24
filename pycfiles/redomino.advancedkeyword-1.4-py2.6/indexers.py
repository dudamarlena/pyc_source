# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/indexers.py
# Compiled at: 2013-05-08 04:41:18
from plone.indexer import indexer
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from redomino.advancedkeyword.config import KEYWORD_SEPARATOR

def subject_splitter(subject):
    """
        >>> subject = 'redomino.prodotti.recatalog'
        >>> subject_splitter(subject)
        ['redomino', 'redomino.prodotti', 'redomino.prodotti.recatalog']

        >>> subject = 'redomino'
        >>> subject_splitter(subject)
        ['redomino']

        >>> subject = None
        >>> subject_splitter(subject)
        []

        >>> subject = ''
        >>> subject_splitter(subject)
        []

        >>> subject = 'redomino.'
        >>> subject_splitter(subject)
        ['redomino']
    """
    results = []
    if subject:
        splitted_subject = subject.split(KEYWORD_SEPARATOR)
        results.append(splitted_subject[0])
        count = 1
        for item in splitted_subject[1:]:
            if item:
                results.append('%s%s%s' % (results[(count - 1)], KEYWORD_SEPARATOR, item))
                count = count + 1

    return results


def subjects_splitter(subjects):
    """
        >>> subjects = ['redomino', 'pippo.pluto']
        >>> subjects_splitter(subjects)
        ['pippo', 'pippo.pluto', 'redomino']
    """
    results = []
    for subject in subjects:
        for splitted in subject_splitter(subject):
            if splitted not in results:
                results.append(splitted)

    results.sort()
    return results


def subjects_indexer(obj):
    """ 
        >>> class FakeObject(object):
        ...     def __init__(self, subjects):
        ...         self.subjects = subjects
        ...     def Subject(self):
        ...         return self.subjects
        >>> subjects = ['redomino.prova', 'redomino.prodotti.recatalog']
        >>> obj1 = FakeObject(subjects)
        >>> set(subjects_indexer(obj1)) == set(['redomino', 'redomino.prova', 'redomino.prodotti', 'redomino.prodotti.recatalog'])
        True
    """
    subjects = obj.Subject()
    results = []
    for item in subjects:
        results = results + subject_splitter(item)

    return list(set(results))


@indexer(IATContentType)
def subjects(obj):
    return subjects_indexer(obj)