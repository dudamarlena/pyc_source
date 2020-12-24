# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/utility/utility.py
# Compiled at: 2020-03-28 11:39:03
# Size of source mod 2**32: 1950 bytes


def extractText(blob):
    if '<code' in blob:
        return extractTextHelper('', blob)
    return blob


def extractTextHelper(title, blob):
    if '<code' not in blob:
        title += blob
        return title
    idx0 = blob.find('<code')
    firstSub = blob[0:idx0]
    title += firstSub
    idx1 = blob.find('"pre">')
    idx2 = blob.find('</span>')
    secondSub = blob[idx1 + 6:idx2]
    title += secondSub
    title += ' '
    idx3 = blob.find('</code>')
    spareBlob = blob[idx2 + 7:idx3]
    if '<span' in spareBlob:
        title = spareBlobHelper(title, spareBlob)
    thirdSub = blob[idx3 + 7:]
    return extractTextHelper(title, thirdSub)


def spareBlobHelper(title, spareBlob):
    if '<span' not in spareBlob:
        return title
    spareIdx0 = spareBlob.find('"pre">')
    spareIdx1 = spareBlob.find('</span>')
    spareSub = spareBlob[spareIdx0 + 6:spareIdx1]
    title += spareSub
    title += ' '
    spareBlob = spareBlob[spareIdx1 + 7:]
    return spareBlobHelper(title, spareBlob)


def extractTextII(blob):
    if '</span>' in blob:
        blob = blob.replace('<span class="section-number">', '')
        blob = blob.replace('</span>', '')
        return blob
    if '<strong>' in blob:
        title = ''
        idx0 = blob.find('<strong>')
        firstSub = blob[0:idx0]
        title += firstSub
        idx1 = blob.find('</strong')
        secondSub = blob[idx0 + 8:idx1]
        title += secondSub
        title += ' '
        thirdSub = blob[idx1 + 10:]
        title += thirdSub
        return title
    return blob


def setup(app):
    import jinja2
    jinja2.filters.FILTERS['extractText'] = extractText
    jinja2.filters.FILTERS['extractTextII'] = extractTextII