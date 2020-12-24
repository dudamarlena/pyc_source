# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/HTMLPlotter/CustomModels/timestamp.py
# Compiled at: 2020-04-24 00:12:01
# Size of source mod 2**32: 1875 bytes
from bokeh.core.properties import String
from bokeh.models import LayoutDOM
from bokeh.util.compiler import TypeScript
JS_CODE = '\nimport * as p from "core/properties"\nimport {div, empty} from "core/dom"\nimport {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"\nimport {LayoutItem} from "core/layout"\n\nexport class TimeStampView extends LayoutDOMView {\n    model: TimeStamp\n    \n    initialize(): void {\n        super.initialize()\n    }\n    render(): void {\n        empty(this.el)\n        this.el.appendChild(div({\n          style: {\n            \'width\': \'800px\',\n            \'word-spacing\': \'10px\',\n            \'font-size\': \'11px\',\n            \'color\': \'#000000\',\n            \'background-color\': \'#ffffff\',\n            },\n        }, `${this.model.text}`))\n    }\n    \n    _update_layout(): void {\n        this.layout = new LayoutItem()\n        this.layout.set_sizing(this.box_sizing())\n    }\n    \n    get child_models(): LayoutDOM[] {\n        return []\n      }\n}\n\n\nexport namespace TimeStamp {\n  export type Attrs = p.AttrsOf<Props>\n\n  export type Props = LayoutDOM.Props & {\n    text: p.Property<string>\n  }\n}\n\nexport interface TimeStamp extends TimeStamp.Attrs {}\n\nexport class TimeStamp extends LayoutDOM {\n    properties: TimeStamp.Props\n    static initClass(): void {\n    \n        this.prototype.default_view = TimeStampView\n    \n        this.define<TimeStamp.Props>({\n            text: [ p.String ]\n        })\n    }\n}\n\nTimeStamp.initClass()\n\n'

class TimeStamp(LayoutDOM):
    __implementation__ = TypeScript(JS_CODE)
    text = String(default='Testing')