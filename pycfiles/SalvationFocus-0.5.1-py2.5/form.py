# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salvationfocus/model/form.py
# Compiled at: 2008-03-10 17:05:02
import formencode
from formencode import Invalid
from formencode.validators import FormValidator
from salvationfocus.model import Session
from salvationfocus.model.Submitter import Submitter
from salvationfocus.model.Prebeliever import Prebeliever
from salvationfocus.model.Administrator import Administrator

class SubmitterUniqueNameValidator(FormValidator):
    """checks that the whole name, first and last, is unique
    
    >>> unv = UniqueNameValidator('fname', 'lname')
    >>> unv.to_python({'fname':'Atticus', 'lname':'Finch'})
    {'lname': 'Finch', 'fname': 'Atticus'}
    >>> unv.to_python({'fname':'Racer', 'lname':'X'})
    Traceback (most recent call last):
        ...
    Invalid: The name Racer X already exists
    """
    __unpackargs__ = ('*', 'field_names')
    messages = {'invalid': '%(fst)s %(lst)s already exists.'}
    field_names = None

    def validate_python(self, field_dict, state):
        fname = field_dict[self.field_names[0]]
        lname = field_dict[self.field_names[1]]
        if not self._valid_name(fname, lname):
            msg = self.message('invalid', state, fst=fname, lst=lname)
            raise Invalid(msg, field_dict, state, error_dict={'form': msg})
        return field_dict

    def _valid_name(self, fname, lname):
        """check the database here"""
        if Session.query(Submitter).filter_by(first_name=fname, last_name=lname).first():
            return False
        else:
            return True


class PrebelieverUniqueNameValidator(FormValidator):
    """checks that the whole name, first and last, is unique
    
    >>> unv = UniqueNameValidator('fname', 'lname')
    >>> unv.to_python({'fname':'Atticus', 'lname':'Finch'})
    {'lname': 'Finch', 'fname': 'Atticus'}
    >>> unv.to_python({'fname':'Racer', 'lname':'X'})
    Traceback (most recent call last):
        ...
    Invalid: The name Racer X already exists
    """
    __unpackargs__ = ('*', 'field_names')
    messages = {'invalid': '%(fst)s %(lst)s already exists.'}
    field_names = None

    def validate_python(self, field_dict, state):
        fname = field_dict[self.field_names[0]]
        lname = field_dict[self.field_names[1]]
        if not self._valid_name(fname, lname):
            msg = self.message('invalid', state, fst=fname, lst=lname)
            raise Invalid(msg, field_dict, state, error_dict={'form': msg})
        return field_dict

    def _valid_name(self, fname, lname):
        """check the database here"""
        if Session.query(Prebeliever).filter_by(first_name=fname, last_name=lname).first():
            return False
        else:
            return True


class AdministratorUniqueNameValidator(FormValidator):
    """checks that the login name is unique
    
    >>> unv = AdministratorUniqueNameValidator('lname')
    """
    __unpackargs__ = ('*', 'field_names')
    messages = {'invalid': '%(log)s already exists.'}
    field_names = None

    def validate_python(self, field_dict, state):
        lname = field_dict[self.field_names[0]]
        if not self._valid_name(lname):
            msg = self.message('invalid', state, log=lname)
            raise Invalid(msg, field_dict, state, error_dict={'form': msg})
        return field_dict

    def _valid_name(self, lname):
        """check the database here"""
        if Session.query(Administrator).filter_by(login_name=lname).first():
            return False
        else:
            return True


class BaseForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True


class AddSubmitterForm(BaseForm):
    first_name = formencode.validators.String(not_empty=True)
    last_name = formencode.validators.String(not_empty=True)
    phone = formencode.validators.PhoneNumber(not_empty=True)
    email = formencode.validators.Email(not_empty=True)
    chained_validators = [
     SubmitterUniqueNameValidator('first_name', 'last_name')]


class AddPrebelieverForm(BaseForm):
    first_name = formencode.validators.String(not_empty=True)
    last_name = formencode.validators.String(not_empty=True)
    submitter_id = formencode.validators.Int(not_empty=True)
    chained_validators = [
     PrebelieverUniqueNameValidator('first_name', 'last_name')]


class AddAdministratorForm(BaseForm):
    login_name = formencode.validators.String(not_empty=True)
    password = formencode.validators.String(not_empty=True)
    password_confirm = formencode.validators.String(not_empty=True)
    email = formencode.validators.Email(not_empty=True)
    chained_validators = [
     formencode.validators.FieldsMatch('password', 'password_confirm'),
     AdministratorUniqueNameValidator('login_name')]


class EditSubmitterForm(BaseForm):
    first_name = formencode.validators.String(not_empty=True)
    last_name = formencode.validators.String(not_empty=True)
    phone = formencode.validators.PhoneNumber(not_empty=True)
    email = formencode.validators.Email(not_empty=True)


class EditPrebelieverForm(BaseForm):
    first_name = formencode.validators.String(not_empty=True)
    last_name = formencode.validators.String(not_empty=True)
    submitter_id = formencode.validators.Int(not_empty=True)


class EditAdministratorEmail(BaseForm):
    email = formencode.validators.Email(not_empty=True)


class EditAdministratorPassword(BaseForm):
    current_password = formencode.validators.String(not_empty=True)
    new_password = formencode.validators.String(not_empty=True)
    confirm_password = formencode.validators.String(not_empty=True)
    chained_validators = [
     formencode.validators.FieldsMatch('new_password', 'confirm_password')]