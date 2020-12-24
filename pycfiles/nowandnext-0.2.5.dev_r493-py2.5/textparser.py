# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/utils/textparser.py
# Compiled at: 2009-05-11 19:02:37
import re, logging
log = logging.getLogger(__name__)

class textparser(object):
    """
    Extracts dictionaries of key: value pairs from blocks of text.
    """
    RE_MATCH_LINE = re.compile('^(?P<key>[a-zA-Z0-9_\\-\\.]+):\\s+(?P<value>[a-zA-Z0-9@ \\-_\\./:&\\+]+)$')
    RE_MATCH_TITLE = re.compile('^(?P<title>.+)\\s*(?P<repeat>\\(\\s*repeat\\s*\\))\\s*$', re.I + re.U)

    def __init__(self):
        pass

    @classmethod
    def parse(cls, input_text):
        unmatched = []
        for textline in input_text.split('\n'):
            match_results = cls.RE_MATCH_LINE.search(textline)
            if match_results:
                matchgroups = match_results.groupdict()
                yield (str(matchgroups['key']).lower(), matchgroups['value'])
            else:
                unmatched.append(textline)

        yield (
         'unmatched', unmatched)

    @classmethod
    def parsetodict(cls, input_text, title=''):
        match_title = cls.RE_MATCH_TITLE.search(title)
        result = dict((a for a in cls.parse(input_text)))
        if match_title:
            if match_title.groupdict()['repeat']:
                result['repeat'] = True
            else:
                result['repeat'] = False
            result['title'] = match_title.groupdict()['title']
        else:
            result['repeat'] = False
            result['title'] = title
        return result

    @staticmethod
    def translate(dictinput):
        dictoutput = {}
        for keyname in ['artist', 'artists', 'producer', 'producers', 'presenter', 'presenters', 'host', 'hosts']:
            if dictinput.has_key(keyname):
                dictoutput['artist'] = dictinput[keyname]

        for keyname in ['picture', 'logo', 'artwork', 'emblem', 'icon']:
            if dictinput.has_key(keyname):
                dictoutput['picture'] = dictinput[keyname]

        for keyname in ['web', 'email']:
            try:
                val = dictinput.get(keyname)
                dictoutput['keyname'] = val
            except KeyError, ke:
                log.debug('Not matched: %s' % keyname)

        dictoutput.update(dictinput)
        return dictoutput


if __name__ == '__main__':
    text = 'hello:goodbye\nnext: fun\nemail: sal@stodge.org\nweb: http://blog.stodge.org\nsite: http://www.hootingyard.org\nsample: this is a message with spaces\npresenters: Josh & Boo\nartists: BARRY + NIGEL\nversion: Version 2.0\nmyspace: http://www.stage4.co.uk/5050\nweb: http://www.stage4.co.uk/5050\npresenters: Jah Beef & Papa Milo\nMaGiC Time: Ignore this item\nMaGiCTimE: fun\nhttp://www.foo.net\nblah\nbloo \nningi\n'
    foo = textparser()
    import pprint
    pprint.pprint(foo.parsetodict(text, 'Hooting Yard (repeat ) '))
    pprint.pprint(foo.parsetodict(text, 'Hooting Yard '))