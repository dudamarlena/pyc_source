# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kss/plugin/livesearch/demo/kss_livesearch_demo.py
# Compiled at: 2008-05-23 06:03:39
from kss.plugin.livesearch.autocompleteview import AutoCompleteView

class DemoView(AutoCompleteView):
    __module__ = __name__
    data = [
     'hauser', 'natea', 'mateola', 'jchamm', 'ree', 'ree_', 'martior', 'dcnoye', 'jonstahl', 'SteveM', 'grahamperrin', 'ErikRose', 'heureso', 'cbcunc', 'enzo', 'esteele', 'geojeff', 'wildintellect', 'Gogo', 'aclark', 'zenwryly', 'SnarfBot', 'siebo', 'siebo_', 'DigitalD', 'place', 'plate', 'plural', 'plone', 'apostle', 'april', 'apple']
    data.sort()

    def update(self, q, limit=10):
        words = self.data
        term = q.strip()
        self.results = results = []
        if not term:
            return
        for w in words:
            if w.lower().startswith(term.lower()):
                if len(results) < limit:
                    results.append(w)
                else:
                    self.showMore = True
                    break