# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/maltfy/textToDeepWebSearch.py
# Compiled at: 2014-12-24 13:01:28
from MaltegoTransform import *
import sys, json, urllib2, i3visiotools.darkfy.lib.processing as darkfy

def textToDeepWebSearch(text=None):
    """ 
                Method that performs a search on different deep web search engines. The output format is as follows:
 {
  "<text_to_be_looked_for>": {
    "i3visio.ahmia": [
      {
        "i3visio.date": [
          "Oct. 7, 2014, 5:12 p.m."
        ], 
        "i3visio.url": [
          " http://doxbinzqkeoso6sl.tor2web.fi/doxviewer.php?dox=Paula_Patr_cia"
        ], 
        "i3visio.text": [], 
        "i3visio.title": [
          " DOXBIN - POWERED BY PLAN9 FROM BELL LABS "
        ]
      }, 
...
}
                :param text:    text to be searched.

                :return:        None
        """
    me = MaltegoTransform()
    jsonData = darkfy.searchTerms(words=[text])
    for text in jsonData.keys():
        results = jsonData[text]
        for platform in results.keys():
            resources = results[platform]
            for res in resources:
                newEnt = me.addEntity('i3visio.text', res['i3visio.title'][0])
                newEnt.setDisplayInformation(json.dumps('<h3>' + res['i3visio.title'][0] + '</h3>\n' + str(res), sort_keys=True, indent=2))
                newEnt.addAdditionalFields('i3visio.platform', 'i3visio.platform', True, platform)
                for field in res.keys():
                    if field != 'i3visio.title':
                        try:
                            newEnt.addAdditionalFields(field, field, True, res[field][0])
                        except:
                            pass

    me.returnOutput()


if __name__ == '__main__':
    textToDeepWebSearch(text=sys.argv[1])