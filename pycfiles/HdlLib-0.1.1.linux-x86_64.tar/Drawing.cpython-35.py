# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Drawing.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 9992 bytes
import math, logging, os, cairocffi as cairo

def draw_test():
    Width, Height = (400, 250)
    output = './GUI/images/circle.png'
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, Width, Height)
    Ctx = cairo.Context(surf)
    Ctx.new_path()
    Ctx.set_source_rgb(0.9, 0.9, 0.9)
    Ctx.rectangle(0, 0, Width, Height)
    Ctx.fill()
    Ctx.set_source_rgb(0, 0, 0)
    txt = 'Hello, Matthieu !'
    Ctx.select_font_face('Ubuntu', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    Ctx.set_font_size(18)
    x_off, y_off, tw, th = Ctx.text_extents(txt)[:4]
    Ctx.move_to(Width / 2 - x_off - tw / 2, Height / 2 - y_off - th / 2)
    Ctx.show_text(txt)
    Ctx.new_path()
    Ctx.set_source_rgb(0, 0.2, 0.8)
    Ctx.arc(Width / 2, Height / 2, tw * 0.6, 0, 2 * pi)
    Ctx.stroke()
    surf.write_to_png(output)
    return output


class CairoDrawing:

    def __init__(self, Width=600, Height=400):
        Surface = cairo.ImageSurface(format=cairo.FORMAT_RGB24, width=Width, height=Height)
        self.Ctx = cairo.Context(Surface)

    def ToPNG(self, OutputPath):
        return self.Ctx.get_target().write_to_png(OutputPath)

    def IP(self, Mod, Width=600, Height=400, Ratio=1):
        if not self.Ctx:
            logging.error('[Drawing.IP] no context to draw.')
            return False
        IPWidth, IPHeight = 400 * Ratio, 400 * Ratio
        x0, y0 = (0, 0)
        Sx, Sy = max(Width, int(IPWidth + x0)) + 5, max(Height, int(IPHeight + y0)) + 5
        WhiteBG(self.Ctx, Sx, Sy)
        W, H = DrawIP(self.Ctx, Mod, x=x0, y=y0, Width=Width, Height=Height, Ratio=Ratio, Compact=False)
        if W > Width or H > Height:
            Sx, Sy = max(Width, int(IPWidth + x0)) + 5, max(Height, int(IPHeight + y0)) + 5
            Surface = cairo.ImageSurface(format=cairo.FORMAT_RGB24, width=Sx, height=Sy)
            self.Ctx = cairo.Context(Surface)
            WhiteBG(self.Ctx, Sx, Sy)
            W, H = DrawIP(self.Ctx, Mod, x=x0, y=y0, Width=Width, Height=Height, Ratio=Ratio, Compact=False)
        return (
         W, H)

    def BackGround(self, Width=600, Height=400):
        """
                Fill everything with blue gradient
                """
        if not self.Ctx:
            logging.error('[Drawing.BackGround] no context to draw.')
            return False
        DefaultBG(self.Ctx, Width, Height)


def DrawIP(Ctx, Mod, x=20, y=20, Width=400, Height=400, Ratio=1, Compact=False, Selected=False):
    """Draw a FPGA in the specified context to x, y location."""
    PinLength = 20 * Ratio
    PinSpace = 20 * Ratio
    FontSize = 20 * Ratio
    CharWidth = 11 * Ratio
    Margin = 20 * Ratio
    Title = '{0}'.format(Mod.Name)
    TitleFont = 20 * Ratio
    LetterWidth = Ctx.text_extents('O')[:4][3]
    while True:
        Ctx.set_font_size(TitleFont)
        x_off, y_off, tw, th = Ctx.text_extents(Title)[:4]
        if tw + LetterWidth < 200 * Ratio:
            break
        else:
            TitleFont *= 0.95

    TitleHeight = th
    PinMargin = TitleHeight
    if Compact is False:
        IOMappings = list(Mod.Ports.values())
        Resets = {}
        Clocks = {}
        Inputs = [x.Name for x in [x for x in IOMappings if x.Direction.upper() == 'IN']]
        Outputs = [x.Name for x in [x for x in IOMappings if x.Direction.upper() == 'OUT']]
        PortsWidth = (max(*[len(i) for i in Inputs]) + max(*[len(i) for i in Outputs])) * CharWidth + 10
        IPWidth = max(200 * Ratio, tw + PinSpace, PortsWidth)
        MaxPorts = max(len(Inputs), len(Outputs))
        PortHeight = PinSpace * MaxPorts + 2 * PinMargin + 2 * FontSize
        IPHeight = max(200 * Ratio, PortHeight)
    else:
        IPWidth = 200 * Ratio
        IPHeight = 200 * Ratio
    x0, y0 = x + Margin + PinLength, y + Margin
    Ctx.set_line_width(1)
    Ctx.set_source_rgba(0.0, 0.3, 0.5, 0.8)
    Ctx.rectangle(x0, y0, IPWidth, IPHeight)
    Ctx.fill()
    Ctx.set_source_rgba(1, 1, 1)
    if Compact:
        TitleYPos = y0 + IPHeight / 2
    else:
        TitleYPos = y0 + TitleHeight - y_off - th / 2
    DrawText(Ctx, x0 + IPWidth / 2, TitleYPos, Text=Title, Color='White', Align='Center', Bold=True, FontSize=TitleFont, Opacity=1)
    Ctx.set_line_width(2)
    if Selected:
        Ctx.set_source_rgba(0.8, 0.2, 0.2, 0.8)
    else:
        Ctx.set_source_rgba(0.0, 0.0, 0.3, 1)
    Ctx.rectangle(x0, y0, IPWidth, IPHeight)
    Ctx.stroke()
    if not Compact:
        Ctx.select_font_face('Ubuntu', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        Ctx.set_line_width(1)
        Ctx.set_font_size(FontSize - 2)
        for i in range(0, len(Inputs)):
            Ctx.set_source_rgba(0, 0, 0, 1)
            Ctx.move_to(x0 - PinLength, y0 + PinSpace * i + PinMargin + 2 * FontSize)
            DrawArrow(Ctx, x0, y0 + PinSpace * i + PinMargin + 2 * FontSize, Start=False, End=True)
            Ctx.stroke()
            Text = Inputs[i]
            Ctx.set_source_rgba(1, 1, 1, 1)
            x_off, y_off, tw, th = Ctx.text_extents(Text)[:4]
            Ctx.move_to(x0 + 5 - x_off, y0 + 2 * FontSize + PinSpace * i + PinMargin - y_off - th / 2)
            Ctx.show_text(Text)

        for i in range(0, len(Outputs)):
            Ctx.set_source_rgba(0, 0, 0, 1)
            Ctx.move_to(x0 + IPWidth, y0 + PinSpace * i + PinMargin + 2 * FontSize)
            DrawArrow(Ctx, x0 + IPWidth + PinLength, y0 + PinSpace * i + PinMargin + 2 * FontSize, Start=False, End=True)
            Ctx.stroke()
            Text = Outputs[i]
            Ctx.set_source_rgba(1, 1, 1, 1)
            x_off, y_off, tw, th = Ctx.text_extents(Text)[:4]
            Ctx.move_to(x0 + IPWidth - tw - 5 - x_off, y0 + 2 * FontSize + PinSpace * i + PinMargin - y_off - th / 2)
            Ctx.show_text(Text)

        Ctx.stroke()
    return (IPWidth + x0, IPHeight + y0 + Margin)


def WhiteBG(Ctx, Width, Height):
    """
        fill everything with blue gradient
        """
    Ctx.new_path()
    Opacity = 1
    Ctx.set_source_rgba(1, 1, 1, Opacity)
    Ctx.rectangle(0, 0, Width, Height)
    Ctx.fill()


def DefaultBG(Ctx, Width, Height):
    """
        fill everything with blue gradient
        """
    Ctx.new_path()
    gradient = cairo.LinearGradient(0, 0, 0, Height)
    gradient.add_color_stop_rgba(0, 0, 0.5, 0.7, 1)
    gradient.add_color_stop_rgba(1, 1, 1, 1, 1)
    Ctx.set_source(gradient)
    Ctx.rectangle(0, 0, Width, Height)
    Ctx.fill()


def DrawArrow(Ctx, x, y, Start=True, End=True):
    Cur_x, Cur_y = Ctx.get_current_point()
    ALength = 10
    ADegrees = 50
    if Start:
        Angle = math.atan2(Cur_y - y, Cur_x - x) + math.pi
        x1 = Cur_x + ALength * math.cos(Angle - ADegrees)
        y1 = Cur_y + ALength * math.sin(Angle - ADegrees)
        x2 = Cur_x + ALength * math.cos(Angle + ADegrees)
        y2 = Cur_y + ALength * math.sin(Angle + ADegrees)
        Ctx.move_to(Cur_x, Cur_y)
        Ctx.line_to(x1, y1)
        Ctx.move_to(Cur_x, Cur_y)
        Ctx.line_to(x2, y2)
    Ctx.move_to(Cur_x, Cur_y)
    Ctx.line_to(x, y)
    if End:
        Angle = math.atan2(y - Cur_y, x - Cur_x) + math.pi
        x1 = x + ALength * math.cos(Angle - ADegrees)
        y1 = y + ALength * math.sin(Angle - ADegrees)
        x2 = x + ALength * math.cos(Angle + ADegrees)
        y2 = y + ALength * math.sin(Angle + ADegrees)
        Ctx.move_to(x, y)
        Ctx.line_to(x1, y1)
        Ctx.move_to(x, y)
        Ctx.line_to(x2, y2)
    return True


def DrawText(Ctx, x, y, Text=None, Color='Black', Align='Left', Bold=False, FontSize=15, Opacity=1):
    if not Text:
        return False
    if Color == 'Black':
        Ctx.set_source_rgba(0, 0, 0, Opacity)
    else:
        if Color == 'White':
            Ctx.set_source_rgba(1, 1, 1, Opacity)
        else:
            if Color == 'Red':
                Ctx.set_source_rgba(1, 0, 0, Opacity)
            else:
                if Color == 'Green':
                    Ctx.set_source_rgba(0, 1, 0, Opacity)
                else:
                    if Color == 'Blue':
                        Ctx.set_source_rgba(0, 0, 1, Opacity)
                    else:
                        if Color == 'Orange':
                            Ctx.set_source_rgba(0.9, 0.9, 0.8, Opacity)
                        else:
                            Ctx.set_source_rgba(0, 0, 0, Opacity)
                if Bold:
                    Ctx.select_font_face('Ubuntu', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                else:
                    Ctx.select_font_face('Ubuntu', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            Ctx.set_font_size(FontSize)
            x_off, y_off, tw, th = Ctx.text_extents(Text)[:4]
            if Align == 'Left':
                Ctx.move_to(x, y)
            else:
                if Align == 'Right':
                    Ctx.move_to(x - tw, y)
                else:
                    Ctx.move_to(x - tw / 2, y)
    Ctx.show_text(Text)
    return (
     tw, th)