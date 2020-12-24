# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miranda/.virtualenvs/vf_utils/lib/python3.6/site-packages/vf_createproducts_core/json_templates.py
# Compiled at: 2018-10-04 13:50:12
# Size of source mod 2**32: 2680 bytes
"""
Copyright (2017) Raydel Miranda 

This file is part of "VillaFlores Product Creator".

    "VillaFlores Product Creator" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "VillaFlores Product Creator" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "VillaFlores Product Creator".  If not, see <http://www.gnu.org/licenses/>.
"""
FABRIC_JSON = '{\n  "templateId": "emptyTemplate",\n  "drawingAreaId": "drawingArea",\n  "width": 800,\n  "height": 800,\n  "shapes": [\n    {\n      "type": "appImage",\n      "order": 1,\n      "selectable": true,\n      "url": "%(background_url)s",\n      "left": 0,\n      "top": 0,\n      "width": 800,\n      "height": 800,\n      "originX": "left",\n      "originY": "top",\n      "fill": "",\n      "stroke": null,\n      "strokeWidth": 1,\n      "strokeDashArray": null,\n      "strokeLineCap": "butt",\n      "strokeLineJoin": "miter",\n      "strokeMiterLimit": 10,\n      "scaleX": 1,\n      "scaleY": 1,\n      "angle": 0,\n      "flipX": false,\n      "flipY": false,\n      "opacity": 1,\n      "shadow": null,\n      "visible": true,\n      "clipTo": null,\n      "backgroundColor": "",\n      "fillRule": "nonzero",\n      "globalCompositeOperation": "source-over",\n      "transformMatrix": null,\n      "skewX": 0,\n      "skewY": 0\n    },\n    {\n      "order": 2,\n      "type": "appImage",\n      "originX": "left",\n      "originY": "top",\n      "left": 0,\n      "top": 0,\n      "width": 800,\n      "height": 570,\n      "fill": "rgb(0,0,0)",\n      "stroke": null,\n      "strokeWidth": 0,\n      "strokeDashArray": null,\n      "strokeLineCap": "butt",\n      "strokeLineJoin": "miter",\n      "strokeMiterLimit": 10,\n      "scaleX": 1,\n      "scaleY": 1,\n      "angle": 0,\n      "flipX": false,\n      "flipY": false,\n      "opacity": 1,\n      "shadow": null,\n      "visible": true,\n      "clipTo": null,\n      "backgroundColor": "",\n      "fillRule": "nonzero",\n      "globalCompositeOperation": "source-over",\n      "transformMatrix": null,\n      "skewX": 0,\n      "skewY": 0,\n      "crossOrigin": "",\n      "alignX": "none",\n      "alignY": "none",\n      "meetOrSlice": "meet",\n      "selectable": true,\n      "url": "%(flowers_url)s",\n      "filters": [],\n      "resizeFilters": []\n    }\n  ]\n}\n'