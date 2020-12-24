# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/db/models.py
# Compiled at: 2020-01-18 01:22:03
# Size of source mod 2**32: 8438 bytes
import json, itertools
from django.db import models
from django import forms
from dyn_struct import datatools
from dyn_struct.db import fields
from dyn_struct.exceptions import CheckClassArgumentsException
from swutils.string import transliterate

class ExcludeDeprecatedManager(models.Manager):

    def get_queryset(self):
        return super(ExcludeDeprecatedManager, self).get_queryset().filter(is_deprecated=False)


class DynamicStructure(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    version = models.PositiveIntegerField(editable=False, default=1)
    is_deprecated = models.BooleanField(editable=False, default=False)
    created = models.DateTimeField(auto_now_add=True)
    objects = ExcludeDeprecatedManager()
    standard_objects = models.Manager()

    class Meta:
        verbose_name = 'динамическая структура'
        verbose_name_plural = 'динамические структуры'
        unique_together = ('name', 'version')
        ordering = ('name', '-version')

    @staticmethod
    def get_verbose(data_json):
        table = []
        if not data_json:
            return table
        data = json.loads(data_json)
        verbose_data = data['verbose_data']
        verbose_data.sort(key=(lambda i: i['row']))
        for i, row in itertools.groupby(verbose_data, lambda i: i['row']):
            row = sorted(row, key=(lambda i: i['position']))
            table.append(row)

        return table

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_field_names(self):
        return list(self.fields.values_list('name', flat=True))

    def get_rows(self, form):
        table = []
        for row_number in self.fields.values_list('row', flat=True).order_by('row').distinct():
            row = []
            for field in self.fields.filter(row=row_number).order_by('position'):
                if not field.is_header():
                    field_name = field.get_transliterate_name()
                    field.bound_field = form[field_name]
                row.append(field)

            table.append(row)

        return table

    def build_form(self, data=None, prefix='data'):
        form = forms.Form(data, prefix=prefix)
        for field in self.fields.exclude(name=''):
            field_name = field.get_transliterate_name()
            form.fields[field_name] = field.build()

        return form

    def clone(self, exclude_field=None):
        self.is_deprecated = True
        self.save()
        fields = list(self.fields.all())
        self.id = None
        self.version += 1
        self.is_deprecated = False
        self.save()
        for field in fields:
            if exclude_field:
                if exclude_field.id:
                    if exclude_field.id == field.id:
                        continue
            field.id = None
            field.structure = self
            field.save()

    def delete(self, using=None):
        self.is_deprecated = True
        self.save()


class DynamicStructureField(models.Model):
    FORM_FIELD_CHOICES = [(field, field) for field in datatools.get_django_fields()]
    WIDGETS_CHOICES = [(widget, widget) for widget in datatools.get_django_widgets()]
    structure = models.ForeignKey(DynamicStructure, verbose_name='Структура', related_name='fields', on_delete=(models.PROTECT))
    header = models.CharField(max_length=100, verbose_name='заголовок', blank=True, help_text='при заполнении этого поля, вместо поля формы будет выводить заголовок')
    name = models.CharField(max_length=512, verbose_name='Название', blank=True)
    form_field = models.CharField(max_length=255, choices=FORM_FIELD_CHOICES, verbose_name='Поле', blank=True)
    form_kwargs = fields.ParamsField(verbose_name='Параметры поля', default='{}')
    widget = models.CharField(max_length=255, choices=WIDGETS_CHOICES, verbose_name='Виджет', blank=True)
    widget_kwargs = fields.ParamsField(verbose_name='Параметры виджета', default='{}')
    row = models.PositiveSmallIntegerField(verbose_name='Строка')
    position = models.PositiveSmallIntegerField(verbose_name='Позиция в строке')
    classes = models.CharField(max_length=255, verbose_name='CSS-классы', help_text='col-md-3, custom-class ...', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'поле динамической структуры'
        verbose_name_plural = 'поля динамических структур'
        unique_together = ('structure', 'name', 'header')
        ordering = ('structure__name', 'row', 'position')

    def __str__(self):
        if self.is_header():
            return self.header
        return self.name

    def __unicode__(self):
        if self.is_header():
            return self.header
        return self.name

    def get_transliterate_name(self):
        return transliterate((self.name), space='_').replace("'", '')

    def is_header(self):
        return bool(self.header)

    def clean--- This code section failed: ---

 L. 148         0  LOAD_FAST                'self'
                2  LOAD_METHOD              is_header
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_JUMP_IF_FALSE    38  'to 38'

 L. 149         8  LOAD_FAST                'self'
               10  LOAD_ATTR                name
               12  POP_JUMP_IF_TRUE     26  'to 26'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                form_field
               18  POP_JUMP_IF_TRUE     26  'to 26'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                widget
               24  POP_JUMP_IF_FALSE   254  'to 254'
             26_0  COME_FROM            18  '18'
             26_1  COME_FROM            12  '12'

 L. 150        26  LOAD_GLOBAL              forms
               28  LOAD_METHOD              ValidationError
               30  LOAD_STR                 'Если указывается заголовок, то поля "Название", "Поле" и "Виджет" указывать не нужно'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  RAISE_VARARGS_1       1  'exception instance'
               36  JUMP_FORWARD        254  'to 254'
             38_0  COME_FROM             6  '6'

 L. 155        38  LOAD_FAST                'self'
               40  LOAD_ATTR                name
               42  POP_JUMP_IF_TRUE     58  'to 58'

 L. 156        44  LOAD_GLOBAL              forms
               46  LOAD_ATTR                ValidationError
               48  LOAD_STR                 'Необходимо указать название'
               50  LOAD_STR                 'invalid'
               52  LOAD_CONST               ('code',)
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            42  '42'

 L. 157        58  LOAD_FAST                'self'
               60  LOAD_ATTR                form_field
               62  POP_JUMP_IF_TRUE     78  'to 78'

 L. 158        64  LOAD_GLOBAL              forms
               66  LOAD_ATTR                ValidationError
               68  LOAD_STR                 'Необходимо указать поле'
               70  LOAD_STR                 'invalid'
               72  LOAD_CONST               ('code',)
               74  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            62  '62'

 L. 160        78  SETUP_EXCEPT        146  'to 146'

 L. 161        80  LOAD_FAST                'self'
               82  LOAD_ATTR                form_kwargs
               84  POP_JUMP_IF_FALSE   104  'to 104'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                form_kwargs
               90  LOAD_STR                 '{}'
               92  COMPARE_OP               !=
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L. 162        96  LOAD_FAST                'self'
               98  LOAD_METHOD              _check_field_arguments
              100  CALL_METHOD_0         0  '0 positional arguments'
              102  POP_TOP          
            104_0  COME_FROM            94  '94'
            104_1  COME_FROM            84  '84'

 L. 164       104  LOAD_FAST                'self'
              106  LOAD_ATTR                widget
              108  POP_JUMP_IF_FALSE   134  'to 134'
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                widget_kwargs
              114  POP_JUMP_IF_FALSE   134  'to 134'
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                widget_kwargs
              120  LOAD_STR                 '{}'
              122  COMPARE_OP               !=
              124  POP_JUMP_IF_FALSE   134  'to 134'

 L. 165       126  LOAD_FAST                'self'
              128  LOAD_METHOD              _check_widget_arguments
              130  CALL_METHOD_0         0  '0 positional arguments'
              132  POP_TOP          
            134_0  COME_FROM           124  '124'
            134_1  COME_FROM           114  '114'
            134_2  COME_FROM           108  '108'

 L. 167       134  LOAD_FAST                'self'
              136  LOAD_METHOD              build
              138  CALL_METHOD_0         0  '0 positional arguments'
              140  POP_TOP          
              142  POP_BLOCK        
              144  JUMP_FORWARD        254  'to 254'
            146_0  COME_FROM_EXCEPT     78  '78'

 L. 169       146  DUP_TOP          
              148  LOAD_GLOBAL              CheckClassArgumentsException
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   196  'to 196'
              154  POP_TOP          
              156  STORE_FAST               'ex'
              158  POP_TOP          
              160  SETUP_FINALLY       184  'to 184'

 L. 170       162  LOAD_GLOBAL              forms
              164  LOAD_ATTR                ValidationError
              166  LOAD_GLOBAL              str
              168  LOAD_FAST                'ex'
              170  CALL_FUNCTION_1       1  '1 positional argument'
              172  LOAD_STR                 'invalid'
              174  LOAD_CONST               ('code',)
              176  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              178  POP_TOP          
              180  POP_BLOCK        
              182  LOAD_CONST               None
            184_0  COME_FROM_FINALLY   160  '160'
              184  LOAD_CONST               None
              186  STORE_FAST               'ex'
              188  DELETE_FAST              'ex'
              190  END_FINALLY      
              192  POP_EXCEPT       
              194  JUMP_FORWARD        254  'to 254'
            196_0  COME_FROM           152  '152'

 L. 171       196  DUP_TOP          
              198  LOAD_GLOBAL              Exception
              200  COMPARE_OP               exception-match
              202  POP_JUMP_IF_FALSE   252  'to 252'
              204  POP_TOP          
              206  STORE_FAST               'ex'
              208  POP_TOP          
              210  SETUP_FINALLY       240  'to 240'

 L. 172       212  LOAD_GLOBAL              forms
              214  LOAD_ATTR                ValidationError
              216  LOAD_STR                 'Не удалось создать поле формы ({})'
              218  LOAD_METHOD              format
              220  LOAD_GLOBAL              str
              222  LOAD_FAST                'ex'
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  LOAD_STR                 'invalid'
              230  LOAD_CONST               ('code',)
              232  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              234  RAISE_VARARGS_1       1  'exception instance'
              236  POP_BLOCK        
              238  LOAD_CONST               None
            240_0  COME_FROM_FINALLY   210  '210'
              240  LOAD_CONST               None
              242  STORE_FAST               'ex'
              244  DELETE_FAST              'ex'
              246  END_FINALLY      
              248  POP_EXCEPT       
              250  JUMP_FORWARD        254  'to 254'
            252_0  COME_FROM           202  '202'
              252  END_FINALLY      
            254_0  COME_FROM           250  '250'
            254_1  COME_FROM           194  '194'
            254_2  COME_FROM           144  '144'
            254_3  COME_FROM            36  '36'
            254_4  COME_FROM            24  '24'

 L. 174       254  LOAD_GLOBAL              json
              256  LOAD_ATTR                dumps
              258  LOAD_GLOBAL              json
              260  LOAD_METHOD              loads
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                widget_kwargs
              266  CALL_METHOD_1         1  '1 positional argument'
              268  LOAD_CONST               4
              270  LOAD_CONST               False
              272  LOAD_CONST               ('indent', 'ensure_ascii')
              274  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              276  LOAD_FAST                'self'
              278  STORE_ATTR               widget_kwargs

 L. 175       280  LOAD_GLOBAL              json
              282  LOAD_ATTR                dumps
              284  LOAD_GLOBAL              json
              286  LOAD_METHOD              loads
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                form_kwargs
              292  CALL_METHOD_1         1  '1 positional argument'
              294  LOAD_CONST               4
              296  LOAD_CONST               False
              298  LOAD_CONST               ('indent', 'ensure_ascii')
              300  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              302  LOAD_FAST                'self'
              304  STORE_ATTR               form_kwargs

Parse error at or near `COME_FROM' instruction at offset 38_0

    def build(self):
        assert self.form_field
        field_kwargs = json.loads(self.form_kwargs) if self.form_kwargs else {}
        if 'label' not in field_kwargs:
            field_kwargs['label'] = self.name
        if self.widget:
            widget_class = getattr(forms.widgets, self.widget)
            widget_kwargs = json.loads(self.widget_kwargs) if self.widget_kwargs else {}
            field_kwargs.update({'widget': widget_class(**widget_kwargs)})
        field_class = getattr(forms.fields, self.form_field)
        field = field_class(**field_kwargs)
        field.name = self.name
        return field

    def _check_field_arguments(self):
        field_class = getattr(forms.fields, self.form_field)
        kwargs = json.loads(self.form_kwargs)
        datatools.check_class_arguments(field_class, kwargs)

    def _check_widget_arguments(self):
        widget_class = getattr(forms.widgets, self.widget)
        kwargs = json.loads(self.widget_kwargs)
        datatools.check_class_arguments(widget_class, kwargs)


class DynamicStructureMixin(object):
    data_field = 'data'

    def get_structure_name(self):
        raise NotImplementedError()

    def get_structure(self):
        structure_name = self.get_structure_name()
        data = getattr(self, self.data_field)
        version = json.loads(data)['version']
        structure = DynamicStructure.standard_objects.get(version=version,
          name=structure_name)
        return structure

    def get_verbose_data(self):
        return self.get_structure().get_verbose(self.data)