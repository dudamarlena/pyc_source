# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/project_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 8886 bytes
import unittest
from unittest import mock
from .make import make
from bibliopixel.animation import animation
from bibliopixel.colors import gamma, tables
from bibliopixel.drivers.ledtype import LEDTYPE
BAD_JSON_ERROR = '\nwhile parsing a flow node\nexpected the node content, but found \']\'\n  in "<unicode string>", line 1, column 2:\n    {]\n     ^\n'

class ProjectTest(unittest.TestCase):

    @mock.patch('bibliopixel.util.data_file.ALWAYS_LOAD_YAML', False)
    def test_bad_project_json(self):
        with self.assertRaises(Exception):
            make('{]')

    @mock.patch('bibliopixel.util.data_file.ALWAYS_LOAD_YAML', True)
    def test_bad_project_yaml(self):
        with self.assertRaises(Exception) as (e):
            make('{]')
        self.assertEqual(str(e.exception).strip(), BAD_JSON_ERROR.strip())

    def test_simple(self):
        make(PROJECT)

    def test_types(self):
        animation = make(PROJECT_TYPES)
        kwds = animation.layout.drivers[0]._kwds
        self.assertEqual(kwds['c_order'], (1, 2, 0))
        self.assertEqual(kwds['color'], (0, 255, 0))
        self.assertEqual(kwds['duration'], 3720)
        self.assertEqual(kwds['gamma'].table, gamma.APA102.table)
        self.assertEqual(kwds['time'], 35000)
        self.assertEqual(kwds['ledtype'], LEDTYPE.GENERIC)

    def test_file(self):
        make('test/bibliopixel/project/project.json', False)

    def test_yaml_file(self):
        make('test/bibliopixel/project/project.yml', False)

    def test_super(self):
        animation = make('test/bibliopixel/project/super_project.json', False)
        self.assertEqual(animation.__class__.__name__, 'StripChannelTest')
        self.assertEqual(animation.layout.pixelWidth, 2)

    def test_multi(self):
        animation = make(PROJECT_MULTI)
        k = [d._kwds for d in animation.layout.drivers]
        self.assertEqual(k[0]['device_id'], 10)
        self.assertEqual(k[1]['device_id'], 11)
        self.assertEqual(k[2]['device_id'], 12)

    def test_shared(self):
        make(PROJECT_SHARED)

    def test_sequence(self):
        animation = make(PROJECT_SEQUENCE, run_start=False)
        self.assertEqual(len(animation.animations), 3)
        self.assertIsNotNone(animation.animations[0])
        animation = animation.animations[1]
        self.assertEqual(animation.name, 'mt')
        self.assertEqual(animation.layout.rotation, 90)

    def test_sub_animation_names(self):
        animation = make(PROJECT_SUB_ANIMATIONS, run_start=False)
        self.assertEqual(animation.name, 'Sequence')
        a, b, c, d = animation.animations
        self.assertEqual(a.name, 'StripChannelTest_0')
        self.assertEqual(d.name, 'StripChannelTest_3')
        animation.pre_run()
        self.assertEqual(animation.animations.StripChannelTest_2, c)
        self.assertEqual(animation.animations['StripChannelTest_1'], b)

    def test_numpy(self):
        make(PROJECT_NUMPY)

    def test_pixelwidth(self):
        make(PROJECT_PIXELWIDTH)

    def test_aliases(self):
        make(PROJECT_ALIASES)

    def test_simpixel(self):
        animation = make(PROJECT_SIM, run_start=False)
        self.assertEqual(animation.name, 'test name')
        self.assertEqual(animation.data, {'title': 'test title'})

    def test_project_from_animation_class(self):
        animation = make(PROJECT_ANIMATION)
        self.assertEqual(animation.layout.rotation, 90)

    def test_nested_animation(self):
        make(PROJECT_NESTED_ANIMATION, run_start=False)

    def test_nested_sequence(self):
        make(PROJECT_NESTED_SEQUENCE, run_start=False)

    def test_project_colors(self):
        try:
            make(PROJECT_COLORS, run_start=False)
            self.assertEqual(tables.get_color('bland'), (1, 2, 3))
            self.assertEqual(tables.get_name((3, 2, 1)), 'exciting!!')
            self.assertIs(tables.get_color('exciting'), None)
        finally:
            tables.set_user_colors({})

        self.assertEqual(tables.get_color('bland'), None)

    def test_test_example(self):
        make(PROJECT_TEST_EXAMPLE)


PROJECT = '\n{\n    "driver": "dummy",\n    "shape": 12,\n    "layout": "strip",\n    "animation": ".tests.StripChannelTest",\n    "run": {\n        "max_steps": 2\n    }\n}\n'
PROJECT_TYPES = '\n{\n    "driver": {\n        "typename": "dummy",\n        "c_order": "GBR",\n        "color": "green",\n        "duration": "1 hour, 2 minutes",\n        "gamma": "APA102",\n        "time": "35ks",\n        "ledtype": "GENERIC"\n    },\n\n    "shape": 12,\n    "layout": "strip",\n    "animation": ".tests.StripChannelTest",\n    "run": {\n        "max_steps": 2\n    }\n}\n'
PROJECT_MULTI = '\n{\n    "driver": {\n        "typename": "dummy",\n        "num": 4096\n    },\n\n    "drivers": [\n        {"device_id": 10},\n        {"device_id": 11},\n        {"device_id": 12}\n    ],\n\n    "layout": {\n        "typename": "matrix",\n        "width": 128,\n        "height": 32,\n        "gen_coord_map": [\n            {\n              "dx": 32,\n              "dy": 32\n            },\n            {\n              "dx": 32,\n              "dy": 32\n            },\n            {\n              "dx": 32,\n              "dy": 32\n            }\n        ]\n    },\n\n    "animation": ".tests.MatrixChannelTest",\n\n    "run": {\n        "max_steps": 2\n    }\n}\n'
PROJECT_SHARED = '\n{\n    "driver": {\n        "typename": "dummy",\n        "num": 12\n    },\n\n    "layout": "strip",\n    "animation": ".tests.StripChannelTest",\n    "run": {\n        "max_steps": 2\n    },\n\n    "maker": {\n        "shared_memory": true\n    }\n}\n'
PROJECT_NUMPY = '\n{\n    "driver": {\n        "typename": "dummy",\n        "num": 12\n    },\n\n    "layout": "bibliopixel.layout.strip.Strip",\n    "animation": ".tests.StripChannelTest",\n    "run": {\n        "max_steps": 2\n    },\n\n    "maker": {\n        "numpy_dtype": "float"\n    }\n}\n'
PROJECT_SIM = '\n{\n    "driver": {\n        "typename": ".SimPixel",\n        "num": 12,\n        "port": 1338\n    },\n\n    "layout": {\n        "typename": ".strip"\n    },\n\n    "animation": {\n        "typename": ".tests.StripChannelTest",\n        "name": "test name",\n        "data": {"title": "test title"}\n    },\n\n    "run": {\n        "max_steps": 2\n    }\n}\n'
PROJECT_SEQUENCE = '\n{\n    "driver": "dummy",\n\n    "layout": {\n        "typename": "matrix",\n        "rotation": 92\n    },\n\n    "animation": {\n        "typename": "sequence",\n\n        "animations": [\n            ".tests.MatrixChannelTest",\n            {\n                "typename": ".tests.MatrixChannelTest",\n                "name": "mt",\n                "data": {"title": "test title"}\n            },\n            {\n                "animation": {\n                    "typename": ".tests.MatrixChannelTest",\n                    "name": "mt2",\n                    "data": {"title": "test title"}\n                }\n            }\n        ]\n    }\n}\n'
PROJECT_ALIASES = '\n{\n    "aliases": {\n        "st": "bibliopixel.layout.strip",\n        "stc": ".tests.StripChannelTest"\n    },\n\n    "driver": {\n        "typename": "dummy",\n        "num": 12\n    },\n\n    "layout": "@st.Strip",\n    "animation": "stc",\n    "run": {\n        "max_steps": 2\n    }\n}\n'
PROJECT_PIXELWIDTH = '\n{\n    "driver": {\n        "typename": "dummy",\n        "num": 12\n    },\n\n    "layout": {\n        "typename": "strip",\n        "pixelWidth": 3\n    },\n\n    "animation": ".tests.StripChannelTest",\n    "run": {\n        "max_steps": 2\n    }\n}\n'
PROJECT_SUB_ANIMATIONS = '\n{\n    "driver": {\n        "typename": "dummy",\n        "num": 12\n    },\n\n    "layout": {\n        "typename": "strip",\n        "pixelWidth": 3\n    },\n\n    "animation": {\n        "typename": "sequence",\n        "animations": [".tests.StripChannelTest",\n                       ".tests.StripChannelTest",\n                       ".tests.StripChannelTest",\n                       ".tests.StripChannelTest"]\n    },\n\n    "run": {\n        "max_steps": 2\n    }\n}\n'
PROJECT_ANIMATION = '\n{"animation": "test.bibliopixel.project.project_test.AnimationTest"}\n'
PROJECT_NESTED_ANIMATION = '\nshape: [32, 32]\nanimation:\n  typename: .wrapper\n  animation:\n      typename: .wrapper\n      animation: $bpa.matrix.bloom\n'
PROJECT_NESTED_SEQUENCE = '\nshape: [32, 32]\nanimation:\n  typename: .sequence\n  animations:\n      - typename: .sequence\n        animations:\n        - $bpa.matrix.bloom\n'
PROJECT_COLORS = "\nshape: 32\nanimation: .tests.StripChannelTest\ncolors:\n  bland: [1, 2, 3]\n  'exciting!!': [3, 2, 1]\n"
PROJECT_TEST_EXAMPLE = '\ndriver: dummy\nshape: [48, 24]\nanimation: test.bibliopixel.animation.documentation_class.Example26\nrun:\n  max_steps: 4\n'

class AnimationTest(animation.Animation):
    PROJECT = {'driver':'dummy', 
     'layout':{'typename':'matrix', 
      'rotation':92}, 
     'run':{'max_steps': 2}}

    def step(self, amt=1):
        pass