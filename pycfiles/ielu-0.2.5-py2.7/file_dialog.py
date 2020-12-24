# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ielu/file_dialog.py
# Compiled at: 2016-03-02 14:09:44
""" Defines functions and classes used to create pop-up file dialogs for
    opening and saving files.
"""
from os import R_OK, W_OK, access, mkdir
from os.path import basename, dirname, exists, getatime, getctime, getmtime, getsize, isdir, isfile, join, split, splitext
from time import localtime, strftime
from traits.api import Bool, Button, CList, Event, File, HasPrivateTraits, Instance, Int, Interface, Property, Str, cached_property, implements
from traits.trait_base import user_name_for
from traitsui.api import CodeEditor, FileEditor, HGroup, HSplit, Handler, HistoryEditor, ImageEditor, InstanceEditor, Item, UIInfo, VGroup, VSplit, View, spring
from traitsui.ui_traits import AView
from pyface.api import ImageResource
from pyface.timer.api import do_later
from traitsui.helper import commatize
from traitsui.toolkit import toolkit
MAX_SIZE = 16777216

class IFileDialogModel(Interface):
    """ Defines a model extension to a file dialog.
    """
    file_name = File


class IFileDialogView(Interface):
    """ Defines a visual extension to a file dialog.
    """
    view = AView
    is_fixed = Bool


class IFileDialogExtension(IFileDialogModel, IFileDialogView):
    """ Defines a (convenience) union of the IFileDialogModel and
        IFileDialogView interfaces.
    """
    pass


class MFileDialogModel(HasPrivateTraits):
    implements(IFileDialogModel)
    file_name = File


class MFileDialogView(HasPrivateTraits):
    """ Defines a visual extension to a file dialog.
    """
    view = AView
    is_fixed = Bool(False)


default_view = MFileDialogView()

class MFileDialogExtension(MFileDialogModel, MFileDialogView):
    """ Defines a (convenience) union of the MFileDialogModel and
        MFileDialogView mix-in classes.
    """
    pass


class FileInfo(MFileDialogModel):
    """ Defines a file dialog extension that display various file information.
    """
    size = Property(depends_on='file_name')
    atime = Property(depends_on='file_name')
    mtime = Property(depends_on='file_name')
    ctime = Property(depends_on='file_name')
    view = View(VGroup(Item('size', label='File size', style='readonly'), Item('atime', label='Last access', style='readonly'), Item('mtime', label='Last modified', style='readonly'), Item('ctime', label='Created at', style='readonly'), label='File Information', show_border=True))

    @cached_property
    def _get_size(self):
        try:
            return commatize(getsize(self.file_name)) + ' bytes'
        except:
            return ''

    @cached_property
    def _get_atime(self):
        try:
            return strftime('%m/%d/%Y %I:%M:%S %p', localtime(getatime(self.file_name)))
        except:
            return ''

    @cached_property
    def _get_mtime(self):
        try:
            return strftime('%m/%d/%Y %I:%M:%S %p', localtime(getmtime(self.file_name)))
        except:
            return ''

    @cached_property
    def _get_ctime(self):
        try:
            return strftime('%m/%d/%Y %I:%M:%S %p', localtime(getctime(self.file_name)))
        except:
            return ''


class TextInfo(MFileDialogModel):
    """ Defines a file dialog extension that displays a file's contents as text.
    """
    text = Property(depends_on='file_name')
    view = View(Item('text', style='readonly', show_label=False, editor=CodeEditor()))

    @cached_property
    def _get_text(self):
        try:
            if getsize(self.file_name) > MAX_SIZE:
                return 'File too big...'
            fh = file(self.file_name, 'rb')
            data = fh.read()
            fh.close()
        except:
            return ''

        if data.find('\x00') >= 0 or data.find(b'\xff') >= 0:
            return 'File contains binary data...'
        return data


class ImageInfo(MFileDialogModel):
    """ Defines a file dialog extension that display an image file's dimensions
        and content.
    """
    image = Property(depends_on='file_name')
    width = Property(depends_on='image')
    height = Property(depends_on='image')
    view = View(VGroup(VGroup(Item('width', style='readonly'), Item('height', style='readonly'), label='Image Dimensions', show_border=True), VGroup(Item('image', show_label=False, editor=ImageEditor()), label='Image', show_border=True, springy=True)))

    @cached_property
    def _get_image(self):
        path, name = split(self.file_name)
        if splitext(name)[1] in ('.png', '.gif', '.jpg', '.jpeg'):
            image = ImageResource(name, search_path=[path])
        else:
            image = ImageResource('unknown')
        self._cur_image = image.create_image()
        return image

    @cached_property
    def _get_width(self):
        try:
            return str(toolkit().image_size(self._cur_image)[0]) + ' pixels'
        except:
            return '---'

    @cached_property
    def _get_height(self):
        try:
            return str(toolkit().image_size(self._cur_image)[1]) + ' pixels'
        except:
            return '---'


class CreateDirHandler(Handler):
    """ Controller for the 'create new directory' popup.
    """
    dir_name = Str
    message = Str
    ok = Button('OK')
    cancel = Button('Cancel')
    view = View(VGroup(HGroup(Item('handler.dir_name', label='Name'), Item('handler.ok', show_label=False, enabled_when="handler.dir_name.strip() != ''"), Item('handler.cancel', show_label=False)), HGroup(Item('handler.message', show_label=False, style='readonly', springy=True), show_border=True)), kind='popup')

    def handler_ok_changed(self, info):
        """ Handles the user clicking the OK button.
        """
        dir = info.object.file_name
        if not isdir(dir):
            dir = dirname(dir)
        path = join(dir, self.dir_name)
        try:
            mkdir(path)
            info.object.reload = True
            info.object.file_name = path
            info.ui.dispose(True)
        except:
            self.message = "Could not create the '%s' directory" % self.dir_name

    def handler_cancel_changed(self, info):
        """ Handles the user clicking the Cancel button.
        """
        info.ui.dispose(False)


class FileExistsHandler(Handler):
    """ Controller for the 'file already exists' popup.
    """
    message = Str
    ok = Button('OK')
    cancel = Button('Cancel')
    view = View(VGroup(HGroup(Item('handler.message', editor=ImageEditor(image='@icons:dialog-warning')), Item('handler.message', style='readonly'), show_labels=False), HGroup(spring, Item('handler.ok'), Item('handler.cancel'), show_labels=False)), kind='popup')

    def handler_ok_changed(self, info):
        """ Handles the user clicking the OK button.
        """
        parent = info.ui.parent
        info.ui.dispose(True)
        parent.dispose(True)

    def handler_cancel_changed(self, info):
        """ Handles the user clicking the Cancel button.
        """
        info.ui.dispose(False)


class OpenFileDialog(Handler):
    """ Defines the model and handler for the open file dialog.
    """
    file_name = File
    filter = CList(Str)
    entries = Int(10)
    title = Str('Open File')
    id = Str('traitsui.file_dialog.OpenFileDialog')
    extensions = CList(IFileDialogModel)
    info = Instance(UIInfo)
    reload = Event
    dclick = Event
    extension__ = Instance(IFileDialogModel)
    is_save_file = Bool(False)
    is_save_in_directory = Bool(False)
    is_valid_file = Property(depends_on='file_name')
    can_create_dir = Property(depends_on='file_name')
    ok = Button('OK')
    cancel = Button('Cancel')
    create = Button(image='@icons:folder-new', style='toolbar')

    def init_info(self, info):
        """ Handles the UIInfo object being initialized during view start-up.
        """
        self.info = info

    def _get_is_valid_file(self):
        if self.is_save_in_directory:
            return isdir(self.file_name) or not exists(self.file_name)
        if self.is_save_file:
            return isfile(self.file_name) or not exists(self.file_name)
        return isfile(self.file_name)

    def _get_can_create_dir(self):
        dir = dirname(self.file_name)
        return isdir(dir) and access(dir, R_OK | W_OK)

    def object_ok_changed(self, info):
        """ Handles the user clicking the OK button.
        """
        if self.is_save_file and exists(self.file_name):
            do_later(self._file_already_exists)
        else:
            info.ui.dispose(True)

    def object_cancel_changed(self, info):
        """ Handles the user clicking the Cancel button.
        """
        info.ui.dispose(False)

    def object_create_changed(self, info):
        """ Handles the user clicking the create directory button.
        """
        if not isdir(self.file_name):
            self.file_name = dirname(self.file_name)
        CreateDirHandler().edit_traits(context=self, parent=info.create.control)

    def _dclick_changed(self):
        """ Handles the user double-clicking a file name in the file tree view.
        """
        if self.is_valid_file:
            self.object_ok_changed(self.info)

    def open_file_view(self):
        """ Returns the file dialog view to use.
        """
        item = Item('file_name', id='file_tree', style='custom', show_label=False, width=0.5, editor=FileEditor(filter=self.filter, allow_dir=True, reload_name='reload', dclick_name='dclick'))
        width = height = 0.2
        if len(self.extensions) > 0:
            width *= 2.0
            klass = HGroup
            items = []
            for i, extension in enumerate(self.extensions):
                name = 'extension_%d' % i
                setattr(self, name, extension)
                extension_view = extension
                self.sync_trait('file_name', extension, mutual=True)
                if not extension.has_traits_interface(IFileDialogView):
                    extension_view = default_view
                view = extension.trait_view(extension_view.view)
                if not extension_view.is_fixed:
                    klass = HSplit
                items.append(Item(name, label=user_name_for(extension.__class__.__name__), show_label=False, style='custom', width=0.5, height=0.5, dock='horizontal', resizable=True, editor=InstanceEditor(view=view, id=name)))

            item = klass(item, VSplit(id='splitter2', springy=True, *items), id='splitter')
        return View(VGroup(VGroup(item), HGroup(Item('create', id='create', show_label=False, style='custom', defined_when='is_save_file', enabled_when='can_create_dir', tooltip='Create a new directory'), Item('file_name', id='history', editor=HistoryEditor(entries=self.entries, auto_set=True), springy=True), Item('ok', id='ok', show_label=False, enabled_when='is_valid_file'), Item('cancel', show_label=False))), title=self.title, id=self.id, kind='livemodal', width=width, height=height, close_result=False, resizable=True)

    def _file_already_exists(self):
        """ Handles prompting the user when the selected file already exists,
            and the dialog is a 'save file' dialog.
        """
        FileExistsHandler(message="The file '%s' already exists.\nDo you wish to overwrite it?" % basename(self.file_name)).edit_traits(context=self, parent=self.info.ok.control).set(parent=self.info.ui)


def open_file(**traits):
    """ Returns a file name to open or an empty string if the user cancels the
        operation.
    """
    fd = OpenFileDialog(**traits)
    if fd.edit_traits(view='open_file_view').result:
        return fd.file_name
    return ''


def save_file(**traits):
    """ Returns a file name to save to or an empty string if the user cancels
        the operation. In the case where the file selected already exists, the
        user will be prompted if they want to overwrite the file before the
        selected file name is returned.
    """
    traits.setdefault('title', 'Save File')
    traits['is_save_file'] = True
    fd = OpenFileDialog(**traits)
    if fd.edit_traits(view='open_file_view').result:
        return fd.file_name
    return ''


def save_in_directory(**traits):
    """ Returns a directory to save to or an empty string if the user cancels
        the operation. 
    """
    traits.setdefault('title', 'Select label directory')
    traits['is_save_in_directory'] = True
    fd = OpenFileDialog(**traits)
    if fd.edit_traits(view='open_file_view').result:
        return fd.file_name
    return ''


if __name__ == '__main__':
    print save_file(extensions=[FileInfo(), TextInfo(), ImageInfo()], filter='Python file (*.py)|*.py')