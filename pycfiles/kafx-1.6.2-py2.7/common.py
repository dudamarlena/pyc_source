# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\libs\common.py
# Compiled at: 2012-05-17 12:53:16
"""
Module with different kind of functions
theoretically it doesn't depend on things like cairo or ass
"""
import math, random, itertools
from libs import video

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))


def grouper(n, iterable, fillvalue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
    args = [
     iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


def ClampB(x):
    """Cuts a number (integer) to range 0 to 255"""
    if x > 255:
        x = 255
    if x < 0:
        x = 0
    return x


def Clamp(num):
    """Cuts a float number to range 0.0 to 1.0"""
    if num < 0.0:
        return 0.0
    if num > 1.0:
        return 1.0
    return num


def ChooseByFrame(start_frame, end_frame, active, inactive=None):
    """start_frame has the starting frame
        end_frame the ending frame
        active is what is returned if the actual frame is in range
        inactive is what is returned if the actual frame is not between start_frame and end_frame
        example:
        d.actual.pos_x = ChooseByFrame(100, 200, 0, 20)
        this makes the position_x from dialogue to ONLY be 20 between frames 100 and 200, then it goes back to 0
        other objects can be used like:
        d.actual.color1.CopyFrom(ChooseByFrame(100, 400, d.actual.color2, d.actual.color3)
        """
    if start_frame <= video.cf.framen <= end_frame:
        return active
    else:
        return inactive


def Choose(progress, vector):
    progress = Clamp(progress)
    l = len(vector)
    i = int(l * progress)
    if i == l:
        i = l - 1
    return vector[i]


def i_lineal(p):
    return float(p)


def i_lincycle(p):
    p2 = p % 2
    if p2 > 1:
        p2 = 2 - p2
    return p2


def i_sin(p):
    return math.sin(math.pi * p)


def i_cos(p):
    return math.cos(math.pi * p)


def i_full_sin(p):
    return math.sin(2 * math.pi * p)


def i_full_cos(p):
    return math.cos(2 * math.pi * p)


def i_accel(p):
    return math.sin(math.pi * p * 0.5) ** 2


def i_deccel(p):
    return 1 - i_accel(1 - p)


def i_rand(p):
    return random.random()


def i_log(p):
    return math.log(p * 2 + 1)


def i_b_default(p):
    return PointBezier(p, 0, 0, 0.25, 0.1, 0.25, 1, 1, 1)[1]


def i_b_ease_in(p):
    return PointBezier(p, 0, 0, 0.42, 0.0, 1, 1, 1, 1)[1]


def i_b_ease_out(p):
    return PointBezier(p, 0, 0, 0, 0, 0.58, 1, 1, 1)[1]


def i_b_ease_in_out(p):
    return PointBezier(p, 0, 0, 0.42, 0.0, 0.58, 1, 1, 1)[1]


def i_b_cubic(p):
    return PointBezier(p, 0, 0, 0, 1.0, 1.0, 0, 1, 1)[1]


def i_b_backstart(p):
    return PointBezier(p, 0, 0, 0.2, -0.3, 0.6, 0.26, 1, 1)[1]


def i_b_boing(p):
    return PointBezier(p, 0, 0, 0.42, 0.0, 0.58, 1.5, 1, 1)[1]


def Interpolate(progress, from_val, to_val, function=i_lineal):
    """
        returns a floating number between 2 values, the returned number corresponds to the amount given in the first value
        @progress indicates how close to the start or end should the returned value be, must be a number between 0 and 1 (other values are valid, though)
        @from_val starting value or beginning of range
        @to_val last value, or end of range
        @function personal function that returns a value between 0 and 1 (always float) of a given value of progress between 0 and 1
        (puede usar las funciones que comienzan por i_)
        """
    return function(progress) * (to_val - from_val) + from_val


def LERP(progress, from_val, to_val):
    u"""
        devuelve un número flotante entre 2 valores, el número devuelto corresponde a una cantidad indicada por el primer valor
        @progress indicador de que tan cerca del inico o fin debe estar el valor devuelto, debe ser un número entre 0 y 1 (aunque otros valores funcionan)
        @from_val valor inicial, o comienzo del rango
        @to_val valor final, o final del rango
        Esta funcion es lo mismo que interpolar lineal, pero un poco mas rapida,
        solo para funciones que requieran unicamente interpolacion lineal
        """
    return from_val + float(progress) * (to_val - from_val)


def RanmaBezier(progress, points):
    """
        Devuelve un punto (x, y) sobre una curva bezier dado el avance en la misma
        Admite curvas biezer de cualquier orden
        @progress como en interpolar, normalmente un numero entre 0 y 1 indicando el avance de sobre la curva
        @points : array de points -> [ [0, 0], [1, 1], [2, 2] ]
        es como PointBezier pero permite curvas de cualquier cantidad de points de control (de 1 a (teoricamente) infinito))
        es algo mas lento que PointBezier para curvas de la misma cantidad de points
        escrito por Ranma42 @ irc.freenode.net/#cairo
        """
    while len(points) > 1:
        points2 = []
        for i in range(len(points) - 1):
            px0, py0 = points[i]
            px1, py1 = points[(i + 1)]
            p = (LERP(progress, px0, px1), LERP(progress, py0, py1))
            points2.append(p)

        points = points2

    return points[0]


def PointBezier(progress, x_start, y_start, x1, y1, x2, y2, x_end, y_end):
    u"""
        Devuelve un punto (x, y) sobre una curva bezier dado el avance en la misma
        @x_start, y_start : punto inicial de la curva
        @x1, y1 : 1º punto de control de la curva
        @x2, y2 : 2º punto de control de la curva
        @x_end, y_end : punto final de la curva
        @progress : avance sobre la curva (0 a 1)
        Esta funcion es igual que Bezier pero es algo más rápida, además,
        Está limitada a:
        1 Punto de inicio
        2 points de control
        1 Punto final
        y todos los points son pasados por parámetro secuencialmente.
        #with help of ranma42!
        """
    curvx1 = LERP(progress, x_start, x1)
    curvx2 = LERP(progress, x1, x2)
    curvx3 = LERP(progress, x2, x_end)
    curvx4 = LERP(progress, curvx1, curvx2)
    curvx5 = LERP(progress, curvx2, curvx3)
    curvx6 = LERP(progress, curvx4, curvx5)
    curvy1 = LERP(progress, y_start, y1)
    curvy2 = LERP(progress, y1, y2)
    curvy3 = LERP(progress, y2, y_end)
    curvy4 = LERP(progress, curvy1, curvy2)
    curvy5 = LERP(progress, curvy2, curvy3)
    curvy6 = LERP(progress, curvy4, curvy5)
    return (curvx6, curvy6)


def Chain(duration, progress, objects, function, time=None):
    u"""Realiza una animación en cadena.
        dado una duración maestra y un progress maestro aplicados a
        un array de objetos y un tiempo de animacion por objeto
        se calcula el progress para cada objeto y se llama a la funcion pasada por parametro para cada uno.

        La idea es poder animar sílabas según el diálogo, o letras según la sílaba,
        pero aun así lo pongo acá para que pueda ser usado de otras formas

        @duración Duración del tiempo maestro
        @progress float de rango 0 a 1 que dice el progress maestro
        @objects array de objetos a ser animados en cadena.
                serán pasados a la función func. (sólo debe implementar len y ser iterables (string y array funcionan))

        @función debe ser una funcion
        será llamada progresivamente vez por cada objeto en orden de aparición con los siguientes parámetros:
                objeto, progress

        @time define el tiempo que dura la animación de cada objeto
                si el time es mayor a la duración/len(objects)
                entonces las aniamciones se superpondran.
                si el time es None (o no se especifica) las animaciones se dan
                una atrás de la otra, o sea el time es = duración/len(objects)
                si es menor no sé.
        """
    duration = float(duration)
    slen = len(objects)
    if slen == 0:
        return
    tsil = duration / slen
    if not time:
        time = tsil
    finacum = tsil
    tactualdiag = progress * duration
    for obj in objects:
        tini = finacum - time
        tactualsilaba = tactualdiag - tini
        if tactualsilaba <= 0:
            prog = 0.0
        elif tactualsilaba >= time:
            prog = 1.0
        else:
            prog = tactualsilaba / time
        function(obj, prog)
        finacum += tsil


def SafeGetFloat(dicc, prop, default=0.0):
    u"""
        Devuelve una propiedad un diccionario convertido a float, o un valor default
        @dict diccionario
        @prop propiedad del diccionario a devolver
        @default opcional, valor por default 0.0, es el valor que se devolverá en caso de haber algun error al convertir la propiedad del diccionario
        """
    try:
        return float(dicc[prop])
    except:
        return default


class FxsGroup:
    """Clase de la que desciende un grupo de efectos"""
    in_ms = 0
    out_ms = 0
    syl_in_ms = 0
    syl_out_ms = 0
    letter_in_ms = 0
    letter_out_ms = 0
    skip_frames = True
    reset_style = True
    split_letters = False
    fxs = []
    blur_type = 0

    def OnFrameStarts(self):
        pass

    def OnFrameEnds(self):
        pass


class Fx:
    """Clase de la que desciende un effect"""
    events = []

    def OnDialogue(self, diag):
        pass

    def OnSyllable(self, sil):
        pass

    def OnLetter(self, let):
        pass

    def OnSyllableDead(self, sil):
        pass

    def OnSyllableSleep(self, sil):
        pass

    def OnLetterDead(self, let):
        pass

    def OnLetterSleep(self, let):
        pass

    def OnDialogueIn(self, diag):
        pass

    def OnSyllableIn(self, sil):
        pass

    def OnLetterIn(self, let):
        pass

    def OnDialogueOut(self, diag):
        pass

    def OnSyllableOut(self, sil):
        pass

    def OnLetterOut(self, let):
        pass

    def OnDialogueStarts(self, diag):
        pass

    def OnSyllableStarts(self, sil):
        pass

    def OnLetterStarts(self, let):
        pass


class Event:

    def OnSyllable(self, sil):
        pass

    def OnDialogue(self, diag):
        pass

    def OnLetter(self, let):
        pass

    def SyllableTime(self, sil):
        return (0, 0)

    def DialogueTime(self, diag):
        return (0, 0)

    def LetterTime(self, let):
        return (0, 0)


def MyImport(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod