# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/gtk_tools/gtkexcepthook.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 9333 bytes
import inspect, linecache, pydoc, sys, traceback
from io import StringIO
from gettext import gettext as _
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango
original_excepthook = sys.excepthook

class GtkExceptionHook:
    __doc__ = '\n        Exception handling GTK-dialog hook \n    '
    quit_confirmation_func = None
    exception_dialog_active = False
    RESPONSE_QUIT = 1

    def analyze_simple(self, exctyp, value, tb):
        """
            Analyzes the exception into a human readable stack trace
        """
        trace = StringIO()
        traceback.print_exception(exctyp, value, tb, None, trace)
        return trace

    def lookup(self, name, frame, lcls):
        """Find the value for a given name in the given frame"""
        if name in lcls:
            return ('local', lcls[name])
        else:
            if name in frame.f_globals:
                return (
                 'global', frame.f_globals[name])
            if '__builtins__' in frame.f_globals:
                builtins = frame.f_globals['__builtins__']
                if type(builtins) is dict:
                    if name in builtins:
                        return (
                         'builtin', builtins[name])
                elif hasattr(builtins, name):
                    return (
                     'builtin', getattr(builtins, name))
            return (
             None, [])

    _parent_window = [None]
    _level = 0

    @property
    def parent_window(self):
        return self._parent_window[self._level]

    @parent_window.setter
    def parent_window(self, value):
        self._parent_window[self._level] = value

    def overriden_parent_window(self, parent):
        """
            Sets the parent window temporarily to another value
            and returns itself, so this can be used as a context
            manager.
        """
        self._parent_window.append(parent)
        self._level = len(self._parent_window)
        return self

    def __enter__(self):
        pass

    def __exit__(self):
        if self._level > 0:
            self._parent_window.pop(self._level)
            self._level = len(self._parent_window)

    def analyze(self, exctyp, value, tb):
        """
            Analyzes the exception into a human readable stack trace
        """
        import tokenize, keyword
        trace = StringIO()
        nlines = 3
        frecs = inspect.getinnerframes(tb, nlines)
        trace.write('Traceback (most recent call last):\n')
        for frame, fname, lineno, funcname, context, _ in frecs:
            trace.write('  File "%s", line %d, ' % (fname, lineno))
            args, varargs, varkw, lcls = inspect.getargvalues(frame)

            def readline(lno=[
 lineno], *args):
                if args:
                    print(args)
                try:
                    return linecache.getline(fname, lno[0])
                finally:
                    lno[0] += 1

            all, prev, name, scope = ({}, None, '', None)
            for ttype, tstr, stup, etup, line in tokenize.generate_tokens(readline):
                if ttype == tokenize.NAME and tstr not in keyword.kwlist:
                    if name:
                        if name[(-1)] == '.':
                            try:
                                val = getattr(prev, tstr)
                            except AttributeError:
                                break

                            name += tstr
                    else:
                        assert not name and not scope
                        scope, val = self.lookup(tstr, frame, lcls)
                        name = tstr
                    if val is not None:
                        prev = val
                else:
                    if tstr == '.':
                        if prev:
                            name += '.'
                        else:
                            if name:
                                all[name] = (
                                 scope, prev)
                            prev, name, scope = (None, '', None)
                            if ttype == tokenize.NEWLINE:
                                break

            try:
                details = inspect.formatargvalues(args, varargs, varkw, lcls, formatvalue=(lambda v: '=' + pydoc.text.repr(v)))
            except:
                details = '(no details)'

            trace.write(funcname + details + '\n')
            if context is None:
                context = [
                 '<source context missing>\n']
            trace.write(''.join(['    ' + x.replace('\t', '  ') for x in [a for a in context if a.strip()]]))
            if len(all):
                trace.write('  variables: %s\n' % str(all))

        trace.write('%s: %s' % (exctyp.__name__, value))
        return trace

    def __call__(self, exctyp, value, tb):
        """
            This is called when an exception occurs.
        """
        if exctyp is KeyboardInterrupt:
            return original_excepthook(exctyp, value, tb)
        sys.stderr.write(self.analyze_simple(exctyp, value, tb).getvalue())
        if self.exception_dialog_active:
            return
        Gdk.pointer_ungrab(Gdk.CURRENT_TIME)
        Gdk.keyboard_ungrab(Gdk.CURRENT_TIME)
        self.exception_dialog_active = True
        dialog = Gtk.MessageDialog(parent=(self.parent_window),
          flags=0,
          type=(Gtk.MessageType.WARNING),
          buttons=(Gtk.ButtonsType.NONE))
        dialog.set_title(_('Bug Detected'))
        primary = _('<big><b>A programming error has been detected.</b></big>')
        secondary = _("It probably isn't fatal, but the details should be reported to the developers nonetheless.")
        try:
            setsec = dialog.format_secondary_text
        except AttributeError:
            raise
            dialog.vbox.get_children()[0].get_children()[1].set_markup('%s\n\n%s' % (primary, secondary))
        else:
            del setsec
            dialog.set_markup(primary)
            dialog.format_secondary_text(secondary)
        dialog.add_button(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)
        dialog.add_button(Gtk.STOCK_QUIT, self.RESPONSE_QUIT)

        def expander_cb(expander, *ignore):
            if expander.get_expanded():
                dialog.set_resizable(True)
            else:
                dialog.set_resizable(False)

        details_expander = Gtk.Expander()
        details_expander.set_label(_('Details...'))
        details_expander.connect('notify::expanded', expander_cb)
        textview = Gtk.TextView()
        textview.show()
        textview.set_editable(False)
        textview.modify_font(Pango.FontDescription('Monospace'))
        sw = Gtk.ScrolledWindow()
        sw.show()
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        sw.set_size_request(800, 400)
        sw.add(textview)
        details_expander.add(sw)
        details_expander.show_all()
        dialog.get_content_area().pack_start(details_expander, True, True, 0)
        try:
            trace = self.analyze(exctyp, value, tb).getvalue()
        except:
            trace = _('Exception while analyzing the exception.')

        buf = textview.get_buffer()
        buf.set_text(trace)
        dialog.connect('response', self._dialog_response_cb, trace)
        dialog.set_modal(True)
        dialog.show()
        dialog.present()

    def _dialog_response_cb(self, dialog, resp, trace):
        if resp == self.RESPONSE_QUIT:
            if Gtk.main_level() > 0:
                if not callable(self.quit_confirmation_func):
                    sys.exit(1)
                else:
                    if self.quit_confirmation_func():
                        sys.exit(1)
                    else:
                        dialog.destroy()
                        self.exception_dialog_active = False
        else:
            dialog.destroy()
            self.exception_dialog_active = False


def plugin_gtk_exception_hook():
    hook = GtkExceptionHook()
    sys.excepthook = hook
    return hook