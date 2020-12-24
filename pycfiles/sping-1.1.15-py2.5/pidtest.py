# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\tests\pidtest.py
# Compiled at: 2008-04-09 17:25:19
"""pidtest.py

This module puts the various sping PIDxx backends through their paces.
"""
from sping import pagesizes
from sping.pid import *
import string, math
backends = [
 'PDF', 'PIL', 'TK', 'PS', 'QD', 'SVG', 'WX']
backends.sort()

def minimal(canvasClass):
    """Just a very basic test of line drawing and canvas size."""
    canvas = canvasClass(pagesizes.A6, 'test-minimal')
    drawMinimal(canvas)
    return canvas


def drawMinimal(canvas):
    saver = StateSaver(canvas)
    size = canvas.size
    canvas.defaultLineColor = green
    canvas.drawLine(1, 1, size[0] - 1, size[1] - 1)
    canvas.drawLine(1, size[1] - 1, size[0] - 1, 1)
    canvas.drawRect(1, 1, size[0] - 1, size[1] - 1, edgeWidth=5)
    return canvas


def basics(canvasClass):
    """A general test of most of the drawing primitives except images and strings."""
    canvas = canvasClass((300, 300), 'test-basics')
    return drawBasics(canvas)


def drawBasics(canvas):
    saver = StateSaver(canvas)
    canvas.defaultLineColor = Color(0.7, 0.7, 1.0)
    canvas.drawLines(map(lambda i: (i * 10, 0, i * 10, 300), range(30)))
    canvas.drawLines(map(lambda i: (0, i * 10, 300, i * 10), range(30)))
    canvas.defaultLineColor = black
    canvas.drawLine(10, 200, 20, 190, color=red)
    canvas.drawEllipse(130, 30, 200, 100, fillColor=yellow, edgeWidth=4)
    canvas.drawArc(130, 30, 200, 100, 45, 50, fillColor=blue, edgeColor=navy, edgeWidth=4)
    canvas.defaultLineWidth = 4
    canvas.drawRoundRect(30, 30, 100, 100, fillColor=blue, edgeColor=maroon)
    canvas.drawCurve(20, 20, 100, 50, 50, 100, 160, 160)
    polypoints = [
     (160, 120), (130, 190), (210, 145), (110, 145), (190, 190)]
    canvas.drawPolygon(polypoints, fillColor=lime, edgeColor=red, edgeWidth=3, closed=1)
    canvas.drawRect(200, 200, 260, 260, edgeColor=yellow, edgeWidth=5)
    canvas.drawLine(200, 260, 260, 260, color=green, width=5)
    canvas.drawLine(260, 200, 260, 260, color=red, width=5)
    return canvas


def advanced(canvasClass):
    """A test of figures and images."""
    canvas = canvasClass((300, 300), 'test-advanced')
    return drawAdvanced(canvas)


def drawAdvanced(canvas):
    saver = StateSaver(canvas)
    figure = [
     (
      figureCurve, 20, 20, 100, 50, 50, 100, 160, 160),
     (
      figureLine, 200, 200, 250, 150),
     (
      figureArc, 50, 10, 250, 150, 10, 90)]
    canvas.drawFigure(figure, fillColor=yellow, edgeWidth=4)
    try:
        from PIL import Image
    except:
        canvas.drawString('PIL not available!', 20, 200)
        Image = None

    if Image:
        img = Image.open('python.gif')
        canvas.drawImage(img, 120, 50, 152, 114)
        canvas.drawImage(img, 0, 210, 300, 242)
    return canvas


def bluefunc(x):
    return 1.0 / (1.0 + math.exp(-10 * (x - 0.6)))


def redfunc(x):
    return 1.0 / (1.0 + math.exp(10 * (x - 0.5)))


def greenfunc(x):
    return 1 - pow(redfunc(x + 0.2), 2) - bluefunc(x - 0.3)


def spectrum(canvasClass):
    canvas = canvasClass((300, 300), 'test-spectrum')
    return drawSpectrum(canvas)


def drawSpectrum(canvas):
    """Generates a spectrum plot; illustrates colors and useful application."""
    saver = StateSaver(canvas)

    def plot(f, canvas, offset=0):
        for i in range(0, 100):
            x = float(i) / 100
            canvas.drawLine(i * 3 + offset, 250, i * 3 + offset, 250 - 100 * f(x))

    def genColors(n=100):
        out = [None] * n
        for i in range(n):
            x = float(i) / n
            out[i] = Color(redfunc(x), greenfunc(x), bluefunc(x))

        return out

    colors = genColors(300)
    canvas.drawRect(0, 0, 300, 100, edgeColor=black, fillColor=black)
    for i in range(len(colors)):
        canvas.drawLine(i, 20, i, 80, colors[i])

    canvas.defaultLineColor = red
    plot(redfunc, canvas)
    canvas.defaultLineColor = blue
    plot(bluefunc, canvas, 1)
    canvas.defaultLineColor = green
    plot(greenfunc, canvas, 2)
    return canvas


def strings(canvasClass):
    canvas = canvasClass(size=(400, 400), name='test-strings')
    return drawStrings(canvas)


def drawStrings(canvas):
    """Checks font metrics, and also illustrates the standard fonts."""
    saver = StateSaver(canvas)
    CenterAndBox(canvas, 'spam, spam, spam, baked beans, and spam!')
    StandardFonts(canvas, Write)
    return canvas


def Write(canvas, s, font, curs):
    if font:
        canvas.defaultFont = font
    text = s
    while text and text[(-1)] == '\n':
        text = text[:-1]

    canvas.drawString(text, x=curs[0], y=curs[1])
    if s[(-1)] == '\n':
        curs[0] = 10
        curs[1] = curs[1] + canvas.fontHeight() + canvas.fontDescent()
    else:
        curs[0] = curs[0] + canvas.stringWidth(s)


def StandardFonts(canvas, Write):
    canvas.defaultLineColor = black
    curs = [10, 70]
    for size in (12, 18):
        for fontname in ('times', 'courier', 'helvetica', 'symbol', 'monospaced', 'serif',
                         'sansserif'):
            curs[0] = 10
            curs[1] = curs[1] + size * 1.5
            Write(canvas, '%s %d ' % (fontname, size), Font(face=fontname, size=size), curs)
            Write(canvas, 'bold ', Font(face=fontname, size=size, bold=1), curs)
            Write(canvas, 'italic ', Font(face=fontname, size=size, italic=1), curs)
            Write(canvas, 'underline', Font(face=fontname, size=size, underline=1), curs)


def CenterAndBox(canvas, s, cx=200, y=40):
    """tests string positioning, stringWidth, fontAscent, and fontDescent"""
    canvas.drawLine(cx, y - 30, cx, y + 30, color=yellow)
    w = canvas
    w = canvas.stringWidth(s)
    canvas.drawLine(cx - w / 2, y, cx + w / 2, y, color=red)
    canvas.drawString(s, cx - w / 2, y)
    canvas.defaultLineColor = Color(0.7, 0.7, 1.0)
    canvas.drawLine(cx - w / 2, y - 20, cx - w / 2, y + 20)
    canvas.drawLine(cx + w / 2, y - 20, cx + w / 2, y + 20)
    asc, desc = canvas.fontAscent(), canvas.fontDescent()
    canvas.drawLine(cx - w / 2 - 20, y - asc, cx + w / 2 + 20, y - asc)
    canvas.drawLine(cx - w / 2 - 20, y + desc, cx + w / 2 + 20, y + desc)


def rotstring(canvasClass):
    canvas = canvasClass((450, 300), name='test-rotstring')
    return drawRotstring(canvas)


def drawRotstring(canvas):
    """Draws rotated strings."""
    saver = StateSaver(canvas)
    canvas.defaultFont = Font(bold=1)
    canvas.defaultLineColor = (blue + white) / 2
    canvas.drawLine(0, 150, 300, 150)
    canvas.drawLine(150, 0, 150, 300)
    s = ' __albatros at '
    w = canvas.stringWidth(s)
    canvas.drawEllipse(150 - w, 150 - w, 150 + w, 150 + w, fillColor=transparent)
    colors = [
     red, orange, yellow, green, blue, purple]
    cnum = 0
    for ang in range(0, 359, 30):
        canvas.defaultLineColor = colors[cnum]
        s2 = s + str(ang)
        canvas.drawString(s2, 150, 150, angle=ang)
        cnum = (cnum + 1) % len(colors)
        canvas.drawString('This is  a\nrotated\nmulti-line string!!!', 350, 100, angle=-90, font=Font(underline=1))

    return canvas


def tkTest(testfunc):
    try:
        import sping.TK, Tkinter
    except:
        print 'A module needed for sping.TK is not available, select another backend'
        return

    root = Tkinter.Tk()
    frame = Tkinter.Frame(root)
    tkcanvas = sping.TK.TKCanvas(size=(400, 400), name='sping-testTK', master=frame)
    bframe = Tkinter.Frame(root)
    minimalB = Tkinter.Button(bframe, text='minimal test', command=lambda c=tkcanvas: (c.clear(), drawMinimal(c), c.flush())).pack(side=Tkinter.LEFT)
    basicB = Tkinter.Button(bframe, text='basic test', command=lambda c=tkcanvas: (c.clear(), drawBasics(c), c.flush())).pack(side=Tkinter.LEFT)
    spectB = Tkinter.Button(bframe, text='spectrum test', command=lambda c=tkcanvas: (c.clear(), drawSpectrum(c), c.flush())).pack(side=Tkinter.LEFT)
    stringsB = Tkinter.Button(bframe, text='strings test', command=lambda c=tkcanvas: (c.clear(), drawStrings(c), c.flush())).pack(side=Tkinter.LEFT)
    rotstrB = Tkinter.Button(bframe, text='rotated strings test', command=lambda c=tkcanvas: (c.clear(), drawRotstring(c), c.flush())).pack(side=Tkinter.LEFT)
    advancedB = Tkinter.Button(bframe, text='advanced test', command=lambda c=tkcanvas: (c.clear(), drawAdvanced(c), c.flush())).pack(side=Tkinter.LEFT)
    bframe.pack(side=Tkinter.TOP)
    tkcanvas.pack()
    frame.pack()
    if testfunc == minimal:
        drawMinimal(tkcanvas)
    elif testfunc == basics:
        drawBasics(tkcanvas)
    elif testfunc == advanced:
        drawAdvanced(tkcanvas)
    elif testfunc == spectrum:
        drawSpectrum(tkcanvas)
    elif testfunc == strings:
        drawStrings(tkcanvas)
    elif testfunc == rotstring:
        drawRotstring(tkcanvas)
    else:
        print 'Illegal testfunc handed to tkTest'
        raise 'Unsupported testfunc'
    tkcanvas.flush()
    root.mainloop()


def wxTest(testfunc):
    global wx_app
    try:
        import sping.WX
        from wx import App
    except:
        print 'A module needed for sping.WX is not available, select another backend'
        return

    if not globals().has_key('wx_app'):

        class CanvasApp(App):
            """The wxApp that runs canvas.  Initializes windows, and handles redrawing"""

            def OnInit(self):
                return 1

        wx_app = CanvasApp(0)
    canvas = testfunc(sping.WX.WXCanvas)
    canvas.flush()
    wx_app.MainLoop()


def runtest(backend, testfunc):
    if backend == 'TK':
        tkTest(testfunc)
        return
    if backend == 'WX':
        wxTest(testfunc)
        return
    modname = 'sping.' + backend
    print 'importing ', modname
    module = __import__('sping.' + backend, globals(), locals(), [backend])
    canvasClass = getattr(module, backend + 'Canvas')
    canvas = testfunc(canvasClass)
    canvas.flush()
    if backend == 'PIL':
        canvas.save(file=canvas.name + '.jpg')
        canvas.save(format='png')
    elif backend == 'piddleVCR':
        filename = canvas.name + '.vcr'
        canvas.save(filename)
        print filename, 'saved'
    else:
        canvas.save()


def mainLoop():
    global backends
    global tests
    backend = None
    test = None
    while True:
        i = 0
        while i < len(backends) or i < len(tests):
            try:
                bstr = str(i + 1) + '. ' + backends[i]
            except:
                bstr = ''

            try:
                tstr = chr(65 + i) + '. ' + tests[i].__name__
            except:
                tstr = ''

            if i == backend:
                bflag = '==>'
            else:
                bflag = ''
            if i == test:
                tflag = '==>'
            else:
                tflag = ''
            print '%10s %-20s %10s %-20s' % (bflag, bstr, tflag, tstr)
            i = i + 1

        print
        inp = raw_input('Selection (0 to exit): ')
        print
        if inp == '0':
            return
        if inp:
            testinp = ''
            if inp[(-1)] in string.letters:
                testinp = inp[(-1)]
            elif inp[0] in string.letters:
                testinp = inp[0]
            backinp = string.join(filter(lambda x: x in '0123456789', inp))
            if backinp:
                backend = int(backinp) - 1
                if backend < len(backends):
                    docstr = __import__('sping.' + backends[backend], globals(), locals(), backends[backend]).__doc__
                    if docstr:
                        print docstr
                    else:
                        print '<no doc string>'
                else:
                    backend = None
            if testinp:
                test = ord(string.upper(testinp[0])) - ord('A')
                if test >= 0 and test < len(tests):
                    docstr = tests[test].__doc__
                    if docstr:
                        print docstr
                else:
                    test = None
        print
        if backend != None and test != None:
            runtest(backends[backend], tests[test])

    return


tests = (
 minimal, basics, advanced, spectrum, strings, rotstring)
if __name__ == '__main__':
    mainLoop()