# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/util/image/extract_gif_lines_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1947 bytes
import unittest
from unittest.mock import patch
from bibliopixel.util.image import extract_gif_lines

class ExtractGifLinesTest(unittest.TestCase):

    def test_extract(self):
        actual = list(extract_gif_lines._extract(GIF_LINES))
        self.assertEqual(actual, EXPECTED1)

    def test_extract_gif_lines(self):
        actual = list(extract_gif_lines.extract_gif_lines(GIF_LINES))
        self.assertEqual(actual, EXPECTED2)

    def test_errors(self):
        actual = list(extract_gif_lines.extract_gif_lines(BAD_LINES))
        self.assertEqual(actual, EXPECTED2)


GIF_LINES = "\n\n# Here's some stuff.\n# now code\n\n.. code-block:: yaml\n\n    math.frog(23)\n    print('glog')\n\n# But there's no GIF file.\n# More code:\n\n.. code-block:: yaml\n\n    animation: BiblioPixelAnimations.matrix.MatrixRain\n    shape: [2, 2]\n\n.. code-block:: yaml\n\n    animation: BiblioPixelAnimations.matrix.MatrixRain\n    shape: [32, 32]\n\n.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/bibliopixel/animations/something.gif\n\n.. code-block:: yaml\n\n    animation: .split\n    shape: 128\n\n.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/bibliopixel/animations/minimal.gif\n".splitlines()
BAD_LINES = GIF_LINES + '\n\n.. code-block:: json\n\n    }}}\n\n... image: blah.gif\n'.splitlines()
YAML_LINES_1 = 'animation: BiblioPixelAnimations.matrix.MatrixRain\nshape: [32, 32]\n'.splitlines()
YAML_LINES_2 = 'animation: .split\nshape: 128\n'.splitlines()
EXPECTED1 = [
 (
  'doc/bibliopixel/animations/something.gif', YAML_LINES_1),
 (
  'doc/bibliopixel/animations/minimal.gif', YAML_LINES_2)]
DATA1 = {'animation':'BiblioPixelAnimations.matrix.MatrixRain', 
 'shape':[
  32, 32]}
DATA2 = {'animation':'.split', 
 'shape':128}
EXPECTED2 = [
 (
  'doc/bibliopixel/animations/something.gif', DATA1),
 (
  'doc/bibliopixel/animations/minimal.gif', DATA2)]