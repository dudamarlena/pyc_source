# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/aui/aui_utilities.py
# Compiled at: 2012-06-09 14:19:28
"""
This module contains some common functions used by :mod:`lib.agw.aui` to
manipulate colours, bitmaps, text, gradient shadings and custom dragging images
for :class:`~lib.agw.aui.auibook.AuiNotebook` tabs.
"""
__author__ = 'Andrea Gavana <andrea.gavana@gmail.com>'
__date__ = '31 March 2009'
import wx
from aui_constants import *
if wx.Platform == '__WXMAC__':
    import Carbon.Appearance

def BlendColour(fg, bg, alpha):
    """
    Blends the two colour component `fg` and `bg` into one colour component, adding
    an optional alpha channel.

    :param Colour `fg`: the first colour component;
    :param Colour `bg`: the second colour component;
    :param integer `alpha`: an optional transparency value.
    """
    result = bg + alpha * (fg - bg)
    if result < 0.0:
        result = 0.0
    if result > 255:
        result = 255
    return result


def StepColour(c, ialpha):
    """
    Darken/lighten the input colour `c`.

    :param Colour `c`: a colour to darken/lighten;
    :param integer `ialpha`: a transparency value.
    """
    if ialpha == 100:
        return c
    r, g, b = c.Red(), c.Green(), c.Blue()
    ialpha = min(ialpha, 200)
    ialpha = max(ialpha, 0)
    alpha = (ialpha - 100.0) / 100.0
    if ialpha > 100:
        bg = 255
        alpha = 1.0 - alpha
    else:
        bg = 0
        alpha = 1.0 + alpha
    r = BlendColour(r, bg, alpha)
    g = BlendColour(g, bg, alpha)
    b = BlendColour(b, bg, alpha)
    return wx.Colour(r, g, b)


def LightContrastColour(c):
    """
    Creates a new, lighter colour based on the input colour `c`.

    :param Colour `c`: the input colour to analyze.
    """
    amount = 120
    if c.Red() < 128 and c.Green() < 128 and c.Blue() < 128:
        amount = 160
    return StepColour(c, amount)


def ChopText(dc, text, max_size):
    """
    Chops the input `text` if its size does not fit in `max_size`, by cutting the
    text and adding ellipsis at the end.

    :param `dc`: a :class:`DC` device context;
    :param string `text`: the text to chop;
    :param integer `max_size`: the maximum size in which the text should fit.
    """
    (x, y, dummy) = dc.GetMultiLineTextExtent(text)
    if x <= max_size:
        return text
    textLen = len(text)
    last_good_length = 0
    for i in xrange(textLen, -1, -1):
        s = text[0:i]
        s += '...'
        (x, y) = dc.GetTextExtent(s)
        last_good_length = i
        if x < max_size:
            break

    ret = text[0:last_good_length] + '...'
    return ret


def BitmapFromBits(bits, w, h, colour):
    """
    A utility function that creates a masked bitmap from raw bits (XBM format).

    :param string `bits`: the raw bits of the bitmap;
    :param integer `w`: the bitmap width;
    :param integer `h`: the bitmap height;
    :param Colour `colour`: the colour which will replace all white pixels in the
     raw bitmap.
    """
    img = wx.BitmapFromBits(bits, w, h).ConvertToImage()
    img.Replace(0, 0, 0, 123, 123, 123)
    img.Replace(255, 255, 255, colour.Red(), colour.Green(), colour.Blue())
    img.SetMaskColour(123, 123, 123)
    return wx.BitmapFromImage(img)


def IndentPressedBitmap(rect, button_state):
    """
    Indents the input rectangle `rect` based on the value of `button_state`.

    :param Rect `rect`: the button bitmap rectangle;
    :param integer `button_state`: the button state.
    """
    if button_state == AUI_BUTTON_STATE_PRESSED:
        rect.x += 1
        rect.y += 1
    return rect


def GetBaseColour():
    """
    Returns the face shading colour on push buttons/backgrounds,
    mimicking as closely as possible the platform UI colours.
    """
    if wx.Platform == '__WXMAC__':
        if hasattr(wx, 'MacThemeColour'):
            base_colour = wx.MacThemeColour(Carbon.Appearance.kThemeBrushToolbarBackground)
        else:
            brush = wx.Brush(wx.BLACK)
            brush.MacSetTheme(Carbon.Appearance.kThemeBrushToolbarBackground)
            base_colour = brush.GetColour()
    else:
        base_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)
    if 255 - base_colour.Red() + (255 - base_colour.Green()) + (255 - base_colour.Blue()) < 60:
        base_colour = StepColour(base_colour, 92)
    return base_colour


def MakeDisabledBitmap(bitmap):
    """
    Convert the given image (in place) to a grayed-out version, appropriate for a 'disabled' appearance.

    :param Bitmap `bitmap`: the bitmap to gray-out.
    """
    anImage = bitmap.ConvertToImage()
    factor = 0.7
    if anImage.HasMask():
        maskColour = (
         anImage.GetMaskRed(), anImage.GetMaskGreen(), anImage.GetMaskBlue())
    else:
        maskColour = None
    data = map(ord, list(anImage.GetData()))
    for i in range(0, len(data), 3):
        pixel = (
         data[i], data[(i + 1)], data[(i + 2)])
        pixel = MakeGray(pixel, factor, maskColour)
        for x in range(3):
            data[i + x] = pixel[x]

    anImage.SetData(('').join(map(chr, data)))
    return anImage.ConvertToBitmap()


def MakeGray(rgbTuple, factor, maskColour):
    """
    Make a pixel grayed-out.

    If the pixel matches the `maskColour`, it won't be changed.

    :param tuple `rgbTuple`: a tuple representing a pixel colour;
    :param integer `factor`: a graying-out factor;
    :param Colour `maskColour`: a colour mask.
    """
    if rgbTuple != maskColour:
        (r, g, b) = rgbTuple
        return map(lambda x: int((230 - x) * factor) + x, (r, g, b))
    else:
        return rgbTuple


def Clip(a, b, c):
    """
    Clips the value in `a` based on the extremes `b` and `c`.

    :param `a`: the value to analyze;
    :param `b`: a minimum value;
    :param `c`: a maximum value.
    """
    return (a < b and [b] or [(a > c and [c] or [a])[0]])[0]


def LightColour(colour, percent):
    """
    Brighten input `colour` by `percent`.

    :param Colour `colour`: the colour to be brightened;
    :param integer `percent`: brightening percentage.
    """
    end_colour = wx.WHITE
    rd = end_colour.Red() - colour.Red()
    gd = end_colour.Green() - colour.Green()
    bd = end_colour.Blue() - colour.Blue()
    high = 100
    i = percent
    r = colour.Red() + i * rd * 100 / high / 100
    g = colour.Green() + i * gd * 100 / high / 100
    b = colour.Blue() + i * bd * 100 / high / 100
    return wx.Colour(r, g, b)


def PaneCreateStippleBitmap():
    """
    Creates a stipple bitmap to be used in a :class:`Brush`.
    
    This is used to draw sash resize hints.
    """
    data = [
     0, 0, 0, 192, 192, 192, 192, 192, 192, 0, 0, 0]
    img = wx.EmptyImage(2, 2)
    counter = 0
    for ii in xrange(2):
        for jj in xrange(2):
            img.SetRGB(ii, jj, data[counter], data[(counter + 1)], data[(counter + 2)])
            counter = counter + 3

    return img.ConvertToBitmap()


def DrawMACCloseButton(colour, backColour=None):
    """
    Draws the wxMAC tab close button using :class:`GraphicsContext`.

    :param Colour `colour`: the colour to use to draw the circle;
    :param Colour `backColour`: the optional background colour for the circle.
    """
    bmp = wx.EmptyBitmapRGBA(16, 16)
    dc = wx.MemoryDC()
    dc.SelectObject(bmp)
    gc = wx.GraphicsContext.Create(dc)
    gc.SetBrush(wx.Brush(colour))
    path = gc.CreatePath()
    path.AddCircle(6.5, 7, 6.5)
    path.CloseSubpath()
    gc.FillPath(path)
    path = gc.CreatePath()
    if backColour is not None:
        pen = wx.Pen(backColour, 2)
    else:
        pen = wx.Pen('white', 2)
    pen.SetCap(wx.CAP_BUTT)
    pen.SetJoin(wx.JOIN_BEVEL)
    gc.SetPen(pen)
    path.MoveToPoint(3.5, 4)
    path.AddLineToPoint(9.5, 10)
    path.MoveToPoint(3.5, 10)
    path.AddLineToPoint(9.5, 4)
    path.CloseSubpath()
    gc.DrawPath(path)
    dc.SelectObject(wx.NullBitmap)
    return bmp


def DarkenBitmap(bmp, caption_colour, new_colour):
    """
    Darkens the input bitmap on wxMAC using the input colour.
    
    :param Bitmap `bmp`: the bitmap to be manipulated;
    :param Colour `caption_colour`: the colour of the pane caption;
    :param Colour `new_colour`: the colour used to darken the bitmap.
    """
    image = bmp.ConvertToImage()
    red = caption_colour.Red() / float(new_colour.Red())
    green = caption_colour.Green() / float(new_colour.Green())
    blue = caption_colour.Blue() / float(new_colour.Blue())
    image = image.AdjustChannels(red, green, blue)
    return image.ConvertToBitmap()


def DrawGradientRectangle(dc, rect, start_colour, end_colour, direction, offset=0, length=0):
    """
    Draws a gradient-shaded rectangle.

    :param `dc`: a :class:`DC` device context;
    :param Rect `rect`: the rectangle in which to draw the gradient;
    :param Colour `start_colour`: the first colour of the gradient;
    :param Colour `end_colour`: the second colour of the gradient;
    :param integer `direction`: the gradient direction (horizontal or vertical).
    """
    if direction == AUI_GRADIENT_VERTICAL:
        dc.GradientFillLinear(rect, start_colour, end_colour, wx.SOUTH)
    else:
        dc.GradientFillLinear(rect, start_colour, end_colour, wx.EAST)


def FindFocusDescendant(ancestor):
    """
    Find a window with the focus, that is also a descendant of the given window.
    This is used to determine the window to initially send commands to.

    :param Window `ancestor`: the window to check for ancestry.    
    """
    focusWin = wx.Window.FindFocus()
    win = focusWin
    while win:
        if win == ancestor:
            break
        else:
            win = win.GetParent()

    if win is None:
        focusWin = None
    return focusWin


def GetLabelSize(dc, label, vertical):
    """
    Returns the :class:`~lib.agw.aui.auibar.AuiToolBar` item label size.

    :param string `label`: the toolbar tool label;
    :param bool `vertical`: whether the toolbar tool orientation is vertical or not.
    """
    text_width = text_height = 0
    (dummy, text_height) = dc.GetTextExtent('ABCDHgj')
    if label.strip():
        (text_width, dummy) = dc.GetTextExtent(label)
    if vertical:
        tmp = text_height
        text_height = text_width
        text_width = tmp
    return wx.Size(text_width, text_height)


class TabDragImage(wx.DragImage):
    """
    This class handles the creation of a custom image in case of drag and drop of a notebook tab.
    """

    def __init__(self, notebook, page, button_state, tabArt):
        """
        Default class constructor.
        
        For internal use: do not call it in your code!

        :param `notebook`: an instance of :class:`~lib.agw.aui.auibook.AuiNotebook`;
        :param `page`: the dragged :class:`~lib.agw.aui.auibook.AuiNotebookPage` page;
        :param integer `button_state`: the state of the close button on the tab;
        :param `tabArt`: an instance of :class:`~lib.agw.aui.tabart.AuiDefaultTabArt` or one of its derivations.
        """
        self._backgroundColour = wx.NamedColour('pink')
        self._bitmap = self.CreateBitmap(notebook, page, button_state, tabArt)
        wx.DragImage.__init__(self, self._bitmap)

    def CreateBitmap(self, notebook, page, button_state, tabArt):
        """
        Actually creates the drag and drop bitmap.

        :param `notebook`: an instance of :class:`~lib.agw.aui.auibook.AuiNotebook`;
        :param `page`: the dragged :class:`~lib.agw.aui.auibook.AuiNotebookPage` page;
        :param integer `button_state`: the state of the close button on the tab;
        :param `tabArt`: an instance of :class:`~lib.agw.aui.tabart.AuiDefaultTabArt` or one of its derivations.
        """
        control = page.control
        memory = wx.MemoryDC(wx.EmptyBitmap(1, 1))
        (tab_size, x_extent) = tabArt.GetTabSize(memory, notebook, page.caption, page.bitmap, page.active, button_state, control)
        (tab_width, tab_height) = tab_size
        rect = wx.Rect(0, 0, tab_width, tab_height)
        bitmap = wx.EmptyBitmap(tab_width + 1, tab_height + 1)
        memory.SelectObject(bitmap)
        if wx.Platform == '__WXMAC__':
            memory.SetBackground(wx.TRANSPARENT_BRUSH)
        else:
            memory.SetBackground(wx.Brush(self._backgroundColour))
        memory.SetBackgroundMode(wx.TRANSPARENT)
        memory.Clear()
        paint_control = wx.Platform != '__WXMAC__'
        tabArt.DrawTab(memory, notebook, page, rect, button_state, paint_control=paint_control)
        memory.SetBrush(wx.TRANSPARENT_BRUSH)
        memory.SetPen(wx.BLACK_PEN)
        memory.DrawRoundedRectangle(0, 0, tab_width + 1, tab_height + 1, 2)
        memory.SelectObject(wx.NullBitmap)
        if wx.Platform != '__WXMAC__':
            timg = bitmap.ConvertToImage()
            if not timg.HasAlpha():
                timg.InitAlpha()
            for y in xrange(timg.GetHeight()):
                for x in xrange(timg.GetWidth()):
                    pix = wx.Colour(timg.GetRed(x, y), timg.GetGreen(x, y), timg.GetBlue(x, y))
                    if pix == self._backgroundColour:
                        timg.SetAlpha(x, y, 0)

            bitmap = timg.ConvertToBitmap()
        return bitmap


def GetDockingImage(direction, useAero, center):
    """
    Returns the correct name of the docking bitmap depending on the input parameters.

    :param bool `useAero`: whether :class:`~lib.agw.aui.framemanager.AuiManager` is using
     Aero-style or Whidbey-style docking images or not;
    :param bool `center`: whether we are looking for the center diamond-shaped bitmap or not. 
    """
    suffix = (center and [''] or ['_single'])[0]
    prefix = ''
    if useAero == 2:
        prefix = 'whidbey_'
    elif useAero == 1:
        prefix = 'aero_'
    if direction == wx.TOP:
        bmp_unfocus = eval('%sup%s' % (prefix, suffix)).GetBitmap()
        bmp_focus = eval('%sup_focus%s' % (prefix, suffix)).GetBitmap()
    elif direction == wx.BOTTOM:
        bmp_unfocus = eval('%sdown%s' % (prefix, suffix)).GetBitmap()
        bmp_focus = eval('%sdown_focus%s' % (prefix, suffix)).GetBitmap()
    elif direction == wx.LEFT:
        bmp_unfocus = eval('%sleft%s' % (prefix, suffix)).GetBitmap()
        bmp_focus = eval('%sleft_focus%s' % (prefix, suffix)).GetBitmap()
    elif direction == wx.RIGHT:
        bmp_unfocus = eval('%sright%s' % (prefix, suffix)).GetBitmap()
        bmp_focus = eval('%sright_focus%s' % (prefix, suffix)).GetBitmap()
    else:
        bmp_unfocus = eval('%stab%s' % (prefix, suffix)).GetBitmap()
        bmp_focus = eval('%stab_focus%s' % (prefix, suffix)).GetBitmap()
    return (bmp_unfocus, bmp_focus)


def TakeScreenShot(rect):
    """
    Takes a screenshot of the screen at given position and size (`rect`).

    :param Rect `rect`: the screen rectangle for which we want to take a screenshot.
    """
    dcScreen = wx.ScreenDC()
    bmp = wx.EmptyBitmap(rect.width, rect.height)
    memDC = wx.MemoryDC()
    memDC.SelectObject(bmp)
    memDC.Blit(0, 0, rect.width, rect.height, dcScreen, rect.x, rect.y)
    memDC.SelectObject(wx.NullBitmap)
    return bmp


def RescaleScreenShot(bmp, thumbnail_size=200):
    """
    Rescales a bitmap to be `thumbnail_size` pixels wide (or tall) at maximum.

    :param Bitmap `bmp`: the bitmap to rescale;
    :param integer `thumbnail_size`: the maximum size of every page thumbnail.
    """
    bmpW, bmpH = bmp.GetWidth(), bmp.GetHeight()
    img = bmp.ConvertToImage()
    newW, newH = bmpW, bmpH
    if bmpW > bmpH:
        if bmpW > thumbnail_size:
            ratio = bmpW / float(thumbnail_size)
            newW, newH = int(bmpW / ratio), int(bmpH / ratio)
            img.Rescale(newW, newH, wx.IMAGE_QUALITY_HIGH)
    elif bmpH > thumbnail_size:
        ratio = bmpH / float(thumbnail_size)
        newW, newH = int(bmpW / ratio), int(bmpH / ratio)
        img.Rescale(newW, newH, wx.IMAGE_QUALITY_HIGH)
    newBmp = img.ConvertToBitmap()
    otherBmp = wx.EmptyBitmap(newW + 5, newH + 5)
    memDC = wx.MemoryDC()
    memDC.SelectObject(otherBmp)
    memDC.SetBackground(wx.WHITE_BRUSH)
    memDC.Clear()
    memDC.SetPen(wx.TRANSPARENT_PEN)
    pos = 0
    for i in xrange(5, 0, -1):
        brush = wx.Brush(wx.Colour(50 * i, 50 * i, 50 * i))
        memDC.SetBrush(brush)
        memDC.DrawRoundedRectangle(0, 0, newW + 5 - pos, newH + 5 - pos, 2)
        pos += 1

    memDC.DrawBitmap(newBmp, 0, 0, True)
    memDC.SelectObject(wx.NullBitmap)
    return otherBmp


def GetSlidingPoints(rect, size, direction):
    """
    Returns the point at which the sliding in and out of a minimized pane begins.

    :param Rect `rect`: the :class:`~lib.agw.aui.auibar.AuiToolBar` tool screen rectangle;
    :param Size `size`: the pane window size;
    :param integer `direction`: the pane docking direction.
    """
    if direction == AUI_DOCK_LEFT:
        startX, startY = rect.x + rect.width + 2, rect.y
    elif direction == AUI_DOCK_TOP:
        startX, startY = rect.x, rect.y + rect.height + 2
    elif direction == AUI_DOCK_RIGHT:
        startX, startY = rect.x - size.x - 2, rect.y
    elif direction == AUI_DOCK_BOTTOM:
        startX, startY = rect.x, rect.y - size.y - 2
    else:
        raise Exception('How did we get here?')
    caption_height = wx.SystemSettings.GetMetric(wx.SYS_CAPTION_Y)
    frame_border_x = wx.SystemSettings.GetMetric(wx.SYS_FRAMESIZE_X)
    frame_border_y = wx.SystemSettings.GetMetric(wx.SYS_FRAMESIZE_Y)
    stopX = size.x + caption_height + frame_border_x
    stopY = size.x + frame_border_y
    return (
     startX, startY, stopX, stopY)


def CopyAttributes(newArt, oldArt):
    """
    Copies pens, brushes, colours and fonts from the old tab art to the new one.

    :param `newArt`: the new instance of :class:`~lib.agw.aui.tabart.AuiDefaultTabArt`;
    :param `oldArt`: the old instance of :class:`~lib.agw.aui.tabart.AuiDefaultTabArt`.
    """
    attrs = dir(oldArt)
    for attr in attrs:
        if attr.startswith('_') and (attr.endswith('_colour') or attr.endswith('_font') or attr.endswith('_font') or attr.endswith('_brush') or attr.endswith('Pen') or attr.endswith('_pen')):
            setattr(newArt, attr, getattr(oldArt, attr))

    return newArt