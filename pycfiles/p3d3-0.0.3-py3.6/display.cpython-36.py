# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p3d3/display.py
# Compiled at: 2018-03-06 12:11:25
# Size of source mod 2**32: 2342 bytes
from IPython.display import HTML, display
from string import Template
import json, uuid
from .util import sanitize, P3JsonEncoder

def init(version='4.13.0'):
    display(HTML('<script>\nrequirejs.config({\n    paths: {\n        d3: "//cdnjs.cloudflare.com/ajax/libs/d3/' + version + '/d3",\n        vg: "https://cdn.jsdelivr.net/npm/vega@3.0.10?noext",\n        vl: "https://cdn.jsdelivr.net/npm/vega-lite@2.1.3?noext",\n        vg_embed: "https://cdn.jsdelivr.net/npm/vega-embed@3.0.0?noext"\n    },\n    shim: {\n        vg_embed: {deps: ["vg.global", "vl.global"]},\n        vl: {deps: ["vg"]},\n        vg: {deps: ["d3"]}\n    }\n});\nrequire([\'d3\'], function(d3) {\n    window.d3 = d3;\n});\n\ndefine(\'vg.global\', [\'vg\'], function(vgGlobal) {\n    window.vega = vgGlobal;\n});\n\ndefine(\'vl.global\', [\'vl\'], function(vlGlobal) {\n    window.vl = vlGlobal;\n});\n\nrequire(["vg_embed"], function(vg_embed) {\n    window.vg_embed = vg_embed;\n});\n</script>'))


def p3d3(df, jsfile, params={}, width=800, height=500):
    script = ''
    with open(jsfile, 'r') as (script_file):
        script = script_file.read()
    tmp = Template('\n        <svg id="$id"></svg>\n        <script type="text/javascript">\n\t(function() {\n        $script\n\n        main(d3.select("#$id"), $data, $params, $width, $height);\n        })();\n        </script>')
    display(HTML(tmp.substitute({'id':'a' + str(uuid.uuid4()), 
     'script':script, 
     'data':sanitize(df).to_json(orient='records'), 
     'params':json.dumps(params, cls=P3JsonEncoder), 
     'width':width, 
     'height':height})))


def vegalite(df, specs):
    tmp = Template('\n        <div id="$id"></div>\n        <script type="text/javascript">\n            vg_embed("#$id", $specs, {actions: {source: false, editor: false} });\n\n        </script>')
    specifications = specs
    specifications['$schema'] = 'https://vega.github.io/schema/vega-lite/v2.json'
    specifications['data'] = dict(values=sanitize(df).to_dict(orient='records'))
    if 'width' not in specifications:
        specifications['width'] = 800
    if 'height' not in specifications:
        specifications['height'] = 500
    display(HTML(tmp.substitute({'id':'a' + str(uuid.uuid4()), 
     'specs':json.dumps(specifications, cls=P3JsonEncoder)})))