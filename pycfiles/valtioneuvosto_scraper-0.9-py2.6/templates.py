# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/valtioneuvosto_scraper/templates.py
# Compiled at: 2010-07-13 17:15:45
tmpl_main = '\n\n<?xml version="1.0" encoding="UTF-8"?>\n<hallitukset xmlns="http://valtioneuvosto.fi/namespaces/2010/07">\n   %s\n</hallitukset>\n\n'
tmpl_government = '\n\n   <hallitus tunniste="%i" tyyppi="%s" kesto="%i">%s\n      <aloitus>%s</aloitus>\n      <lopetus>%s</lopetus>\n      %s\n   </hallitus>\n'
tmpl_position = '      <salkku>%s\n         %s\n      </salkku>'
tmpl_minister = '\n\n         <ministeri puolue="%s">%s\n            <nimitetty>%s</nimitetty>\n            <eronnut>%s</eronnut>\n         </ministeri>\n\n'