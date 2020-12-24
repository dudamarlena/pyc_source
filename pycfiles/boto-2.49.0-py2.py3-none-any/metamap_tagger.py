# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/taxonomy/metamap_tagger.py
# Compiled at: 2012-08-16 08:09:35
import urllib2, xml.dom.minidom
url = 'http://10.1.204.8:8080/mm-service/rest/mapTerm'
CONCEPT_FIELDS = ('cui', 'displayName', 'preferredName', 'sources', 'semanticTypes',
                  'matchedText')

class MetamapWrapper(object):
    """
    Wrapper class for the RESTful metamamap server instance
    """

    def __init__(self):
        self.url = botnee_config.METAMAP_SERVER

    def query_by_text(self, text):
        """
        Queries the metamap instance using the supplied text string
        """
        values = {'text': text}
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        self.xml_result = xml.dom.minidom.parseString(the_page)
        return self.process_result(self.xml_result)

    def process_result(self, xml_result):
        """
        Takes the xml result and constructs a list of dictionary objects
        """
        tags = []
        for option in xml_result.getElementsByTagName('option'):
            tags.append({})
            for label in ['score', 'start', 'length']:
                tags[(-1)][label] = option.getElementsByTagName(label)[0].childNodes[0].data

            concept = option.getElementsByTagName('concept')[0]
            tags[(-1)]['concept'] = {}
            for concept_field in CONCEPT_FIELDS:
                nodes = concept.getElementsByTagName(concept_field)
                if len(nodes) == 1:
                    tags[(-1)]['concept'][concept_field] = nodes[0].childNodes[0].data
                else:
                    tags[(-1)]['concept'][concept_field] = [ node.childNodes[0].data for node in nodes ]

        return tags