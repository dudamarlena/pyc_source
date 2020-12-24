# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\PhD\phiflow_github\webglviewer\Webglviewer.py
# Compiled at: 2020-02-07 14:00:04
# Size of source mod 2**32: 2300 bytes
from dash.development.base_component import Component, _explicitize_args

class Webglviewer(Component):
    __doc__ = 'A Webglviewer component.\nExampleComponent is an example component.\nIt takes a property, `label`, and\ndisplays it.\nIt renders an input with the property `value`\nwhich is editable by the user.\n\nKeyword arguments:\n- id (string; required): The ID used to identify this component in Dash callbacks.\n- data (list; optional): A grid or a list of grids that will be rendered when this component is rendered.\n- idx (number; optional): Index of datum in data list which should be rendered.\n- sky (list; optional): Sky map, expects an array of six arrays.\nValue have to be between 0 and 255.\nEach array represents one side of the cube map (flattened pixels of an image).\nExpects 4 channels (r,g,b,a).\nImage has to be quadratic.\n- material_type (string; optional): Material type used for rendering.\nPossible types: SMOKE, DARK_SMOKE, LIGHT_SMOKE, SOLID, LIQUID\n- representation_type (string; optional): Specifies the representation type used.\nPossible types: DENSITY, SDF, PARTICLE\n- scale (number; optional): Particle scale.'

    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, data=Component.UNDEFINED, idx=Component.UNDEFINED, sky=Component.UNDEFINED, material_type=Component.UNDEFINED, representation_type=Component.UNDEFINED, scale=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data', 'idx', 'sky', 'material_type', 'representation_type', 'scale']
        self._type = 'Webglviewer'
        self._namespace = 'webglviewer'
        self._valid_wildcard_attributes = []
        self.available_properties = ['id', 'data', 'idx', 'sky', 'material_type', 'representation_type', 'scale']
        self.available_wildcard_properties = []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)
        args = {k:_locals[k] for k in _explicit_args if k != 'children'}
        for k in ('id', ):
            if k not in args:
                raise TypeError('Required argument `' + k + '` was not specified.')

        (super(Webglviewer, self).__init__)(**args)