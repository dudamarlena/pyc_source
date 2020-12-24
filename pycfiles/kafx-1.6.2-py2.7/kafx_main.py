# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\kafx_main.py
# Compiled at: 2012-03-28 16:24:42
"""
Kick Ass FX
copyright Barraco Mármol Jerónimo, David Pineda Melendez, Martín Dunn y Colaboradores 2007
GNU/GPL
"""
import traceback, cProfile
traceback.sys.stdout = open('kafx_log.txt', 'w', 0)
traceback.sys.stderr = open('error_log.txt', 'w', 0)
version_info = (1, 8, 0, 'newfinalrc4')
print 'Python version', traceback.sys.version_info
if traceback.sys.version_info[:3] < (2, 7, 0):
    print "\n\tThe python version used isn't 2.7, this can bring problems with cairo.\n\tPlease try to use version  2.7 of python (do not use 3.2).\n\t"
print 'Loading Cairo...'
import cairo
print 'Cairo loaded. Version:', cairo.version_info
print 'Loading KAFX...'
from libs import video, common, asslib
print 'KAFX loaded. Libreries version:', version_info
print 'Yay! The libraries were successfully loaded.'
cf = None
vi = None
fx = None
frames = []
no_frames = []
fop = None
m = None
ass = None

def DBug(msg):
    traceback.sys.stdout.write(str(msg))


def PainOnScreen(msg):
    """Prints text on screen, super slow, multiline supported"""
    lasty = 10
    for line in msg.split('\n'):
        error_obj = asslib.cSyllable(line, last_pos=(20, lasty))
        error_obj.Paint()
        lasty += error_obj.original._line_height


def Error(msg=''):
    """Prints the error message in archive and on screen,
        not always on screen, depends on the error"""
    traceback.sys.stderr.write(msg + '\n')
    traceback.print_exc()
    traceback.sys.stderr.write('\n---------------\n')
    PainOnScreen(traceback.format_exc())


def OnDestroy():
    """This function is called from the dll
        it's called before destroying everything, it's completely unnecessary to use this in python... but just in case...
        It's better to use special methods from __del__ class
        """
    print "I'm leaving, I've been told to finish."


def OnInit(filename, assfile, pixel_type, image_type, width, height, fpsn, fpsd, numframes):
    """This function is called from dll
        initialize everything
        """
    global ass
    global cf
    global fop
    global fx
    global m
    global vi
    try:
        DBug("I'm being initialized...\n")
        fop = cairo.FontOptions()
        fop.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        cf = video.cf
        vi = video.vi
        vi.pixel_type = pixel_type
        vi.modo = video.GetMode(vi.pixel_type)
        vi.image_type = image_type
        vi.width = width
        vi.height = height
        vi.fps_numerator = fpsn
        vi.fps_denominator = fpsd
        vi.num_frames = numframes
        vi.fps = float(fpsn) / fpsd
        vi.fpscof1 = vi.fps / 1000.0
        vi.fpscof2 = 1000.0 / vi.fps
        vi.fake_stride = width * 4
        cf.ctx = cairo.Context(cairo.ImageSurface(vi.modo, vi.width, vi.height))
        DBug('Importing Effect.\n')
        m = common.MyImport(filename)
        DBug('Loading Subtitles.\n')
        fx = m.FxsGroup()
        ass = asslib.Ass(assfile, len(fx.fxs) - 1)
        DBug('Making calculations for events.\n')
        __PreLoad()
        DBug('All was apparently successfully loaded.\n')
    except:
        print "Something bad happened and we don't know what it is. It is really bad. Seriously, it is really bad. Really."
        Error()


def OnFrame(pframe, stride, cuadro):
    """This function is called from dll
        It's called for each frame
        """
    global __CallFuncs
    global no_frames
    try:
        if fx.skip_frames:
            if pframe > len(no_frames):
                return
            if no_frames[pframe]:
                return
        cf.framen = pframe
        cf.sfc = cairo.ImageSurface.create_for_data(cuadro, vi.modo, vi.width, vi.height, stride)
        cf.ctx = cairo.Context(cf.sfc)
        cf.ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        cf.ctx.set_font_options(fop)
        cf.ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        cf.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        __CallFuncs()
        cf.sfc.flush()
    except:
        print 'e'
        Error()


def __CallFuncsProfile():
    cProfile.runctx('__CallFuncsNormal()', globals(), locals(), filename='profile')


def __CallFuncsNormal():
    """This function calls all the events of the effect
        If an event is added, don't forget to add it in __PreLoad"""
    global frames
    frame = frames[cf.framen]
    fx.OnFrameStarts()
    for evento, o, prog in frame:
        o.progress = prog
        if fx.reset_style:
            o.Restore()
        evento(o)

    fx.OnFrameEnds()


__CallFuncs = __CallFuncsNormal

def SetProfiling(do=False):
    global __CallFuncs
    global __CallFuncsNormal
    global __CallFuncsProfile
    if do:
        print 'Profiling active'
        __CallFuncs = __CallFuncsProfile
    else:
        print 'Profiling inactive'
        __CallFuncs = __CallFuncsNormal


def __AddEvent(ini, end, dif, evento, element):
    ms2f = video.vi.MSToFrame
    cfn = video.vi.ClampFrameNum
    inif = cfn(ms2f(ini))
    endf = cfn(ms2f(end))
    diff = float(ms2f(dif) - 1) or 1.0
    for i, f in enumerate(xrange(inif, endf)):
        p = i / diff
        frames[f].append((evento, element, p))
        no_frames[f] = False


def __PreLoad():
    """This function creates arrays of no_frames and frames,
        and initializes things of the effect, too
        """
    global frames
    global no_frames
    from libs.draw import advanced
    num_frames = vi.num_frames
    fs = fx.fxs
    advanced.fBlur = advanced.fBlurs[fx.blur_type]
    no_frames = [
     True] * (num_frames + 1)
    frames = [ [] for i in range(num_frames + 1) ]
    dialogos = ass.dialogues
    for diag in dialogos:
        diag.progress = 0.0
        efecto = fs[diag.effect]
        inicio = getattr(efecto, 'OnDialogueStarts', None)
        if inicio:
            inicio(diag)
        evento = getattr(efecto, 'OnDialogueOut', None)
        if not evento:
            continue
        ini = diag._end
        end = diag._end + fx.out_ms
        dif = end - ini
        __AddEvent(ini, end, dif, evento, diag)

    for diag in dialogos:
        evento = getattr(fs[diag.effect], 'OnDialogueIn', None)
        if not evento:
            continue
        ini = diag._start - fx.in_ms
        end = diag._start
        dif = end - ini
        __AddEvent(ini, end, dif, evento, diag)

    for diag in dialogos:
        evento = getattr(fs[diag.effect], 'OnDialogue', None)
        if not evento:
            continue
        ini = diag._start
        end = diag._end
        dif = end - ini
        __AddEvent(ini, end, dif, evento, diag)

    for diag in dialogos:
        eventos = getattr(fs[diag.effect], 'events', None)
        if not eventos:
            continue
        for evento in eventos:
            enDialogo = getattr(evento, 'OnDialogue', None)
            if not enDialogo:
                continue
            ini, end = evento.DialogueTime(diag)
            dif = end - ini
            __AddEvent(ini, end, dif, enDialogo, diag)

    for diag in dialogos:
        __PreLoadSyllables(diag)

    if fx.split_letters:
        for diag in dialogos:
            syllables = diag._syllables
            for sil in syllables:
                __PreLoadLetters(sil)

    def keyfunc(item):
        """A function that for each item in each frame, returns the value which to compare with
                explanation:
                each frame contains several items, in the ordering process, this function is called for each item
                each item has 3 elements (event, dialogue and progress)
                we take the element 1 (the 2nd) the dialogue.
                from the dialogue we take the original style, and from there the layer
                """
        return item[1].original._layer

    for i in range(len(frames)):
        f = frames[i]
        f.sort(key=keyfunc)
        frames[i] = tuple(f)

    frames = tuple(frames)
    no_frames = tuple(no_frames)
    return


def __PreLoadSyllables(diag):
    """
                Loads syllables
        """
    fs = fx.fxs
    syllables = diag._syllables
    for sil in syllables:
        sil.progress = 0.0
        inicio = getattr(fs[sil.effect], 'OnSyllableStarts', None)
        if inicio:
            inicio(sil)

    for sil in syllables:
        evento = getattr(fs[sil.effect], 'OnSyllableDead', None)
        if not evento:
            continue
        ini = sil._end
        end = diag._end
        dif = end - ini
        __AddEvent(ini, end, dif, evento, sil)

    for sil in syllables:
        evento = getattr(fs[sil.effect], 'OnSyllableSleep', None)
        if not evento:
            continue
        ini = diag._start
        end = sil._start
        dif = end - ini
        __AddEvent(ini, end, dif, evento, sil)

    for sil in syllables:
        evento = getattr(fs[sil.effect], 'OnSyllableOut', None)
        if not evento:
            continue
        ini = sil._end
        end = sil._end + fx.syl_out_ms
        dif = end - ini
        __AddEvent(ini, end, dif, evento, sil)

    for sil in syllables:
        evento = getattr(fs[sil.effect], 'OnSyllableIn', None)
        if not evento:
            continue
        ini = sil._start - fx.syl_in_ms
        end = sil._start
        dif = end - ini
        __AddEvent(ini, end, dif, evento, sil)

    for sil in syllables:
        evento = getattr(fs[sil.effect], 'OnSyllable', None)
        if not evento:
            continue
        ini = sil._start
        end = sil._end
        dif = end - ini
        __AddEvent(ini, end, dif, evento, sil)

    for sil in syllables:
        eventos = getattr(fs[sil.effect], 'events', None)
        if not eventos:
            continue
        for evento in eventos:
            enSilaba = getattr(evento, 'OnSyllable', None)
            if not enSilaba:
                continue
            ini, end = evento.SyllableTime(sil)
            dif = end - ini
            __AddEvent(ini, end, dif, enSilaba, sil)

    return


def __PreLoadLetters(sil):
    fs = fx.fxs
    sil.SplitLetters()
    letras = sil._letters
    for letra in letras:
        letra.progress = 0.0
        efecto = fs[letra.effect]
        inicio = getattr(efecto, 'OnLetterStarts', None)
        if inicio:
            inicio(letra)
        evento = getattr(fs[sil.effect], 'OnLetterDead', None)
        if not evento:
            continue
        ini = letra._end
        end = sil._end
        dif = end - ini
        __AddEvent(ini, end, dif, evento, letra)

    for letra in letras:
        evento = getattr(fs[sil.effect], 'OnLetterSleep', None)
        if not evento:
            continue
        ini = sil._start
        end = letra._start
        dif = end - ini
        __AddEvent(ini, end, dif, evento, letra)

    for letra in letras:
        letra.progress = 0.0
        efecto = fs[letra.effect]
        evento = getattr(efecto, 'OnLetterIn', None)
        if not evento:
            continue
        ini = letra._start - fx.letter_in_ms
        end = letra._start
        dif = end - ini
        __AddEvent(ini, end, dif, evento, letra)

    for letra in letras:
        evento = getattr(fs[letra.effect], 'OnLetterOut', None)
        if not evento:
            continue
        ini = letra._end
        end = letra._end + fx.letter_out_ms
        dif = end - ini
        __AddEvent(ini, end, dif, evento, letra)

    for letra in letras:
        evento = getattr(fs[letra.effect], 'OnLetter', None)
        if not evento:
            continue
        ini = letra._start
        end = letra._end
        dif = end - ini
        __AddEvent(ini, end, dif, evento, letra)

    for letra in letras:
        eventos = getattr(fs[letra.effect], 'events', None)
        if not eventos:
            continue
        for evento in eventos:
            enLetra = getattr(evento, 'OnLetter', None)
            if not enLetra:
                continue
            ini, end = evento.LetterTime(letra)
            dif = end - ini
            __AddEvent(ini, end, dif, enLetra, letra)

    return