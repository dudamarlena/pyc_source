# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gsteditor/pad.py
# Compiled at: 2009-05-03 07:55:20
import goocanvas, logging, gst

class Pad(goocanvas.Group):
    """Represents gstreamer pad"""
    minSize = 3
    radius = 4

    def __init__(self, pad):
        goocanvas.Group.__init__(self)
        self.widget = goocanvas.Ellipse(radius_x=self.radius, radius_y=self.radius, fill_color='blue', line_width=2, stroke_color='black')
        self.add_child(self.widget)
        self.model = pad
        self.link = None
        self.logger = logging.getLogger(self.model.get_name())
        self.model.set_data('widget', self)
        self.widget.props.tooltip = self.model.get_name()
        self.model.connect('linked', self.onLinked)
        self.model.connect('unlinked', self.onUnlinked)
        return

    def onLinked(self, pad1, pad2):
        self.logger.debug('linked. pad1=' + str(pad1) + ' pad2=' + str(pad2))
        assert pad1 == self.model
        peer = pad2.get_data('widget')
        if peer:
            if peer.link:
                self.link = peer.link
            else:
                peer.link = self.link = self.get_parent().get_parent().makeLink(self, peer)
        else:
            ghostPad = pad2.get_parent()
            if ghostPad.__class__ == gst.GhostPad:
                if not ghostPad.get_parent():
                    self.logger.warning('no parent for pad ' + str(ghostPad) + '- delaying signal handler')
                    ghostPad.set_data('link-handler', lambda : self.onLinked(pad1, pad2))
                else:
                    peer = Pad(pad2)
                    ghostPad.get_data('widget').add_child(peer)
                    self.link = peer.get_parent().get_parent().makeLink(self, peer)
                    self.link.props.line_dash = goocanvas.LineDash([3.0])
            else:
                self.logger.warning('no widget for pad ' + str(pad2) + '- delaying signal handler')
                pad2.set_data('link-handler', lambda : self.onLinked(pad1, pad2))

    def onUnlinked(self, pad1, pad2):
        logging.debug('unlinked. pad1=' + str(pad1) + ' pad2=' + str(pad2))
        assert pad1 == self.model
        assert pad2.get_parent().__class__ == gst.GhostPad or pad2.get_data('widget').link == self.link or not pad2.get_data('widget').link
        self.link.get_parent().destroyLink(self.link)
        self.link = None
        return

    def tryLink(self, peer):
        if self.model.can_link(peer.model):
            if peer.model.get_direction() == gst.PAD_SRC:
                peer.model.link(self.model)
            else:
                self.model.link(peer.model)
            self.onLinked(self.model, peer.model)
            peer.onLinked(peer.model, self.model)

    def updateLink(self):
        if self.model.is_linked():
            self.onLinked(self.model, self.model.get_peer())

    def setPosition(self, x, y):
        self.set_simple_transform(x, y, 1, 0)