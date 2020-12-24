# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/tests/test_etl.py
# Compiled at: 2015-07-08 07:34:06
"""dossier.models.tests for ETL

.. This software is released under an MIT/X11 open source license.
   Copyright 2015 Diffeo, Inc.
"""
from dossier.models.tests import nltk_data
from dossier.models.etl import html_to_fc
test_html = '\n\n    <body id="ViewAd">\n  <!-- Google Tag Manager -->\n  <noscript><iframe src="//www.googletagmanager.com/ns.html?id=GTM-5KCSP8"\n  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({\'gtm.start\': \n  new Date().getTime(),event:\'gtm.js\'});var f=d.getElementsByTagName(s)[0],\n  j=d.createElement(s),dl=l!=\'dataLayer\'?\'&l=\'+l:\'\';j.async=true;j.src=\n  \'//www.googletagmanager.com/gtm.js?id=\'+i+dl;f.parentNode.insertBefore(j,f);\n  })(window,document,\'script\',\'bpDataLayer\',\'GTM-5KCSP8\');</script>\n  <!-- End Google Tag Manager -->\n    <div id="tlHeader">\n<div id="postAdButton">\n<form name="formPost" id="formPost" action="http://posting.newyork.backpage.com/online/classifieds/PostAdPPI.html/nyc/newyork.backpage.com/" method="get">\n      <input type="submit" value="Post Ad" class="button" id="postAdButton">\n      <input type="hidden" name="u" value="nyc">\n      <input type="hidden" name="serverName" value="newyork.backpage.com">\n    </form>\n        </div><!-- #postAdButton -->\n          <span class="formSearchHideOnSmallScreens">\n          <input type="text" size="15" name="keyword" value=" keyword" onFocus="if (document.formSearch.keyword.value == \' keyword\') document.formSearch.keyword.value = \'\'; return true;" maxlength="100">\n            <select name="section">\n                  <option value="26197783">local places\n                  <option value="4382">community\n                  <option value="4378">buy/ sell/ trade\n                  <option value="153676">automotive\n                  <option value="4380">musician\n                  <option value="4376">rentals\n                  <option value="4375">real estate\n                  <option value="4373">jobs\n</select>\nTraveling across the country to buy real estate.\n</body>\n'

def test_html_to_fc(nltk_data):
    fc = html_to_fc(test_html.decode('utf8'))
    assert 'Date' not in fc['meta_clean_html']
    assert 'bowNP_unnorm' in fc
    assert set(fc['bowNP_unnorm'].keys()) == set(['real estate', 'country'])