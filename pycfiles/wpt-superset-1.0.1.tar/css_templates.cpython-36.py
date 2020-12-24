# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/data/css_templates.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 3617 bytes
import textwrap
from superset import db
from superset.models.core import CssTemplate

def load_css_templates():
    """Loads 2 css templates to demonstrate the feature"""
    print('Creating default CSS templates')
    obj = db.session.query(CssTemplate).filter_by(template_name='Flat').first()
    if not obj:
        obj = CssTemplate(template_name='Flat')
    css = textwrap.dedent("    .gridster div.widget {\n        transition: background-color 0.5s ease;\n        background-color: #FAFAFA;\n        border: 1px solid #CCC;\n        box-shadow: none;\n        border-radius: 0px;\n    }\n    .gridster div.widget:hover {\n        border: 1px solid #000;\n        background-color: #EAEAEA;\n    }\n    .navbar {\n        transition: opacity 0.5s ease;\n        opacity: 0.05;\n    }\n    .navbar:hover {\n        opacity: 1;\n    }\n    .chart-header .header{\n        font-weight: normal;\n        font-size: 12px;\n    }\n    /*\n    var bnbColors = [\n        //rausch    hackb      kazan      babu      lima        beach     tirol\n        '#ff5a5f', '#7b0051', '#007A87', '#00d1c1', '#8ce071', '#ffb400', '#b4a76c',\n        '#ff8083', '#cc0086', '#00a1b3', '#00ffeb', '#bbedab', '#ffd266', '#cbc29a',\n        '#ff3339', '#ff1ab1', '#005c66', '#00b3a5', '#55d12e', '#b37e00', '#988b4e',\n     ];\n    */\n    ")
    obj.css = css
    db.session.merge(obj)
    db.session.commit()
    obj = db.session.query(CssTemplate).filter_by(template_name='Courier Black').first()
    if not obj:
        obj = CssTemplate(template_name='Courier Black')
    css = textwrap.dedent("    .gridster div.widget {\n        transition: background-color 0.5s ease;\n        background-color: #EEE;\n        border: 2px solid #444;\n        border-radius: 15px;\n        box-shadow: none;\n    }\n    h2 {\n        color: white;\n        font-size: 52px;\n    }\n    .navbar {\n        box-shadow: none;\n    }\n    .gridster div.widget:hover {\n        border: 2px solid #000;\n        background-color: #EAEAEA;\n    }\n    .navbar {\n        transition: opacity 0.5s ease;\n        opacity: 0.05;\n    }\n    .navbar:hover {\n        opacity: 1;\n    }\n    .chart-header .header{\n        font-weight: normal;\n        font-size: 12px;\n    }\n    .nvd3 text {\n        font-size: 12px;\n        font-family: inherit;\n    }\n    body{\n        background: #000;\n        font-family: Courier, Monaco, monospace;;\n    }\n    /*\n    var bnbColors = [\n        //rausch    hackb      kazan      babu      lima        beach     tirol\n        '#ff5a5f', '#7b0051', '#007A87', '#00d1c1', '#8ce071', '#ffb400', '#b4a76c',\n        '#ff8083', '#cc0086', '#00a1b3', '#00ffeb', '#bbedab', '#ffd266', '#cbc29a',\n        '#ff3339', '#ff1ab1', '#005c66', '#00b3a5', '#55d12e', '#b37e00', '#988b4e',\n     ];\n    */\n    ")
    obj.css = css
    db.session.merge(obj)
    db.session.commit()