# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/andrew/dev/python/stocki/stocki/stocki.py
# Compiled at: 2018-07-13 15:04:16
import sys, urwid, requests
from urwid.widget import BOX, FLOW, FIXED
VERSION = '0.1.1'
SCROLL_LINE_UP = 'line up'
SCROLL_LINE_DOWN = 'line down'
SCROLL_PAGE_UP = 'page up'
SCROLL_PAGE_DOWN = 'page down'
SCROLL_TO_TOP = 'to top'
SCROLL_TO_END = 'to end'
YELLOW = '\x1b[33m'
RED = '\x1b[31m'
BOLD = '\x1b[1m'
UNDERLINE = '\x1b[4m'
END = '\x1b[0m'

class Scrollable(urwid.WidgetDecoration):

    def sizing(self):
        return frozenset([BOX])

    def selectable(self):
        return True

    def __init__(self, widget):
        """Box widget that makes a fixed or flow widget vertically scrollable.

        Note:
            This code is based off of code from:
                https://github.com/rndusr/stig/blob/master/stig/tui/scroll.py
        """
        self._trim_top = 0
        self._scroll_action = None
        self._forward_keypress = None
        self._old_cursor_coords = None
        self._rows_max_cached = 0
        self.__super.__init__(widget)
        return

    def render(self, size, focus=False):
        maxcol, maxrow = size
        ow = self._original_widget
        ow_size = self._get_original_widget_size(size)
        canv = urwid.CompositeCanvas(ow.render(ow_size, focus))
        canv_cols, canv_rows = canv.cols(), canv.rows()
        if canv_cols <= maxcol:
            pad_width = maxcol - canv_cols
            if pad_width > 0:
                canv.pad_trim_left_right(0, pad_width)
        if canv_rows <= maxrow:
            fill_height = maxrow - canv_rows
            if fill_height > 0:
                canv.pad_trim_top_bottom(0, fill_height)
        if canv_cols <= maxcol and canv_rows <= maxrow:
            return canv
        else:
            self._adjust_trim_top(canv, size)
            trim_top = self._trim_top
            trim_end = canv_rows - maxrow - trim_top
            trim_right = canv_cols - maxcol
            if trim_top > 0:
                canv.trim(trim_top)
            if trim_end > 0:
                canv.trim_end(trim_end)
            if trim_right > 0:
                canv.pad_trim_left_right(0, -trim_right)
            if canv.cursor is not None:
                curscol, cursrow = canv.cursor
                if cursrow >= maxrow or cursrow < 0:
                    canv.cursor = None
            self._forward_keypress = bool(canv.cursor)
            return canv

    def keypress(self, size, key):
        if self._forward_keypress:
            ow = self._original_widget
            ow_size = self._get_original_widget_size(size)
            if hasattr(ow, 'get_cursor_coords'):
                self._old_cursor_coords = ow.get_cursor_coords(ow_size)
            key = ow.keypress(ow_size, key)
            if key is None:
                return
        command_map = self._command_map
        if command_map[key] == urwid.CURSOR_UP:
            self._scroll_action = SCROLL_LINE_UP
        elif command_map[key] == urwid.CURSOR_DOWN:
            self._scroll_action = SCROLL_LINE_DOWN
        elif command_map[key] == urwid.CURSOR_PAGE_UP:
            self._scroll_action = SCROLL_PAGE_UP
        elif command_map[key] == urwid.CURSOR_PAGE_DOWN:
            self._scroll_action = SCROLL_PAGE_DOWN
        elif command_map[key] == urwid.CURSOR_MAX_LEFT:
            self._scroll_action = SCROLL_TO_TOP
        elif command_map[key] == urwid.CURSOR_MAX_RIGHT:
            self._scroll_action = SCROLL_TO_END
        else:
            return key
        self._invalidate()
        return

    def mouse_event(self, size, event, button, col, row, focus):
        if button == 5:
            self._scroll_action = SCROLL_LINE_DOWN
        elif button == 4:
            self._scroll_action = SCROLL_LINE_UP
        self._invalidate()
        ow = self._original_widget
        if hasattr(ow, 'mouse_event'):
            ow_size = self._get_original_widget_size(size)
            row += self._trim_top
            return ow.mouse_event(ow_size, event, button, col, row, focus)
        else:
            return False

    def _adjust_trim_top(self, canv, size):
        action = self._scroll_action
        self._scroll_action = None
        maxcol, maxrow = size
        trim_top = self._trim_top
        canv_rows = canv.rows()
        if trim_top < 0:
            trim_top = canv_rows - maxrow + trim_top + 1
        if canv_rows <= maxrow:
            self._trim_top = 0
            return
        else:

            def ensure_bounds(new_trim_top):
                return max(0, min(canv_rows - maxrow, new_trim_top))

            if action == SCROLL_LINE_UP:
                self._trim_top = ensure_bounds(trim_top - 1)
            elif action == SCROLL_LINE_DOWN:
                self._trim_top = ensure_bounds(trim_top + 1)
            elif action == SCROLL_PAGE_UP:
                self._trim_top = ensure_bounds(trim_top - maxrow + 1)
            elif action == SCROLL_PAGE_DOWN:
                self._trim_top = ensure_bounds(trim_top + maxrow - 1)
            elif action == SCROLL_TO_TOP:
                self._trim_top = 0
            elif action == SCROLL_TO_END:
                self._trim_top = canv_rows - maxrow
            else:
                self._trim_top = ensure_bounds(trim_top)
            if self._old_cursor_coords is not None and self._old_cursor_coords != canv.cursor:
                self._old_cursor_coords = None
                curscol, cursrow = canv.cursor
                if cursrow < self._trim_top:
                    self._trim_top = cursrow
                elif cursrow >= self._trim_top + maxrow:
                    self._trim_top = max(0, cursrow - maxrow + 1)
            return

    def _get_original_widget_size(self, size):
        ow = self._original_widget
        sizing = ow.sizing()
        if FIXED in sizing:
            return ()
        if FLOW in sizing:
            return (size[0],)

    def get_scrollpos(self, size=None, focus=False):
        return self._trim_top

    def set_scrollpos(self, position):
        self._trim_top = int(position)
        self._invalidate()

    def rows_max(self, size=None, focus=False):
        if size is not None:
            ow = self._original_widget
            ow_size = self._get_original_widget_size(size)
            sizing = ow.sizing()
            if FIXED in sizing:
                self._rows_max_cached = ow.pack(ow_size, focus)[1]
            elif FLOW in sizing:
                self._rows_max_cached = ow.rows(ow_size, focus)
            else:
                raise RuntimeError('Not a flow/box widget: %r' % self._original_widget)
        return self._rows_max_cached


class App:

    def __init__(self, content):
        self._palette = [
         ('menu', 'black', 'light gray', 'standout'),
         ('title', 'default,bold', 'default', 'bold')]
        menu = urwid.Text(['\n', ('menu', ' Q '), ('light gray', ' Quit')])
        layout = urwid.Frame(body=content, footer=menu)
        main_loop = urwid.MainLoop(layout, self._palette, unhandled_input=self._handle_input)
        main_loop.run()

    def _handle_input(self, input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()


def load(ticker):
    base_url = 'https://api.iextrading.com/1.0/stock'
    ticker = ticker.upper()
    try:
        r_quote = requests.get(('{}/{}/quote').format(base_url, ticker))
        r_info = requests.get(('{}/{}/company').format(base_url, ticker))
        data = r_quote.json()
        data.update(r_info.json())
        pile = urwid.Pile([
         urwid.Text('STOCKI: The CLI Interface for fetching stock market data\n', align='center'),
         urwid.Text(('title', ('{} OVERVIEW').format(ticker))),
         urwid.Padding(urwid.Text(('Price: {}').format(data['latestPrice'])), left=5),
         urwid.Padding(urwid.Text(('Change: {} ({:%})').format(data['change'], data['changePercent'])), left=5),
         urwid.Padding(urwid.Text(('Volume: {}').format(data['latestVolume'])), left=5),
         urwid.Padding(urwid.Text(('Market Cap: {}').format(data['marketCap'])), left=5),
         urwid.Padding(urwid.Text(('52 Week Range: {}-{}').format(data['week52Low'], data['week52High'])), left=5),
         urwid.Padding(urwid.Text(('YTD Change: {:%}\n').format(float(data['ytdChange']))), left=5),
         urwid.Text(('title', 'COMPANY INFO')),
         urwid.Padding(urwid.Text(('Name: {}').format(data['companyName'])), left=5),
         urwid.Padding(urwid.Text(('Industry: {}').format(data['industry'])), left=5),
         urwid.Padding(urwid.Text(('Sector: {}').format(data['sector'])), left=5),
         urwid.Padding(urwid.Text(('Website: {}').format(data['website'])), left=5),
         urwid.Padding(urwid.Text(('CEO: {}\n').format(data['CEO'])), left=5),
         urwid.Text(('title', 'DESCRIPTION')),
         urwid.Padding(urwid.Text(data['description']), left=5)])
        padding = urwid.Padding(Scrollable(pile), left=1, right=1)
        return padding
    except Exception as e:
        return

    return


def help():
    print ('').join([BOLD, ('stocki {} – Made by @andrewrporter').format(VERSION), END, '\n'])
    print 'The CLI for fetching stock market data.\n'
    print ('').join([UNDERLINE, 'Usage', END, ':', ' $ stocki ', YELLOW, 'ticker', END])


def version():
    print ('stocki {}').format(VERSION)


def main():
    if len(sys.argv) == 1:
        help()
    elif sys.argv[1].lower() in ('-h', '--help'):
        help()
    elif sys.argv[1].lower() in ('-v', '--version'):
        version()
    else:
        ticker = sys.argv[1]
        content = load(ticker)
        if content:
            App(content)
        else:
            print ('').join([RED, ("stocki doesn't recognize: '{}'").format(ticker), END])