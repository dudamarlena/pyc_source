# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rnix/workspace/yafowil.demo/devsrc/yafowil.widget.dict/src/yafowil/widget/dict/tests.py
# Compiled at: 2018-07-16 08:38:37
from node.utils import UNSET
from odict import odict
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.compat import IS_PY2
from yafowil.tests import YafowilTestCase
from yafowil.tests import fxml
import yafowil.loader
if not IS_PY2:
    from importlib import reload

class TestDictWidget(YafowilTestCase):

    def setUp(self):
        super(TestDictWidget, self).setUp()
        from yafowil.widget.dict import widget
        reload(widget)

    def test_empty_dict(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        form['mydict'] = factory('dict', props={'key_label': 'Key', 
           'value_label': 'Value'})
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data" id="form-myform"\n              method="post" novalidate="novalidate">\n          <table class="dictwidget key-keyfield value-valuefield"\n                 id="dictwidget_myform.mydict.entry">\n            <thead>\n              <tr>\n                <th>Key</th>\n                <th>Value</th>\n                <th class="actions">\n                  <div class="dict_actions">\n                    <a class="dict_row_add" href="#">\n                      <span class="icon-plus-sign"> </span>\n                    </a>\n                  </div>\n                </th>\n              </tr>\n            </thead>\n            <tbody/>\n          </table>\n        </form>\n        ', fxml(form()))

    def test_key_label_and_value_label_callables(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        form['mydict'] = factory('dict', props={'key_label': lambda : 'Computed Key', 
           'value_label': lambda : 'Computed Value'})
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data" id="form-myform"\n              method="post" novalidate="novalidate">\n          <table class="dictwidget key-keyfield value-valuefield"\n                 id="dictwidget_myform.mydict.entry">\n            <thead>\n              <tr>\n                <th>Computed Key</th>\n                <th>Computed Value</th>\n                ...\n              </tr>\n            </thead>\n            <tbody/>\n          </table>\n        </form>\n        ', fxml(form()))

    def test_bc_head_property(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        form['mydict'] = factory('dict', props={'head': {'key': 'B/C Key', 
                    'value': 'B/C Value'}})
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data" id="form-myform"\n              method="post" novalidate="novalidate">\n          <table class="dictwidget key-keyfield value-valuefield"\n                 id="dictwidget_myform.mydict.entry">\n            <thead>\n              <tr>\n                <th>B/C Key</th>\n                <th>B/C Value</th>\n                ...\n              </tr>\n            </thead>\n            <tbody/>\n          </table>\n        </form>\n        ', fxml(form()))

    def test_bc_head_property_labels_callable(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        form['mydict'] = factory('dict', props={'head': {'key': lambda : 'Computed B/C Key', 
                    'value': lambda : 'Computed B/C Value'}})
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data" id="form-myform"\n              method="post" novalidate="novalidate">\n          <table class="dictwidget key-keyfield value-valuefield"\n                 id="dictwidget_myform.mydict.entry">\n            <thead>\n              <tr>\n                <th>Computed B/C Key</th>\n                <th>Computed B/C Value</th>\n                ...\n              </tr>\n            </thead>\n            <tbody/>\n          </table>\n        </form>\n        ', fxml(form()))

    def test_skip_labels(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        form['mydict'] = factory('dict')
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data" id="form-myform"\n              method="post" novalidate="novalidate">\n          <table class="dictwidget key-keyfield value-valuefield"\n                 id="dictwidget_myform.mydict.entry">\n            <thead>\n              <tr>\n                <th> </th>\n                <th> </th>\n                ...\n              </tr>\n            </thead>\n            <tbody/>\n          </table>\n        </form>\n        ', fxml(form()))

    def test_dict_with_preset_values(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        value = odict()
        value['key1'] = 'Value1'
        value['key2'] = 'Value2'
        form['mydict'] = factory('dict', value=value, props={'key_label': 'Key', 
           'value_label': 'Value'})
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data" id="form-myform"\n              method="post" novalidate="novalidate">\n          <table class="dictwidget key-keyfield value-valuefield"\n                 id="dictwidget_myform.mydict.entry">\n            <thead>\n              <tr>\n                <th>Key</th>\n                <th>Value</th>\n                <th class="actions">\n                  <div class="dict_actions">\n                    <a class="dict_row_add" href="#">\n                      <span class="icon-plus-sign"> </span>\n                    </a>\n                  </div>\n                </th>\n              </tr>\n            </thead>\n            <tbody>\n              <tr>\n                <td class="key">\n                  <input class="keyfield" id="input-myform-mydict-entry0-key"\n                         name="myform.mydict.entry0.key" type="text"\n                         value="key1"/>\n                </td>\n                <td class="value">\n                  <input class="valuefield"\n                         id="input-myform-mydict-entry0-value"\n                         name="myform.mydict.entry0.value"\n                         type="text" value="Value1"/>\n                </td>\n                <td class="actions">\n                  <div class="dict_actions">\n                    <a class="dict_row_add" href="#">\n                      <span class="icon-plus-sign"> </span>\n                    </a>\n                    <a class="dict_row_remove" href="#">\n                      <span class="icon-minus-sign"> </span>\n                    </a>\n                    <a class="dict_row_up" href="#">\n                      <span class="icon-circle-arrow-up"> </span>\n                    </a>\n                    <a class="dict_row_down" href="#">\n                      <span class="icon-circle-arrow-down"> </span>\n                    </a>\n                  </div>\n                </td>\n              </tr>\n              <tr>\n                <td class="key">\n                  <input class="keyfield" id="input-myform-mydict-entry1-key"\n                         name="myform.mydict.entry1.key" type="text"\n                         value="key2"/>\n                </td>\n                <td class="value">\n                  <input class="valuefield"\n                         id="input-myform-mydict-entry1-value"\n                         name="myform.mydict.entry1.value"\n                         type="text" value="Value2"/>\n                </td>\n                <td class="actions">\n                  <div class="dict_actions">\n                    ...\n                  </div>\n                </td>\n              </tr>\n            </tbody>\n          </table>\n        </form>\n        ', fxml(form()))

    def test_extraction(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        value = odict()
        value['key1'] = 'Value1'
        value['key2'] = 'Value2'
        form['mydict'] = factory('dict', value=value, props={'key_label': 'Key', 
           'value_label': 'Value'})
        form()
        self.assertEqual(form.treerepr().split('\n'), [
         "<class 'yafowil.base.Widget'>: myform",
         "  <class 'yafowil.base.Widget'>: mydict",
         "    <class 'yafowil.base.Widget'>: table",
         "      <class 'yafowil.base.Widget'>: head",
         "        <class 'yafowil.base.Widget'>: row",
         "          <class 'yafowil.base.Widget'>: key",
         "          <class 'yafowil.base.Widget'>: value",
         "          <class 'yafowil.base.Widget'>: actions",
         "      <class 'yafowil.base.Widget'>: body",
         "        <class 'yafowil.base.Widget'>: entry0",
         "          <class 'yafowil.base.Widget'>: key",
         "          <class 'yafowil.base.Widget'>: value",
         "          <class 'yafowil.base.Widget'>: actions",
         "        <class 'yafowil.base.Widget'>: entry1",
         "          <class 'yafowil.base.Widget'>: key",
         "          <class 'yafowil.base.Widget'>: value",
         "          <class 'yafowil.base.Widget'>: actions",
         ''])
        request = {'myform.mydict.entry0.key': 'key1', 
           'myform.mydict.entry0.value': 'New Value 1', 
           'myform.mydict.entry1.key': 'key2', 
           'myform.mydict.entry1.value': 'New Value 2'}
        data = form.extract(request=request)
        self.assertEqual(data.fetch('myform.mydict.entry0.value').extracted, 'New Value 1')
        self.assertEqual(data.fetch('myform.mydict.entry1.value').extracted, 'New Value 2')
        self.assertEqual(data.fetch('myform.mydict').extracted, odict([('key1', 'New Value 1'), ('key2', 'New Value 2')]))

    def test_extraction_entries_increased_in_ui(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        value = odict()
        value['key1'] = 'Value1'
        value['key2'] = 'Value2'
        form['mydict'] = factory('dict', value=value, props={'key_label': 'Key', 
           'value_label': 'Value'})
        request = {'myform.mydict.entry0.key': 'key1', 
           'myform.mydict.entry0.value': 'New Value 1', 
           'myform.mydict.entry1.key': 'key2', 
           'myform.mydict.entry1.value': 'New Value 2', 
           'myform.mydict.entry2.key': 'key3', 
           'myform.mydict.entry2.value': 'New Value 3'}
        data = form.extract(request=request)
        self.assertEqual(data.fetch('myform.mydict').extracted, odict([
         ('key1', 'New Value 1'),
         ('key2', 'New Value 2'),
         ('key3', 'New Value 3')]))
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data"\n        ...\n        value="New Value 1"\n        ...\n        value="New Value 2"\n        ...\n        value="New Value 3"\n        ...\n        ', form(data=data))

    def test_extraction_entries_decreased_in_ui(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        value = odict()
        value['key1'] = 'Value1'
        value['key2'] = 'Value2'
        form['mydict'] = factory('dict', value=value, props={'key_label': 'Key', 
           'value_label': 'Value'})
        request = {'myform.mydict.entry0.key': 'key1', 
           'myform.mydict.entry0.value': 'Very New Value 1'}
        data = form.extract(request=request)
        self.assertEqual(data.fetch('myform.mydict').extracted, odict([('key1', 'Very New Value 1')]))
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data"\n        ...\n        value="Very New Value 1"\n        ...\n        ', form(data=data))
        self.assertEqual(form(data=data).find('New Value 2'), -1)

    def test_extraction_empty_keys_ignored(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        value = odict()
        value['key1'] = 'Value1'
        value['key2'] = 'Value2'
        form['mydict'] = factory('dict', value=value, props={'key_label': 'Key', 
           'value_label': 'Value'})
        request = {'myform.mydict.entry0.key': 'key1', 
           'myform.mydict.entry0.value': 'Very New Value 1', 
           'myform.mydict.entry1.key': '', 
           'myform.mydict.entry1.value': ''}
        data = form.extract(request=request)
        self.assertEqual(data.fetch('myform.mydict').extracted, odict([('key1', 'Very New Value 1')]))

    def test_extraction_required(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        form['mydict'] = factory('error:dict', props={'required': 'I am required', 
           'key_label': 'Key', 
           'value_label': 'Value'})
        request = {}
        data = form.extract(request=request)
        self.assertEqual([
         data.name, data.value, data.extracted, data.errors], [
         'myform', UNSET, odict([('mydict', UNSET)]), []])
        self.assertTrue(data.has_errors)
        ddata = data['mydict']
        self.assertEqual([
         ddata.name, ddata.value, ddata.extracted, ddata.errors], [
         'mydict', UNSET, UNSET, [ExtractionError('I am required')]])
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data" id="form-myform"\n              method="post" novalidate="novalidate">\n          <div class="error">\n            <div class="errormessage">I am required</div>\n            <table class="dictwidget key-keyfield value-valuefield"\n                   id="dictwidget_myform.mydict.entry">\n              <thead>\n                <tr>\n                  <th>Key</th>\n                  <th>Value</th>\n                  <th class="actions">\n                    <div class="dict_actions">\n                      <a class="dict_row_add" href="#">\n                        <span class="icon-plus-sign"> </span>\n                      </a>\n                    </div>\n                  </th>\n                </tr>\n              </thead>\n              <tbody/>\n            </table>\n          </div>\n        </form>\n        ', fxml(form(data=data)))
        request = {'myform.mydict.entry0.key': 'key1', 
           'myform.mydict.entry0.value': 'Very New Value 1'}
        data = form.extract(request=request)
        self.assertFalse(data.has_errors)
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data"\n        ...\n        value="Very New Value 1"\n        ...\n        ', form(data=data))
        self.assertEqual(form(data=data).find('error'), -1)

    def test_render_static_dict(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        form['mydict'] = factory('error:dict', value=odict([('k1', 'v1')]), props={'required': 'I am required', 
           'static': True, 
           'key_label': 'Key', 
           'value_label': 'Value'})
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data" id="form-myform"\n              method="post" novalidate="novalidate">\n          <table class="dictwidget key-keyfield value-valuefield"\n                 id="dictwidget_myform.mydict.entry">\n            <thead>\n              <tr>\n                <th>Key</th>\n                <th>Value</th>\n              </tr>\n            </thead>\n            <tbody>\n              <tr>\n                <td class="key">\n                  <input class="keyfield" disabled="disabled"\n                         id="input-myform-mydict-entry0-key"\n                         name="myform.mydict.entry0.key"\n                         type="text" value="k1"/>\n                </td>\n                <td class="value">\n                  <input class="valuefield"\n                         id="input-myform-mydict-entry0-value"\n                         name="myform.mydict.entry0.value"\n                         type="text" value="v1"/>\n                </td>\n              </tr>\n            </tbody>\n          </table>\n        </form>\n        ', fxml(form()))

    def test_extract_static_dict(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        form['mydict'] = factory('error:dict', value=odict([('k1', 'v1')]), props={'static': True, 
           'key_label': 'Key', 
           'value_label': 'Value'})
        request = {'myform.mydict.entry0.value': 'New Value 1'}
        data = form.extract(request=request)
        self.assertEqual(data.fetch('myform.mydict').extracted, odict([('k1', 'New Value 1')]))
        request = {'myform.mydict.entry0.value': 'New Value 1', 
           'myform.mydict.entry1.key': 'Wrong Key 2', 
           'myform.mydict.entry1.value': 'Wrong Value 2'}
        data = form.extract(request=request)
        self.assertEqual(data['mydict'].errors, [
         ExtractionError('Invalid number of static values')])

    def test_required_static_dict(self):
        form = factory('form', name='myform', props={'action': 'myaction'})
        form['mydict'] = factory('error:dict', value=odict([('k1', 'v1')]), props={'required': 'I am required', 
           'static': True, 
           'key_label': 'Key', 
           'value_label': 'Value'})
        request = {}
        data = form.extract(request=request)
        self.assertEqual(data.fetch('myform.mydict').errors, [
         ExtractionError('I am required')])
        request = {'myform.mydict.entry0.value': ''}
        data = form.extract(request=request)
        self.assertEqual(data.fetch('myform.mydict').errors, [
         ExtractionError('I am required')])
        self.check_output('\n        <form action="myaction" enctype="multipart/form-data" id="form-myform"\n              method="post" novalidate="novalidate">\n          <div class="error">\n            <div class="errormessage">I am required</div>\n            <table class="dictwidget key-keyfield value-valuefield"\n                   id="dictwidget_myform.mydict.entry">\n              <thead>\n                <tr>\n                  <th>Key</th>\n                  <th>Value</th>\n                </tr>\n              </thead>\n              <tbody>\n                <tr>\n                  <td class="key">\n                    <input class="keyfield" disabled="disabled"\n                           id="input-myform-mydict-entry0-key"\n                           name="myform.mydict.entry0.key"\n                           type="text" value="k1"/>\n                  </td>\n                  <td class="value">\n                    <input class="valuefield"\n                           id="input-myform-mydict-entry0-value"\n                           name="myform.mydict.entry0.value"\n                           type="text" value=""/>\n                  </td>\n                </tr>\n              </tbody>\n            </table>\n          </div>\n        </form>\n        ', fxml(form(data)))
        form['mydict'].attrs['required'] = True
        request = {'myform.mydict.entry0.value': ''}
        data = form.extract(request=request)
        self.assertEqual(data.fetch('myform.mydict').errors, [
         ExtractionError('Mandatory field was empty')])

    def test_display_renderer(self):
        value = odict()
        value['foo'] = 'Foo'
        value['bar'] = 'Bar'
        widget = factory('dict', name='display_dict', value=value, props={'key_label': 'Key', 
           'value_label': 'Value'}, mode='display')
        self.check_output('\n        <div>\n          <h5>Key: Value</h5>\n          <dl>\n            <dt>foo</dt>\n            <dd>Foo</dd>\n            <dt>bar</dt>\n            <dd>Bar</dd>\n          </dl>\n        </div>\n        ', fxml(('<div>{}</div>').format(widget())))

    def test_display_renderer_empty_values(self):
        widget = factory('dict', name='display_dict', props={'key_label': 'Key', 
           'value_label': 'Value'}, mode='display')
        self.check_output('\n        <div>\n          <h5>Key: Value</h5>\n          <dl/>\n        </div>\n        ', fxml(('<div>{}</div>').format(widget())))

    def test_display_renderer_callable_labels(self):
        widget = factory('dict', name='display_dict', props={'key_label': lambda : 'Computed Key', 
           'value_label': lambda : 'Computed Value'}, mode='display')
        self.check_output('\n        <div>\n          <h5>Computed Key: Computed Value</h5>\n          <dl/>\n        </div>\n        ', fxml(('<div>{}</div>').format(widget())))

    def test_display_renderer_bc_labels(self):
        widget = factory('dict', name='display_dict', props={'head': {'key': 'B/C Key', 
                    'value': 'B/C Value'}}, mode='display')
        self.check_output('\n        <div>\n          <h5>B/C Key: B/C Value</h5>\n          <dl/>\n        </div>\n        ', fxml(('<div>{}</div>').format(widget())))

    def test_display_renderer_computed_bc_labels(self):
        widget = factory('dict', name='display_dict', props={'head': {'key': lambda : 'Computed B/C Key', 
                    'value': lambda : 'Computed B/C Value'}}, mode='display')
        self.check_output('\n        <div>\n          <h5>Computed B/C Key: Computed B/C Value</h5>\n          <dl/>\n        </div>\n        ', fxml(('<div>{}</div>').format(widget())))

    def test_display_renderer_no_labels(self):
        widget = factory('dict', name='display_dict', mode='display')
        self.check_output('\n        <div>\n          <dl/>\n        </div>\n        ', fxml(('<div>{}</div>').format(widget())))


if __name__ == '__main__':
    unittest.main()