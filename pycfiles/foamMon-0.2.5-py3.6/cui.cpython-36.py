# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/FoamMon/cui.py
# Compiled at: 2018-09-24 09:00:08
# Size of source mod 2**32: 13608 bytes
import urwid
from .header import foamMonHeader
import os
from .FoamDataStructures import Cases, default_elements
import threading, time, datetime, cProfile, pstats, sys, json
palette = [
 ('titlebar', 'dark red', ''),
 ('refresh button', 'dark green,bold', ''),
 ('progress', '', 'dark green'),
 ('unprogressed', '', 'dark blue'),
 ('sampling', '', 'yellow'),
 ('quit button', 'dark red,bold', ''),
 ('getting quote', 'dark blue', ''),
 ('active', 'white,bold', ''),
 ('mode button', 'white,bold', ''),
 ('inactive ', 'light gray', ''),
 ('change negative', 'dark red', '')]
CASE_CTR = 0
CASE_REFS = {}
MODE_SWITCH = False
FOCUS_ID = None
FILTER = None
FPS = 1.0
COLUMNS = {}
FILTER = {}

class ProgressBar:
    events = []

    def __init__(self, size, progress=0):
        self.size = size
        self.done_char = ('progress', ' ')
        self.undone_char = ('unprogressed', ' ')
        self.digits_done = [self.done_char for _ in range(int(progress * size))]
        self.digits_undone = [self.undone_char for _ in range(size - int(progress * size))]
        self.digits = self.digits_done + self.digits_undone

    def add_event(self, percentage, color):
        index = int(percentage * self.size)
        self.digits[index] = (color, ' ')

    def draw(self):
        return ''.join(self.digits)

    def render(self):
        return urwid.Text(self.digits)


class TableHeader:

    def __init__(self, lengths):
        global FILTER
        self.lengths = lengths
        self.columns = [CaseColumn(name, self.lengths.get(name, 20), None) for name in default_elements if COLUMNS[name]]
        self.columns += [CaseColumn(el, 20, None) for el in FILTER.keys()]

    @property
    def header_text(self):
        s = ''.join([c.getName() for c in self.columns])
        return s


class CaseColumn:

    def __init__(self, name, length, reference):
        self.name = name
        self.length = length
        self.reference = reference

    def get_pack(self, mode):
        if isinstance(self.name, str):
            if self.name == 'progressbar':
                return (
                 'pack', urwid.Text(self.bar()))
            return ('pack',
             urwid.Text((mode,
              '{: ^{length}}'.format((getattr(self.reference, self.name)),
                length=(self.length + 2)))))
        else:
            return (
             'pack',
             urwid.Text((mode,
              '{: ^{length}}'.format((self.reference.custom_filter(self.name[1])),
                length=(self.length + 2)))))

    def bar(self):
        bar = ProgressBar(50, self.reference.progress)
        bar.add_event(self.reference.case.startSamplingPerc, 'sampling')
        return bar.digits

    def getName(self):
        return '{: ^{length}}'.format((self.name), length=(self.length + 2))


class CaseRow(urwid.WidgetWrap):

    def __init__(self, case, Id, length=False, active=False):
        global CASE_CTR
        global CASE_REFS
        self.case = case
        self.active = active
        self.lengths = length
        CASE_CTR += 1
        self.Id = CASE_CTR
        CASE_REFS[int(self.Id)] = self.case.case
        mode_text = 'active' if self.active else 'inactive'
        if self.case:
            self.columns = [CaseColumn(name, self.lengths.get(name, 20), self.case) for name in default_elements if COLUMNS[name]]
            self.columns += [CaseColumn(el, 20, self.case) for el in FILTER.items()]
        else:
            self.columns = []
        urwid.WidgetWrap.__init__(self, urwid.Columns([
         (
          'pack', urwid.Text((mode_text, '{: ^2} '.format(self.Id))))] + self.status_packs(mode_text)))

    def status_packs(self, mode):
        return [c.get_pack(mode) for c in self.columns]


class DisplaySub(urwid.WidgetWrap):

    def __init__(self, Id, name, elems, lengths, hide_inactive):
        self.path = name
        self.elems = elems
        self.lengths = lengths
        self.Id = Id
        self.hide_inactive = hide_inactive
        self.frame = self.draw()
        urwid.WidgetWrap.__init__(self, self.frame)

    @property
    def active(self):
        return self.elems['active']

    @property
    def inactive(self):
        return self.elems['inactive']

    def draw(self):
        items = [('pack', CaseRow(c, ((i + 1) * self.Id), (self.lengths), active=True)) for i, c in enumerate(self.active)]
        if not self.hide_inactive:
            items += [('pack', CaseRow(c, ((i + 1 + len(self.active)) * self.Id), (self.lengths), active=False)) for i, c in enumerate(self.inactive)]
        return urwid.BoxAdapter(urwid.Frame(header=(urwid.Text(('casefolder', self.props_str))),
          body=(urwid.Pile(items)),
          footer=(urwid.Divider('─'))),
          height=(len(items) + 2))

    @property
    def props_str(self):
        num_active = len(self.elems['active'])
        num_inactive = len(self.elems['inactive'])
        return 'Folder: {} total: {}, active: {}'.format(self.path, num_inactive + num_active, num_active)

    def update(self):
        self._w = self.draw()
        return self


class CasesListFrame:

    def __init__(self, cases, hide_inactive):
        self.cases = cases
        self.hide_inactive = hide_inactive

    def draw(self):
        """ return a ListBox with all sub folder """
        lengths, valid_cases = self.cases.get_valid_cases()
        items = [urwid.Text(TableHeader(lengths).header_text)]
        items += [DisplaySub(i + 1, path, elems, lengths, self.hide_inactive) for i, (path, elems) in enumerate(valid_cases.items())]
        return urwid.ListBox(urwid.SimpleFocusListWalker(items))

    def toggle_hide(self):
        self.hide_inactive = not self.hide_inactive


class ScreenParent(urwid.WidgetWrap):

    def __init__(self, frame, mode_switch):
        self._w = frame
        self.input_mode = False
        self.mode_switch = mode_switch
        self.input_txt = ''
        urwid.WidgetWrap.__init__(self, self._w)

    def update(self):
        self._w = self.draw()
        return self

    def keypress_parent(self, size, key):
        global FILTER
        global FOCUS_ID
        global MODE_SWITCH
        if key == 'Q' or key == 'q':
            self.cases.running = False
            raise urwid.ExitMainLoop()
        elif self.input_mode:
            if key != 'enter' and key != 'backspace':
                self.input_txt += key
                self.input_mode_footer_txt += key
                self._w = self.draw()
            else:
                if key == 'backspace':
                    self.input_txt = self.input_txt[0:-1]
                    self.input_mode_footer_txt = self.input_mode_footer_txt[0:-1]
                    self._w = self.draw()
                else:
                    if 'enter' in key:
                        if self.input_mode == 'Focus':
                            FOCUS_ID = self.input_txt
                            MODE_SWITCH = True
                            FILTER = None
                            self.input_mode = False
                if 'enter' in key:
                    if self.input_mode == 'Filter':
                        FILTER = self.input_txt
                        self.input_mode = False


class OverviewScreen(ScreenParent):

    def __init__(self, cases, focus_id, mode_switch, hide_inactive=False):
        self.cases = cases
        self.focus_id = focus_id
        self.hide_inactive = hide_inactive
        self.cases_list_frame = CasesListFrame(self.cases, self.hide_inactive)
        self.input_mode_footer_txt = 'Case ID: '
        self._w = urwid.Text('')
        self.mode_switch = mode_switch
        ScreenParent.__init__(self, self._w, self.mode_switch)
        self._w = self.draw()

    @property
    def footer(self):
        if not self.input_mode:
            menu = urwid.Text([
             'Press (', ('mode button', 'T'), ') to toggle active, ',
             '(', ('mode button', 'F'), ') to focus, ',
             '(', ('quit button', 'Q'), ') to quit,'],
              align='right')
            legend = urwid.Text(['Legend: ',
             ('progress', ' '), ' Progress ',
             ('active', 'Active'), ' ',
             ('inactive', 'Inactive'), ' ',
             ('sampling', ' '), ' Sampling Start'])
            return urwid.Columns([legend, menu])
        else:
            return urwid.Edit(self.input_mode_footer_txt)

    def draw(self):
        banner = urwid.Text(foamMonHeader, 'center')
        body = urwid.LineBox(self.cases_list_frame.draw())
        footer = self.footer
        return urwid.Frame(header=banner, body=body, footer=footer)

    def keypress(self, size, key):
        if key == 'F' or key == 'f':
            self.input_mode = 'Focus'
            self._w = self.draw()
        else:
            if key == 'T' or key == 't':
                self.cases_list_frame.toggle_hide()
                self._w = self.draw()
            else:
                self.keypress_parent(size, key)


class FocusScreen(ScreenParent):

    def __init__(self, focus_id):
        self.focus_id = focus_id
        self.hide_inactive = False
        self.input_mode_footer_txt = 'Filter: '
        self._w = urwid.Text('')
        ScreenParent.__init__(self, self._w, False)
        self._w = self.draw()

    def draw(self):
        banner = urwid.Text(foamMonHeader, 'center')
        body = urwid.Pile([
         (
          'pack', urwid.Text(CASE_REFS[int(FOCUS_ID)].path)),
         (
          'pack', urwid.Text(CASE_REFS[int(FOCUS_ID)].log.text(FILTER)))])
        footer = self.footer
        return urwid.Frame(header=banner, body=body, footer=footer)

    @property
    def footer(self):
        if not self.input_mode:
            menu = urwid.Text([
             'Press (', ('mode button', 'O'), ') for overview mode, ',
             '(', ('mode button', '/'), ') to filter, ',
             '(', ('quit button', 'Q'), ') to quit,'],
              align='right')
            legend = urwid.Text(['Legend: ',
             ('progress', ' '), ' Progress ',
             ('active', 'Active'), ' ',
             ('inactive', 'Inactive'), ' ',
             ('sampling', ' '), ' Sampling Start'])
            return urwid.Columns([legend, menu])
        else:
            return urwid.Edit(self.input_mode_footer_txt)

    def keypress(self, size, key):
        global MODE_SWITCH
        if key == '/':
            self.input_mode = 'Filter'
            self._w = self.draw()
        else:
            if key == 'O' or key == 'o' and not self.input_mode:
                MODE_SWITCH = True
            else:
                self.keypress_parent(size, key)


class LogMonFrame(urwid.WidgetWrap):

    def __init__(self, cases):
        self.cases = cases
        self.focus_mode = False
        self.focus_id = None
        self.mode_switch = False
        self.frame = OverviewScreen(self.cases, self.focus_id, self.mode_switch)
        self._w = self.frame
        urwid.WidgetWrap.__init__(self, self._w)

    def draw(self):
        """ returns either a FocusScreen or OverviewScreen instance """
        global FPS
        global MODE_SWITCH
        if not MODE_SWITCH:
            self.frame = self.frame.update()
            return self.frame
        else:
            if isinstance(self.frame, OverviewScreen):
                self.frame = FocusScreen(self.focus_id)
                MODE_SWITCH = False
                FPS = 30.0
                return self.frame
            self.frame = OverviewScreen(self.cases, self.focus_id, self.mode_switch)
            FPS = 1.0
            MODE_SWITCH = False
            return self.frame

    def keypress(self, size, key):
        """ delegates keypress to the actual screen """
        self._w.keypress(size, key)

    def animate(self, loop=None, data=None):
        global CASE_CTR
        CASE_CTR = 0
        self.frame = self.draw()
        self._w = self.frame
        self.animate_alarm = self.loop.set_alarm_in(1.0 / FPS, self.animate)


def cui_main(arguments):
    global COLUMNS
    global FILTER
    cases = Cases(os.getcwd())
    COLUMNS = {c:(False if arguments.get('--' + c) == 'False' else True) for c in ('progressbar',
                                                                                   'folder',
                                                                                   'logfile',
                                                                                   'time',
                                                                                   'writeout',
                                                                                   'remaining')}
    FILTER = json.loads(arguments.get('--custom_filter'))
    frame = LogMonFrame(cases)
    mainloop = urwid.MainLoop(frame, palette, handle_mouse=False)
    mainloop.screen.set_terminal_properties(colors=256)
    frame.loop = mainloop
    frame.animate()
    mainloop.run()