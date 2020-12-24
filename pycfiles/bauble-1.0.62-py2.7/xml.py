# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/plugins/imex/xml.py
# Compiled at: 2016-10-03 09:39:22
import os, traceback, logging
logger = logging.getLogger(__name__)
import gtk.gdk, bauble, bauble.db as db, bauble.utils as utils, bauble.pluginmgr as pluginmgr, bauble.task
from bauble.i18n import _

def ElementFactory(parent, name, **kwargs):
    try:
        text = kwargs.pop('text')
    except KeyError:
        text = None

    el = etree.SubElement(parent, name, **kwargs)
    try:
        if text is not None:
            el.text = unicode(text, 'utf8')
    except (AssertionError, TypeError):
        el.text = unicode(str(text), 'utf8')

    return el


class XMLExporter:

    def __init__(self):
        pass

    def start(self, path=None):
        d = gtk.Dialog('Ghini - XML Exporter', bauble.gui.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (
         gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
         gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        box = gtk.VBox(spacing=20)
        d.vbox.pack_start(box, padding=10)
        file_chooser = gtk.FileChooserButton(_('Select a directory'))
        file_chooser.set_select_multiple(False)
        file_chooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        box.pack_start(file_chooser)
        check = gtk.CheckButton(_('Save all data in one file'))
        check.set_active(True)
        box.pack_start(check)
        d.connect('response', self.on_dialog_response, file_chooser.get_filename(), check.get_active())
        d.show_all()
        d.run()
        d.hide()

    def on_dialog_response(self, dialog, response, filename, one_file):
        logger.debug('on_dialog_response(%s, %s)' % (filename, one_file))
        if response == gtk.RESPONSE_ACCEPT:
            self.__export_task(filename, one_file)
        dialog.destroy()

    def __export_task(self, path, one_file=True):
        if not one_file:
            tableset_el = etree.Element('tableset')
        for table_name, table in db.metadata.tables.iteritems():
            if one_file:
                tableset_el = etree.Element('tableset')
            logger.info('exporting %s...' % table_name)
            table_el = ElementFactory(tableset_el, 'table', attrib={'name': table_name})
            results = table.select().execute().fetchall()
            columns = table.c.keys()
            try:
                for row in results:
                    row_el = ElementFactory(table_el, 'row')
                    for col in columns:
                        ElementFactory(row_el, 'column', attrib={'name': col}, text=row[col])

            except ValueError as e:
                utils.message_details_dialog(utils.xml_safe(e), traceback.format_exc(), gtk.MESSAGE_ERROR)
                return

            if one_file:
                tree = etree.ElementTree(tableset_el)
                filename = os.path.join(path, '%s.xml' % table_name)
                tree.write(filename, encoding='utf8', xml_declaration=True)

        if not one_file:
            tree = etree.ElementTree(tableset_el)
            filename = os.path.join(path, 'bauble.xml')
            tree.write(filename, encoding='utf8', xml_declaration=True)


class XMLExportCommandHandler(pluginmgr.CommandHandler):
    command = 'exxml'

    def __call__(self, cmd, arg):
        logger.debug('XMLExportCommandHandler(%s)' % arg)
        exporter = XMLExporter()
        logger.debug('starting')
        exporter.start(arg)
        logger.debug('started')


class XMLExportTool(pluginmgr.Tool):
    category = _('Export')
    label = _('XML')

    @classmethod
    def start(cls):
        c = XMLExporter()
        c.start()


class XMLImexPlugin(pluginmgr.Plugin):
    tools = [
     XMLExportTool]
    commands = [XMLExportCommandHandler]


try:
    import lxml.etree as etree
except ImportError:
    utils.message_dialog('The <i>lxml</i> package is required for the XML Import/Exporter plugin')