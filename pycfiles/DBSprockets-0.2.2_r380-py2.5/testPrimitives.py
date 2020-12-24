# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/test/testPrimitives.py
# Compiled at: 2008-06-30 11:43:30
from dbsprockets.primitives import *
from dbsprockets.test.model import *
from dbsprockets.test.base import setupDatabase, session
from tw.forms.fields import PasswordField
from tw.forms import Form
from formencode.validators import FieldsMatch
from formencode import Schema
from nose.tools import raises, eq_
from difflib import ndiff

def setup():
    global getTableValue
    global makeForm
    global makeTable
    setupDatabase()
    import dbsprockets.primitives as p
    p.generator = SprocketGenerator()
    p.fetcher = DataFetcher()
    p.makeForm = p.generator.makeForm
    p.makeTable = p.generator.makeTable
    p.getTableValue = p.fetcher.getTableValue
    p.SAORMDBHelper = p._SAORMDBHelper()
    makeForm = p.makeForm
    makeTable = p.makeTable
    getTableValue = p.getTableValue


class TestDBHelper:

    def setup(self):
        self.helper = DBHelper()

    @raises(NotImplementedError)
    def testGetMetadata(self):
        self.helper.getMetadata(None)
        return

    @raises(NotImplementedError)
    def testGetIdentifier(self):
        self.helper.getIdentifier(None)
        return

    @raises(NotImplementedError)
    def testValidateModel(self):
        self.helper.validateModel(None)
        return


class TestSAORMHelper:

    def setup(self):
        self.helper = SAORMDBHelper

    @raises(TypeError)
    def testValidateModelBad(self):
        self.helper.validateModel(None)
        return

    @raises(Exception)
    def testValidateModelBadNoFields(self):

        class Dummy:
            c = {}

        self.helper.validateModel(Dummy)


class TestDatabaseMixin:

    def setup(self):
        self.mixin = DatabaseMixin()

    def testCreate(self):
        pass

    @raises(Exception)
    def test_getHelperBad(self):
        self.mixin._getHelper(None)
        return


@raises(Exception)
def _create(model, action, identifier='', controller='', hiddenFields=[], disabledFields=[], requiredFields=[], omittedFields=[], additionalFields=[], limitFields=None, fieldAttrs={}, widgets={}, validators={}, formValidator=None, checkIfUnique=True):
    makeForm(model=model, action=action, identifier=identifier, controller=controller, hiddenFields=hiddenFields, disabledFields=disabledFields, requiredFields=reduce, omittedFields=omittedFields, additionalFields=additionalFields, limitFields=limitFields, fieldAttrs=fieldAttrs, widgets=widgets, validators=validators, formValidator=formValidator, checkIfUnique=checkIfUnique)


def testMakeFormBad():
    badInput = (
     'a', (), [], 1, 1.2, False, {}, None)
    for input in badInput[1:]:
        yield (
         _create, User, input)

    for input in badInput[1:]:
        yield (
         _create, User, 'a', input)

    for input in badInput[1:]:
        yield (
         _create, User, 'a', 'a', input)

    badInput = (
     'a', 1, 1.2, False, {}, None)
    for input in badInput:
        yield (
         _create, User, 'a', 'a', 'a', input)

    for input in badInput:
        yield (
         _create, User, 'a', 'a', 'a', [], input)

    for input in badInput:
        yield (
         _create, User, 'a', 'a', 'a', [], [], input)

    for input in badInput:
        yield (
         _create, User, 'a', 'a', 'a', [], [], [], input)

    badInput = (
     'a', 1, 1.2, False, ())
    for input in badInput:
        yield (
         _create, User, 'a', 'a', 'a', [], [], [], [], input)

    badInput = ('a', 1, 1.2, False, None)
    for input in badInput:
        yield (
         _create, User, 'a', 'a', 'a', [], [], [], [], [], input)

    badInput = ('a', 1, 1.2, False, (), [], None)
    for input in badInput:
        yield (
         _create, User, 'a', 'a', 'a', [], [], [], [], [], None, input)

    badInput = (
     'a', 1, 1.2, False, (), [])
    for input in badInput:
        yield (
         _create, User, 'a', 'a', 'a', [], [], [], [], [], None, {}, input)

    for input in badInput:
        yield (
         _create, User, 'a', 'a', 'a', [], [], [], [], [], None, {}, {}, input)

    for input in badInput:
        yield (
         _create, User, 'a', 'a', 'a', [], [], [], [], [], None, {}, {}, {}, input)

    badInput = (
     'a', 1, 1.2, (), [], {})
    for input in badInput:
        yield (
         _create, User, 'a', 'a', 'a', [], [], [], [], [], None, {}, {}, {}, None, input)

    return


def testMakeForm():
    form = makeForm(User, 'add')
    rendered = form()
    assert rendered.endswith('</tr><tr class="even">\n            <th>\n            </th>\n            <td>\n                <input type="submit" class="submitbutton" id="EditableRecordViewConfig_tg_user_submit" value="Submit" />\n            </td>\n        </tr>\n    </table>\n</form>'), rendered


def testMakeFormWithHiddenFields():
    form = makeForm(User, 'add', hiddenFields=['email_address', 'tg_groups', 'town', 'password', 'display_name'])
    rendered = form()
    assert '<input type="hidden" name="town" class="hiddenfield" id="EditableRecordViewConfig_tg_user_town" value="" />\n            <input type="hidden" name="password" class="hiddenfield" id="EditableRecordViewConfig_tg_user_password" value="" />' in rendered, rendered


def testMakeFormWithlimitFields():
    form = makeForm(User, 'add', limitFields=['user_name', 'password'])
    rendered = form()
    assert '<tr class="even">\n            <th>\n                <label id="EditableRecordViewConfig_tg_user_user_name.label" for="EditableRecordViewConfig_tg_user_user_name" class="fieldlabel">User Name</label>\n            </th>\n            <td>\n                <input type="text" name="user_name" class="textfield" id="EditableRecordViewConfig_tg_user_user_name" value="" maxlength="16" size="16" />\n            </td>\n        </tr>' in rendered, rendered


def testMakeFormWithOmittedFields():
    form = makeForm(User, 'add', omittedFields=['email_address', 'tg_groups', 'town', 'password', 'display_name'])
    rendered = form()
    assert 'password' not in rendered, rendered


def testMakeFormWithWidgetType():
    form = makeForm(User, 'add', omittedFields=['email_address', 'tg_groups', 'town', 'password', 'display_name'], formWidgetType=Form)
    rendered = form()
    assert '<form xmlns="http://www.w3.org/1999/xhtml" id="EditableRecordViewConfig_tg_user" action="add" method="post" class="required form">\n    <div>' in rendered, rendered


def testMakeFormWithAdditionalField():
    form = makeForm(User, 'add', omittedFields=['email_address', 'tg_groups', 'town', 'password', 'display_name'])
    rendered = form()
    assert 'password' not in rendered, rendered


def testMakeFormWithDisabledField():
    form = makeForm(User, 'add', disabledFields=['user_id'])
    rendered = form()
    assert '<th>\n                <label id="EditableRecordViewConfig_tg_user_user_id.label" for="EditableRecordViewConfig_tg_user_user_id" class="fieldlabel">User Id</label>\n            </th>\n            <td>\n                <input type="text" name="user_id" class="textfield" id="EditableRecordViewConfig_tg_user_user_id" value="" disabled="disabled" />\n            </td>\n        </tr>' in rendered, rendered


def testMakeFormUltimateUseCase():
    requiredFields = [
     'user_name']
    omittedFields = ['enabled', 'user_id', 'tg_groups', 'created', 'town', 'password', 'email_address', 'display_name']
    additionalFields = [PasswordField('passwordVerification', label_text='Verify')]
    formValidator = Schema(chained_validators=(
     FieldsMatch('password', 'passwordVerification', messages={'invalidNoMatch': 'Passwords do not match'}),))
    form = makeForm(User, 'add', requiredFields=requiredFields, omittedFields=omittedFields, additionalFields=additionalFields, formValidator=formValidator)
    rendered = form()
    assert rendered == '<form xmlns="http://www.w3.org/1999/xhtml" id="EditableRecordViewConfig_tg_user" action="add" method="post" class="dbsprocketstableform required">\n    <div>\n            <input type="hidden" name="tableName" class="hiddenfield" id="EditableRecordViewConfig_tg_user_tableName" value="" />\n            <input type="hidden" name="dbsprockets_id" class="hiddenfield" id="EditableRecordViewConfig_tg_user_dbsprockets_id" value="" />\n    </div>\n    <table border="0" cellspacing="0" cellpadding="2">\n        <tr class="even">\n            <th>\n                <label id="EditableRecordViewConfig_tg_user_user_name.label" for="EditableRecordViewConfig_tg_user_user_name" class="fieldlabel required">User Name</label>\n            </th>\n            <td>\n                <input type="text" name="user_name" class="textfield required" id="EditableRecordViewConfig_tg_user_user_name" value="" maxlength="16" size="16" />\n            </td>\n        </tr><tr class="odd">\n            <th>\n                <label id="EditableRecordViewConfig_tg_user_passwordVerification.label" for="EditableRecordViewConfig_tg_user_passwordVerification" class="fieldlabel">Verify</label>\n            </th>\n            <td>\n                <input type="password" name="passwordVerification" class="passwordfield" id="EditableRecordViewConfig_tg_user_passwordVerification" value="" />\n            </td>\n        </tr><tr class="even">\n            <th>\n            </th>\n            <td>\n                <input type="submit" class="submitbutton" id="EditableRecordViewConfig_tg_user_submit" value="Submit" />\n            </td>\n        </tr>\n    </table>\n</form>', rendered


def testMakeTableWithData():
    actual = getTableValue(User)
    table = makeTable(User, '/')
    rendered = table(value=actual)
    assert '<table xmlns="http://www.w3.org/1999/xhtml" id="TableViewConfig_tg_user" class="grid" cellpadding="0" cellspacing="1" border="0">\n    <thead>\n        <tr>\n            <th class="col_0">\n            </th><th class="col_1">\n            user_id\n            </th><th class="col_2">\n            user_name\n            </th><th class="col_3">\n            email_address\n            </th><th class="col_4">\n            display_name\n            </th><th class="col_5">\n            password\n            </th><th class="col_6">\n            town\n            </th><th class="col_7">\n            created\n            </th><th class="col_8">\n            tg_groups\n            </th>\n        </tr>\n    </thead>\n    <tbody>\n        <tr class="even">\n            <td><a href="//editRecord/tg_user?user_id=1">edit</a>|<a href="//delete/tg_user?user_id=1">delete</a></td><td>1</td><td>asdf</td><td></td><td></td><td>******</td><td>Arvada</td><td>' in rendered, rendered


def testMakeTableWithDataAndNoController():
    actual = getTableValue(User)
    table = makeTable(User)
    rendered = table(value=actual)
    assert '<table xmlns="http://www.w3.org/1999/xhtml" id="TableViewConfig_tg_user" class="grid" cellpadding="0" cellspacing="1" border="0">\n    <thead>\n        <tr>\n            <th class="col_0">\n            user_id\n            </th><th class="col_1">\n            user_name\n            </th><th class="col_2">\n            email_address\n            </th><th class="col_3">\n            display_name\n            </th><th class="col_4">\n            password\n            </th><th class="col_5">\n            town\n            </th><th class="col_6">\n            created\n            </th><th class="col_7">\n            tg_groups\n            </th>\n        </tr>\n    </thead>\n    <tbody>\n        <tr class="even">\n            <td>1</td><td>asdf</td><td></td><td></td><td>******</td><td>Arvada</td>' in rendered, rendered


def testGetTableValue():
    actual = getTableValue(User)
    expected = [
     {'town': 'Arvada', 'user_id': 1, 'email_address': None, 
        'display_name': None, 'password': '******', 'user_name': 'asdf'}]
    for (i, item) in enumerate(expected):
        for (key, value) in item.iteritems():
            assert actual[i][key] == value

    return


def testMakeRecordValue():
    actual = makeRecordView(User)
    value = {'town': 'Arvada', 'user_id': 1, 'email_address': None, 
       'display_name': None, 'password': '******', 'user_name': 'asdf', 'created': None}
    actual = actual.render(value)
    expected = '<table xmlns="http://www.w3.org/1999/xhtml" id="RecordViewConfig_tg_user" class="recordviewwidget">\n<tr><th>Name</th><th>Value</th></tr>\n<tr class="recordfieldwidget">\n    <td>\n        <b>user_id</b>\n    </td>\n    <td> 1\n    </td>\n</tr>\n<tr class="recordfieldwidget">\n    <td>\n        <b>user_name</b>\n    </td>\n    <td> asdf\n    </td>\n</tr>\n<tr class="recordfieldwidget">\n    <td>\n        <b>email_address</b>\n    </td>\n    <td>\n    </td>\n</tr>\n<tr class="recordfieldwidget">\n    <td>\n        <b>display_name</b>\n    </td>\n    <td>\n    </td>\n</tr>\n<tr class="recordfieldwidget">\n    <td>\n        <b>password</b>\n    </td>\n    <td> ******\n    </td>\n</tr>\n<tr class="recordfieldwidget">\n    <td>\n        <b>town</b>\n    </td>\n    <td> Arvada\n    </td>\n</tr>\n<tr class="recordfieldwidget">\n    <td>\n        <b>created</b>\n    </td>\n    <td>\n    </td>\n</tr>\n<input type="hidden" name="dbsprockets_id" class="hiddenfield" id="RecordViewConfig_tg_user_dbsprockets_id" value="townuser_idcreateduser_namedisplay_namepasswordemail_address" />\n</table>'
    assert actual == expected, ('').join((a for a in ndiff(expected.splitlines(1), actual.splitlines(1))))
    return


class TestSAORMDBHelperSAORMDBHelper:

    def setup(self):
        self.helper = SAORMDBHelper

    def testGetIdentifier(self):
        eq_(self.helper.getIdentifier(User), 'tg_user')


def testGetFormDefaults():
    actual = getFormDefaults(Example)
    assert sorted(actual.keys()) == ['Integer', 'created'], sorted(actual.keys())
    assert actual['Integer'] == 10