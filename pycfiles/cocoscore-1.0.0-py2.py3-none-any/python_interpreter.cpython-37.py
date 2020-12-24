# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\layer\python_interpreter.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 10131 bytes
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import sys, os, code, pyglet
from pyglet import graphics
from pyglet import text
from pyglet.text import caret, document, layout
import cocos
import cocos.director as director
from .base_layers import Layer
from .util_layers import ColorLayer
__all__ = [
 'PythonInterpreterLayer']

class Output:

    def __init__(self, display, realstdout):
        self.out = display
        self.realstdout = realstdout
        self.data = ''

    def write(self, data):
        self.out(data)


class MyInterpreter(code.InteractiveInterpreter):

    def __init__(self, locals, display):
        self.write = display
        code.InteractiveInterpreter.__init__(self, locals=locals)

    def execute(self, input):
        old_stdout = sys.stdout
        sys.stdout = Output(self.write, old_stdout)
        more = self.runsource(input)
        sys.stdout = old_stdout
        return more


class PythonInterpreterLayer(ColorLayer):
    """PythonInterpreterLayer"""
    cfg = {'code.font_name':'Arial', 
     'code.font_size':12, 
     'code.color':(255, 255, 255, 255), 
     'caret.color':(255, 255, 255)}
    name = 'py'
    prompt = '>>> '
    prompt_more = '... '
    doing_more = False
    is_event_handler = True

    def __init__(self):
        super(PythonInterpreterLayer, self).__init__(32, 32, 32, 192)
        self.content = self.prompt
        local_vars = director.interpreter_locals
        local_vars['self'] = self
        self.interpreter = MyInterpreter(local_vars, self._write)
        self.current_input = []
        self.history = [
         '']
        self.history_pos = 0

    def on_enter(self):
        super(PythonInterpreterLayer, self).on_enter()
        vw, vh = cocos.director.director.get_window_size()
        self.document = document.FormattedDocument(self.content)
        self.document.set_style(0, len(self.document.text), {'font_name':self.cfg['code.font_name'], 
         'font_size':self.cfg['code.font_size'], 
         'color':self.cfg['code.color']})
        self.batch = graphics.Batch()
        self.layout = layout.IncrementalTextLayout((self.document), vw,
          vh, multiline=True, batch=(self.batch))
        self.layout.anchor_y = 'top'
        self.caret = caret.Caret((self.layout), color=(self.cfg['caret.color']))
        self.caret.on_activate()
        self.on_resize(vw, vh)
        self.start_of_line = len(self.document.text)

    def on_resize(self, x, y):
        vw, vh = director.get_window_size()
        self.layout.begin_update()
        self.layout.height = vh
        self.layout.x = 2
        self.layout.width = vw - 4
        self.layout.y = vh
        self.layout.end_update()
        x, y = director.window.width, director.window.height
        self.layout.top_group._scissor_width = x - 4
        self.caret.position = len(self.document.text)

    def on_exit(self):
        super(PythonInterpreterLayer, self).on_exit()
        self.content = self.document.text
        self.document = None
        self.layout = None
        self.batch = None
        self.caret = None

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.TAB:
            return self.caret.on_text('\t')
            if symbol in (pyglet.window.key.ENTER, pyglet.window.key.NUM_ENTER):
                self._write('\n')
                line = self.document.text[self.start_of_line:]
                if line.strip() == 'help()':
                    line = 'print "help() not supported, sorry!"'
                self.current_input.append(line)
                self.history_pos = len(self.history)
                if line.strip():
                    self.history[self.history_pos - 1] = line.strip()
                    self.history.append('')
                more = False
                if not self.doing_more:
                    more = self.interpreter.execute('\n'.join(self.current_input))
                if self.doing_more:
                    if not line.strip():
                        self.doing_more = False
                        self.interpreter.execute('\n'.join(self.current_input))
                more = more or 
                if not more:
                    self.current_input = []
                    self._write(self.prompt)
                else:
                    self.doing_more = True
                    self._write(self.prompt_more)
                self.start_of_line = len(self.document.text)
                self.caret.position = len(self.document.text)
        elif symbol == pyglet.window.key.SPACE:
            pass
        else:
            return pyglet.event.EVENT_UNHANDLED
        return pyglet.event.EVENT_HANDLED

    def on_text(self, symbol):
        if symbol == '\r':
            return pyglet.event.EVENT_HANDLED
        self._scroll_to_bottom()
        return self.caret.on_text(symbol)

    def on_text_motion(self, motion):
        at_sol = self.caret.position == self.start_of_line
        if motion == pyglet.window.key.MOTION_UP:
            line = self.document.text[self.start_of_line:]
            if self.history_pos == len(self.history) - 1:
                self.history[self.history_pos] = line
            self.history_pos = max(0, self.history_pos - 1)
            self.document.delete_text(self.start_of_line, len(self.document.text))
            self._write(self.history[self.history_pos])
            self.caret.position = len(self.document.text)
        elif motion == pyglet.window.key.MOTION_DOWN:
            self.history_pos = min(len(self.history) - 1, self.history_pos + 1)
            self.document.delete_text(self.start_of_line, len(self.document.text))
            self._write(self.history[self.history_pos])
            self.caret.position = len(self.document.text)
        elif motion == pyglet.window.key.MOTION_BACKSPACE:
            if not at_sol:
                return self.caret.on_text_motion(motion)
        elif motion == pyglet.window.key.MOTION_LEFT:
            if not at_sol:
                return self.caret.on_text_motion(motion)
        elif motion == pyglet.window.key.MOTION_PREVIOUS_WORD:
            if not at_sol:
                return self.caret.on_text_motion(motion)
        else:
            return self.caret.on_text_motion(motion)
        return pyglet.event.EVENT_HANDLED

    def _write(self, s):
        self.document.insert_text(len(self.document.text), s, {'font_name':self.cfg['code.font_name'], 
         'font_size':self.cfg['code.font_size'], 
         'color':self.cfg['code.color']})
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        if self.layout.height < self.layout.content_height:
            self.layout.anchor_y = 'bottom'
            self.layout.y = 0
            self.layout.view_y = 0
        if self.caret.position < self.start_of_line:
            self.caret.position = len(self.document.text)

    def draw(self):
        super(PythonInterpreterLayer, self).draw()
        self.batch.draw()