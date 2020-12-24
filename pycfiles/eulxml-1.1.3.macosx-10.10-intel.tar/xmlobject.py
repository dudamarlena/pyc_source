# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/forms/xmlobject.py
# Compiled at: 2016-02-19 17:15:24
from __future__ import unicode_literals
from collections import defaultdict
from string import capwords
from django.forms import BaseForm, CharField, IntegerField, BooleanField, ChoiceField, Field, Form, DateField
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.forms import get_declared_fields
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.models import ModelFormOptions
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
import six
from eulxml import xmlmap
from eulxml.utils.compat import u

def fieldname_to_label(name):
    """Default conversion from xmlmap Field variable name to Form field label:
    convert '_' to ' ' and capitalize words.  Should only be used when verbose_name
    is not set."""
    return capwords(name.replace(b'_', b' '))


def _parse_field_list(fieldnames, include_parents=False):
    """
    Parse a list of field names, possibly including dot-separated subform
    fields, into an internal ParsedFieldList object representing the base
    fields and subform listed.

    :param fieldnames: a list of field names as strings. dot-separated names
        are interpreted as subform fields.
    :param include_parents: optional boolean, defaults to False. if True,
        subform fields implicitly include their parent fields in the parsed
        list.
    """
    field_parts = (name.split(b'.') for name in fieldnames)
    return _collect_fields(field_parts, include_parents)


def _collect_fields(field_parts_list, include_parents):
    """utility function to enable recursion in _parse_field_list()"""
    fields = []
    subpart_lists = defaultdict(list)
    for parts in field_parts_list:
        field, subparts = parts[0], parts[1:]
        if subparts:
            if include_parents and field not in fields:
                fields.append(field)
            subpart_lists[field].append(subparts)
        else:
            fields.append(field)

    subfields = dict((field, _collect_fields(subparts, include_parents)) for field, subparts in six.iteritems(subpart_lists))
    return ParsedFieldList(fields, subfields)


class ParsedFieldList(object):
    """A parsed list of fields, used internally by :class:`XmlObjectForm`
    for tracking field and exclude lists."""

    def __init__(self, fields, subfields):
        self.fields = fields
        self.subfields = subfields


class SubformAwareModelFormOptions(ModelFormOptions):
    """A :class:`~django.forms.models.ModelFormOptions` subclass aware of
    fields and exclude lists, parsing them for later reference by
    :class:`XmlObjectForm` internals."""

    def __init__(self, options=None):
        super(SubformAwareModelFormOptions, self).__init__(options)
        self.max_num = getattr(options, b'max_num', None)
        self.can_delete = getattr(options, b'can_delete', True)
        self.can_order = getattr(options, b'can_order', False)
        self.extra = getattr(options, b'extra', 1)
        self.parsed_fields = None
        if isinstance(self.fields, ParsedFieldList):
            self.parsed_fields = self.fields
        elif self.fields is not None:
            self.parsed_fields = _parse_field_list(self.fields, include_parents=True)
        self.parsed_exclude = None
        if isinstance(self.exclude, ParsedFieldList):
            self.parsed_exclude = self.exclude
        elif self.exclude is not None:
            self.parsed_exclude = _parse_field_list(self.exclude, include_parents=False)
        return


def formfields_for_xmlobject(model, fields=None, exclude=None, widgets=None, options=None, declared_subforms=None, max_num=None, extra=None):
    """
    Returns three sorted dictionaries (:class:`django.utils.datastructures.SortedDict`).
     * The first is a dictionary of form fields based on the
       :class:`~eulxml.xmlmap.XmlObject` class fields and their types.
     * The second is a sorted dictionary of subform classes for any fields of type
       :class:`~eulxml.xmlmap.fields.NodeField` on the model.
     * The third is a sorted dictionary of formsets for any fields of type
       :class:`~eulxml.xmlmap.fields.NodeListField` on the model.

    Default sorting (within each dictionary) is by XmlObject field creation order.

    Used by :class:`XmlObjectFormType` to set up a new :class:`XmlObjectForm`
    class.

    :param fields: optional list of field names; if specified, only the named fields
                will be returned, in the specified order
    :param exclude: optional list of field names that should not be included on
                the form; if a field is listed in both ``fields`` and ``exclude``,
                it will be excluded
    :param widgets: optional dictionary of widget options to be passed to form
                field constructor, keyed on field name
    :param options: optional :class:`~django.forms.models.ModelFormOptions`.
                if specified then fields, exclude, and widgets will default
                to its values.
    :param declared_subforms: optional dictionary of field names and form classes;
                if specified, the specified form class will be used to initialize
                the corresponding subform (for a :class:`~eulxml.xmlmap.fields.NodeField`)
                or a formset (for a :class:`~eulxml.xmlmap.fields.NodeListField`)
    :param max_num: optional value for the maximum number of times a fieldset should repeat.
    :param max_num: optional value for the number of extra forms to provide.
    """
    fieldlist = getattr(options, b'parsed_fields', None)
    if isinstance(fields, ParsedFieldList):
        fieldlist = fields
    elif fields is not None:
        fieldlist = _parse_field_list(fields, include_parents=True)
    excludelist = getattr(options, b'parsed_exclude', None)
    if isinstance(fields, ParsedFieldList):
        fieldlist = fields
    else:
        if exclude is not None:
            excludelist = _parse_field_list(exclude, include_parents=False)
        if widgets is None and options is not None:
            widgets = options.widgets
        if max_num is None and options is not None:
            max_num = options.max_num
        formfields = {}
        subforms = {}
        formsets = {}
        field_order = {}
        subform_labels = {}
        for name, field in six.iteritems(model._fields):
            if fieldlist and name not in fieldlist.fields:
                continue
            if excludelist and name in excludelist.fields:
                continue
            if widgets and name in widgets:
                kwargs = {b'widget': widgets[name]}
            else:
                kwargs = {}
            field_type = None
            if field.required is not None:
                kwargs[b'required'] = field.required
            if field.verbose_name is not None:
                kwargs[b'label'] = field.verbose_name
            if field.help_text is not None:
                kwargs[b'help_text'] = field.help_text
            if hasattr(field, b'choices') and field.choices:
                field_type = ChoiceField
                kwargs[b'choices'] = [ (val, val) for val in field.choices ]
                if field.required == False and b'' not in field.choices:
                    kwargs[b'choices'].insert(0, ('', ''))
            elif isinstance(field, xmlmap.fields.StringField):
                field_type = CharField
            elif isinstance(field, xmlmap.fields.IntegerField):
                field_type = IntegerField
            elif isinstance(field, xmlmap.fields.DateField):
                field_type = DateField
            elif isinstance(field, xmlmap.fields.SimpleBooleanField):
                kwargs[b'required'] = False
                field_type = BooleanField
            elif isinstance(field, xmlmap.fields.NodeField) or isinstance(field, xmlmap.fields.NodeListField):
                form_label = kwargs[b'label'] if b'label' in kwargs else fieldname_to_label(name)
                subform_labels[name] = form_label
                if name in declared_subforms:
                    subform = declared_subforms[name]
                else:
                    subform_opts = {b'fields': fieldlist.subfields[name] if fieldlist and name in fieldlist.subfields else None, 
                       b'exclude': excludelist.subfields[name] if excludelist and name in excludelist.subfields else None, 
                       b'widgets': widgets[name] if widgets and name in widgets else None, 
                       b'label': form_label}
                    subform = xmlobjectform_factory(field.node_class, **subform_opts)
                if isinstance(field, xmlmap.fields.NodeField):
                    subforms[name] = subform
                elif isinstance(field, xmlmap.fields.NodeListField):
                    formsets[name] = formset_factory(subform, formset=BaseXmlObjectFormSet, max_num=subform._meta.max_num, can_delete=subform._meta.can_delete, extra=subform._meta.extra, can_order=subform._meta.can_order)
                    formsets[name].form_label = form_label
            elif isinstance(field, xmlmap.fields.StringListField) or isinstance(field, xmlmap.fields.IntegerListField):
                form_label = kwargs[b'label'] if b'label' in kwargs else fieldname_to_label(name)
                if isinstance(field, xmlmap.fields.IntegerListField):
                    listform = IntegerListFieldForm
                else:
                    listform = ListFieldForm
                formsets[name] = formset_factory(listform, formset=BaseXmlObjectListFieldFormSet)
                formsets[name].form_label = form_label
            else:
                raise Exception(b'Error on field "%s": XmlObjectForm does not yet support auto form field generation for %s.' % (
                 name, field.__class__))
            if field_type is not None:
                if b'label' not in kwargs:
                    kwargs[b'label'] = fieldname_to_label(name)
                formfields[name] = field_type(**kwargs)
            field_order[field.creation_counter] = name

    if fieldlist:
        ordered_fields = SortedDict((name, formfields[name]) for name in fieldlist.fields if name in formfields)
        ordered_subforms = SortedDict((name, subforms[name]) for name in fieldlist.fields if name in subforms)
        ordered_formsets = SortedDict((name, formsets[name]) for name in fieldlist.fields if name in formsets)
    else:
        ordered_fields = SortedDict([ (field_order[key], formfields[field_order[key]]) for key in sorted(field_order.keys()) if field_order[key] in formfields
                                    ])
        ordered_subforms = SortedDict([ (field_order[key], subforms[field_order[key]]) for key in sorted(field_order.keys()) if field_order[key] in subforms
                                      ])
        ordered_formsets = SortedDict([ (field_order[key], formsets[field_order[key]]) for key in sorted(field_order.keys()) if field_order[key] in formsets
                                      ])
    return (ordered_fields, ordered_subforms, ordered_formsets, subform_labels)


def xmlobject_to_dict(instance, fields=None, exclude=None, prefix=b''):
    """
    Generate a dictionary based on the data in an XmlObject instance to pass as
    a Form's ``initial`` keyword argument.

    :param instance: instance of :class:`~eulxml.xmlmap.XmlObject`
    :param fields: optional list of fields - if specified, only the named fields
            will be included in the data returned
    :param exclude: optional list of fields to exclude from the data
    """
    data = {}
    if prefix:
        prefix = b'%s-' % prefix
    else:
        prefix = b''
    for name, field in six.iteritems(instance._fields):
        if fields and name not in fields:
            continue
        if exclude and name in exclude:
            continue
        if isinstance(field, xmlmap.fields.NodeField):
            nodefield = getattr(instance, name)
            if nodefield is not None:
                subprefix = b'%s%s' % (prefix, name)
                node_data = xmlobject_to_dict(nodefield, prefix=subprefix)
                data.update(node_data)
        if isinstance(field, xmlmap.fields.NodeListField):
            for i, child in enumerate(getattr(instance, name)):
                subprefix = b'%s%s-%d' % (prefix, name, i)
                node_data = xmlobject_to_dict(child, prefix=subprefix)
                data.update(node_data)

        else:
            data[prefix + name] = getattr(instance, name)

    return data


class XmlObjectFormType(type):
    """
    Metaclass for :class:`XmlObject`.

    Analogous to, and substantially based on, Django's ``ModelFormMetaclass``.

    Initializes the XmlObjectForm based on the :class:`~eulxml.xmlmap.XmlObject`
    instance associated as a model. Adds form fields for supported
    :class:`~eulxml.xmlmap.fields.Field`s and 'subform' XmlObjectForm classes
    for any :class:`~eulxml.xmlmap.fields.NodeField` to the Form object.
    """

    def __new__(cls, name, bases, attrs):
        tmp_fields = get_declared_fields(bases, attrs, with_base_fields=False)
        declared_fields = {}
        declared_subforms = {}
        declared_subform_labels = {}
        for fname, f in six.iteritems(tmp_fields):
            if isinstance(f, SubformField):
                declared_subforms[fname] = f.formclass
                if hasattr(f, b'form_label') and f.form_label is not None:
                    declared_subform_labels[fname] = f.form_label
                elif hasattr(f.formclass, b'form_label') and f.formclass.form_label is not None:
                    declared_subform_labels[fname] = f.formclass.form_label
            else:
                declared_fields[fname] = f

        new_class = super(XmlObjectFormType, cls).__new__(cls, name, bases, attrs)
        opts = new_class._meta = SubformAwareModelFormOptions(getattr(new_class, b'Meta', None))
        if opts.model:
            fields, subforms, formsets, subform_labels = formfields_for_xmlobject(opts.model, options=opts, declared_subforms=declared_subforms)
            fields.update(declared_fields)
            new_class.subforms = subforms
            new_class.formsets = formsets
            subform_labels.update(declared_subform_labels)
            new_class.subform_labels = subform_labels
        else:
            fields = declared_fields
            new_class.subforms = {}
            new_class.formsets = {}
        new_class.declared_fields = declared_fields
        new_class.base_fields = fields
        return new_class


class XmlObjectForm(six.with_metaclass(XmlObjectFormType, BaseForm)):
    """Django Form based on an :class:`~eulxml.xmlmap.XmlObject` model,
    analogous to Django's ModelForm.

    Note that not all :mod:`eulxml.xmlmap.fields` are currently supported; all
    released field types are supported in their single-node variety, but no list
    field types are currently supported.  Attempting to define an XmlObjectForm
    without excluding unsupported fields will result in an Exception.

    Unlike Django's ModelForm, which provides a save() method, XmlObjectForm
    provides analogous functionality via :meth:`update_instance`.  Since an
    XmlObject by itself does not have a save method, and can only be saved
    in particular contexts, there is no general way for an XmlObjectForm to
    save an associated model instance to the appropriate datastore.

    If you wish to customize the html display for an XmlObjectForm, rather than
    using the built-in form display functions, be aware that if your XmlObject
    has any fields of type :class:`~eulxml.xmlmap.fields.NodeField`, you should
    make sure to display the subforms for those fields.

    NOTE: If your XmlObject includes NodeField elements and you do not want
    empty elements in your XML output when empty values are entered into the form,
    you may wish to extend :meth:`eulxml.xmlmap.XmlObject.is_empty` to correctly
    identify when your NodeField elements should be considered empty (if the
    default definition is not accurate or appropriate).  Empty elements will not
    be added to the :class:`eulxml.xmlmap.XmlObject` instance returned by
    :meth:`update_instance`.
    """
    _html_section = None
    subforms = {}
    form_label = None

    def __init__(self, data=None, instance=None, prefix=None, initial={}, **kwargs):
        opts = self._meta
        local_initial = initial.copy()
        if instance is None:
            if opts.model is None:
                raise ValueError(b'XmlObjectForm has no XmlObject model class specified')
            self.instance = opts.model()
        else:
            self.instance = instance
            local_initial.update(xmlobject_to_dict(self.instance))
        self.instance.xmlschema
        self._init_subforms(data, prefix)
        self._init_formsets(data, prefix)
        super_init = super(XmlObjectForm, self).__init__
        super_init(data=data, prefix=prefix, initial=local_initial, **kwargs)
        return

    def _init_subforms(self, data=None, prefix=None):
        self.subforms = SortedDict()
        for name, subform in six.iteritems(self.__class__.subforms):
            if self.instance is not None:
                getattr(self.instance, b'create_' + name)()
                subinstance = getattr(self.instance, name, None)
            else:
                subinstance = None
            if prefix:
                subprefix = b'%s-%s' % (prefix, name)
            else:
                subprefix = name
            newform = subform(data=data, instance=subinstance, prefix=subprefix)
            if newform.form_label is None:
                if name in self.subform_labels:
                    newform.form_label = self.subform_labels[name]
            self.subforms[name] = newform

        return

    def _init_formsets(self, data=None, prefix=None):
        self.formsets = {}
        for name, formset in six.iteritems(self.__class__.formsets):
            if self.instance is not None:
                subinstances = getattr(self.instance, name, None)
            else:
                subinstances = None
            if prefix is not None:
                subprefix = b'%s-%s' % (prefix, name)
            else:
                subprefix = name
            self.formsets[name] = formset(data=data, instances=subinstances, prefix=subprefix)

        return

    def update_instance(self):
        """Save bound form data into the XmlObject model instance and return the
        updated instance."""
        if hasattr(self, b'cleaned_data'):
            opts = self._meta
            fields_in_order = []
            if hasattr(self.Meta, b'fields'):
                fields_in_order.extend(self.Meta.fields)
                fields_in_order.extend([ name for name in six.iterkeys(self.instance._fields) if name in self.Meta.fields
                                       ])
            else:
                fields_in_order = self.instance._fields.keys()
            for name in fields_in_order:
                if opts.fields and name not in opts.parsed_fields.fields:
                    continue
                if opts.exclude and name in opts.parsed_exclude.fields:
                    continue
                if name in self.cleaned_data:
                    if self.cleaned_data[name] == b'':
                        self.cleaned_data[name] = None
                    setattr(self.instance, name, self.cleaned_data[name])

            for name, subform in six.iteritems(self.subforms):
                self._update_subinstance(name, subform)

            for formset in six.itervalues(self.formsets):
                formset.update_instance()

        return self.instance

    def _update_subinstance(self, name, subform):
        """Save bound data for a single subform into the XmlObject model
        instance."""
        old_subinstance = getattr(self.instance, name)
        new_subinstance = subform.update_instance()
        if old_subinstance is None and not new_subinstance.is_empty():
            setattr(self.instance, name, new_subinstance)
        if old_subinstance is not None and new_subinstance.is_empty():
            delattr(self.instance, name)
        return

    def is_valid(self):
        """Returns True if this form and all subforms (if any) are valid.

        If all standard form-validation tests pass, uses :class:`~eulxml.xmlmap.XmlObject`
        validation methods to check for schema-validity (if a schema is associated)
        and reporting errors.  Additonal notes:

         * schema validation requires that the :class:`~eulxml.xmlmap.XmlObject`
           be initialized with the cleaned form data, so if normal validation
           checks pass, the associated :class:`~eulxml.xmlmap.XmlObject` instance
           will be updated with data via :meth:`update_instance`
         * schema validation errors SHOULD NOT happen in a production system

        :rtype: boolean
        """
        valid = super(XmlObjectForm, self).is_valid() and all(s.is_valid() for s in six.itervalues(self.subforms)) and all(s.is_valid() for s in six.itervalues(self.formsets))
        if valid and self.instance is not None:
            instance = self.update_instance()
            if instance.is_valid():
                return True
            if NON_FIELD_ERRORS not in self._errors:
                self._errors[NON_FIELD_ERRORS] = self.error_class()
            self._errors[NON_FIELD_ERRORS].append(b'There was an unexpected schema validation error.  ' + b'This should not happen!  Please report the following errors:')
            for err in instance.validation_errors():
                self._errors[NON_FIELD_ERRORS].append(b'VALIDATION ERROR: %s' % err.message)

            return False
        return valid

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        """Extend BaseForm's helper function for outputting HTML. Used by as_table(), as_ul(), as_p().

        Combines the HTML version of the main form's fields with the HTML content
        for any subforms.
        """
        parts = []
        parts.append(super(XmlObjectForm, self)._html_output(normal_row, error_row, row_ender, help_text_html, errors_on_separate_row))

        def _subform_output(subform):
            return subform._html_output(normal_row, error_row, row_ender, help_text_html, errors_on_separate_row)

        for name, subform in six.iteritems(self.subforms):
            if hasattr(subform, b'form_label'):
                name = subform.form_label
            parts.append(self._html_subform_output(subform, name, _subform_output))

        for name, formset in six.iteritems(self.formsets):
            parts.append(u(formset.management_form))
            if hasattr(formset.forms[0], b'form_label') and formset.forms[0].form_label is not None:
                name = formset.forms[0].form_label
            else:
                if hasattr(formset, b'form_label'):
                    name = formset.form_label
                subform_parts = list()
                for subform in formset.forms:
                    subform_parts.append(self._html_subform_output(subform, gen_html=_subform_output, suppress_section=True))

            parts.append(self._html_subform_output(name=name, content=(b'\n').join(subform_parts)))

        return mark_safe((b'\n').join(parts))

    def _html_subform_output(self, subform=None, name=None, gen_html=None, content=None, suppress_section=False):
        if subform is not None:
            subform._html_section = self._html_section
            if gen_html is not None:
                content = gen_html(subform)
        if self._html_section is not None and not suppress_section:
            return self._html_section % {b'label': fieldname_to_label(name), b'content': content}
        else:
            return content
            return

    def as_table(self):
        """Behaves exactly the same as Django Form's as_table() method,
        except that it also includes the fields for any associated subforms
        in table format.

        Subforms, if any, will be grouped in a <tbody> labeled with a heading
        based on the label of the field.
        """
        self._html_section = b'<tbody><tr><th colspan="2" class="section">%(label)s</th></tr><tr><td colspan="2"><table class="subform">\n%(content)s</table></td></tr></tbody>'
        return super(XmlObjectForm, self).as_table()

    def as_p(self):
        """Behaves exactly the same as Django Form's as_p() method,
        except that it also includes the fields for any associated subforms
        in paragraph format.

        Subforms, if any, will be grouped in a <div> of class 'subform',
        with a heading based on the label of the field.
        """
        self._html_section = b'<div class="subform"><p class="label">%(label)s</p>%(content)s</div>'
        return super(XmlObjectForm, self).as_p()

    def as_ul(self):
        """Behaves exactly the same as Django Form's as_ul() method,
        except that it also includes the fields for any associated subforms
        in list format.

        Subforms, if any, will be grouped in a <ul> of class 'subform',
        with a heading based on the label of the field.
        """
        self._html_section = b'<li class="subform"><p class="label">%(label)s</p><ul>%(content)s</ul></li>'
        return super(XmlObjectForm, self).as_ul()


def xmlobjectform_factory(model, form=XmlObjectForm, fields=None, exclude=None, widgets=None, max_num=None, label=None, can_delete=True, extra=None, can_order=False):
    """Dynamically generate a new :class:`XmlObjectForm` class using the
    specified :class:`eulxml.xmlmap.XmlObject` class.

    Based on django's modelform_factory.
    """
    attrs = {b'model': model}
    if fields is not None:
        attrs[b'fields'] = fields
    if exclude is not None:
        attrs[b'exclude'] = exclude
    if widgets is not None:
        attrs[b'widgets'] = widgets
    if max_num is not None:
        attrs[b'max_num'] = max_num
    if extra is not None:
        attrs[b'extra'] = extra
    if can_delete is not None:
        attrs[b'can_delete'] = can_delete
    if can_order is not None:
        attrs[b'can_order'] = can_order
    parent = (
     object,)
    if hasattr(form, b'Meta'):
        parent = (
         form.Meta, object)
    Meta = type(str(b'Meta'), parent, attrs)
    class_name = model.__name__ + str(b'XmlObjectForm')
    form_class_attrs = {b'Meta': Meta, 
       b'form_label': label}
    return XmlObjectFormType(class_name, (form,), form_class_attrs)


class BaseXmlObjectFormSet(BaseFormSet):

    def __init__(self, instances, **kwargs):
        self.instances = instances
        if b'initial' not in kwargs:
            kwargs[b'initial'] = [ xmlobject_to_dict(instance) for instance in instances ]
        super_init = super(BaseXmlObjectFormSet, self).__init__
        super_init(**kwargs)

    def _construct_form(self, i, **kwargs):
        try:
            defaults = {b'instance': self.instances[i]}
        except:
            defaults = {}

        defaults.update(kwargs)
        super_construct = super(BaseXmlObjectFormSet, self)._construct_form
        return super_construct(i, **defaults)

    def update_instance(self):
        for form in getattr(self, b'deleted_forms', []):
            if form.instance in self.instances:
                self.instances.remove(form.instance)

        if self.can_order:
            for form in self.ordered_forms:
                if form.instance in self.instances:
                    self.instances.remove(form.instance)
                form.update_instance()
                self.instances.append(form.instance)

        else:
            for form in self.initial_forms:
                if form.has_changed():
                    form.update_instance()

            for form in self.extra_forms:
                if form.has_changed():
                    form.update_instance()
                    self.instances.append(form.instance)


class SubformField(Field):
    """This is a pseudo-form field: use to override the form class of a subform or
    formset that belongs to an :class:`XmlObjectForm`.

    Note that if you specify a list of fields, the subform or formset needs to
    be included in that list or it will not be displayed when the form is generated.

    Example usage::

        class MyFormPart(XmlObjectForm):
            id = StringField(label='my id', required=False)
            ...

        class MyForm(XmlObjectForm):
            part = SubformField(formclass=MyFormPart)
            ...

    In this example, the subform ``part`` on an instance of **MyForm** will be
    created as an instance of **MyFormPart**.
    """

    def __init__(self, formclass=None, label=None, can_delete=True, can_order=False, *args, **kwargs):
        if formclass is not None:
            self.formclass = formclass
        if label is not None:
            self.form_label = label
        self.can_delete = can_delete
        self.can_order = can_order
        super(SubformField, self).__init__(*args, **kwargs)
        return


class ListFieldForm(Form):
    """Basic, single-input form to use for non-nodelist xmlmap list field formsets"""
    val = CharField(label=b'', required=False)

    def __init__(self, instance=None, *args, **kwargs):
        if instance is not None:
            kwargs[b'initial'] = {b'val': instance}
        super(ListFieldForm, self).__init__(*args, **kwargs)
        return

    @property
    def value(self):
        cleaned_data = self.clean()
        if b'val' in cleaned_data:
            return cleaned_data[b'val']


class IntegerListFieldForm(ListFieldForm):
    """Extend :class:`ListFieldForm` and set input field to be an IntegerField"""
    val = IntegerField(label=b'', required=False)


class BaseXmlObjectListFieldFormSet(BaseFormSet):
    """Formset class for non-node-based xmlmap list fields (e.g., string & integer list fields)"""

    def __init__(self, instances, **kwargs):
        self.instance = instances
        super(BaseXmlObjectListFieldFormSet, self).__init__(**kwargs)

    def initial_form_count(self):
        return len(self.instance)

    def _construct_form(self, i, **kwargs):
        try:
            defaults = {b'instance': self.instance[i]}
        except:
            defaults = {}

        defaults.update(kwargs)
        return super(BaseXmlObjectListFieldFormSet, self)._construct_form(i, **defaults)

    def update_instance(self):
        values = [ form.value for form in self.forms if form.value ]
        while len(self.instance):
            self.instance.pop()

        self.instance.extend(values)