# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/plugins/imex/iojson.py
# Compiled at: 2016-10-03 09:39:22
import os, gtk, logging
logger = logging.getLogger(__name__)
from bauble.i18n import _
import bauble.utils as utils, bauble.db as db
from bauble.plugins.plants import Familia, Genus, Species, VernacularName
from bauble.plugins.garden.plant import Plant, PlantNote
from bauble.plugins.garden.accession import Accession, AccessionNote
from bauble.plugins.garden.location import Location
import bauble.task, bauble.editor as editor, bauble.paths as paths, json, bauble.pluginmgr as pluginmgr
from bauble import pb_set_fraction

def serializedatetime(obj):
    """Default JSON serializer."""
    import calendar, datetime
    if isinstance(obj, (Familia, Genus, Species)):
        return str(obj)
    else:
        if isinstance(obj, datetime.datetime):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()
        millis = calendar.timegm(obj.timetuple()) * 1000
        try:
            millis += int(obj.microsecond / 1000)
        except AttributeError:
            pass

        return {'__class__': 'datetime', 'millis': millis}


class JSONExporter(editor.GenericEditorPresenter):
    """Export taxonomy and plants in JSON format.

    the Presenter ((M)VP)"""
    last_folder = ''
    widget_to_field_map = {'sbo_selection': 'selection_based_on', 
       'sbo_taxa': 'selection_based_on', 
       'sbo_accessions': 'selection_based_on', 
       'sbo_plants': 'selection_based_on', 
       'ei_referred': 'export_includes', 
       'ei_referring': 'export_includes', 
       'chkincludeprivate': 'include_private', 
       'filename': 'filename'}
    view_accept_buttons = [
     'sed-button-ok', 'sed-button-cancel']

    def __init__(self, view):
        self.selection_based_on = 'sbo_selection'
        self.export_includes = 'ei_referred'
        self.include_private = True
        self.filename = ''
        super(JSONExporter, self).__init__(model=self, view=view, refresh_view=True)

    def get_objects(self):
        """return the list of objects to be exported

        if "based_on" is "selection", return the top level selection only.

        if "based_on" is something else, return all that is needed to create
        a complete export.
        """
        if self.selection_based_on == 'sbo_selection':
            if self.include_private:
                logger.info('exporting selection overrides `include_private`')
            return self.view.get_selection()
        result = []
        if self.selection_based_on == 'sbo_plants':
            plant_query = self.session.query(Plant).order_by(Plant.code).join(Accession).order_by(Accession.code)
            if self.include_private is False:
                plant_query = plant_query.filter(Accession.private == False)
            plants = plant_query.all()
            plantnotes = self.session.query(PlantNote).filter(PlantNote.plant_id.in_([ j.id for j in plants ])).all()
            locations = self.session.query(Location).filter(Location.id.in_([ j.location_id for j in plants ])).all()
            accessions = self.session.query(Accession).filter(Accession.id.in_([ j.accession_id for j in plants ])).order_by(Accession.code).all()
            accessionnotes = self.session.query(AccessionNote).filter(AccessionNote.accession_id.in_([ j.id for j in accessions ])).all()
            result.extend(locations)
            result.extend(plants)
            result.extend(plantnotes)
        elif self.selection_based_on == 'sbo_accessions':
            accessions = self.session.query(Accession).order_by(Accession.code).all()
            if self.include_private is False:
                accessions = [ j for j in accessions if j.private is False ]
            accessionnotes = self.session.query(AccessionNote).filter(AccessionNote.accession_id.in_([ j.id for j in accessions ])).all()
        if self.selection_based_on == 'sbo_taxa':
            species = self.session.query(Species).order_by(Species.sp).all()
        else:
            result = accessions + accessionnotes + result
            species = self.session.query(Species).filter(Species.id.in_([ j.species_id for j in accessions ])).order_by(Species.sp).all()
        vernacular = self.session.query(VernacularName).filter(VernacularName.species_id.in_([ j.id for j in species ])).all()
        genera = self.session.query(Genus).filter(Genus.id.in_([ j.genus_id for j in species ])).order_by(Genus.genus).all()
        families = self.session.query(Familia).filter(Familia.id.in_([ j.family_id for j in genera ])).order_by(Familia.family).all()
        result = families + genera + species + vernacular + result
        return result

    def on_btnbrowse_clicked(self, button):
        self.view.run_file_chooser_dialog(_('Choose a file...'), None, action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(
         gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL), last_folder=self.last_folder, target='filename')
        filename = self.view.widget_get_value('filename')
        JSONExporter.last_folder, bn = os.path.split(filename)
        return

    def on_btnok_clicked(self, widget):
        self.run()

    def on_btncancel_clicked(self, widget):
        pass

    def run(self):
        """perform the export"""
        filename = self.filename
        if os.path.exists(filename) and not os.path.isfile(filename):
            raise ValueError('%s exists and is not a a regular file' % filename)
        objects = self.get_objects()
        if objects is None:
            s = db.Session()
            objects = s.query(Familia).all()
            objects.extend(s.query(Genus).all())
            objects.extend(s.query(Species).all())
            objects.extend(s.query(VernacularName).all())
            objects.extend(s.query(Accession).all())
            objects.extend(s.query(Plant).all())
            objects.extend(s.query(Location).all())
        count = len(objects)
        if count > 3000:
            msg = _('You are exporting %(nplants)s objects to JSON format.  Exporting this many objects may take several minutes.  \n\n<i>Would you like to continue?</i>') % {'nplants': count}
            if not self.view.run_yes_no_dialog(msg):
                return
        import codecs
        with codecs.open(filename, 'wb', 'utf-8') as (output):
            output.write('[')
            output.write((',\n ').join([ json.dumps(obj.as_dict(), default=serializedatetime, sort_keys=True) for obj in objects
                                       ]))
            output.write(']')
        return


class JSONImporter(editor.GenericEditorPresenter):
    """The import process will be queued as a bauble task. there is no callback
    informing whether it is successfully completed or not.

    the Presenter ((M)VP)
    Model (attributes container) is the Presenter itself.
    """
    widget_to_field_map = {'chk_create': 'create', 'chk_update': 'update', 
       'input_filename': 'filename'}
    last_folder = ''
    view_accept_buttons = [
     'sid-button-ok', 'sid-button-cancel']

    def __init__(self, view):
        self.filename = ''
        self.update = True
        self.create = True
        super(JSONImporter, self).__init__(model=self, view=view, refresh_view=True)
        self.__error = False
        self.__cancel = False
        self.__pause = False
        self.__error_exc = False

    def on_btnbrowse_clicked(self, button):
        self.view.run_file_chooser_dialog(_('Choose a file...'), None, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(
         gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL), last_folder=self.last_folder, target='input_filename')
        filename = self.view.widget_get_value('input_filename')
        JSONImporter.last_folder, bn = os.path.split(filename)
        return

    def on_btnok_clicked(self, widget):
        obj = json.load(open(self.filename))
        a = isinstance(obj, list) and obj or [obj]
        bauble.task.queue(self.run(a))

    def on_btncancel_clicked(self, widget):
        pass

    def run(self, objects):
        session = db.Session()
        n = len(objects)
        for i, obj in enumerate(objects):
            try:
                db.construct_from_dict(session, obj, self.create, self.update)
                session.commit()
            except Exception as e:
                session.rollback()
                logger.warning('could not import %s (%s: %s)' % (
                 obj, type(e).__name__, e.args))

            pb_set_fraction(float(i) / n)
            yield

        session.commit()


class JSONImportTool(pluginmgr.Tool):
    category = _('Import')
    label = _('JSON')

    @classmethod
    def start(cls):
        """
        Start the JSON importer.  This tool will also reinitialize the
        plugins after importing.
        """
        s = db.Session()
        filename = os.path.join(paths.lib_dir(), 'plugins', 'imex', 'select_export.glade')
        presenter = JSONImporter(view=editor.GenericEditorView(filename, root_widget_name='select_import_dialog'))
        presenter.start()
        presenter.cleanup()
        s.close()


class JSONExportTool(pluginmgr.Tool):
    category = _('Export')
    label = _('JSON')

    @classmethod
    def start(cls):
        s = db.Session()
        filename = os.path.join(paths.lib_dir(), 'plugins', 'imex', 'select_export.glade')
        presenter = JSONExporter(view=editor.GenericEditorView(filename, root_widget_name='select_export_dialog'))
        presenter.start()
        presenter.cleanup()
        s.close()