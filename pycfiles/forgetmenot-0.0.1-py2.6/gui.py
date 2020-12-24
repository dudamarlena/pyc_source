# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/forgetmenot/gui.py
# Compiled at: 2010-03-29 08:26:38
import pygtk, gtk, gtk.glade
from pango import FontDescription
import pkg_resources
GLADE_RESOURCE = 'forgetmenot.glade'

def load_glade_xml():
    return pkg_resources.resource_string('forgetmenot', GLADE_RESOURCE)


class GuiQuiz(object):

    def __init__(self, quiz, font_size):
        self.flipped = False
        self.quiz = quiz
        xml = load_glade_xml()
        glade_xml = gtk.glade.xml_new_from_buffer(xml, len(xml))
        glade_xml.signal_autoconnect(self)
        (self.text_widget, self.flip_widget, self.skip_widget, self.next_widget) = map(glade_xml.get_widget, ('text',
                                                                                                              'flip',
                                                                                                              'skip',
                                                                                                              'next'))
        self.text_widget.modify_font(FontDescription('normal %d' % font_size))
        self.next_card(None)
        return

    def gtk_main_quit(self, *args):
        gtk.main_quit()

    def game_over(self):
        self.text_widget.set_text('game over')
        self.flip_widget.set_sensitive(False)
        self.skip_widget.set_sensitive(False)
        self.next_widget.set_sensitive(False)

    def on_flip_clicked(self, p):
        if not self.flipped:
            text = ('; ').join(self.question.answers)
        else:
            text = self.question.prompt
        self.text_widget.set_text(text)
        self.flipped = not self.flipped

    def next_card(self, remove):
        try:
            self.question = self.quiz.send(remove)
            self.flipped = False
            self.text_widget.set_text(self.question.prompt)
        except StopIteration:
            self.game_over()

    def on_skip_clicked(self, p):
        self.next_card(False)

    def on_next_clicked(self, p):
        self.next_card(True)


def run_quiz(quiz, font_size):
    GuiQuiz(quiz, font_size)
    gtk.main()