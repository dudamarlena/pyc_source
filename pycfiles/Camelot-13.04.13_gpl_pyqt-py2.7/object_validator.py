# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/admin/validator/object_validator.py
# Compiled at: 2013-04-11 17:47:52
from copy import copy
import logging
logger = logging.getLogger('camelot.admin.validator.object_validator')
from PyQt4 import QtCore
from camelot.view.fifo import Fifo
from camelot.view.model_thread import post
from camelot.core.utils import ugettext as _

class ObjectValidator(QtCore.QObject):
    """A validator class for normal python objects.  By default this validator
    declares all objects valid.  Subclass this class and overwrite it's
    objectValidity method to change it's behaviour.
    """
    validity_changed_signal = QtCore.pyqtSignal(int)

    def __init__(self, admin, model=None, initial_validation=False):
        """
        :param model: a collection proxy the validator should inspect, or None 
            if only the objectValidity method is going to get used.
        :param verifiy_initial_validity: do an inital check to see if all rows 
            in a model are valid, defaults to False,
            since this might take a lot of time on large collections.
        """
        super(ObjectValidator, self).__init__()
        self.admin = admin
        self.model = model
        self.message_cache = Fifo(10)
        if model:
            model.dataChanged.connect(self.data_changed)
            model.layoutChanged.connect(self.layout_changed)
        self._invalid_rows = set()
        self._related_validators = dict()
        if initial_validation:
            post(self.validate_all_rows)

    def get_related_validator(self, cls):
        """Get the validator for another Class
        :param cls: the `Class` for which to get the validator
        :return: an `ObjectValidator` instance
        """
        try:
            return self._related_validators[cls]
        except KeyError:
            validator = self.admin.get_related_admin(cls).get_validator()
            self._related_validators[cls] = validator
            return validator

    def validate_all_rows(self):
        """Force validation of all rows in the model"""
        for row in range(self.model.getRowCount()):
            self.isValid(row)

    def validate_invalid_rows(self):
        for row in copy(self._invalid_rows):
            self.isValid(row)

    @QtCore.pyqtSlot()
    def layout_changed(self):
        post(self.validate_invalid_rows)

    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    def data_changed(self, from_index, thru_index):

        def create_validity_updater(from_row, thru_row):

            def validity_updater():
                for i in range(from_row, thru_row + 1):
                    self.isValid(i)

            return validity_updater

        post(create_validity_updater(from_index.row(), thru_index.row()))

    def objectValidity(self, entity_instance):
        """deprecated, use `validate_object` instead
        """
        return self.validate_object(entity_instance)

    def validate_object(self, obj):
        """:return: list of messages explaining invalid data
        empty list if object is valid
        """
        from camelot.view.controls import delegates
        messages = []
        fields_and_attributes = dict(self.admin.get_columns())
        fields_and_attributes.update(dict(self.admin.get_fields()))
        for field, attributes in fields_and_attributes.items():
            if attributes['editable']:
                if attributes['nullable'] != True:
                    value = getattr(obj, field)
                    logger.debug('column %s is required' % field)
                    if 'delegate' not in attributes:
                        raise Exception('no delegate specified for %s' % field)
                    is_null = False
                    if value == None:
                        is_null = True
                    elif attributes['delegate'] == delegates.CodeDelegate and sum(len(c) for c in value) == 0:
                        is_null = True
                    elif attributes['delegate'] == delegates.PlainTextDelegate and len(value) == 0:
                        is_null = True
                    elif attributes['delegate'] == delegates.Many2OneDelegate and value == None:
                        is_null = True
                    elif attributes['delegate'] == delegates.VirtualAddressDelegate and not value[1]:
                        is_null = True
                    if is_null:
                        messages.append(_('%s is a required field') % attributes['name'])

        if not len(messages):
            for compound_obj in self.admin.get_compounding_objects(obj):
                related_validator = self.get_related_validator(type(compound_obj))
                messages.extend(related_validator.validate_object(compound_obj))

            logger.debug('messages : %s' % (',').join(messages))
        return messages

    def number_of_invalid_rows(self):
        """
        :return: the number of invalid rows in a model, as they have been verified
        """
        return len(self._invalid_rows)

    def isValid(self, row):
        """Verify if a row in a model is 'valid' meaning it could be flushed to
        the database
        """
        messages = []
        logger.debug('isValid for row %s' % row)
        try:
            entity_instance = self.model._get_object(row)
            if entity_instance != None:
                messages = self.objectValidity(entity_instance)
                self.message_cache.add_data(row, entity_instance, messages)
        except Exception as e:
            logger.error('programming error while validating object', exc_info=e)

        valid = len(messages) == 0
        if not valid:
            if row not in self._invalid_rows:
                self._invalid_rows.add(row)
                self.validity_changed_signal.emit(row)
        elif row in self._invalid_rows:
            self._invalid_rows.remove(row)
            self.validity_changed_signal.emit(row)
        logger.debug('valid : %s' % valid)
        return valid

    def validityMessages(self, row):
        try:
            return self.message_cache.get_data_at_row(row)
        except KeyError:
            raise Exception('Programming error : isValid should be called before calling validityMessage')

    def validityDialog(self, row, parent):
        """Return a QDialog that asks the user to discard his changes or
        continue to edit the row until it is valid.
        """
        from PyQt4 import QtGui
        return QtGui.QMessageBox(QtGui.QMessageBox.Warning, _('Invalid form'), ('\n').join(self.validityMessages(row)), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Discard, parent)