# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/gtk_batch_downloader.py
# Compiled at: 2014-02-04 18:18:19
# Size of source mod 2**32: 23078 bytes
"""

    Bat-man - YouTube video batch downloader
    Copyright (C) 2013 ElegantMonkey

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see [http://www.gnu.org/licenses/].

"""
import batman.batch_downloader as bd
from batman.threads import HelperThread, InserterThread
from batman import definitions
from batman.definitions import path_with
from batman.codec_interface import base_codec
from batman.codec_interface import utils as codec_utils
codec_utils.load_all_codecs()
from batman.options import Options
from gi.repository import Gtk, GObject, Gdk
if not definitions.WINDOWS:
    from gi.repository import Notify
import gettext, locale, os, gc
from multiprocessing import freeze_support
import logging, sys
from contextlib import contextmanager
GObject.threads_init()
APP = 'batman'
DIR = path_with('locale')
if definitions.WINDOWS:
    os.environ['LANG'] = locale.getdefaultlocale()[0]
try:
    locale.bindtextdomain(APP, DIR)
except:
    logging.warning("Couldn't bind text domain, translations are partially disabled")

gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
gettext.install(APP, DIR)

def prepare_builder_for_translation(builder):
    builder.set_translation_domain(APP)


class OptionsDialog(object):

    def __init__(self):
        self.builder = Gtk.Builder()
        prepare_builder_for_translation(self.builder)
        self.builder.add_from_file(path_with('glade', 'optionsDialog.glade'))
        self.dialog = self.builder.get_object('optionsDialog')
        self.videoqualityComboBox = self.builder.get_object('videoqualityComboBox')
        self.conversionqualityScale = self.builder.get_object('conversionqualityScale')
        self.videocodecCheckButton = self.builder.get_object('videocodecCheckButton')
        self.audiocodecCheckButton = self.builder.get_object('audiocodecCheckButton')
        self.videocodecComboBox = self.builder.get_object('videocodecComboBox')
        self.audiocodecComboBox = self.builder.get_object('audiocodecComboBox')
        qualityIndex = [
         240, 360, 480, 720, 1080].index(definitions.OPTIONS.quality)
        self.videoqualityComboBox.set_active(qualityIndex)
        self.conversionqualityScale.set_value(definitions.OPTIONS.VBRquality)
        self.videocodecCheckButton.set_active(definitions.OPTIONS.videoCodecEnabled)
        self.audiocodecCheckButton.set_active(definitions.OPTIONS.audioCodecEnabled)
        self.videoCodecEnabled = definitions.OPTIONS.videoCodecEnabled
        self.audioCodecEnabled = definitions.OPTIONS.audioCodecEnabled
        if self.videoCodecEnabled:
            self.videoCodec = definitions.OPTIONS.videoCodec
        if self.audioCodecEnabled:
            self.audioCodec = definitions.OPTIONS.audioCodec
        self.videocodecListStore = Gtk.ListStore(object, str)
        self.audiocodecListStore = Gtk.ListStore(object, str)
        self.builder.connect_signals(self)
        with self.handlers_blocked():
            self.set_combo_boxes_fields()
        renderer_text = Gtk.CellRendererText()
        with self.handlers_blocked():
            self.videocodecComboBox.set_model(self.videocodecListStore)
            self.videocodecComboBox.pack_start(renderer_text, True)
            self.videocodecComboBox.add_attribute(renderer_text, 'text', 1)
            self.audiocodecComboBox.set_model(self.audiocodecListStore)
            self.audiocodecComboBox.pack_start(renderer_text, True)
            self.audiocodecComboBox.add_attribute(renderer_text, 'text', 1)

    @contextmanager
    def handlers_blocked(self):
        self.videocodecComboBox.handler_block_by_func(self.onVideocodecComboBoxChanged)
        self.audiocodecComboBox.handler_block_by_func(self.onAudiocodecComboBoxChanged)
        try:
            yield
        finally:
            self.videocodecComboBox.handler_unblock_by_func(self.onVideocodecComboBoxChanged)
            self.audiocodecComboBox.handler_unblock_by_func(self.onAudiocodecComboBoxChanged)

    def set_combo_boxes_fields(self, set_index=True):
        self.videocodecListStore.clear()
        self.audiocodecListStore.clear()
        if self.videoCodecEnabled and self.audioCodecEnabled:
            index = 0
            for codec in base_codec.REGISTERED_VIDEO_CODECS:
                logging.info('Adding "{}" codec'.format(codec.PRETTY_NAME))
                self.videocodecListStore.append([codec, codec.PRETTY_NAME])
                if codec == self.videoCodec:
                    if set_index:
                        logging.info('Setting active video codec - {}'.format(index))
                        self.videocodecComboBox.set_active(index)
                index += 1

            index = 0
            for interactor in base_codec.REGISTERED_INTERACTIONS:
                if interactor[0][0] == self.videoCodec:
                    self.audiocodecListStore.append([interactor[0][1], interactor[0][1].PRETTY_NAME])
                    if interactor[0][1] == self.audioCodec:
                        if set_index:
                            logging.info('Setting active audio codec - {}'.format(index))
                            self.audiocodecComboBox.set_active(index)
                    index += 1
                    continue

        else:
            if self.videoCodecEnabled:
                for codec in base_codec.REGISTERED_VIDEO_CODECS:
                    logging.info('Adding "{}" codec'.format(codec.PRETTY_NAME))
                    self.videocodecListStore.append([codec, codec.PRETTY_NAME])

                index = base_codec.REGISTERED_VIDEO_CODECS.index(self.videoCodec)
                if set_index:
                    logging.info('Setting active video codec - {}'.format(index))
                    self.videocodecComboBox.set_active(index)
            elif self.audioCodecEnabled:
                for codec in base_codec.REGISTERED_AUDIO_CODECS:
                    logging.info('Adding "{}" codec'.format(codec.PRETTY_NAME))
                    self.audiocodecListStore.append([codec, codec.PRETTY_NAME])

                index = base_codec.REGISTERED_AUDIO_CODECS.index(self.audioCodec)
                if set_index:
                    logging.info('Setting active audio codec - {}'.format(index))
                    self.audiocodecComboBox.set_active(index)

    def onVideocodecToggled(self, *args):
        logging.info('Video codec toggled cb')
        self.videoCodecEnabled = self.videocodecCheckButton.get_active()
        self.videoCodec = base_codec.REGISTERED_VIDEO_CODECS[0]
        with self.handlers_blocked():
            self.set_combo_boxes_fields(set_index=True)

    def onAudiocodecToggled(self, *args):
        logging.info('Audio codec toggled cb')
        self.audioCodecEnabled = self.audiocodecCheckButton.get_active()
        self.audioCodec = base_codec.REGISTERED_AUDIO_CODECS[0]
        with self.handlers_blocked():
            self.set_combo_boxes_fields(set_index=True)

    def onVideocodecComboBoxChanged(self, *args):
        logging.info('Video codec combobox cb')
        treeiter = self.videocodecComboBox.get_active_iter()
        if treeiter != None:
            self.videoCodec = self.videocodecListStore.get_value(treeiter, 0)
            with self.handlers_blocked():
                self.set_combo_boxes_fields(set_index=True)
        return

    def onAudiocodecComboBoxChanged(self, *args):
        logging.info('Audio codec combobox cb')
        treeiter = self.audiocodecComboBox.get_active_iter()
        if treeiter != None:
            self.audioCodec = self.audiocodecListStore.get_value(treeiter, 0)
            with self.handlers_blocked():
                self.set_combo_boxes_fields(set_index=True)
        return

    def onClose(self, *args):
        quality = int(self.videoqualityComboBox.get_active_text()[0:-1])
        definitions.OPTIONS.quality = quality
        definitions.OPTIONS.VBRquality = int(self.conversionqualityScale.get_value())
        try:
            definitions.OPTIONS.audioCodec = self.audioCodec
        except (NameError, AttributeError):
            pass

        try:
            definitions.OPTIONS.audioCodecEnabled = self.audioCodecEnabled
        except (NameError, AttributeError):
            pass

        try:
            definitions.OPTIONS.videoCodec = self.videoCodec
        except (NameError, AttributeError):
            pass

        try:
            definitions.OPTIONS.videoCodecEnabled = self.videoCodecEnabled
        except (NameError, AttributeError):
            pass

        definitions.OPTIONS.write()
        definitions.OPTIONS.reload_codecs()


class AboutDialog(object):

    def __init__(self):
        self.builder = Gtk.Builder()
        prepare_builder_for_translation(self.builder)
        self.builder.add_from_file(path_with('glade', 'aboutDialog.glade'))
        self.dialog = self.builder.get_object('aboutDialog')
        self.dialog.set_version(definitions.VERSION)


class InsertLinksDialog(object):

    def __init__(self):
        self.builder = Gtk.Builder()
        prepare_builder_for_translation(self.builder)
        self.builder.add_from_file(path_with('glade', 'insertDialog.glade'))
        self.dialog = self.builder.get_object('insertDialog')
        self.builder.connect_signals(self)
        self.links = self.builder.get_object('links')

    def add_new_links(self):
        response = self.dialog.run()
        if response == 0:
            bounds = self.links.get_buffer().get_bounds()
            if len(bounds) != 0:
                start, end = bounds
                text = self.links.get_buffer().get_text(start, end, True)
                return text.split('\n')
            else:
                return
        else:
            return
        return

    def hide(self):
        self.dialog.hide()

    def onInsertClicked(self, *args):
        pass

    def onCancelClicked(self, *args):
        pass


class MainWindow(object):

    def __init__(self, marshaller):
        self.helperThread = HelperThread(marshaller)
        self.inserterThread = InserterThread(self.helperThread)
        self.inserterThread.message_callback = self.on_inserter_thread_callback
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.builder = Gtk.Builder()
        prepare_builder_for_translation(self.builder)
        self.builder.add_from_file(path_with('glade', 'mainWindow.glade'))
        self.window = self.builder.get_object('mainWindow')
        self.insertLinksDialog = InsertLinksDialog()
        self.aboutDialog = AboutDialog()
        self.optionsDialog = OptionsDialog()
        self.destination = definitions.OPTIONS.defaultFolder
        self.folderChoose = Gtk.FileChooserDialog(title=_('Choose destination folder'), action=Gtk.FileChooserAction.SELECT_FOLDER, buttons=(
         Gtk.STOCK_OK, Gtk.ResponseType.OK,
         Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        self.liststore = self.builder.get_object('videoListStore')
        self.marshaller = marshaller
        self.marshaller.on_video_start_download = lambda x, y: GObject.idle_add(lambda *args: self.refresh_marshaller(), None)
        self.marshaller.on_video_progress = lambda *args: GObject.idle_add(lambda *args: self.refresh_download_progress(), None)
        self.marshaller.on_video_start_encoding = lambda x, y, z: GObject.idle_add(self.on_video_start_encoding, None)
        self.marshaller.on_video_finish = lambda x, y: GObject.idle_add(self.on_video_finish, x, y)
        self.helperThread.start()
        self.inserterThread.start()
        self.treeview = self.builder.get_object('videoTreeView')
        cellRendererTitle = Gtk.CellRendererText()
        columnTitle = Gtk.TreeViewColumn(_('Title'), cellRendererTitle, text=1)
        cellRendererState = Gtk.CellRendererText()
        columnState = Gtk.TreeViewColumn(_('State'), cellRendererState, text=2)
        self.treeview.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.treeview.connect('drag-data-received', self.onTreeViewDragDataRecieved)
        self.treeview.drag_dest_add_text_targets()
        self.clear_list = self.builder.get_object('clearList')
        self.clear_list.set_sensitive(False)
        self.set_destination = self.builder.get_object('setDestination')
        self.treeview.append_column(columnTitle)
        self.treeview.append_column(columnState)
        self.popupTreeView = self.builder.get_object('popupTreeView')
        self.progressbar = self.builder.get_object('progressbar')
        self.download_progressbar = self.builder.get_object('downloadProgressbar')
        self.download_progressbar.set_show_text(True)
        self.download_progressbar.set_text('')
        self.general_data = self.builder.get_object('generalData')
        self.statusbar = self.builder.get_object('statusbar')
        ctx_id = self.statusbar.get_context_id('inserter')
        self.statusbar.push(ctx_id, _('Ready!'))
        self.itemFeedback = self.builder.get_object('imagemenuitemFeedback')
        self.refresh_marshaller()
        self.reset_destination()
        self.reset_data_label()
        self.builder.connect_signals(self)
        if not definitions.WINDOWS:
            self.notification = Notify.Notification.new('Bat-man', '', path_with('glade', 'batman-logo.png'))

    def on_inserter_thread_callback(self, inserter, element):
        return
        size = len(self.inserterThread.queue)
        ctx_id = self.statusbar.get_context_id('inserter')
        if element == None and size > 0:
            self.statusbar.push(ctx_id, _('Adding videos... ({}/{})').format(0, size))
        else:
            if element == None and size == 0:
                self.statusbar.push(ctx_id, _('Ready!'))
            else:
                i = self.inserterThread.queue.index(element)
                self.statusbar.push(ctx_id, _('Adding videos... ({}/{})').format(i, size))
        self.reset_data_label()
        return

    def on_video_start_encoding(self, *args):
        logging.info('on_video_start_encoding called')
        self.refresh_marshaller()
        self.refresh_download_progress()

    def on_video_finish(self, marshaller, video):
        logging.info('on_video_finish called')
        self.refresh_marshaller()
        self.refresh_download_progress()
        self.reset_data_label()
        if not definitions.WINDOWS:
            finished = len(self.marshaller.finished)
            total = len(self.marshaller.all)
            string = _('"{}" finished. ({}/{})').format(video.video.title, finished, total)
            self.notification.update('Bat-man', string, path_with('glade', 'batman-logo.png'))
            self.notification.show()

    def reset_data_label(self):
        self.general_data.set_text(_('- {} video(s)\n- Destination: {}').format(len(self.marshaller.all), self.destination))

    def reset_destination(self):
        for i in self.marshaller.all:
            i.set_outfolder(self.destination)

    def refresh_marshaller(self):
        progress = 0
        size = len(self.marshaller.all)
        self.liststore.clear()
        for video in self.marshaller.all:
            state = self.marshaller.find_state_of_video(video)
            if state == bd.DownloadAndEncodeMarshaller.NON_EXISTANT:
                progress += 0
                self.liststore.append([video, video.video.title, _('Non existant')])
            elif state == bd.DownloadAndEncodeMarshaller.PENDING:
                progress += 0
                self.liststore.append([video, video.video.title, _('Pending')])
            elif state == bd.DownloadAndEncodeMarshaller.DOWNLOADING:
                progress += 0.3333333333333333 / size
                self.liststore.append([video, video.video.title, _('Downloading')])
            elif state == bd.DownloadAndEncodeMarshaller.ENCODING:
                progress += 0.6666666666666666 / size
                self.liststore.append([video, video.video.title, _('Encoding')])
            elif state == bd.DownloadAndEncodeMarshaller.FINISHED:
                progress += 1 / size
                self.liststore.append([video, video.video.title, _('Finished')])
            elif state == bd.DownloadAndEncodeMarshaller.NOT_FOUND:
                progress += 0
                self.liststore.append([video, video.video.title, _('Not found')])
                continue

        self.progressbar.set_fraction(progress)
        if len(self.marshaller.finished) > 0:
            self.clear_list.set_sensitive(True)

    def refresh_download_progress(self):
        size = len(self.marshaller.downloading)
        progress = 0.0
        speed = 0
        for video in self.marshaller.downloading:
            if video.download_progress != None:
                progress += video.download_progress[2] / size
                speed += video.download_progress[3]
                continue

        self.download_progressbar.set_fraction(progress)
        if size != 0:
            self.download_progressbar.set_text('{:.2%} @ {:.0f} KBps'.format(progress, speed / size))
        else:
            self.download_progressbar.set_text('')
        return

    def onItemInsertActivate(self, *args):
        links = self.insertLinksDialog.add_new_links()
        self.insertLinksDialog.hide()
        if links != None:
            for l in links:
                if l.strip() != '':
                    self.inserterThread.add_video_to_download(l, self.destination, definitions.OPTIONS.quality, definitions.OPTIONS.VBRquality)
                    continue

            self.refresh_marshaller()
            self.reset_data_label()
        return

    def onCloseCalled(self, *args):
        Gtk.main_quit()
        self.inserterThread.quit()
        self.helperThread.quit()
        sys.exit(0)

    def onItemAboutActivate(self, *args):
        self.aboutDialog.dialog.run()
        self.aboutDialog.dialog.hide()

    def onItemFeedbackActivate(self, *args):
        feedback.open_email_sender_for_feedback()

    def onItemOptionsActivate(self, *args):
        self.optionsDialog.dialog.run()
        self.optionsDialog.dialog.hide()
        self.marshaller.reload_codecs()

    def onSetDestinationClicked(self, *args):
        response = self.folderChoose.run()
        self.folderChoose.hide()
        if response == Gtk.ResponseType.OK:
            self.destination = self.folderChoose.get_filename()
            definitions.OPTIONS.defaultFolder = self.destination
            definitions.OPTIONS.write()
            self.reset_destination()
            self.reset_data_label()

    def onClearListClicked(self, *args):
        for video in self.marshaller.finished:
            try:
                self.marshaller.finished.remove(video)
                self.marshaller.all.remove(video)
            except Exception as e:
                logging.debug(e.strerror)

        self.refresh_marshaller()
        self.reset_data_label()
        self.clear_list.set_sensitive(False)

    def onTreeViewClicked(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 3:
                self.popupTreeView.popup(None, None, None, None, event.button, event.time)
        return

    def onTreeViewPaste(self, *args):
        content = self.clipboard.wait_for_text()
        if content != None:
            for line in content.split('\n'):
                self.inserterThread.add_video_to_download(line, self.destination, definitions.OPTIONS.quality, definitions.OPTIONS.VBRquality)

            self.refresh_marshaller()
            self.reset_data_label()
        return

    def onTreeViewDragDataRecieved(self, widget, drag_context, x, y, data, info, time):
        links = data.get_text().split('\n')
        for line in links:
            self.inserterThread.add_video_to_download(line, self.destination, definitions.OPTIONS.quality, definitions.OPTIONS.VBRquality)

        self.refresh_marshaller()
        self.reset_data_label()


def main():
    if not definitions.WINDOWS:
        Notify.init('Bat-man')
    freeze_support()
    marshaller = bd.DownloadAndEncodeMarshaller()
    w = MainWindow(marshaller)
    w.window.show_all()
    Gtk.main()
    del marshaller
    gc.collect()


if __name__ == '__main__':
    main()