# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\libs\asslib.py
# Compiled at: 2012-05-17 11:57:04
"""This module defines the necessary things to load an ASS file,
and the objects that allow to draw text with cairo"""
import codecs, math
from draw import extra
import common
S_NAME = 'name'
S_FONT = 'fontname'
S_SIZE = 'fontsize'
S_FORMAT = 'format'
S_PCOLOR = 'primarycolour'
S_SCOLOR = 'secondarycolour'
S_OCOLOR = 'outlinecolour'
S_BCOLOR = 'backcolour'
S_MARGINV = 'marginv'
S_MARGINR = 'marginr'
S_MARGINL = 'marginl'
S_OUTLINE = 'outline'
S_ALIGN = 'alignment'
S_SHADOW = 'shadow'
S_BOLD = 'bold'
S_ITALIC = 'italic'
S_ANGLE = 'angle'
S_SCALE_X = 'scalex'
S_SCALE_Y = 'scaley'
E_FORMAT = 'format'
E_DIALOG = 'dialogue'
E_START = 'start'
E_END = 'end'
E_LAYER = 'layer'
E_STYLE = 'style'
E_TEXT = 'text'
E_EFFECT = 'effect'
F_EVENTS = '[events]'
F_SINFO = '[script info]'
F_STYLE4P = '[v4+ styles]'
F_STYLE4 = '[v4 styles]'

def TimeToMS(time):
    """Converts a string from type '0:00:00.00' from ASS to miliseconds in integer"""
    h, m, s = time.split(':')
    s, ms = s.split('.')
    result = int(h) * 60
    result += int(m)
    result *= 60
    result += int(s)
    result *= 1000
    result += int(ms) * 10
    return result


class cProperties:

    def __init__(self, other=None, dicc=None):
        """There are 3 ways to create a style:
                with nothing, it's done with default values.
                cProperties(other=othercopy) or cProperties(othercopy) copies the values of other
                cProperties(dicc=dictionary) initialize with the values of a ass dictionary"""
        self.color1 = extra.cCairoColor(number=4294909984)
        self.color2 = extra.cCairoColor(number=4286611584)
        self.color3 = extra.cCairoColor(number=4279242768)
        self.color4 = extra.cCairoColor(number=4286611584)
        self._layer = 0
        if other:
            self.CopyAllFrom(other)
        else:
            self.scale_x = 1.0
            self.scale_y = 1.0
            self.border = 3
            self.shadow = 0
            self.angle = 0
            self.pos_x = 30
            self.pos_y = 30
            self.org_x = 0
            self.org_y = 0
            self.shad_x = 0
            self.shad_y = 0
            self.mode_fill = 0
            self.mode_border = 0
            self.mode_shadow = 0
            self.mode_particle = 0
            self._name = 'EstiloManualmenteCreado'
            self._size = 12
            self._font = 'Verdana'
            self._bold = False
            self._italic = False
            self._marginv = 30
            self._marginr = 30
            self._marginl = 30
            self._align = 2
            self._x_bearing = 0
            self._y_bearing = 0
            self._x_advance = 0
            self._y_advance = 0
            self._ascent = 0
            self._descent = 0
            self._max_x_advance = 0
            self._max_y_advance = 0
            if dicc:
                self.FromDict(dicc)
        self._height = None
        self._width = None
        self._line_height = None
        return

    def CopyAllFrom(self, other):
        self.CopyFrom(other)
        self._name = other._name
        self._font = other._font
        self._size = other._size
        self._bold = other._bold
        self._italic = other._italic
        self._marginv = other._marginv
        self._marginr = other._marginr
        self._marginl = other._marginl
        self._align = other._align

    def CopyFrom(self, other):
        """Copies the data of another object from the same type
                @other it's an object of cProperties type

                only the animatable data is copied, it makes them faster that way.
                """
        self.pos_x = other.pos_x
        self.pos_y = other.pos_y
        self.org_x = other.org_x
        self.org_y = other.org_y
        self.shad_x = other.shad_x
        self.shad_y = other.shad_y
        self.scale_x = other.scale_x
        self.scale_y = other.scale_y
        self.angle = other.angle
        self.color1.CopyFrom(other.color1)
        self.color4.CopyFrom(other.color4)
        self.color3.CopyFrom(other.color3)
        self.color2.CopyFrom(other.color2)
        self.border = other.border
        self.shadow = other.shadow
        self.mode_fill = other.mode_fill
        self.mode_border = other.mode_border
        self.mode_shadow = other.mode_shadow
        self.mode_particle = other.mode_particle

    def FromDict(self, style):
        """Creates the values from a dictionary for internal use"""
        self.angle = math.radians(common.SafeGetFloat(style, S_ANGLE))
        self.color1 = extra.cCairoColor(text=style.get(S_PCOLOR, 0))
        self.color3 = extra.cCairoColor(text=style.get(S_OCOLOR, 0))
        self.color4 = extra.cCairoColor(text=style.get(S_BCOLOR, 0))
        self.color2 = extra.cCairoColor(text=style.get(S_SCOLOR, 0))
        self.border = common.SafeGetFloat(style, S_OUTLINE)
        self.shadow = int(common.SafeGetFloat(style, S_SHADOW))
        self.scale_x = common.SafeGetFloat(style, S_SCALE_X, 100) / 100.0
        self.scale_y = common.SafeGetFloat(style, S_SCALE_Y, 100) / 100.0
        self._name = style.get(S_NAME, '')
        self._font = style.get(S_FONT, '')
        self._size = common.SafeGetFloat(style, S_SIZE)
        self._bold = not style.get(S_BOLD, '0') == '0'
        self._italic = not style.get(S_ITALIC, '0') == '0'
        self._marginv = int(common.SafeGetFloat(style, S_MARGINV))
        self._marginr = int(common.SafeGetFloat(style, S_MARGINR))
        self._marginl = int(common.SafeGetFloat(style, S_MARGINL))
        self._align = int(common.SafeGetFloat(style, S_ALIGN))


class cSyllable(extra.cVector):

    def __init__(self, text='', style=None, parent=None, last_pos=None):
        """
                A syllable. It's better that the dialogue creates them because they need a special initialization.
                To use the syllable later we must call changeText(text, preposition)

                :param text: syllable's text
                :param style: Style of the syllable
                :param parent: Parent object
                :type text: string
                :type style: :class:`cProperties`
                :type parent: :class:`cDialogue`
                """
        extra.cVector.__init__(self, text=text, style=style, parent=parent, last_pos=last_pos)
        self._letters = []

    def SplitLetters(self):
        """Computes the characters of the syllable...
                Use if you change __text
                it's slow and eats more ram
                to access the Syllables use _letters later
                and activate the option in FxsGroup, too.
                """
        self._letters = []
        time = self._start
        last = (self.original.pos_x, self.original.pos_y)
        if not self._text:
            self._text = ''
            cdur = 0.0
        else:
            cdur = float(self._dur) / len(self._text)
        for i, tchar in enumerate(self._text):
            char = extra.cVector(text=tchar, style=self.original, parent=self, last_pos=last)
            char._indice = i
            char._start = time
            char._dur = cdur
            char._end = time = time + cdur
            char.effect = self.effect
            last = (char._next_x, char._next_y)
            self._letters.append(char)

    def Chain(self, function, duration=None):
        """Allows to Chain the characters to a animation.
                Before calling this function call DivideLetters
                or enable the option in FxsGroup
                @function function that will be called for each syllable and the progress
                @duration=None duration of the animatio of each character
                If not specified, a duration that animates one character per time will be used.
                (Note: do not change _text if you don't want inconsistencies)
                """
        common.Chain(self._dur, self.progress, self._letters, function, duration)

    def FullWiggle(self, amplitude=4, frequency=2, dx=None, dy=None):
        """the wiggle that AbelKM wanted, part 2
                """
        if dx is None:
            dx, dy = self.Wiggle(amplitude, frequency)
        o = self.original
        if not hasattr(o, 'old_x'):
            o.old_x = o.pos_x
            o.old_y = o.pos_y
        o.pos_x = o.old_x + dx
        o.pos_y = o.old_y + dy
        for let in self._letters:
            o = let.original
            if not hasattr(o, 'old_x'):
                o.old_x = o.pos_x
                o.old_y = o.pos_y
            o.pos_x = o.old_x + dx
            o.pos_y = o.old_y + dy

        return


class cDialogue(extra.cVector):
    """A Dialogue represents a text line,
        This takes the text, each Syllable of the text and it's karaoke times.
        This object is the most complex one, almost imposible for you to create, better use cSyllable or directly extra.cVector
        """

    def __init__(self, dialogue, styles, max_effect=0):
        """
                @dialogue the dialogue line in ASS form (inner)
                @styles array with styles
                optionals:
                @max_effect maximum number that can take as effect
                """
        t_estilo = dialogue[E_STYLE]
        est = styles[0]
        for i in styles:
            if t_estilo == i._name:
                est = i
                break

        estilo = cProperties(est)
        estilo._layer = common.SafeGetFloat(dialogue, E_LAYER) or estilo._layer
        estilo._marginv = common.SafeGetFloat(dialogue, S_MARGINV) or estilo._marginv
        estilo._marginr = common.SafeGetFloat(dialogue, S_MARGINR) or estilo._marginr
        estilo._marginl = common.SafeGetFloat(dialogue, S_MARGINL) or estilo._marginl
        extra.cVector.__init__(self, text=None, style=estilo)
        self._start = TimeToMS(dialogue[E_START])
        self._end = TimeToMS(dialogue[E_END])
        self._dur = self._end - self._start
        self.effect = min(max_effect, int(common.SafeGetFloat(dialogue, E_EFFECT)))
        self.__SetSyllables(dialogue[E_TEXT])
        return

    def __SetSyllables(self, text):
        """Creats the objects Syllables from a dialogue,
                code was taken from ZheoFX (C) brother project

                Zheo y Alchemist, thanks guys, you're awesome! :D"""
        import re
        texto = re.sub('({[\\s\\w\\d]+})*', '', text)
        pattern = '(?:\\\\[k]?[K|ko|kf])(\\d+)(?:\\\\[\\w\\d]+)*(\\\\-[\\w\\d]+)*(?:\\\\[\\w\\d]+)*}([^\\{\\}]+)*'
        info = list(re.findall(pattern, texto))
        plain_text = ('').join([ tx for ti, ifx, tx in info ])
        if not plain_text:
            plain_text = re.sub('{.*}', '', texto)
        self.SetText(plain_text)
        if self.original.angle:
            pre = self.matrix.transform_point(0, 0)
        else:
            pre = (
             self.original.pos_x, self.original.pos_y)
        self._syllables = []
        tiempo = self._start
        i = 0
        for ti, ifx, tx in info:
            syl = cSyllable(tx, self.original, parent=self, last_pos=pre)
            syl._indice = i
            syl._start = tiempo
            dur = int(ti) * 10.0
            syl._dur = dur
            syl._end = tiempo = syl._start + syl._dur
            if len(ifx) > 2:
                try:
                    ifx = int(ifx[2:])
                except:
                    ifx = None

            else:
                ifx = None
            syl.effect = ifx or self.effect
            self._syllables.append(syl)
            i += 1
            pre = (syl._next_x, syl._next_y)

        return

    def Chain(self, function, duration=None):
        """
                Allows to chain the Syllables to a animationn

                :param function: function to call for each syllable and the progress
                :param duraton:
                        duration of the animation of each syllable
                        If not specified, a duration that animates
                        one syllable per time will be used.
                :type function: `method`
                :type duration: int milliseconds

                """
        common.Chain(self._dur, self.progress, self._syllables, function, duration)

    def FullWiggle(self, amplitude=4, frequency=2):
        """el wiggle que queria AbelKM"""
        dx, dy = self.Wiggle(amplitude, frequency)
        for sil in self._syllables:
            sil.FullWiggle(amplitude, frequency, dx, dy)


class Ass:
    """This class parses the .ass file, luckily you won't need to use it"""

    def __init__(self, file, max):
        """When initialized, the file to load can be specified
                @file .ass file to load
                @max maximum number of effects"""
        if file:
            self.LoadFromFile(file, max)

    def __pHeader(self, text):
        """Function to parse a header"""
        titulo, valor = text.split(':', 1)
        self.info[titulo.strip().lower()] = valor.strip()

    def __none(self, text):
        """null parseator"""
        pass

    def __v4PStyle(self, text):
        """style parseator"""
        titulo, valor = text.split(':', 1)
        titulo = titulo.strip().lower()
        if titulo == S_FORMAT:
            self.formato = [ v.strip().lower() for v in valor.split(',') ]
        else:
            valores = [ v.strip().lower() for v in valor.split(',') ]
            self.styles.append(cProperties(dicc=dict(zip(self.formato, valores))))

    def __Events(self, text):
        """event parseator"""
        titulo, valor = text.split(':', 1)
        titulo = titulo.strip().lower()
        if titulo == E_FORMAT:
            self.eformato = [ v.strip().lower() for v in valor.split(',') ]
        elif titulo == E_DIALOG:
            valores_raw = [ v.strip() for v in valor.split(',', len(self.eformato) - 1) ]
            valores = [ v.lower() for v in valores_raw[:-1] ]
            valores.append(valores_raw[(-1)])
            nuevo_d = dict(zip(self.eformato, valores))
            nuevo_d[E_EFFECT] = int(common.SafeGetFloat(nuevo_d, E_EFFECT))
            d = cDialogue(nuevo_d, self.styles, self.max_effect)
            d._indice = self.index
            self.dialogues.append(d)
            self.index += 1

    def LoadFromFile(self, file, max):
        """Loading a ass file"""
        self.info = {}
        self.styles = []
        self.dialogues = []
        self.index = 0
        self.max_effect = max
        f = codecs.open(file, mode='r', encoding='utf-8')
        parser = self.__none
        for line in f:
            s = line.strip().lower()
            if s == '' or s[0] == ';':
                pass
            elif s == F_EVENTS:
                parser = self.__Events
            elif s == F_SINFO:
                parser = self.__pHeader
            elif s == F_STYLE4P or s == F_STYLE4:
                parser = self.__v4PStyle
            else:
                parser(line)