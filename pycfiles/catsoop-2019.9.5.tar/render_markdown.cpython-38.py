# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__UTIL__/api/render_markdown.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1272 bytes
import bs4, json
if 'source' in cs_form:
    try:
        sources = json.loads(cs_form['source'])
    except:
        sources = [
         cs_form['source']]

else:
    sources = []
cs_handler = 'raw_response'
content_type = 'application/json'
lang = csm_language
soup = bs4.BeautifulSoup
response = [csm_language._md_format_string(globals(), i, False) for i in sources]
response = json.dumps([str(lang.handle_math_tags(soup(i, 'html.parser'))) for ix, i in enumerate(response)])