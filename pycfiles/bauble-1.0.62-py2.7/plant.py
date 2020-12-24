# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/plugins/garden/plant.py
# Compiled at: 2016-10-03 09:39:22
"""
Defines the plant table and handled editing plants
"""
import os, traceback
from random import random
import logging
logger = logging.getLogger(__name__)
import gtk
from bauble.i18n import _
from sqlalchemy import and_, func
from sqlalchemy import ForeignKey, Column, Unicode, Integer, Boolean, UnicodeText, UniqueConstraint
from sqlalchemy.orm import relation, backref, object_mapper, validates
from sqlalchemy.orm.session import object_session
from sqlalchemy.exc import DBAPIError
import bauble.db as db
from bauble.error import CheckConditionError
from bauble.editor import GenericEditorView, GenericEditorPresenter, GenericModelViewPresenterEditor, NotesPresenter, PicturesPresenter
import bauble.meta as meta, bauble.paths as paths
from bauble.plugins.plants.species_model import Species
from bauble.plugins.garden.location import Location, LocationEditor
from bauble.plugins.garden.propagation import PlantPropagation
import bauble.prefs as prefs
from bauble.search import SearchStrategy
import bauble.btypes as types, bauble.utils as utils
from bauble.view import InfoBox, InfoExpander, PropertiesExpander, select_in_search_results, Action
import bauble.view as view
plant_delimiter_key = 'plant_delimiter'
default_plant_delimiter = '.'

def edit_callback(plants):
    e = PlantEditor(model=plants[0])
    return e.start() is not None


def branch_callback(plants):
    if plants[0].quantity <= 1:
        msg = _('Not enough plants to branch.  A plant should have at least a quantity of 2 before it can be branched')
        utils.message_dialog(msg, gtk.MESSAGE_WARNING)
        return
    else:
        e = PlantEditor(model=plants[0], branch_mode=True)
        return e.start() is not None


def remove_callback(plants):
    s = (', ').join([ str(p) for p in plants ])
    msg = _('Are you sure you want to remove the following plants?\n\n%s') % utils.xml_safe(s)
    if not utils.yes_no_dialog(msg):
        return
    session = db.Session()
    for plant in plants:
        obj = session.query(Plant).get(plant.id)
        session.delete(obj)

    try:
        try:
            session.commit()
        except Exception as e:
            msg = _('Could not delete.\n\n%s') % utils.xml_safe(e)
            utils.message_details_dialog(msg, traceback.format_exc(), type=gtk.MESSAGE_ERROR)

    finally:
        session.close()

    return True


edit_action = Action('plant_edit', _('_Edit'), callback=edit_callback, accelerator='<ctrl>e', multiselect=True)
branch_action = Action('plant_branch', _('_Branch'), callback=branch_callback, accelerator='<ctrl>b')
remove_action = Action('plant_remove', _('_Delete'), callback=remove_callback, accelerator='<ctrl>Delete', multiselect=True)
plant_context_menu = [
 edit_action, branch_action, remove_action]

def get_next_code(acc):
    """
    Return the next available plant code for an accession.

    This function should be specific to the institution.

    If there is an error getting the next code the None is returned.
    """
    session = db.Session()
    from bauble.plugins.garden import Accession
    codes = session.query(Plant.code).join(Accession).filter(Accession.id == acc.id).all()
    next = 1
    if codes:
        try:
            next = max([ int(code[0]) for code in codes ]) + 1
        except Exception as e:
            logger.debug(e)
            return

    return utils.utf8(next)


def is_code_unique(plant, code):
    """
    Return True/False if the code is a unique Plant code for accession.

    This method will also take range values for code that can be passed
    to utils.range_builder()
    """
    codes = map(utils.utf8, utils.range_builder(code))
    if len(codes) == 1:
        codes = [
         utils.utf8(code)]
    session = db.Session()
    from bauble.plugins.garden import Accession
    count = session.query(Plant).join('accession').filter(and_(Accession.id == plant.accession.id, Plant.code.in_(codes))).count()
    session.close()
    return count == 0


class PlantSearch(SearchStrategy):

    def __init__(self):
        super(PlantSearch, self).__init__()

    def search(self, text, session):
        """returns a result if the text looks like a quoted plant code

        special search strategy, can't be obtained in MapperSearch
        """
        if text[0] == text[(-1)] and text[0] in ('"', "'"):
            text = text[1:-1]
        else:
            logger.debug('text is not quoted, should strategy apply?')
        delimiter = Plant.get_delimiter()
        if delimiter not in text:
            logger.debug("delimiter not found, can't split the code")
            return []
        acc_code, plant_code = text.rsplit(delimiter, 1)
        logger.debug('ac: %s, pl: %s' % (acc_code, plant_code))
        try:
            from bauble.plugins.garden import Accession
            query = session.query(Plant).filter(Plant.code == unicode(plant_code)).join(Accession).filter(utils.ilike(Accession.code, '%%%s' % unicode(acc_code)))
            return query.all()
        except Exception as e:
            logger.debug('%s %s' % (e.__class__.name, e))
            return []


class PlantNote(db.Base, db.Serializable):
    __tablename__ = 'plant_note'
    __mapper_args__ = {'order_by': 'plant_note.date'}
    date = Column(types.Date, default=func.now())
    user = Column(Unicode(64))
    category = Column(Unicode(32))
    note = Column(UnicodeText, nullable=False)
    plant_id = Column(Integer, ForeignKey('plant.id'), nullable=False)
    plant = relation('Plant', uselist=False, backref=backref('notes', cascade='all, delete-orphan'))

    def as_dict(self):
        result = db.Serializable.as_dict(self)
        result['plant'] = self.plant.accession.code + Plant.get_delimiter() + self.plant.code
        return result

    @classmethod
    def retrieve(cls, session, keys):
        q = session.query(cls)
        if 'plant' in keys:
            acc_code, plant_code = keys['plant'].rsplit(Plant.get_delimiter(), 1)
            q = q.join(Plant).filter(Plant.code == unicode(plant_code)).join(Accession).filter(Accession.code == unicode(acc_code))
        if 'date' in keys:
            q = q.filter(cls.date == keys['date'])
        if 'category' in keys:
            q = q.filter(cls.category == keys['category'])
        try:
            return q.one()
        except:
            return

        return

    @classmethod
    def compute_serializable_fields(cls, session, keys):
        """plant is given as text, should be object"""
        result = {'plant': None}
        acc_code, plant_code = keys['plant'].rsplit(Plant.get_delimiter(), 1)
        logger.debug('acc-plant: %s-%s' % (acc_code, plant_code))
        q = session.query(Plant).filter(Plant.code == unicode(plant_code)).join(Accession).filter(Accession.code == unicode(acc_code))
        plant = q.one()
        result['plant'] = plant
        return result


change_reasons = {'DEAD': _('Dead'), 
   'DISC': _('Discarded'), 
   'DISW': _('Discarded, weedy'), 
   'LOST': _('Lost, whereabouts unknown'), 
   'STOL': _('Stolen'), 
   'WINK': _('Winter kill'), 
   'ERRO': _('Error correction'), 
   'DIST': _('Distributed elsewhere'), 
   'DELE': _('Deleted, yr. dead. unknown'), 
   'ASS#': _('Transferred to another acc.no.'), 
   'FOGS': _('Given to FOGs to sell'), 
   'PLOP': _('Area transf. to Plant Ops.'), 
   'BA40': _('Given to Back 40 (FOGs)'), 
   'TOTM': _('Transfered to Totem Field'), 
   'SUMK': _('Summer Kill'), 
   'DNGM': _('Did not germinate'), 
   'DISN': _('Discarded seedling in nursery'), 
   'GIVE': _('Given away (specify person)'), 
   'OTHR': _('Other'), 
   None: ''}

class PlantChange(db.Base):
    """
    """
    __tablename__ = 'plant_change'
    __mapper_args__ = {'order_by': 'plant_change.date'}
    plant_id = Column(Integer, ForeignKey('plant.id'), nullable=False)
    parent_plant_id = Column(Integer, ForeignKey('plant.id'))
    from_location_id = Column(Integer, ForeignKey('location.id'))
    to_location_id = Column(Integer, ForeignKey('location.id'))
    person = Column(Unicode(64))
    quantity = Column(Integer, autoincrement=False, nullable=False)
    note_id = Column(Integer, ForeignKey('plant_note.id'))
    reason = Column(types.Enum(values=change_reasons.keys(), translations=change_reasons))
    date = Column(types.DateTime, default=func.now())
    plant = relation('Plant', uselist=False, primaryjoin='PlantChange.plant_id == Plant.id', backref=backref('changes', cascade='all, delete-orphan'))
    parent_plant = relation('Plant', uselist=False, primaryjoin='PlantChange.parent_plant_id == Plant.id', backref=backref('branches', cascade='all, delete-orphan'))
    from_location = relation('Location', primaryjoin='PlantChange.from_location_id == Location.id')
    to_location = relation('Location', primaryjoin='PlantChange.to_location_id == Location.id')


condition_values = {'Excellent': _('Excellent'), 
   'Good': _('Good'), 
   'Fair': _('Fair'), 
   'Poor': _('Poor'), 
   'Questionable': _('Questionable'), 
   'Indistinguishable': _('Indistinguishable Mass'), 
   'UnableToLocate': _('Unable to Locate'), 
   'Dead': _('Dead'), 
   None: ''}
flowering_values = {'Immature': _('Immature'), 
   'Flowering': _('Flowering'), 
   'Old': _('Old Flowers'), 
   None: ''}
fruiting_values = {'Unripe': _('Unripe'), 
   'Ripe': _('Ripe'), 
   None: ''}
sex_values = {'Female': _('Female'), 
   'Male': _('Male'), 
   'Both': ''}

class PlantStatus(db.Base):
    """
    date: date checked
    status: status of plant
    comment: comments on check up
    checked_by: person who did the check
    """
    __tablename__ = 'plant_status'
    date = Column(types.Date, default=func.now())
    condition = Column(types.Enum(values=condition_values.keys(), translations=condition_values))
    comment = Column(UnicodeText)
    checked_by = Column(Unicode(64))
    flowering_status = Column(types.Enum(values=flowering_values.keys(), translations=flowering_values))
    fruiting_status = Column(types.Enum(values=fruiting_values.keys(), translations=fruiting_values))
    autumn_color_pct = Column(Integer, autoincrement=False)
    leaf_drop_pct = Column(Integer, autoincrement=False)
    leaf_emergence_pct = Column(Integer, autoincrement=False)
    sex = Column(types.Enum(values=sex_values.keys(), translations=sex_values))


acc_type_values = {'Plant': _('Plant'), 'Seed': _('Seed/Spore'), 
   'Vegetative': _('Vegetative Part'), 
   'Tissue': _('Tissue Culture'), 
   'Other': _('Other'), 
   None: ''}

class Plant(db.Base, db.Serializable, db.DefiningPictures, db.WithNotes):
    """
    :Table name: plant

    :Columns:
        *code*: :class:`sqlalchemy.types.Unicode`
            The plant code

        *acc_type*: :class:`bauble.types.Enum`
            The accession type

            Possible values:
                * Plant: Whole plant

                * Seed/Spore: Seed or Spore

                * Vegetative Part: Vegetative Part

                * Tissue Culture: Tissue culture

                * Other: Other, probably see notes for more information

                * None: no information, unknown

        *accession_id*: :class:`sqlalchemy.types.Integer`
            Required.

        *location_id*: :class:`sqlalchemy.types.Integer`
            Required.

    :Properties:
        *accession*:
            The accession for this plant.
        *location*:
            The location for this plant.
        *notes*:
            The notes for this plant.

    :Constraints:
        The combination of code and accession_id must be unique.
    """
    __tablename__ = 'plant'
    __table_args__ = (UniqueConstraint('code', 'accession_id'), {})
    __mapper_args__ = {'order_by': ['plant.accession_id', 'plant.code']}
    code = Column(Unicode(6), nullable=False)

    @validates('code')
    def validate_stripping(self, key, value):
        if value is None:
            return
        else:
            return value.strip()

    acc_type = Column(types.Enum(values=acc_type_values.keys(), translations=acc_type_values), default=None)
    memorial = Column(Boolean, default=False)
    quantity = Column(Integer, autoincrement=False, nullable=False)
    accession_id = Column(Integer, ForeignKey('accession.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    propagations = relation('Propagation', cascade='all, delete-orphan', single_parent=True, secondary=PlantPropagation.__table__, backref=backref('plant', uselist=False))
    _delimiter = None

    def search_view_markup_pair(self):
        """provide the two lines describing object for SearchView row.
        """
        import inspect
        logger.debug('entering search_view_markup_pair %s, %s' % (
         self, str(inspect.stack()[1])))
        sp_str = self.accession.species_str(markup=True)
        dead_color = '#9900ff'
        if self.quantity <= 0:
            dead_markup = '<span foreground="%s">%s</span>' % (
             dead_color, utils.xml_safe(self))
            return (
             dead_markup, sp_str)
        else:
            located_counted = '%s <span foreground="#555555" size="small" weight="light">- %s alive in %s</span>' % (
             utils.xml_safe(self), self.quantity, utils.xml_safe(self.location))
            return (located_counted, sp_str)

    @classmethod
    def get_delimiter(cls, refresh=False):
        """
        Get the plant delimiter from the BaubleMeta table.

        The delimiter is cached the first time it is retrieved.  To refresh
        the delimiter from the database call with refresh=True.

        """
        if cls._delimiter is None or refresh:
            cls._delimiter = meta.get_default(plant_delimiter_key, default_plant_delimiter).value
        return cls._delimiter

    def _get_delimiter(self):
        return Plant.get_delimiter()

    delimiter = property(lambda self: self._get_delimiter())

    def __str__(self):
        return '%s%s%s' % (self.accession, self.delimiter, self.code)

    def duplicate(self, code=None, session=None):
        """
        Return a Plant that is a duplicate of this Plant with attached
        notes, changes and propagations.
        """
        plant = Plant()
        if not session:
            session = object_session(self)
            if session:
                session.add(plant)
        ignore = ('id', 'changes', 'notes', 'propagations')
        properties = filter(lambda p: p.key not in ignore, object_mapper(self).iterate_properties)
        for prop in properties:
            setattr(plant, prop.key, getattr(self, prop.key))

        plant.code = code
        for note in self.notes:
            new_note = PlantNote()
            for prop in object_mapper(note).iterate_properties:
                setattr(new_note, prop.key, getattr(note, prop.key))

            new_note.id = None
            new_note.plant = plant

        for change in self.changes:
            new_change = PlantChange()
            for prop in object_mapper(change).iterate_properties:
                setattr(new_change, prop.key, getattr(change, prop.key))

            new_change.id = None
            new_change.plant = plant

        for propagation in self.propagations:
            new_propagation = PlantPropagation()
            for prop in object_mapper(propagation).iterate_properties:
                setattr(new_propagation, prop.key, getattr(propagation, prop.key))

            new_propagation.id = None
            new_propagation.plant = plant

        return plant

    def markup(self):
        return '%s%s%s (%s)' % (self.accession, self.delimiter, self.code,
         self.accession.species_str(markup=True))

    def as_dict(self):
        result = db.Serializable.as_dict(self)
        result['accession'] = self.accession.code
        result['location'] = self.location.code
        return result

    @classmethod
    def compute_serializable_fields(cls, session, keys):
        result = {'accession': None, 'location': None}
        acc_keys = {}
        acc_keys.update(keys)
        acc_keys['code'] = keys['accession']
        accession = Accession.retrieve_or_create(session, acc_keys, create='taxon' in acc_keys and 'rank' in acc_keys)
        loc_keys = {}
        loc_keys.update(keys)
        if 'location' in keys:
            loc_keys['code'] = keys['location']
            location = Location.retrieve_or_create(session, loc_keys)
        else:
            location = None
        result['accession'] = accession
        result['location'] = location
        return result

    @classmethod
    def retrieve(cls, session, keys):
        try:
            return session.query(cls).filter(cls.code == keys['code']).join(Accession).filter(Accession.code == keys['accession']).one()
        except:
            return

        return

    def top_level_count(self):
        sd = self.accession.source and self.accession.source.source_detail
        return {(1, 'Plantings'): 1, (2, 'Accessions'): set([self.accession.id]), 
           (3, 'Species'): set([self.accession.species.id]), 
           (4, 'Genera'): set([self.accession.species.genus.id]), 
           (5, 'Families'): set([self.accession.species.genus.family.id]), 
           (6, 'Living plants'): self.quantity, 
           (7, 'Locations'): set([self.location.id]), 
           (8, 'Sources'): set(sd and [sd.id] or [])}


from bauble.plugins.garden.accession import Accession

class PlantEditorView(GenericEditorView):
    _tooltips = {'plant_code_entry': _('The plant code must be a unique code for the accession.  You may also use ranges like 1,2,7 or 1-3 to create multiple plants.'), 
       'plant_acc_entry': _('The accession must be selected from the list of completions.  To add an accession use the Accession editor.'), 
       'plant_loc_comboentry': _('The location of the plant in your collection.'), 
       'plant_acc_type_combo': _('The type of the plant material.\n\nPossible values: %s') % (', ').join(acc_type_values.values()), 
       'plant_loc_add_button': _('Create a new location.'), 
       'plant_loc_edit_button': _('Edit the selected location.'), 
       'prop_add_button': _('Create a new propagation record for this plant.'), 
       'pad_cancel_button': _('Cancel your changes.'), 
       'pad_ok_button': _('Save your changes.'), 
       'pad_next_button': _('Save your changes changes and add another plant.')}

    def __init__(self, parent=None):
        glade_file = os.path.join(paths.lib_dir(), 'plugins', 'garden', 'plant_editor.glade')
        super(PlantEditorView, self).__init__(glade_file, parent=parent)
        self.widgets.pad_ok_button.set_sensitive(False)
        self.widgets.pad_next_button.set_sensitive(False)

        def acc_cell_data_func(column, renderer, model, treeiter, data=None):
            v = model[treeiter][0]
            renderer.set_property('text', '%s (%s)' % (str(v), str(v.species)))

        self.attach_completion('plant_acc_entry', acc_cell_data_func, minimum_key_length=2)
        self.init_translatable_combo('plant_acc_type_combo', acc_type_values)
        self.init_translatable_combo('reason_combo', change_reasons)
        utils.setup_date_button(self, 'plant_date_entry', 'plant_date_button')
        self.widgets.plant_notebook.set_current_page(0)
        return

    def get_window(self):
        return self.widgets.plant_editor_dialog

    def save_state(self):
        pass

    def restore_state(self):
        pass


class PlantEditorPresenter(GenericEditorPresenter):
    widget_to_field_map = {'plant_code_entry': 'code', 'plant_acc_entry': 'accession', 
       'plant_loc_comboentry': 'location', 
       'plant_acc_type_combo': 'acc_type', 
       'plant_memorial_check': 'memorial', 
       'plant_quantity_entry': 'quantity'}
    PROBLEM_DUPLICATE_PLANT_CODE = str(random())

    def __init__(self, model, view):
        """
        :param model: should be an instance of Plant class
        :param view: should be an instance of PlantEditorView
        """
        super(PlantEditorPresenter, self).__init__(model, view)
        self.session = object_session(model)
        self._original_accession_id = self.model.accession_id
        self._original_code = self.model.code
        self._original_quantity = None
        if model not in self.session.new:
            self._original_quantity = self.model.quantity
        self._dirty = False
        if self.model.id is None and self.model.acc_type is None:
            self.model.acc_type = 'Plant'
        notes_parent = self.view.widgets.notes_parent_box
        notes_parent.foreach(notes_parent.remove)
        self.notes_presenter = NotesPresenter(self, 'notes', notes_parent)
        pictures_parent = self.view.widgets.pictures_parent_box
        pictures_parent.foreach(pictures_parent.remove)
        self.pictures_presenter = PicturesPresenter(self, 'notes', pictures_parent)
        from bauble.plugins.garden.propagation import PropagationTabPresenter
        self.prop_presenter = PropagationTabPresenter(self, self.model, self.view, self.session)
        if self.model.accession and not self.model.code:
            code = get_next_code(self.model.accession)
            if code:
                self.set_model_attr('code', code)
        self.refresh_view()
        self.change = PlantChange()
        self.session.add(self.change)
        self.change.plant = self.model
        self.change.from_location = self.model.location
        self.change.quantity = self.model.quantity

        def on_reason_changed(combo):
            it = combo.get_active_iter()
            self.change.reason = combo.get_model()[it][0]

        sensitive = False
        if self.model not in self.session.new:
            self.view.connect(self.view.widgets.reason_combo, 'changed', on_reason_changed)
            sensitive = True
        self.view.widgets.reason_combo.props.sensitive = sensitive
        self.view.widgets.reason_label.props.sensitive = sensitive
        self.view.connect('plant_date_entry', 'changed', self.on_date_entry_changed)

        def on_location_select(location):
            self.set_model_attr('location', location)
            if self.change.quantity is None:
                self.change.quantity = self.model.quantity
            return

        from bauble.plugins.garden import init_location_comboentry
        init_location_comboentry(self, self.view.widgets.plant_loc_comboentry, on_location_select)

        def acc_get_completions(text):
            query = self.session.query(Accession)
            return query.filter(Accession.code.like(unicode('%s%%' % text))).order_by(Accession.code)

        def on_select(value):
            self.set_model_attr('accession', value)
            self.view.widgets.acc_species_label.set_markup('')
            if value is not None:
                sp_str = self.model.accession.species.str(markup=True)
                self.view.widgets.acc_species_label.set_markup(sp_str)
                self.view.widgets.plant_code_entry.emit('changed')
            return

        self.assign_completions_handler('plant_acc_entry', acc_get_completions, on_select=on_select)
        if self.model.accession:
            sp_str = self.model.accession.species.str(markup=True)
        else:
            sp_str = ''
        self.view.widgets.acc_species_label.set_markup(sp_str)
        self.view.connect('plant_code_entry', 'changed', self.on_plant_code_entry_changed)
        self.assign_simple_handler('plant_acc_type_combo', 'acc_type')
        self.assign_simple_handler('plant_memorial_check', 'memorial')
        self.view.connect('plant_quantity_entry', 'changed', self.on_quantity_changed)
        self.view.connect('plant_loc_add_button', 'clicked', self.on_loc_button_clicked, 'add')
        self.view.connect('plant_loc_edit_button', 'clicked', self.on_loc_button_clicked, 'edit')
        return

    def dirty(self):
        return self.pictures_presenter.dirty() or self.notes_presenter.dirty() or self.prop_presenter.dirty() or self._dirty

    def on_date_entry_changed(self, entry, *args):
        self.change.date = entry.props.text

    def on_quantity_changed(self, entry, *args):
        value = entry.props.text
        try:
            value = abs(int(value))
        except ValueError as e:
            logger.debug(e)
            value = None

        self.set_model_attr('quantity', value)
        if value is None:
            self.refresh_sensitivity()
            return
        else:
            if self._original_quantity:
                self.change.quantity = abs(self._original_quantity - self.model.quantity)
            else:
                self.change.quantity = self.model.quantity
            self.refresh_sensitivity()
            return

    def on_plant_code_entry_changed(self, entry, *args):
        """
        Validates the accession number and the plant code from the editors.
        """
        text = utils.utf8(entry.get_text())
        if text == '':
            self.set_model_attr('code', None)
        else:
            self.set_model_attr('code', utils.utf8(text))
        if not self.model.accession:
            self.remove_problem(self.PROBLEM_DUPLICATE_PLANT_CODE, entry)
            self.refresh_sensitivity()
            return
        else:
            if self.model.code is not None and not is_code_unique(self.model, self.model.code) and not (self._original_accession_id == self.model.accession.id and self.model.code == self._original_code):
                self.add_problem(self.PROBLEM_DUPLICATE_PLANT_CODE, entry)
            else:
                self.remove_problem(self.PROBLEM_DUPLICATE_PLANT_CODE, entry)
                entry.modify_bg(gtk.STATE_NORMAL, None)
                entry.modify_base(gtk.STATE_NORMAL, None)
                entry.queue_draw()
            self.refresh_sensitivity()
            return

    def refresh_sensitivity(self):
        logger.debug('refresh_sensitivity()')
        logger.debug((self.model.accession is not None,
         self.model.code is not None,
         self.model.location is not None,
         self.model.quantity is not None,
         self.dirty(),
         len(self.problems) == 0))
        logger.debug(self.problems)
        sensitive = self.model.accession is not None and self.model.code is not None and self.model.location is not None and self.model.quantity is not None and self.dirty() and len(self.problems) == 0
        self.view.widgets.pad_ok_button.set_sensitive(sensitive)
        self.view.widgets.pad_next_button.set_sensitive(sensitive)
        return

    def set_model_attr(self, field, value, validator=None):
        logger.debug('set_model_attr(%s, %s)' % (field, value))
        super(PlantEditorPresenter, self).set_model_attr(field, value, validator)
        self._dirty = True
        self.refresh_sensitivity()

    def on_loc_button_clicked(self, button, cmd=None):
        location = self.model.location
        combo = self.view.widgets.plant_loc_comboentry
        if cmd is 'edit' and location:
            LocationEditor(location, parent=self.view.get_window()).start()
            self.session.refresh(location)
            self.view.widget_set_value(combo, location)
        else:
            editor = LocationEditor(parent=self.view.get_window())
            if editor.start():
                location = self.model.location = editor.presenter.model
                self.session.add(location)
                self.remove_problem(None, combo)
                self.view.widget_set_value(combo, location)
                self.set_model_attr('location', location)
        return

    def refresh_view(self):
        for widget, field in self.widget_to_field_map.iteritems():
            value = getattr(self.model, field)
            self.view.widget_set_value(widget, value)
            logger.debug('%s: %s = %s' % (widget, field, value))

        self.view.widget_set_value('plant_acc_type_combo', acc_type_values[self.model.acc_type], index=1)
        self.view.widgets.plant_memorial_check.set_inconsistent(False)
        self.view.widgets.plant_memorial_check.set_active(self.model.memorial is True)
        self.refresh_sensitivity()

    def cleanup(self):
        super(PlantEditorPresenter, self).cleanup()
        msg_box_parent = self.view.widgets.message_box_parent
        map(msg_box_parent.remove, msg_box_parent.get_children())
        self.view.widgets.plant_acc_entry.props.editable = True

    def start(self):
        return self.view.start()


class PlantEditor(GenericModelViewPresenterEditor):
    RESPONSE_NEXT = 22
    ok_responses = (RESPONSE_NEXT,)

    def __init__(self, model=None, parent=None, branch_mode=False):
        """
        :param model: Plant instance or None
        :param parent: None
        :param branch_mode:
        """
        if branch_mode:
            if model is None:
                raise CheckConditionError(_('branch_mode requires a model'))
            elif object_session(model) and model in object_session(model).new:
                raise CheckConditionError(_('cannot branch a new plant'))
        if model is None:
            model = Plant()
        self.branched_plant = None
        if branch_mode:
            self.branched_plant = model
            model = self.branched_plant.duplicate(code=None)
        super(PlantEditor, self).__init__(model, parent)
        if self.branched_plant:
            self.branched_plant = self.session.merge(self.branched_plant)
        import bauble
        if not parent and bauble.gui:
            parent = bauble.gui.window
        self.parent = parent
        self._committed = []
        view = PlantEditorView(parent=self.parent)
        self.presenter = PlantEditorPresenter(self.model, view)
        self.attach_response(view.get_window(), gtk.RESPONSE_OK, 'Return', gtk.gdk.CONTROL_MASK)
        self.attach_response(view.get_window(), self.RESPONSE_NEXT, 'n', gtk.gdk.CONTROL_MASK)
        if self.model.accession is None:
            view.widgets.plant_acc_entry.grab_focus()
        else:
            view.widgets.plant_code_entry.grab_focus()
        return

    def commit_changes(self):
        """
        """
        codes = utils.range_builder(self.model.code)
        if len(codes) <= 1 or self.model not in self.session.new and not self.branched_plant:
            change = self.presenter.change
            if self.branched_plant:
                self.branched_plant.quantity -= self.model.quantity
                change.parent_plant = self.branched_plant
                if not change.to_location:
                    change.to_location = self.model.location
            elif change.quantity is None or change.quantity == self.model.quantity and change.from_location == self.model.location and change.quantity == self.presenter._original_quantity:
                utils.delete_or_expunge(change)
                self.model.change = None
            elif self.model.location != change.from_location:
                change.to_location = self.model.location
            elif self.model.quantity > self.presenter._original_quantity and not change.to_location:
                change.to_location = self.model.location
                change.from_location = None
            else:
                change.quantity = -change.quantity
            super(PlantEditor, self).commit_changes()
            self._committed.append(self.model)
            return
        else:
            plants = []
            mapper = object_mapper(self.model)
            for code in codes:
                new_plant = Plant()
                self.session.add(new_plant)
                ignore = ('changes', 'notes', 'propagations')
                for prop in mapper.iterate_properties:
                    if prop.key not in ignore:
                        setattr(new_plant, prop.key, getattr(self.model, prop.key))

                new_plant.code = utils.utf8(code)
                new_plant.id = None
                new_plant._created = None
                new_plant._last_updated = None
                plants.append(new_plant)
                for note in self.model.notes:
                    new_note = PlantNote()
                    for prop in object_mapper(note).iterate_properties:
                        setattr(new_note, prop.key, getattr(note, prop.key))

                    new_note.plant = new_plant

            try:
                map(self.session.expunge, self.model.notes)
                self.session.expunge(self.model)
                super(PlantEditor, self).commit_changes()
            except:
                self.session.add(self.model)
                raise

            self._committed.extend(plants)
            return

    def handle_response(self, response):
        not_ok_msg = _('Are you sure you want to lose your changes?')
        if response == gtk.RESPONSE_OK or response in self.ok_responses:
            try:
                if self.presenter.dirty():
                    self.commit_changes()
            except DBAPIError as e:
                exc = traceback.format_exc()
                logger.debug(exc)
                msg = _('Error committing changes.\n\n%s') % e.orig
                utils.message_details_dialog(msg, str(e), gtk.MESSAGE_ERROR)
                self.session.rollback()
                return False
            except Exception as e:
                msg = _('Unknown error when committing changes. See the details for more information.\n\n%s') % utils.xml_safe(e)
                logger.debug(traceback.format_exc())
                utils.message_details_dialog(msg, traceback.format_exc(), gtk.MESSAGE_ERROR)
                self.session.rollback()
                return False

        else:
            if self.presenter.dirty() and utils.yes_no_dialog(not_ok_msg) or not self.presenter.dirty():
                self.session.rollback()
                return True
            else:
                return False

        more_committed = None
        if response == self.RESPONSE_NEXT:
            self.presenter.cleanup()
            e = PlantEditor(Plant(accession=self.model.accession), parent=self.parent)
            more_committed = e.start()
        if more_committed is not None:
            self._committed = [
             self._committed]
            if isinstance(more_committed, list):
                self._committed.extend(more_committed)
            else:
                self._committed.append(more_committed)
        return True

    def start(self):
        from bauble.plugins.garden.accession import Accession
        sub_editor = None
        if self.session.query(Accession).count() == 0:
            msg = 'You must first add or import at least one Accession into the database before you can add plants.\n\nWould you like to open the Accession editor?'
            if utils.yes_no_dialog(msg):
                self.presenter.cleanup()
                from bauble.plugins.garden.accession import AccessionEditor
                sub_editor = AccessionEditor()
                self._commited = sub_editor.start()
        if self.session.query(Location).count() == 0:
            msg = 'You must first add or import at least one Location into the database before you can add plants.\n\nWould you like to open the Location editor?'
            if utils.yes_no_dialog(msg):
                self.presenter.cleanup()
                sub_editor = LocationEditor()
                self._commited = sub_editor.start()
        if self.branched_plant:
            self.presenter.view.get_window().props.title += utils.utf8(' - %s' % _('Branch Mode'))
            message_box_parent = self.presenter.view.widgets.message_box_parent
            map(message_box_parent.remove, message_box_parent.get_children())
            msg = _('Branching from %(plant_code)s.  The quantity will be subtracted from %(plant_code)s') % {'plant_code': str(self.branched_plant)}
            box = self.presenter.view.add_message_box(utils.MESSAGE_BOX_INFO)
            box.message = msg
            box.show_all()
            self.presenter.view.widgets.plant_acc_entry.props.editable = False
        if not sub_editor:
            while True:
                response = self.presenter.start()
                self.presenter.view.save_state()
                if self.handle_response(response):
                    break

        self.session.close()
        self.presenter.cleanup()
        return self._committed


class GeneralPlantExpander(InfoExpander):
    """
    general expander for the PlantInfoBox
    """

    def __init__(self, widgets):
        """
        """
        super(GeneralPlantExpander, self).__init__(_('General'), widgets)
        general_box = self.widgets.general_box
        self.widgets.remove_parent(general_box)
        self.vbox.pack_start(general_box)
        self.current_obj = None

        def on_acc_code_clicked(*args):
            select_in_search_results(self.current_obj.accession)

        utils.make_label_clickable(self.widgets.acc_code_data, on_acc_code_clicked)

        def on_species_clicked(*args):
            select_in_search_results(self.current_obj.accession.species)

        utils.make_label_clickable(self.widgets.name_data, on_species_clicked)

        def on_location_clicked(*args):
            select_in_search_results(self.current_obj.location)

        utils.make_label_clickable(self.widgets.location_data, on_location_clicked)
        return

    def update(self, row):
        """
        """
        self.current_obj = row
        acc_code = str(row.accession)
        plant_code = str(row)
        head, tail = plant_code[:len(acc_code)], plant_code[len(acc_code):]
        self.widget_set_value('acc_code_data', '<big>%s</big>' % utils.xml_safe(unicode(head)), markup=True)
        self.widget_set_value('plant_code_data', '<big>%s</big>' % utils.xml_safe(unicode(tail)), markup=True)
        self.widget_set_value('name_data', row.accession.species_str(markup=True), markup=True)
        self.widget_set_value('location_data', str(row.location))
        self.widget_set_value('quantity_data', row.quantity)
        status_str = _('Alive')
        if row.quantity <= 0:
            status_str = _('Dead')
        self.widget_set_value('status_data', status_str, False)
        self.widget_set_value('type_data', acc_type_values[row.acc_type], False)
        image_size = gtk.ICON_SIZE_MENU
        stock = gtk.STOCK_NO
        if row.memorial:
            stock = gtk.STOCK_YES
        self.widgets.memorial_image.set_from_stock(stock, image_size)


class ChangesExpander(InfoExpander):
    """
    ChangesExpander
    """

    def __init__(self, widgets):
        """
        """
        super(ChangesExpander, self).__init__(_('Changes'), widgets)
        self.vbox.props.spacing = 5
        self.table = gtk.Table()
        self.vbox.pack_start(self.table, expand=False, fill=False)
        self.table.props.row_spacing = 3
        self.table.props.column_spacing = 5

    def update(self, row):
        """
        """
        self.table.foreach(self.table.remove)
        if not row.changes:
            return
        else:
            nrows = len(row.changes)
            self.table.resize(nrows, 2)
            date_format = prefs.prefs[prefs.date_format_pref]
            current_row = 0

            def _cmp(x, y):
                """
            Sort by change.date and then change._created.  If they are
            equal then removals sort before transfers.
            """
                if x.date < y.date:
                    return -1
                else:
                    if x.date > y.date:
                        return 1
                    if x.date == y.date and x._created < y._created:
                        return -1
                    if x.date == y.date and x._created > y._created:
                        return 1
                    if x.quantity < 0:
                        return -1
                    return 1

            for change in sorted(row.changes, cmp=_cmp, reverse=True):
                date = change.date.strftime(date_format)
                label = gtk.Label('%s:' % date)
                label.set_alignment(0, 0)
                self.table.attach(label, 0, 1, current_row, current_row + 1, xoptions=gtk.FILL)
                if change.to_location and change.from_location:
                    s = '%(quantity)s Transferred from %(from_loc)s to %(to)s' % dict(quantity=change.quantity, from_loc=change.from_location, to=change.to_location)
                elif change.quantity < 0:
                    s = '%(quantity)s Removed from %(location)s' % dict(quantity=-change.quantity, location=change.from_location)
                elif change.quantity > 0:
                    s = '%(quantity)s Added to %(location)s' % dict(quantity=change.quantity, location=change.to_location)
                else:
                    s = '%s: %s -> %s' % (change.quantity, change.from_location,
                     change.to_location)
                if change.reason is not None:
                    s += '\n%s' % change_reasons[change.reason]
                label = gtk.Label(s)
                label.set_alignment(0, 0.5)
                self.table.attach(label, 1, 2, current_row, current_row + 1, xoptions=gtk.FILL)
                current_row += 1
                if change.parent_plant:
                    s = _('<i>Branched from %(plant)s</i>') % dict(plant=utils.xml_safe(change.parent_plant))
                    label = gtk.Label()
                    label.set_alignment(0, 0.5)
                    label.set_markup(s)
                    eb = gtk.EventBox()
                    eb.add(label)
                    self.table.attach(eb, 1, 2, current_row, current_row + 1, xoptions=gtk.FILL)

                    def on_clicked(widget, event, parent):
                        select_in_search_results(parent)

                    utils.make_label_clickable(label, on_clicked, change.parent_plant)
                    current_row += 1

            self.vbox.show_all()
            return


class PropagationExpander(InfoExpander):
    """
    Propagation Expander
    """

    def __init__(self, widgets):
        """
        """
        super(PropagationExpander, self).__init__(_('Propagations'), widgets)
        self.vbox.set_spacing(3)

    def update(self, row):
        sensitive = True
        if not row.propagations:
            sensitive = False
        self.props.expanded = sensitive
        self.props.sensitive = sensitive
        self.vbox.foreach(self.vbox.remove)
        format = prefs.prefs[prefs.date_format_pref]
        for prop in row.propagations:
            s = '<b>%s</b>: %s' % (prop.date.strftime(format),
             prop.get_summary())
            label = gtk.Label()
            label.set_markup(s)
            label.props.wrap = True
            label.set_alignment(0.0, 0.5)
            self.vbox.pack_start(label)

        self.vbox.show_all()


class PlantInfoBox(InfoBox):
    """
    an InfoBox for a Plants table row
    """

    def __init__(self):
        """
        """
        InfoBox.__init__(self)
        filename = os.path.join(paths.lib_dir(), 'plugins', 'garden', 'plant_infobox.glade')
        self.widgets = utils.load_widgets(filename)
        self.general = GeneralPlantExpander(self.widgets)
        self.add_expander(self.general)
        self.transfers = ChangesExpander(self.widgets)
        self.add_expander(self.transfers)
        self.propagations = PropagationExpander(self.widgets)
        self.add_expander(self.propagations)
        self.links = view.LinksExpander('notes')
        self.add_expander(self.links)
        self.props = PropertiesExpander()
        self.add_expander(self.props)

    def update(self, row):
        """
        """
        self.general.update(row)
        self.transfers.update(row)
        self.propagations.update(row)
        urls = filter(lambda x: x != [], [ utils.get_urls(note.note) for note in row.notes ])
        if not urls:
            self.links.props.visible = False
            self.links._sep.props.visible = False
        else:
            self.links.props.visible = True
            self.links._sep.props.visible = True
            self.links.update(row)
        self.props.update(row)