# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fabrizio/Dropbox/free_range_factory/boot/boot_pkg/editor.py
# Compiled at: 2012-08-06 02:45:06
import pygtk, gtk, pango
pygtk.require('2.0')
from pygments.lexers import PythonLexer
from pygments.styles.tango import TangoStyle

class text_editor:
    """This is a simple text editor GUI used by boot for displaying and editing 
       text files within boot.
    """

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        self.window2.destroy()
        gtk.main_quit()

    def load_file(self, widget):
        _txt = ''
        with open(self.local_file, 'r') as (f):
            _txt = f.read()
        f.close()
        print len(_txt), 'characters loaded.'
        STYLE = TangoStyle
        styles = {}
        for token, value in PythonLexer().get_tokens(_txt):
            while not STYLE.styles_token(token) and token.parent:
                token = token.parent

            if token not in styles:
                styles[token] = self.textbuffer.create_tag()
            start = self.textbuffer.get_end_iter()
            self.textbuffer.insert_with_tags(start, value.encode('utf-8'), styles[token])

        for token, tag in styles.iteritems():
            style = STYLE.style_for_token(token)
            if style['bgcolor']:
                tag.set_property('background', '#' + style['bgcolor'])
            if style['color']:
                tag.set_property('foreground', '#' + style['color'])
            if style['bold']:
                tag.set_property('weight', pango.WEIGHT_BOLD)
            if style['italic']:
                tag.set_property('style', pango.STYLE_ITALIC)
            if style['underline']:
                tag.set_property('underline', pango.UNDERLINE_SINGLE)

    def save_content(self, widget):
        _txt = self.textbuffer.get_text(self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter(), include_hidden_chars=True)
        with open(self.local_file, 'w') as (f):
            f.write(_txt)
        f.close()
        print 'Content saved in local file.'

    def __init__(self, _file):
        self.local_file = _file
        self.window2 = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window2.connect('delete_event', self.delete_event)
        self.window2.connect('destroy', self.destroy)
        win_title = self.local_file
        if len(win_title) > 50:
            win_title = '... ' + win_title[len(win_title) - 50:len(win_title)]
        self.window2.set_title(win_title)
        self.window2.set_border_width(3)
        self.window2.set_size_request(680, 500)
        viewer_btn_save = gtk.Button('Save Changes')
        viewer_btn_close = gtk.Button('Close Window')
        viewer_btn_close.connect('clicked', self.destroy)
        viewer_btn_save.connect('clicked', self.save_content)
        viewer_Vbox = gtk.VBox(False, 0)
        viewer_Hbox = gtk.HBox(False, 0)
        viewer_Hbox.pack_end(viewer_btn_close, False, False, 2)
        viewer_Hbox.pack_end(viewer_btn_save, False, False, 2)
        self.texteditorsw = gtk.ScrolledWindow()
        self.texteditorsw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.texteditorsw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.texteditor = gtk.TextView(buffer=None)
        self.texteditor.set_left_margin(5)
        self.texteditor.set_right_margin(5)
        self.textbuffer = self.texteditor.get_buffer()
        self.texteditor.modify_font(pango.FontDescription('monospace 10'))
        self.texteditor.set_wrap_mode(gtk.WRAP_WORD)
        self.texteditor.set_editable(True)
        self.texteditor.set_justification(gtk.JUSTIFY_LEFT)
        self.texteditorsw.add(self.texteditor)
        self.window2.add(viewer_Vbox)
        viewer_Vbox.pack_start(self.texteditorsw, True, True, 0)
        viewer_Vbox.pack_start(viewer_Hbox, False, False, 2)
        self.window2.show_all()
        return

    def start(self):
        self.load_file(self)
        gtk.main()