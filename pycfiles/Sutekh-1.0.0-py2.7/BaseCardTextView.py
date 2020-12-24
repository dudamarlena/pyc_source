# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/BaseCardTextView.py
# Compiled at: 2019-12-11 16:37:48
"""Widget for displaying the card text for the given card."""
import logging, gtk, pango
from .MessageBus import MessageBus, CARD_TEXT_MSG

class BaseCardTextBuffer(gtk.TextBuffer):
    """Base class for buffer object which holds the actual card text.
       """

    def __init__(self):
        super(BaseCardTextBuffer, self).__init__(None)
        self._oIconTabs = pango.TabArray(1, True)
        self._oIconTabs.set_tab(0, pango.TAB_LEFT, 15)
        self.create_tag('label', underline=pango.UNDERLINE_SINGLE)
        self.create_tag('card_name', weight=pango.WEIGHT_BOLD)
        self._oIter = None
        return

    def tag_text(self, *aArgs, **kwargs):
        """Inset the text (possibly with tags) at the current position"""
        self.insert_with_tags_by_name(self._oIter, *aArgs, **kwargs)

    def add_tag(self, sTag):
        """Add a simple tag"""
        self.create_tag(sTag, style=pango.STYLE_ITALIC)
        self.create_mark(sTag, self.get_start_iter(), True)

    def add_list_tag(self, sTag):
        """Add a tag with the list style indents"""
        self.create_tag(sTag, style=pango.STYLE_ITALIC, left_margin=15, tabs=self._oIconTabs)
        self.create_mark(sTag, self.get_start_iter(), True)

    def labelled_value(self, sLabel, sValue, sTag, oIcon=None):
        """Add a single value to the buffer."""
        self.tag_text('\n')
        self.tag_text(sLabel, 'label')
        self.tag_text(': ')
        if oIcon:
            self.insert_pixbuf(self._oIter, oIcon)
            self.insert(self._oIter, ' ')
        self.tag_text(sValue, sTag)
        self.move_mark(self.get_mark(sTag), self._oIter)

    def labelled_list(self, sLabel, aValues, sTag, dIcons=None):
        """Add a list of values to the Buffer"""

        def _insert_line(sText, sTag, oPixbuf):
            """Insert a line, prefixed by oPixbuf."""
            if oPixbuf:
                self.tag_text('\n', sTag)
                oMark1 = self.create_mark(None, self._oIter, True)
                self.tag_text('\t%s' % sText, sTag)
                oMarkEnd = self.create_mark(None, self._oIter, True)
                self.insert_pixbuf(self.get_iter_at_mark(oMark1), oPixbuf)
                self._oIter = self.get_iter_at_mark(oMarkEnd)
                self.delete_mark(oMark1)
                self.delete_mark(oMarkEnd)
            else:
                self.tag_text('\n*\t%s' % sText, sTag)
            return

        self.tag_text('\n')
        self.tag_text(sLabel, 'label')
        self.tag_text(':')
        for sValue in aValues:
            if dIcons:
                if sValue in dIcons and dIcons[sValue]:
                    _insert_line(sValue, sTag, dIcons[sValue])
                elif sValue.lower() in dIcons and dIcons[sValue.lower()]:
                    _insert_line(sValue, sTag, dIcons[sValue.lower()])
                else:
                    _insert_line(sValue, sTag, None)
            else:
                _insert_line(sValue, sTag, None)

        self.move_mark(self.get_mark(sTag), self._oIter)
        return

    def labelled_compact_list(self, sLabel, aValues, sTag):
        """More compact list for clans, etc."""
        self.labelled_value(sLabel, (' / ').join(aValues), sTag)

    def labelled_exp_list(self, sLabel, dValues, sTag):
        """Special case for expansion labels"""
        aValues = []
        for sExp in sorted(dValues):
            aRarities = list(set(dValues[sExp]))
            sValue = '%s (%s)' % (sExp, (', ').join(sorted(aRarities)))
            aValues.append(sValue)

        self.labelled_list(sLabel, aValues, sTag)

    def reset_iter(self):
        """Reset the iterator to point at the start of the buffer."""
        self._oIter = self.get_iter_at_offset(0)

    def get_cur_iter(self):
        """Get the current text iter position"""
        return self._oIter

    def set_cur_iter(self, oNewIter):
        """Set the current text iter to the given position"""
        self._oIter = oNewIter

    def set_cur_iter_to_mark(self, sMarkName):
        """Set the iter to the position of the given mark"""
        oMark = self.get_mark(sMarkName)
        if oMark:
            self._oIter = self.get_iter_at_mark(oMark)


class BaseCardTextView(gtk.TextView):
    """Base class for TextView widget which holds the TextBuffer."""

    def __init__(self, oBuffer, oIconManager, oMainWindow):
        super(BaseCardTextView, self).__init__()
        self._oBuf = oBuffer
        self._oMainWindow = oMainWindow
        self._oNameOffset = None
        self._oLastCard = None
        self.set_buffer(self._oBuf)
        self.set_editable(False)
        self.set_cursor_visible(False)
        self.set_wrap_mode(gtk.WRAP_WORD)
        self._oIconManager = oIconManager
        oContext = self.get_pango_context()
        logging.info('Pango Language : %s', oContext.get_language())
        logging.info('Pango Font Description : %s', oContext.get_font_description())
        return

    text_buffer = property(fget=lambda self: self._oBuf, doc='Return reference to text buffer')

    def update_to_new_db(self):
        """Handle any database changes as required"""
        pass

    def set_card_text(self, oPhysCard):
        """Add the text for oCard to the TextView."""
        self._oLastCard = oPhysCard
        self._reload_card()

    def _reload_card(self):
        if self._oLastCard:
            self.clear_text()
            self.print_card_to_buffer(self._oLastCard.abstractCard)
            MessageBus.publish(CARD_TEXT_MSG, 'post_set_text', self._oLastCard)

    def add_button_to_text(self, oButton, sPrefix='\n'):
        """Adds a button to the text view."""
        if oButton in self.get_children():
            return
        oPos = self._oBuf.get_iter_at_line_offset(0, self._oNameOffset)
        self._oBuf.insert(oPos, sPrefix)
        oAnchor = self._oBuf.create_child_anchor(oPos)
        self.add_child_at_anchor(oButton, oAnchor)
        oButton.show()

    def clear_text(self):
        """Clear the text buffer."""
        for oChild in self.get_children():
            self.remove(oChild)

        oStart, oEnd = self._oBuf.get_bounds()
        self._oBuf.delete(oStart, oEnd)

    def print_card_to_buffer(self, oCard):
        """Format the text for the card and add it to the buffer."""
        self._oBuf.reset_iter()
        self._oBuf.tag_text(oCard.name, 'card_name')
        self._oNameOffset = self._oBuf.get_end_iter().get_offset()