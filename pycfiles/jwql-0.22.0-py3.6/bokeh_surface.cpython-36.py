# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/bokeh_templating/bokeh_surface.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 6146 bytes
"""
Created on Mon May 21 13:45:34 2018

@author: gkanarek
"""
from bokeh.core.properties import Instance, String, Any, Dict
from bokeh.models import ColumnDataSource, LayoutDOM
DEFAULTS = {'width':'600px', 
 'height':'600px', 
 'style':'surface', 
 'showPerspective':True, 
 'showGrid':True, 
 'keepAspectRatio':True, 
 'verticalRatio':1.0, 
 'legendLabel':'stuff', 
 'cameraPosition':{'horizontal':-0.35, 
  'vertical':0.22, 
  'distance':1.8}}
JS_CODE = '\n# This file contains the JavaScript (CoffeeScript) implementation\n# for a Bokeh custom extension. The "surface3d.py" contains the\n# python counterpart.\n#\n# This custom model wraps one part of the third-party vis.js library:\n#\n#     http://visjs.org/index.html\n#\n# Making it easy to hook up python data analytics tools (NumPy, SciPy,\n# Pandas, etc.) to web presentations using the Bokeh server.\n\n# These "require" lines are similar to python "import" statements\nimport * as p from "core/properties"\nimport {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"\n\n# This defines some default options for the Graph3d feature of vis.js\n# See: http://visjs.org/graph3d_examples.html for more details.\nOPTIONS =\n  width:  \'600px\'\n  height: \'600px\'\n  style: \'surface\'\n  showPerspective: true\n  showGrid: true\n  keepAspectRatio: true\n  verticalRatio: 1.0\n  legendLabel: \'stuff\'\n  cameraPosition:\n    horizontal: -0.35\n    vertical: 0.22\n    distance: 1.8\n\n# To create custom model extensions that will render on to the HTML canvas\n# or into the DOM, we must create a View subclass for the model. Currently\n# Bokeh models and views are based on BackBone. More information about\n# using Backbone can be found here:\n#\n#     http://backbonejs.org/\n#\n# In this case we will subclass from the existing BokehJS ``LayoutDOMView``,\n# corresponding to our\nexport class Surface3dView extends LayoutDOMView\n\n  initialize: (options) ->\n    super(options)\n\n    url = "https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"\n\n    script = document.createElement(\'script\')\n    script.src = url\n    script.async = false\n    script.onreadystatechange = script.onload = () => @_init()\n    document.querySelector("head").appendChild(script)\n\n  _init: () ->\n    # Create a new Graph3s using the vis.js API. This assumes the vis.js has\n    # already been loaded (e.g. in a custom app template). In the future Bokeh\n    # models will be able to specify and load external scripts automatically.\n    #\n    # Backbone Views create <div> elements by default, accessible as @el. Many\n    # Bokeh views ignore this default <div>, and instead do things like draw\n    # to the HTML canvas. In this case though, we use the <div> to attach a\n    # Graph3d to the DOM.\n    @_graph = new vis.Graph3d(@el, @get_data(), @model.options)\n\n    # Set Backbone listener so that when the Bokeh data source has a change\n    # event, we can process the new data\n    @listenTo(@model.data_source, \'change\', () =>\n        @_graph.setData(@get_data())\n    )\n\n  # This is the callback executed when the Bokeh data has an change. Its basic\n  # function is to adapt the Bokeh data source to the vis.js DataSet format.\n  get_data: () ->\n    data = new vis.DataSet()\n    source = @model.data_source\n    for i in [0...source.get_length()]\n      data.add({\n        x:     source.get_column(@model.x)[i]\n        y:     source.get_column(@model.y)[i]\n        z:     source.get_column(@model.z)[i]\n      })\n    return data\n\n# We must also create a corresponding JavaScript Backbone model sublcass to\n# correspond to the python Bokeh model subclass. In this case, since we want\n# an element that can position itself in the DOM according to a Bokeh layout,\n# we subclass from ``LayoutDOM``\nexport class Surface3d extends LayoutDOM\n\n  # This is usually boilerplate. In some cases there may not be a view.\n  default_view: Surface3dView\n\n  # The ``type`` class attribute should generally match exactly the name\n  # of the corresponding Python class.\n  type: "Surface3d"\n\n  # The @define block adds corresponding "properties" to the JS model. These\n  # should basically line up 1-1 with the Python model class. Most property\n  # types have counterparts, e.g. ``bokeh.core.properties.String`` will be\n  # ``p.String`` in the JS implementatin. Where the JS type system is not yet\n  # as rich, you can use ``p.Any`` as a "wildcard" property type.\n  @define {\n    x:           [ p.String           ]\n    y:           [ p.String           ]\n    z:           [ p.String           ]\n    data_source: [ p.Instance         ]\n    options:     [ p.Any,     OPTIONS ]\n  }\n'

class Surface3d(LayoutDOM):
    __implementation__ = JS_CODE
    data_source = Instance(ColumnDataSource)
    x = String
    y = String
    z = String
    color = String
    options = Dict(String, Any, default=DEFAULTS)