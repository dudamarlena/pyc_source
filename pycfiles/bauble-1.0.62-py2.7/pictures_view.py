# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/pictures_view.py
# Compiled at: 2016-10-03 09:39:22
import gtk, logging
logger = logging.getLogger(__name__)
import bauble.utils as utils

class PicturesView(gtk.HBox):
    """shows pictures corresponding to selection.

    at any time, no more than one PicturesView object will exist.

    when activated, the PicturesView object will be informed of changes
    to the selection and whatever the selection contains, the
    PicturesView object will ask each object in the selection to please
    return pictures, so that the PicturesView object can display them.

    if an object in the selection does not know of pictures (like it
    raises an exception because it does not define the 'pictures'
    property), the PicturesView object will silently accept the failure.

    """

    def __init__(self, parent=None, fake=False):
        logger.debug('entering PicturesView.__init__(parent=%s, fake=%s)' % (
         parent, fake))
        super(PicturesView, self).__init__()
        if fake:
            self.fake = True
            return
        self.fake = False
        import os
        from bauble import paths
        glade_file = os.path.join(paths.lib_dir(), 'pictures_view.glade')
        self.widgets = utils.BuilderWidgets(glade_file)
        self.widgets.remove_parent(self.widgets.scrolledwindow2)
        parent.add(self.widgets.scrolledwindow2)
        parent.show_all()
        self.widgets.scrolledwindow2.show()

    def set_selection(self, selection):
        logger.debug('PicturesView.set_selection(%s)' % selection)
        if self.fake:
            return
        self.box = self.widgets.pictures_box
        for k in self.box.children():
            k.destroy()

        for o in selection:
            try:
                pics = o.pictures
            except AttributeError:
                logger.debug('object %s does not know of pictures' % o)
                pics = []

            for p in pics:
                logger.debug('object %s has picture %s' % (o, p))
                expander = gtk.HBox()
                expander.add(p)
                self.box.pack_end(expander, expand=False, fill=False)
                self.box.reorder_child(expander, 0)
                expander.show_all()
                p.show()

        self.box.show_all()

    def add_picture(self, picture=None):
        """
        Add a new picture to the model.
        """
        expander = self.ContentBox(self, picture)
        self.box.pack_start(expander, expand=False, fill=False)
        expander.show_all()
        return expander


floating_window = None

def show_pictures_callback(selection):
    """activate a modal window showing plant pictures.

    the current selection defines what pictures should be shown. it
    makes sense for plant, accession and species.

    plants: show the pictures directly associated to them;

    accessions: show all pictures for the plants in the selected
    accessions.

    species: show the voucher.
    """
    floating_window.set_selection(selection)