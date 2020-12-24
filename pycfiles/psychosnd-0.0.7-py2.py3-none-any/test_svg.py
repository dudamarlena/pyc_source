# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mindhive/dicarlolab/u/qbilius/libs/psychopy_ext/psychopy_ext/tests/test_svg.py
# Compiled at: 2015-12-11 19:53:11
from psychopy import visual, core
from .. import exp
import unittest

class TestSVG(unittest.TestCase):

    def test_write(self):
        win = visual.Window([600, 400], units='height')
        svg = exp.SVG(win, filename='stims')
        circle = visual.Circle(win, pos=(-0.5, 0), fillColor='yellow', lineColor=None)
        circle.draw()
        svg.write(circle)
        line = visual.Line(win, pos=(0, 0), lineColor='black', lineWidth=5)
        line.draw()
        svg.write(line)
        rect = visual.Rect(win, height=0.8, pos=(0.5, 0))
        rect.draw()
        svg.write(rect)
        shape = visual.ShapeStim(win, fillColor='blue', opacity=0.5)
        shape.draw()
        svg.write(shape)
        text = visual.TextStim(win, pos=(0.5, 0.25))
        text.draw()
        svg.write(text)
        thick = exp.ThickShapeStim(win, vertices=[(-0.5, 0.5), (0.5, -0.5)], lineWidth=0.01)
        thick.draw()
        svg.write(thick)
        win.flip()
        core.wait(5)
        return


if __name__ == '__main__':
    unittest.main()