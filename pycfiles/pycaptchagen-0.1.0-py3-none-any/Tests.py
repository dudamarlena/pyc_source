# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Captcha/Visual/Tests.py
# Compiled at: 2006-02-05 00:25:47
__doc__ = ' Captcha.Visual.Tests\n\nVisual CAPTCHA tests\n'
from Captcha.Visual import Text, Backgrounds, Distortions, ImageCaptcha
from Captcha import Words
import random
__all__ = [
 'PseudoGimpy', 'AngryGimpy', 'AntiSpam']

class PseudoGimpy(ImageCaptcha):
    """A relatively easy CAPTCHA that's somewhat easy on the eyes"""
    __module__ = __name__

    def getLayers(self):
        word = Words.defaultWordList.pick()
        self.addSolution(word)
        return [
         random.choice([Backgrounds.CroppedImage(), Backgrounds.TiledImage()]), Text.TextLayer(word, borderSize=1), Distortions.SineWarp()]


class AngryGimpy(ImageCaptcha):
    """A harder but less visually pleasing CAPTCHA"""
    __module__ = __name__

    def getLayers(self):
        word = Words.defaultWordList.pick()
        self.addSolution(word)
        return [
         Backgrounds.TiledImage(), Backgrounds.RandomDots(), Text.TextLayer(word, borderSize=1), Distortions.WigglyBlocks()]


class AntiSpam(ImageCaptcha):
    """A fixed-solution CAPTCHA that can be used to hide email addresses or URLs from bots"""
    __module__ = __name__
    fontFactory = Text.FontFactory(20, 'vera/VeraBd.ttf')
    defaultSize = (512, 50)

    def getLayers(self, solution='murray@example.com'):
        self.addSolution(solution)
        textLayer = Text.TextLayer(solution, borderSize=2, fontFactory=self.fontFactory)
        return [
         Backgrounds.CroppedImage(), textLayer, Distortions.SineWarp(amplitudeRange=(2, 4))]