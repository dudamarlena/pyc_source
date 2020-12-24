# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/consoletk.py
# Compiled at: 2016-05-20 18:14:39
__doc__ = " ConsoleTK is a simple, stand-alone Python class to draw colorful command-line interfaces.\nThink 'curses for dummies'.\n\nTo draw your interface, you first place your cursor with `moveto(x,y)` (or `relmoveto(x,y)` \nfor a relative motion), and you then draw a widget: label, bars, separators, etc.\n\nConsoleTK also implements *non-blocking polling of the keyboard* (including\narrow keys) that enables user interactions.\n\nNote that ConsoleTK requires a terminal emulator that supports ANSI sequences and 256 colours.\n\nInitialization\n--------------\n\nSimply create a canvas with:\n\n```python\nimport consoletk\n\nwith ConsoleTK(height=20) as console:\n    #...\n```\n\nObviously, change the height to your liking.\nThe width of the area is the current width of the terminal. Note that ConsoleTK\ndoes not perform any form of reflow if you change the geometry of your\ninterface.\n\nNote that the cursor is initially at position `(1,1)` (and not `(0,0)`) to leave a small margin.\nYou can still move to `(0,0)` with `console.moveto(0,0)`.\n\nColours\n-------\n\nMany widgets can take as parameter foreground (`fg`) and background (`bg`) colours.\n\nIn its current version, ConsoleTK uses a system of colour palettes, and as such,\ncolours must be one of:\n\n- `yellow`\n- `orange`\n- `red`  \n- `magenta`\n- `violet`\n- `blue` \n- `cyan` \n- `green`\n- `base03` (black)\n- `base02` (almost black)\n- `base01` (darker grey)\n- `base00` (dark grey)\n- `base0` (grey)\n- `base1` (light grey)\n- `base2` (very light)\n- `base3` (white)\n\nBesides, you can also often specify `bold=True` and `blink=True` to enable the\ncorresponding effects (effective rendering depends on your terminal).\n\nMotions\n-------\n\nYou can move your cursor with `moveto(x,y)` or `relmoveto(x,y)`.\nYou can also save and restore a previous position with `savepos()` and `restorepose()`.\n\nWidgets\n-------\n\n- Labels: `label(text, fg, bg, bold, blink)`\n- Lines: `vsep(height)`, `hsep(width)`\n- Boxes: `box(width,height)`\n- Tickboxes: `boolean(state,label)`\n- Horizontal progressbars: `bar(...)` and `absolutebar(...)`\n\nNote that *drawing a widget does not move the cursor*: the cursor remains where it was before you\nissued the drawing call.\n\nOthers\n------\n\n- `clear()` clears the entire interface.\n- `clear(width, height)` clears a rectangle below the cursor.\n- `get_keypress()` returns the last key pressed (or `ConsoleTK.ARROW_LEFT|RIGHT|UP|DOWN` for the\narrows).\n"
import sys, os, termios, sys

class ConsoleTK():
    solarized_scheme = {'base03': 234, 
       'base02': 235, 
       'base01': 240, 
       'base00': 241, 
       'base0': 244, 
       'base1': 245, 
       'base2': 254, 
       'base3': 230, 
       'yellow': 136, 
       'orange': 166, 
       'red': 160, 
       'magenta': 125, 
       'violet': 61, 
       'blue': 33, 
       'cyan': 37, 
       'green': 64}
    solarized_palette = [
     (
      'red', False),
     (
      'orange', False),
     (
      'yellow', False),
     (
      'green', False)]
    csi = '\x1b['
    reset = '\x1b[0m'

    def __init__(self, height=10):
        self.out = os.fdopen(sys.stdout.fileno(), 'w', 0)
        self.color_map = self.solarized_scheme
        self.palette = self.solarized_palette
        self.fg = 'base2'
        self.bg = None
        self.bold = False
        self.blink = False
        self.height = height
        self._initzone(self.height)
        self.cur_x = 0
        self.cur_y = 0
        return

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def _initzone(self, height=10):
        self.out.write('\n' * height)
        self.out.write(self.csi + '?25l')
        self.out.write(self.csi + '%sF' % height)
        self.cur_x = 0
        self.cur_y = 0
        self.clear()
        self.relmoveto(1, 1)
        self.cur_x = 0
        self.cur_y = 0

    def _gethotcolor(self, percent, reverse=False):
        percent = 100 - percent if reverse else percent
        idx = min(int(len(self.palette) * percent / 100.0), len(self.palette) - 1)
        return self.palette[idx]

    def _colorize(self, message, fg=None, bg=None, bold=None, blink=None):
        fg = fg or self.fg
        bg = bg or self.bg
        bold = self.bold if bold is None else bold
        blink = self.blink if blink is None else blink
        params = []
        if bg in self.color_map:
            params.append('48;5;%s' % self.color_map[bg])
        if fg in self.color_map:
            params.append('38;5;%s' % self.color_map[fg])
        if bold:
            params.append('1')
        elif blink:
            params.append('5')
        if params:
            message = ('').join((self.csi, (';').join(params),
             'm', message, self.reset))
        return message

    def _colorint(self, val, warning=False):
        if warning:
            return self._colorize('%.2f' % val, fg='orange')
        else:
            return self._colorize('%.2f' % val, fg='base3')

    def label(self, message, fg=None, bg=None, bold=None, blink=None):
        """ Print a text at the current position.
        """
        self.savepos()
        self.out.write(self._colorize(message, fg, bg, bold, blink))
        self.restorepos()

    def hsep(self, width=1, fg=None, bg=None, double=False):
        """ Print a horizontal separator starting at the current cursor position

        If double=True, prints a double line
        """
        self.savepos()
        self.out.write(self._colorize(('═' if double else '─') * width, fg, bg))
        self.restorepos()

    def vsep(self, height=1, double=False):
        """ Print a vertical separator below the current cursor position,
        starting at the cursor position.
        """
        self.savepos()
        for i in range(height):
            if double:
                self.out.write('║' + self.csi + '1B' + self.csi + '1D')
            else:
                self.out.write('│' + self.csi + '1B' + self.csi + '1D')

        self.restorepos()

    def box(self, width, height, border_fg=None, border_bg=None, bg=None, double=False):
        self.savepos()
        corner1 = self._colorize('╔' if double else '┌', border_fg, border_bg)
        corner2 = self._colorize('╗' if double else '┐', border_fg, border_bg)
        corner3 = self._colorize('╚' if double else '└', border_fg, border_bg)
        corner4 = self._colorize('╝' if double else '┘', border_fg, border_bg)
        vbar = self._colorize('║' if double else '│', border_fg, border_bg)
        background = self._colorize(' ' * (width - 2), bg=bg)
        content_line = vbar + background + vbar
        self.out.write(corner1 + self._colorize(('═' if double else '─') * (width - 2), border_fg, border_bg) + corner2 + self.csi + '1B' + self.csi + '%sD' % width)
        for i in range(height - 2):
            self.out.write(content_line + self.csi + '1B' + self.csi + '%sD' % width)

        self.out.write(corner3 + self._colorize(('═' if double else '─') * (width - 2), border_fg, border_bg) + corner4)
        self.restorepos()

    def clear(self, width=None, height=None):
        """Clears a (widthxheight) rectangle below the cursor, or the whole interface zone if
        no parameter is provided.
        """
        if width is None and height is None:
            self.moveto(0, 0)
            self.out.write(self.csi + 'J')
        else:
            self.savepos()
            for i in range(height):
                self.out.write(' ' * width + self.csi + '1B' + self.csi + '%sD' % width)

            self.restorepos()
        return

    def boolean(self, state, label=None):
        """Displays a green ticked (if `state=True`) or red crossed (if `state=False`) tickbox at
        cursor position, follows by the given label (if any).
        """
        self.savepos()
        label = self._colorize(label, fg='base0')
        msg = (self._colorize('☑', fg='green') if state else self._colorize('☒', fg='red')) + ' ' + label
        self.out.write(msg)
        self.restorepos()

    def bar(self, percent, maxlength=30, msg='', showvalue=True, label=None, color='base1', autocolor=False, highishot=False):
        """Displays an horizontal progressbar based on a percentage.

        :param percent: the percentage of the maxlength
        :param maxlength: length of the bar (default: 30)
        :param showvalue: display the percentage in numerical form
        :param label: the label of the bar
        :param color: color of the bar (not used if autocolor is True)
        :param autocolor: if True, the color depends on the percentage value
        :param highishot: if True, the higher the percentage, the closer to red,
                          else, the higher the percentage, the closer to green.
        """
        msg = msg if msg else ('{0}%').format(self._colorint(percent))
        self.savepos()
        if label:
            label = self._colorize(label, fg='base0')
        self.out.write(('%s |' % label if label else '|') + self.csi + '%sC' % (maxlength - 2) + '|' + (' ' + msg if showvalue else ''))
        self.restorepos()
        bold = False
        if autocolor:
            color, bold = self._gethotcolor(percent, reverse=highishot)
        barlen = int(percent / 100.0 * (maxlength - 2))
        bar = self._colorize('█' * barlen + ' ' * (maxlength - 2 - barlen), fg=color, bold=bold)
        self.out.write(('%s |' % label if label else '|') + bar)
        self.restorepos()

    def absolutebar(self, value, maxvalue, unit, label='', maxlength=30, color='base1', autocolor=False, highishot=False, minvalue=0):
        """Displays an horizontal progressbar based on an absolute value.

        :param value: the value to be represented
        :param maxvalue: upperbound of the admissible values
        :param minvalue: lowerbound of the admissible values
        :param unit: the unit of the data (display next to the numerical value)

        See ConsoleTK.bar for the other parameters.
        """
        msg = '%s%s' % (self._colorint(value, warning=value > maxvalue or value < minvalue), unit)
        clampedvalue = max(minvalue, min(value, maxvalue))
        self.bar((clampedvalue - minvalue) * 100.0 / (maxvalue - minvalue), maxlength, msg, label=label, showvalue=True, color=color, autocolor=autocolor, highishot=highishot)

    def booleanmatrix(self, values, label=''):
        """ 'values' is a list of columns.
        """
        cell = '██'
        if label:
            label = self._colorize(label, fg='base0')
            self.label(label)
            self.relmoveto(0, 1)
        orig_x = self.cur_x
        orig_y = self.cur_y
        for i, col in enumerate(values):
            for j, val in enumerate(col):
                self.moveto(orig_x + i * 2, orig_y + j)
                self.label(cell, fg='green' if val else 'red')

        self.moveto(orig_x, orig_y - (1 if label else 0))

    def savepos(self):
        """Saves the current cursor position for later restoration with restorepos()
        """
        self.out.write(self.csi + 's')

    def restorepos(self):
        """Restores the last cursor position saved with savepos().

        Does nothing if no position has been saved sofar.
        """
        self.out.write(self.csi + 'u')

    def moveto(self, x=0, y=0):
        """Moves the cursor to the given absolute position within the UI area.
        """
        if x < 0:
            raise ValueError('moveto x out of bounds')
        if y < 0 or y > self.height:
            raise ValueError('moveto y out of bounds')
        self.relmoveto(x - self.cur_x, y - self.cur_y)

    def relmoveto(self, x=0, y=0):
        """Moves the cursor relative to its current position.
        """
        self.cur_x += x
        self.cur_y += y
        if x < 0:
            self.out.write(self.csi + '%sD' % -x)
        elif x > 0:
            self.out.write(self.csi + '%sC' % x)
        if y < 0:
            self.out.write(self.csi + '%sA' % -y)
        elif y > 0:
            self.out.write(self.csi + '%sB' % y)

    def __enter__(self):
        self._configure_keyboard()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self._restore_keyboard()
        self.moveto(0, 0)
        self.relmoveto(-1, -1)
        self.cur_x = 0
        self.cur_y = 0
        self.clear()
        self.out.write(self.csi + '?25h')

    def _configure_keyboard(self):
        """
        set keyboard to read single chars lookahead only
        """
        fd = sys.stdin.fileno()
        self.original_kbd_settings = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ECHO
        new[3] = new[3] & ~termios.ICANON
        new[6][6] = '\x00'
        termios.tcsetattr(fd, termios.TCSADRAIN, new)

    def _restore_keyboard(self):
        """
        restore previous keyboard settings
        """
        if hasattr(self, 'original_kbd_settings'):
            fd = sys.stdin.fileno()
            termios.tcsetattr(fd, termios.TCSADRAIN, self.original_kbd_settings)

    ARROW_UP = 'up'
    ARROW_DOWN = 'down'
    ARROW_RIGHT = 'right'
    ARROW_LEFT = 'left'

    def get_keypress(self):
        """
        Non-blocking polling of the keyboard.
        Read max 1 chars from look ahead.

        Process as well common ANSI escape sequences for arrows.
        """
        key = sys.stdin.read(1)
        if key:
            if ord(key) == 27:
                sys.stdin.read(1)
                ansicode = sys.stdin.read(1)
                if ansicode == 'A':
                    return self.ARROW_UP
                if ansicode == 'B':
                    return self.ARROW_DOWN
                if ansicode == 'C':
                    return self.ARROW_RIGHT
                if ansicode == 'D':
                    return self.ARROW_LEFT
                return key
            return key


if __name__ == '__main__':
    import time
    with ConsoleTK(height=10) as (console):
        key = None
        lastkey = None
        i = 0
        while not key or ord(key) != 27:
            i += 1
            key = console.get_keypress()
            if key:
                lastkey = key
            console.boolean(True, "I'm true")
            console.relmoveto(10, 0)
            console.boolean(False, "I'm false")
            console.moveto(22, 0)
            console.absolutebar(i % 10, 10, 'kg', label='Scale', maxlength=20, autocolor=True, highishot=True)
            console.moveto(0, 2)
            console.absolutebar(i % 10 / 10.0, 1, 'rad.s^-1', label=' Youpla')
            console.moveto(78, 2)
            console.vsep(3)
            console.moveto(80, 2)
            console.label('Press a key... (esc to quit)')
            console.moveto(80, 3)
            if lastkey:
                console.label('Keypress: %s (code: %s)' % (lastkey, ord(lastkey)))
            console.moveto(0, 0)
            time.sleep(0.1)