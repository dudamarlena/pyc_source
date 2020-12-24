# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uche/dev/amara/test/bindery/test_examplotron_model.py
# Compiled at: 2010-12-28 02:49:14
import unittest
from amara.lib import testsupport
from amara import tree
import os, re, tempfile
from amara.lib import U
from amara import bindery
from amara.bindery.model import generate_metadata
from amara.bindery.model.examplotron import examplotron_model
MODEL_A = '<?xml version="1.0" encoding="utf-8"?>\n<labels xmlns:eg="http://examplotron.org/0/" xmlns:ak="http://purl.org/xml3k/akara/xmlmodel">\n  <label id="tse" added="2003-06-10" eg:occurs="*" ak:resource="@id"> <!-- use ak:resource="" for an anon resource -->\n    <quote eg:occurs="?">\n      <emph>Midwinter</emph> Spring is its own <strong>season</strong>...\n    </quote>\n    <name>Thomas Eliot</name>\n    <address ak:rel="\'place\'" ak:value="concat(city, \',\', province)">\n      <street>3 Prufrock Lane</street>\n      <city>Stamford</city>\n      <province>CT</province>\n    </address>\n    <opus year="1932" ak:rel="" ak:resource="">\n      <title ak:rel="name()">The Wasteland</title>\n    </opus>\n    <tag eg:occurs="*" ak:rel="">old possum</tag>\n  </label>\n</labels>\n'
INSTANCE_A_1 = '<?xml version="1.0" encoding="iso-8859-1"?>\n<labels>\n  <label id=\'ep\' added="2003-06-10">\n    <name>Ezra Pound</name>\n    <address>\n      <street>45 Usura Place</street>\n      <city>Hailey</city>\n      <province>ID</province>\n    </address>\n  </label>\n  <label id=\'tse\' added="2003-06-20">\n    <name>Thomas Eliot</name>\n    <address>\n      <street>3 Prufrock Lane</street>\n      <city>Stamford</city>\n      <province>CT</province>\n    </address>\n    <opus>\n      <title>The Wasteland</title>\n    </opus>\n    <tag>old possum</tag>\n    <tag>poet</tag>\n  </label>\n  <label id="lh" added="2004-11-01">\n    <name>Langston Hughes</name>\n    <address>\n      <street>10 Bridge Tunnel</street>\n      <city>Harlem</city>\n      <province>NY</province>\n    </address>\n    <tag>poet</tag>\n  </label>\n  <label id="co" added="2004-11-15">\n    <name>Christopher Okigbo</name>\n    <address>\n      <street>7 Heaven\'s Gate</street>\n      <city>Idoto</city>\n      <province>Anambra</province>\n    </address>\n    <opus>\n      <title>Heaven\'s Gate</title>\n    </opus>\n    <tag>biafra</tag>\n    <tag>poet</tag>\n  </label>\n</labels>\n'

def normalize_generated_ids(meta_list):
    pat = re.compile('r(\\d+)e')

    def normalize_id(id):
        m = pat.match(id)
        if m:
            id = 'r*e' + id[m.end():]
        return id

    for (i, (s, p, o)) in enumerate(meta_list):
        s = normalize_id(s)
        o = normalize_id(U(o))
        meta_list[i] = (s, p, o)

    return meta_list


class Test_parse_model_a(unittest.TestCase):
    """Testing nasty tag soup 1"""

    def test_metadata_extraction(self):
        """Test metadata extraction"""
        model = examplotron_model(MODEL_A)
        doc = bindery.parse(INSTANCE_A_1, model=model)
        metadata = generate_metadata(doc)
        EXPECTED_MD = [('ep', 'place', 'Hailey,ID'),
         ('tse', 'place', 'Stamford,CT'),
         ('tse', 'opus', 'r2e0e3e5'),
         ('r2e0e3e5', 'title', 'The Wasteland'),
         ('tse', 'tag', 'old possum'),
         ('tse', 'tag', 'poet'),
         ('lh', 'place', 'Harlem,NY'),
         ('lh', 'tag', 'poet'),
         ('co', 'place', 'Idoto,Anambra'),
         ('co', 'opus', 'r2e0e7e5'),
         ('r2e0e7e5', 'title', "Heaven's Gate"),
         ('co', 'tag', 'biafra'),
         ('co', 'tag', 'poet')]
        import sys
        print >> sys.stderr, list(metadata)
        meta_list = normalize_generated_ids(list(metadata))
        self.assertEqual(meta_list, normalize_generated_ids(EXPECTED_MD))


if __name__ == '__main__':
    from amara.test import test_main
    testsupport.test_main()