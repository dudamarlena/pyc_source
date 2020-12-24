# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/libgenerateDS/gui/generateds_gui_session.py
# Compiled at: 2019-11-29 14:56:28
# Size of source mod 2**32: 61028 bytes
import sys, re as re_, base64, datetime as datetime_, warnings as warnings_
from lxml import etree as etree_
Validate_simpletypes_ = True
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        parser = etree_.ETCompatXMLParser()
    doc = (etree_.parse)(infile, parser=parser, **kwargs)
    return doc


try:
    from generatedssuper import GeneratedsSuper
except ImportError as exp:
    try:

        class GeneratedsSuper(object):
            tzoff_pattern = re_.compile('(\\+|-)((0\\d|1[0-3]):[0-5]\\d|14:00)$')

            class _FixedOffsetTZ(datetime_.tzinfo):

                def __init__(self, offset, name):
                    self._FixedOffsetTZ__offset = datetime_.timedelta(minutes=offset)
                    self._FixedOffsetTZ__name = name

                def utcoffset(self, dt):
                    return self._FixedOffsetTZ__offset

                def tzname(self, dt):
                    return self._FixedOffsetTZ__name

                def dst(self, dt):
                    pass

            def gds_format_string(self, input_data, input_name=''):
                return input_data

            def gds_validate_string(self, input_data, node=None, input_name=''):
                if not input_data:
                    return ''
                return input_data

            def gds_format_base64(self, input_data, input_name=''):
                return base64.b64encode(input_data)

            def gds_validate_base64(self, input_data, node=None, input_name=''):
                return input_data

            def gds_format_integer(self, input_data, input_name=''):
                return '%d' % input_data

            def gds_validate_integer(self, input_data, node=None, input_name=''):
                return input_data

            def gds_format_integer_list(self, input_data, input_name=''):
                return '%s' % ' '.join(input_data)

            def gds_validate_integer_list(self, input_data, node=None, input_name=''):
                values = input_data.split()
                for value in values:
                    try:
                        int(value)
                    except (TypeError, ValueError):
                        raise_parse_error(node, 'Requires sequence of integers')

                return values

            def gds_format_float(self, input_data, input_name=''):
                return ('%.15f' % input_data).rstrip('0')

            def gds_validate_float(self, input_data, node=None, input_name=''):
                return input_data

            def gds_format_float_list(self, input_data, input_name=''):
                return '%s' % ' '.join(input_data)

            def gds_validate_float_list(self, input_data, node=None, input_name=''):
                values = input_data.split()
                for value in values:
                    try:
                        float(value)
                    except (TypeError, ValueError):
                        raise_parse_error(node, 'Requires sequence of floats')

                return values

            def gds_format_double(self, input_data, input_name=''):
                return '%e' % input_data

            def gds_validate_double(self, input_data, node=None, input_name=''):
                return input_data

            def gds_format_double_list(self, input_data, input_name=''):
                return '%s' % ' '.join(input_data)

            def gds_validate_double_list(self, input_data, node=None, input_name=''):
                values = input_data.split()
                for value in values:
                    try:
                        float(value)
                    except (TypeError, ValueError):
                        raise_parse_error(node, 'Requires sequence of doubles')

                return values

            def gds_format_boolean(self, input_data, input_name=''):
                return ('%s' % input_data).lower()

            def gds_validate_boolean(self, input_data, node=None, input_name=''):
                return input_data

            def gds_format_boolean_list(self, input_data, input_name=''):
                return '%s' % ' '.join(input_data)

            def gds_validate_boolean_list(self, input_data, node=None, input_name=''):
                values = input_data.split()
                for value in values:
                    if value not in ('true', '1', 'false', '0'):
                        raise_parse_error(node, 'Requires sequence of booleans ("true", "1", "false", "0")')

                return values

            def gds_validate_datetime(self, input_data, node=None, input_name=''):
                return input_data

            def gds_format_datetime(self, input_data, input_name=''):
                if input_data.microsecond == 0:
                    _svalue = '%04d-%02d-%02dT%02d:%02d:%02d' % (
                     input_data.year,
                     input_data.month,
                     input_data.day,
                     input_data.hour,
                     input_data.minute,
                     input_data.second)
                else:
                    _svalue = '%04d-%02d-%02dT%02d:%02d:%02d.%s' % (
                     input_data.year,
                     input_data.month,
                     input_data.day,
                     input_data.hour,
                     input_data.minute,
                     input_data.second,
                     ('%f' % (float(input_data.microsecond) / 1000000))[2:])
                if input_data.tzinfo is not None:
                    tzoff = input_data.tzinfo.utcoffset(input_data)
                    if tzoff is not None:
                        total_seconds = tzoff.seconds + 86400 * tzoff.days
                        if total_seconds == 0:
                            _svalue += 'Z'
                        else:
                            if total_seconds < 0:
                                _svalue += '-'
                                total_seconds *= -1
                            else:
                                _svalue += '+'
                            hours = total_seconds // 3600
                            minutes = (total_seconds - hours * 3600) // 60
                            _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
                return _svalue

            @classmethod
            def gds_parse_datetime(cls, input_data):
                tz = None
                if input_data[(-1)] == 'Z':
                    tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                    input_data = input_data[:-1]
                else:
                    results = GeneratedsSuper.tzoff_pattern.search(input_data)
                    if results is not None:
                        tzoff_parts = results.group(2).split(':')
                        tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                        if results.group(1) == '-':
                            tzoff *= -1
                        tz = GeneratedsSuper._FixedOffsetTZ(tzoff, results.group(0))
                        input_data = input_data[:-6]
                    else:
                        time_parts = input_data.split('.')
                        if len(time_parts) > 1:
                            micro_seconds = int(float('0.' + time_parts[1]) * 1000000)
                            input_data = '%s.%s' % (time_parts[0], micro_seconds)
                            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%dT%H:%M:%S.%f')
                        else:
                            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%dT%H:%M:%S')
                    dt = dt.replace(tzinfo=tz)
                    return dt

            def gds_validate_date(self, input_data, node=None, input_name=''):
                return input_data

            def gds_format_date(self, input_data, input_name=''):
                _svalue = '%04d-%02d-%02d' % (
                 input_data.year,
                 input_data.month,
                 input_data.day)
                try:
                    if input_data.tzinfo is not None:
                        tzoff = input_data.tzinfo.utcoffset(input_data)
                        if tzoff is not None:
                            total_seconds = tzoff.seconds + 86400 * tzoff.days
                            if total_seconds == 0:
                                _svalue += 'Z'
                            else:
                                if total_seconds < 0:
                                    _svalue += '-'
                                    total_seconds *= -1
                                else:
                                    _svalue += '+'
                                hours = total_seconds // 3600
                                minutes = (total_seconds - hours * 3600) // 60
                                _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
                except AttributeError:
                    pass

                return _svalue

            @classmethod
            def gds_parse_date(cls, input_data):
                tz = None
                if input_data[(-1)] == 'Z':
                    tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                    input_data = input_data[:-1]
                else:
                    results = GeneratedsSuper.tzoff_pattern.search(input_data)
                    if results is not None:
                        tzoff_parts = results.group(2).split(':')
                        tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                        if results.group(1) == '-':
                            tzoff *= -1
                        tz = GeneratedsSuper._FixedOffsetTZ(tzoff, results.group(0))
                        input_data = input_data[:-6]
                dt = datetime_.datetime.strptime(input_data, '%Y-%m-%d')
                dt = dt.replace(tzinfo=tz)
                return dt.date()

            def gds_validate_time(self, input_data, node=None, input_name=''):
                return input_data

            def gds_format_time(self, input_data, input_name=''):
                if input_data.microsecond == 0:
                    _svalue = '%02d:%02d:%02d' % (
                     input_data.hour,
                     input_data.minute,
                     input_data.second)
                else:
                    _svalue = '%02d:%02d:%02d.%s' % (
                     input_data.hour,
                     input_data.minute,
                     input_data.second,
                     ('%f' % (float(input_data.microsecond) / 1000000))[2:])
                if input_data.tzinfo is not None:
                    tzoff = input_data.tzinfo.utcoffset(input_data)
                    if tzoff is not None:
                        total_seconds = tzoff.seconds + 86400 * tzoff.days
                        if total_seconds == 0:
                            _svalue += 'Z'
                        else:
                            if total_seconds < 0:
                                _svalue += '-'
                                total_seconds *= -1
                            else:
                                _svalue += '+'
                            hours = total_seconds // 3600
                            minutes = (total_seconds - hours * 3600) // 60
                            _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
                return _svalue

            def gds_validate_simple_patterns(self, patterns, target):
                found1 = True
                for patterns1 in patterns:
                    found2 = False
                    for patterns2 in patterns1:
                        if re_.search(patterns2, target) is not None:
                            found2 = True
                            break

                    if not found2:
                        found1 = False
                        break

                return found1

            @classmethod
            def gds_parse_time(cls, input_data):
                tz = None
                if input_data[(-1)] == 'Z':
                    tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                    input_data = input_data[:-1]
                else:
                    results = GeneratedsSuper.tzoff_pattern.search(input_data)
                    if results is not None:
                        tzoff_parts = results.group(2).split(':')
                        tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                        if results.group(1) == '-':
                            tzoff *= -1
                        tz = GeneratedsSuper._FixedOffsetTZ(tzoff, results.group(0))
                        input_data = input_data[:-6]
                    elif len(input_data.split('.')) > 1:
                        dt = datetime_.datetime.strptime(input_data, '%H:%M:%S.%f')
                    else:
                        dt = datetime_.datetime.strptime(input_data, '%H:%M:%S')
                    dt = dt.replace(tzinfo=tz)
                    return dt.time()

            def gds_str_lower(self, instring):
                return instring.lower()

            def get_path_(self, node):
                path_list = []
                self.get_path_list_(node, path_list)
                path_list.reverse()
                path = '/'.join(path_list)
                return path

            Tag_strip_pattern_ = re_.compile('\\{.*\\}')

            def get_path_list_(self, node, path_list):
                if node is None:
                    return
                tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
                if tag:
                    path_list.append(tag)
                self.get_path_list_(node.getparent(), path_list)

            def get_class_obj_(self, node, default_class=None):
                class_obj1 = default_class
                if 'xsi' in node.nsmap:
                    classname = node.get('{%s}type' % node.nsmap['xsi'])
                    if classname is not None:
                        names = classname.split(':')
                        if len(names) == 2:
                            classname = names[1]
                        class_obj2 = globals().get(classname)
                        if class_obj2 is not None:
                            class_obj1 = class_obj2
                return class_obj1

            def gds_build_any(self, node, type_name=None):
                pass

            @classmethod
            def gds_reverse_node_mapping(cls, mapping):
                return dict(((v, k) for k, v in mapping.iteritems()))

            @staticmethod
            def gds_encode(instring):
                if sys.version_info.major == 2:
                    return instring.encode(ExternalEncoding)
                return instring


        def getSubclassFromModule_(module, class_):
            """Get the subclass of a class from a specific module."""
            name = class_.__name__ + 'Sub'
            if hasattr(module, name):
                return getattr(module, name)
            return


    finally:
        exp = None
        del exp

ExternalEncoding = 'ascii'
Tag_pattern_ = re_.compile('({.*})?(.*)')
String_cleanup_pat_ = re_.compile('[\\n\\r\\s]+')
Namespace_extract_pat_ = re_.compile('{(.*)}(.*)')
CDATA_pattern_ = re_.compile('<!\\[CDATA\\[.*?\\]\\]>', re_.DOTALL)
CurrentSubclassModule_ = None

def showIndent(outfile, level, pretty_print=True):
    if pretty_print:
        for idx in range(level):
            outfile.write('    ')


def quote_xml(inStr):
    """Escape markup chars, but do not modify CDATA sections."""
    if not inStr:
        return ''
    s1 = isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr
    s2 = ''
    pos = 0
    matchobjects = CDATA_pattern_.finditer(s1)
    for mo in matchobjects:
        s3 = s1[pos:mo.start()]
        s2 += quote_xml_aux(s3)
        s2 += s1[mo.start():mo.end()]
        pos = mo.end()

    s3 = s1[pos:]
    s2 += quote_xml_aux(s3)
    return s2


def quote_xml_aux(inStr):
    s1 = inStr.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1


def quote_attrib(inStr):
    s1 = isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', '&quot;')
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1


def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail

    return text


def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    else:
        if len(attr_parts) == 2:
            prefix, name = attr_parts
            namespace = node.nsmap.get(prefix)
            if namespace is not None:
                value = attrs.get('{%s}%s' % (namespace, name))
    return value


class GDSParseError(Exception):
    pass


def raise_parse_error(node, msg):
    msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline)
    raise GDSParseError(msg)


class MixedContainer:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    TypeBase64 = 8

    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value

    def getCategory(self):
        return self.category

    def getContenttype(self, content_type):
        return self.content_type

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def export(self, outfile, level, name, namespace, pretty_print=True):
        if self.category == MixedContainer.CategoryText:
            if self.value.strip():
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:
            self.value.export(outfile, level, namespace, name, pretty_print)

    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (
             self.name, self.value, self.name))
        else:
            if self.content_type == MixedContainer.TypeInteger or self.content_type == MixedContainer.TypeBoolean:
                outfile.write('<%s>%d</%s>' % (
                 self.name, self.value, self.name))
            else:
                if self.content_type == MixedContainer.TypeFloat or self.content_type == MixedContainer.TypeDecimal:
                    outfile.write('<%s>%f</%s>' % (
                     self.name, self.value, self.name))
                else:
                    if self.content_type == MixedContainer.TypeDouble:
                        outfile.write('<%s>%g</%s>' % (
                         self.name, self.value, self.name))
                    else:
                        if self.content_type == MixedContainer.TypeBase64:
                            outfile.write('<%s>%s</%s>' % (
                             self.name, base64.b64encode(self.value), self.name))

    def to_etree(self, element):
        if self.category == MixedContainer.CategoryText:
            if self.value.strip():
                if len(element) > 0:
                    if element[(-1)].tail is None:
                        element[(-1)].tail = self.value
                    else:
                        element[(-1)].tail += self.value
                elif element.text is None:
                    element.text = self.value
                else:
                    element.text += self.value
        elif self.category == MixedContainer.CategorySimple:
            subelement = etree_.SubElement(element, '%s' % self.name)
            subelement.text = self.to_etree_simple()
        else:
            self.value.to_etree(element)

    def to_etree_simple(self):
        if self.content_type == MixedContainer.TypeString:
            text = self.value
        else:
            if self.content_type == MixedContainer.TypeInteger or self.content_type == MixedContainer.TypeBoolean:
                text = '%d' % self.value
            else:
                if self.content_type == MixedContainer.TypeFloat or self.content_type == MixedContainer.TypeDecimal:
                    text = '%f' % self.value
                else:
                    if self.content_type == MixedContainer.TypeDouble:
                        text = '%g' % self.value
                    else:
                        if self.content_type == MixedContainer.TypeBase64:
                            text = '%s' % base64.b64encode(self.value)
        return text

    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write('model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
             self.category, self.content_type, self.name, self.value))
        else:
            if self.category == MixedContainer.CategorySimple:
                showIndent(outfile, level)
                outfile.write('model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                 self.category, self.content_type, self.name, self.value))
            else:
                showIndent(outfile, level)
                outfile.write('model_.MixedContainer(%d, %d, "%s",\n' % (
                 self.category, self.content_type, self.name))
                self.value.exportLiteral(outfile, level + 1)
                showIndent(outfile, level)
                outfile.write(')\n')


class MemberSpec_(object):

    def __init__(self, name='', data_type='', container=0):
        self.name = name
        self.data_type = data_type
        self.container = container

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_data_type(self, data_type):
        self.data_type = data_type

    def get_data_type_chain(self):
        return self.data_type

    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[(-1)]
            return 'xs:string'
        else:
            return self.data_type

    def set_container(self, container):
        self.container = container

    def get_container(self):
        return self.container


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)


class SessionTypeMixin(object):

    def copy(self):
        """Produce a copy of myself.
        """
        new_session = sessionType(input_schema=(self.input_schema),
          output_superclass=(self.output_superclass),
          output_subclass=(self.output_subclass),
          force=(self.force),
          prefix=(self.prefix),
          namespace_prefix=(self.namespace_prefix),
          empty_namespace_prefix=(self.empty_namespace_prefix),
          behavior_filename=(self.behavior_filename),
          properties=(self.properties),
          subclass_suffix=(self.subclass_suffix),
          root_element=(self.root_element),
          superclass_module=(self.superclass_module),
          auto_super=(self.auto_super),
          old_getters_setters=(self.old_getters_setters),
          validator_bodies=(self.validator_bodies),
          user_methods=(self.user_methods),
          no_dates=(self.no_dates),
          no_versions=(self.no_versions),
          no_process_includes=(self.no_process_includes),
          silence=(self.silence),
          namespace_defs=(self.namespace_defs),
          external_encoding=(self.external_encoding),
          member_specs=(self.member_specs),
          export_spec=(self.export_spec),
          one_file_per_xsd=(self.one_file_per_xsd),
          output_directory=(self.output_directory),
          module_suffix=(self.module_suffix),
          preserve_cdata_tags=(self.preserve_cdata_tags),
          cleanup_name_list=(self.cleanup_name_list))
        return new_session

    def __eq__(self, obj):
        """Implement the == operator.
        """
        if obj.input_schema == self.input_schema:
            if obj.output_superclass == self.output_superclass:
                if obj.output_subclass == self.output_subclass:
                    if obj.force == self.force:
                        if obj.prefix == self.prefix:
                            if obj.namespace_prefix == self.namespace_prefix:
                                if obj.empty_namespace_prefix == self.empty_namespace_prefix:
                                    if obj.behavior_filename == self.behavior_filename:
                                        if obj.properties == self.properties:
                                            if obj.subclass_suffix == self.subclass_suffix:
                                                if obj.root_element == self.root_element:
                                                    if obj.superclass_module == self.superclass_module:
                                                        if obj.auto_super == self.auto_super:
                                                            if obj.old_getters_setters == self.old_getters_setters:
                                                                if obj.validator_bodies == self.validator_bodies:
                                                                    if obj.user_methods == self.user_methods:
                                                                        if obj.no_dates == self.no_dates:
                                                                            if obj.no_versions == self.no_versions:
                                                                                if obj.no_process_includes == self.no_process_includes:
                                                                                    if obj.silence == self.silence:
                                                                                        if obj.namespace_defs == self.namespace_defs:
                                                                                            if obj.external_encoding == self.external_encoding:
                                                                                                if obj.member_specs == self.member_specs:
                                                                                                    if obj.export_spec == self.export_spec:
                                                                                                        if obj.one_file_per_xsd == self.one_file_per_xsd:
                                                                                                            if obj.output_directory == self.output_directory:
                                                                                                                if obj.module_suffix == self.module_suffix:
                                                                                                                    if obj.preserve_cdata_tags == self.preserve_cdata_tags:
                                                                                                                        if obj.cleanup_name_list == self.cleanup_name_list:
                                                                                                                            return True
        return False

    def __ne__(self, obj):
        """Implement the != operator.
        """
        return not self.__eq__(obj)


class sessionType(GeneratedsSuper, SessionTypeMixin):
    member_data_items_ = [
     MemberSpec_('input_schema', 'xs:string', 0),
     MemberSpec_('output_superclass', 'xs:string', 0),
     MemberSpec_('output_subclass', 'xs:string', 0),
     MemberSpec_('force', 'xs:boolean', 0),
     MemberSpec_('prefix', 'xs:string', 0),
     MemberSpec_('namespace_prefix', 'xs:string', 0),
     MemberSpec_('empty_namespace_prefix', 'xs:boolean', 0),
     MemberSpec_('behavior_filename', 'xs:string', 0),
     MemberSpec_('properties', 'xs:boolean', 0),
     MemberSpec_('subclass_suffix', 'xs:string', 0),
     MemberSpec_('root_element', 'xs:string', 0),
     MemberSpec_('superclass_module', 'xs:string', 0),
     MemberSpec_('auto_super', 'xs:boolean', 0),
     MemberSpec_('old_getters_setters', 'xs:boolean', 0),
     MemberSpec_('validator_bodies', 'xs:string', 0),
     MemberSpec_('user_methods', 'xs:string', 0),
     MemberSpec_('no_dates', 'xs:boolean', 0),
     MemberSpec_('no_versions', 'xs:boolean', 0),
     MemberSpec_('no_process_includes', 'xs:boolean', 0),
     MemberSpec_('silence', 'xs:boolean', 0),
     MemberSpec_('namespace_defs', 'xs:string', 0),
     MemberSpec_('external_encoding', 'xs:string', 0),
     MemberSpec_('get_encoded', 'xs:boolean', 0),
     MemberSpec_('member_specs', 'xs:string', 0),
     MemberSpec_('export_spec', 'xs:string', 0),
     MemberSpec_('one_file_per_xsd', 'xs:boolean', 0),
     MemberSpec_('output_directory', 'xs:string', 0),
     MemberSpec_('module_suffix', 'xs:string', 0),
     MemberSpec_('preserve_cdata_tags', 'xs:boolean', 0),
     MemberSpec_('cleanup_name_list', 'xs:string', 0)]
    subclass = None
    superclass = None

    def __init__(self, input_schema=None, output_superclass=None, output_subclass=None, force=None, prefix=None, namespace_prefix=None, empty_namespace_prefix=None, behavior_filename=None, properties=None, subclass_suffix=None, root_element=None, superclass_module=None, auto_super=None, old_getters_setters=None, validator_bodies=None, user_methods=None, no_dates=None, no_versions=None, no_process_includes=None, silence=None, namespace_defs=None, external_encoding=None, get_encoded=None, member_specs=None, export_spec=None, one_file_per_xsd=None, output_directory=None, module_suffix=None, preserve_cdata_tags=None, cleanup_name_list=None):
        self.original_tagname_ = None
        self.input_schema = input_schema
        self.output_superclass = output_superclass
        self.output_subclass = output_subclass
        self.force = force
        self.prefix = prefix
        self.namespace_prefix = namespace_prefix
        self.empty_namespace_prefix = empty_namespace_prefix
        self.behavior_filename = behavior_filename
        self.properties = properties
        self.subclass_suffix = subclass_suffix
        self.root_element = root_element
        self.superclass_module = superclass_module
        self.auto_super = auto_super
        self.old_getters_setters = old_getters_setters
        self.validator_bodies = validator_bodies
        self.user_methods = user_methods
        self.no_dates = no_dates
        self.no_versions = no_versions
        self.no_process_includes = no_process_includes
        self.silence = silence
        self.namespace_defs = namespace_defs
        self.external_encoding = external_encoding
        self.get_encoded = get_encoded
        self.member_specs = member_specs
        self.export_spec = export_spec
        self.one_file_per_xsd = one_file_per_xsd
        self.output_directory = output_directory
        self.module_suffix = module_suffix
        self.preserve_cdata_tags = preserve_cdata_tags
        self.cleanup_name_list = cleanup_name_list

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, sessionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if sessionType.subclass:
            return (sessionType.subclass)(*args_, **kwargs_)
        return sessionType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_input_schema(self):
        return self.input_schema

    def set_input_schema(self, input_schema):
        self.input_schema = input_schema

    def get_output_superclass(self):
        return self.output_superclass

    def set_output_superclass(self, output_superclass):
        self.output_superclass = output_superclass

    def get_output_subclass(self):
        return self.output_subclass

    def set_output_subclass(self, output_subclass):
        self.output_subclass = output_subclass

    def get_force(self):
        return self.force

    def set_force(self, force):
        self.force = force

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix

    def get_namespace_prefix(self):
        return self.namespace_prefix

    def set_namespace_prefix(self, namespace_prefix):
        self.namespace_prefix = namespace_prefix

    def get_empty_namespace_prefix(self):
        return self.empty_namespace_prefix

    def set_empty_namespace_prefix(self, empty_namespace_prefix):
        self.empty_namespace_prefix = empty_namespace_prefix

    def get_behavior_filename(self):
        return self.behavior_filename

    def set_behavior_filename(self, behavior_filename):
        self.behavior_filename = behavior_filename

    def get_properties(self):
        return self.properties

    def set_properties(self, properties):
        self.properties = properties

    def get_subclass_suffix(self):
        return self.subclass_suffix

    def set_subclass_suffix(self, subclass_suffix):
        self.subclass_suffix = subclass_suffix

    def get_root_element(self):
        return self.root_element

    def set_root_element(self, root_element):
        self.root_element = root_element

    def get_superclass_module(self):
        return self.superclass_module

    def set_superclass_module(self, superclass_module):
        self.superclass_module = superclass_module

    def get_auto_super(self):
        return self.auto_super

    def set_auto_super(self, auto_super):
        self.auto_super = auto_super

    def get_old_getters_setters(self):
        return self.old_getters_setters

    def set_old_getters_setters(self, old_getters_setters):
        self.old_getters_setters = old_getters_setters

    def get_validator_bodies(self):
        return self.validator_bodies

    def set_validator_bodies(self, validator_bodies):
        self.validator_bodies = validator_bodies

    def get_user_methods(self):
        return self.user_methods

    def set_user_methods(self, user_methods):
        self.user_methods = user_methods

    def get_no_dates(self):
        return self.no_dates

    def set_no_dates(self, no_dates):
        self.no_dates = no_dates

    def get_no_versions(self):
        return self.no_versions

    def set_no_versions(self, no_versions):
        self.no_versions = no_versions

    def get_no_process_includes(self):
        return self.no_process_includes

    def set_no_process_includes(self, no_process_includes):
        self.no_process_includes = no_process_includes

    def get_silence(self):
        return self.silence

    def set_silence(self, silence):
        self.silence = silence

    def get_namespace_defs(self):
        return self.namespace_defs

    def set_namespace_defs(self, namespace_defs):
        self.namespace_defs = namespace_defs

    def get_external_encoding(self):
        return self.external_encoding

    def set_external_encoding(self, external_encoding):
        self.external_encoding = external_encoding

    def get_get_encoded(self):
        return self.get_encoded

    def set_get_encoded(self, get_encoded):
        self.get_encoded = get_encoded

    def get_member_specs(self):
        return self.member_specs

    def set_member_specs(self, member_specs):
        self.member_specs = member_specs

    def get_export_spec(self):
        return self.export_spec

    def set_export_spec(self, export_spec):
        self.export_spec = export_spec

    def get_one_file_per_xsd(self):
        return self.one_file_per_xsd

    def set_one_file_per_xsd(self, one_file_per_xsd):
        self.one_file_per_xsd = one_file_per_xsd

    def get_output_directory(self):
        return self.output_directory

    def set_output_directory(self, output_directory):
        self.output_directory = output_directory

    def get_module_suffix(self):
        return self.module_suffix

    def set_module_suffix(self, module_suffix):
        self.module_suffix = module_suffix

    def get_preserve_cdata_tags(self):
        return self.preserve_cdata_tags

    def set_preserve_cdata_tags(self, preserve_cdata_tags):
        self.preserve_cdata_tags = preserve_cdata_tags

    def get_cleanup_name_list(self):
        return self.cleanup_name_list

    def set_cleanup_name_list(self, cleanup_name_list):
        self.cleanup_name_list = cleanup_name_list

    def hasContent_--- This code section failed: ---

 L. 865         0  LOAD_FAST                'self'
                2  LOAD_ATTR                input_schema
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
             8_10  POP_JUMP_IF_TRUE    360  'to 360'

 L. 866        12  LOAD_FAST                'self'
               14  LOAD_ATTR                output_superclass
               16  LOAD_CONST               None
               18  COMPARE_OP               is-not
            20_22  POP_JUMP_IF_TRUE    360  'to 360'

 L. 867        24  LOAD_FAST                'self'
               26  LOAD_ATTR                output_subclass
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
            32_34  POP_JUMP_IF_TRUE    360  'to 360'

 L. 868        36  LOAD_FAST                'self'
               38  LOAD_ATTR                force
               40  LOAD_CONST               None
               42  COMPARE_OP               is-not
            44_46  POP_JUMP_IF_TRUE    360  'to 360'

 L. 869        48  LOAD_FAST                'self'
               50  LOAD_ATTR                prefix
               52  LOAD_CONST               None
               54  COMPARE_OP               is-not
            56_58  POP_JUMP_IF_TRUE    360  'to 360'

 L. 870        60  LOAD_FAST                'self'
               62  LOAD_ATTR                namespace_prefix
               64  LOAD_CONST               None
               66  COMPARE_OP               is-not
            68_70  POP_JUMP_IF_TRUE    360  'to 360'

 L. 871        72  LOAD_FAST                'self'
               74  LOAD_ATTR                empty_namespace_prefix
               76  LOAD_CONST               None
               78  COMPARE_OP               is-not
            80_82  POP_JUMP_IF_TRUE    360  'to 360'

 L. 872        84  LOAD_FAST                'self'
               86  LOAD_ATTR                behavior_filename
               88  LOAD_CONST               None
               90  COMPARE_OP               is-not
            92_94  POP_JUMP_IF_TRUE    360  'to 360'

 L. 873        96  LOAD_FAST                'self'
               98  LOAD_ATTR                properties
              100  LOAD_CONST               None
              102  COMPARE_OP               is-not
          104_106  POP_JUMP_IF_TRUE    360  'to 360'

 L. 874       108  LOAD_FAST                'self'
              110  LOAD_ATTR                subclass_suffix
              112  LOAD_CONST               None
              114  COMPARE_OP               is-not
          116_118  POP_JUMP_IF_TRUE    360  'to 360'

 L. 875       120  LOAD_FAST                'self'
              122  LOAD_ATTR                root_element
              124  LOAD_CONST               None
              126  COMPARE_OP               is-not
          128_130  POP_JUMP_IF_TRUE    360  'to 360'

 L. 876       132  LOAD_FAST                'self'
              134  LOAD_ATTR                superclass_module
              136  LOAD_CONST               None
              138  COMPARE_OP               is-not
          140_142  POP_JUMP_IF_TRUE    360  'to 360'

 L. 877       144  LOAD_FAST                'self'
              146  LOAD_ATTR                auto_super
              148  LOAD_CONST               None
              150  COMPARE_OP               is-not
          152_154  POP_JUMP_IF_TRUE    360  'to 360'

 L. 878       156  LOAD_FAST                'self'
              158  LOAD_ATTR                old_getters_setters
              160  LOAD_CONST               None
              162  COMPARE_OP               is-not
          164_166  POP_JUMP_IF_TRUE    360  'to 360'

 L. 879       168  LOAD_FAST                'self'
              170  LOAD_ATTR                validator_bodies
              172  LOAD_CONST               None
              174  COMPARE_OP               is-not
          176_178  POP_JUMP_IF_TRUE    360  'to 360'

 L. 880       180  LOAD_FAST                'self'
              182  LOAD_ATTR                user_methods
              184  LOAD_CONST               None
              186  COMPARE_OP               is-not
          188_190  POP_JUMP_IF_TRUE    360  'to 360'

 L. 881       192  LOAD_FAST                'self'
              194  LOAD_ATTR                no_dates
              196  LOAD_CONST               None
              198  COMPARE_OP               is-not
          200_202  POP_JUMP_IF_TRUE    360  'to 360'

 L. 882       204  LOAD_FAST                'self'
              206  LOAD_ATTR                no_versions
              208  LOAD_CONST               None
              210  COMPARE_OP               is-not
          212_214  POP_JUMP_IF_TRUE    360  'to 360'

 L. 883       216  LOAD_FAST                'self'
              218  LOAD_ATTR                no_process_includes
              220  LOAD_CONST               None
              222  COMPARE_OP               is-not
          224_226  POP_JUMP_IF_TRUE    360  'to 360'

 L. 884       228  LOAD_FAST                'self'
              230  LOAD_ATTR                silence
              232  LOAD_CONST               None
              234  COMPARE_OP               is-not
          236_238  POP_JUMP_IF_TRUE    360  'to 360'

 L. 885       240  LOAD_FAST                'self'
              242  LOAD_ATTR                namespace_defs
              244  LOAD_CONST               None
              246  COMPARE_OP               is-not
          248_250  POP_JUMP_IF_TRUE    360  'to 360'

 L. 886       252  LOAD_FAST                'self'
              254  LOAD_ATTR                external_encoding
              256  LOAD_CONST               None
              258  COMPARE_OP               is-not
          260_262  POP_JUMP_IF_TRUE    360  'to 360'

 L. 887       264  LOAD_FAST                'self'
              266  LOAD_ATTR                get_encoded
              268  LOAD_CONST               None
              270  COMPARE_OP               is-not
          272_274  POP_JUMP_IF_TRUE    360  'to 360'

 L. 888       276  LOAD_FAST                'self'
              278  LOAD_ATTR                member_specs
              280  LOAD_CONST               None
              282  COMPARE_OP               is-not
          284_286  POP_JUMP_IF_TRUE    360  'to 360'

 L. 889       288  LOAD_FAST                'self'
              290  LOAD_ATTR                export_spec
              292  LOAD_CONST               None
              294  COMPARE_OP               is-not
          296_298  POP_JUMP_IF_TRUE    360  'to 360'

 L. 890       300  LOAD_FAST                'self'
              302  LOAD_ATTR                one_file_per_xsd
              304  LOAD_CONST               None
              306  COMPARE_OP               is-not
          308_310  POP_JUMP_IF_TRUE    360  'to 360'

 L. 891       312  LOAD_FAST                'self'
              314  LOAD_ATTR                output_directory
              316  LOAD_CONST               None
              318  COMPARE_OP               is-not
          320_322  POP_JUMP_IF_TRUE    360  'to 360'

 L. 892       324  LOAD_FAST                'self'
              326  LOAD_ATTR                module_suffix
              328  LOAD_CONST               None
              330  COMPARE_OP               is-not
          332_334  POP_JUMP_IF_TRUE    360  'to 360'

 L. 893       336  LOAD_FAST                'self'
              338  LOAD_ATTR                preserve_cdata_tags
              340  LOAD_CONST               None
              342  COMPARE_OP               is-not
          344_346  POP_JUMP_IF_TRUE    360  'to 360'

 L. 894       348  LOAD_FAST                'self'
              350  LOAD_ATTR                cleanup_name_list
              352  LOAD_CONST               None
              354  COMPARE_OP               is-not
          356_358  POP_JUMP_IF_FALSE   364  'to 364'
            360_0  COME_FROM           344  '344'
            360_1  COME_FROM           332  '332'
            360_2  COME_FROM           320  '320'
            360_3  COME_FROM           308  '308'
            360_4  COME_FROM           296  '296'
            360_5  COME_FROM           284  '284'
            360_6  COME_FROM           272  '272'
            360_7  COME_FROM           260  '260'
            360_8  COME_FROM           248  '248'
            360_9  COME_FROM           236  '236'
           360_10  COME_FROM           224  '224'
           360_11  COME_FROM           212  '212'
           360_12  COME_FROM           200  '200'
           360_13  COME_FROM           188  '188'
           360_14  COME_FROM           176  '176'
           360_15  COME_FROM           164  '164'
           360_16  COME_FROM           152  '152'
           360_17  COME_FROM           140  '140'
           360_18  COME_FROM           128  '128'
           360_19  COME_FROM           116  '116'
           360_20  COME_FROM           104  '104'
           360_21  COME_FROM            92  '92'
           360_22  COME_FROM            80  '80'
           360_23  COME_FROM            68  '68'
           360_24  COME_FROM            56  '56'
           360_25  COME_FROM            44  '44'
           360_26  COME_FROM            32  '32'
           360_27  COME_FROM            20  '20'
           360_28  COME_FROM             8  '8'

 L. 896       360  LOAD_CONST               True
              362  RETURN_VALUE     
            364_0  COME_FROM           356  '356'

 L. 898       364  LOAD_CONST               False
              366  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 364

    def export(self, outfile, level, namespace_='', name_='sessionType', namespacedef_='', pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or ''))
            already_processed = set()
            self.exportAttributes(outfile, level, already_processed, namespace_, name_='sessionType')
            if self.hasContent_():
                outfile.write('>%s' % (eol_,))
                self.exportChildren(outfile, (level + 1), namespace_='', name_='sessionType', pretty_print=pretty_print)
                showIndent(outfile, level, pretty_print)
                outfile.write('</%s%s>%s' % (namespace_, name_, eol_))
            else:
                outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='sessionType'):
        pass

    def exportChildren(self, outfile, level, namespace_='', name_='sessionType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.input_schema is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sinput_schema>%s</%sinput_schema>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.input_schema)), input_name='input_schema')), namespace_, eol_))
        if self.output_superclass is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%soutput_superclass>%s</%soutput_superclass>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.output_superclass)), input_name='output_superclass')), namespace_, eol_))
        if self.output_subclass is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%soutput_subclass>%s</%soutput_subclass>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.output_subclass)), input_name='output_subclass')), namespace_, eol_))
        if self.force is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sforce>%s</%sforce>%s' % (namespace_, self.gds_format_boolean((self.force), input_name='force'), namespace_, eol_))
        if self.prefix is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprefix>%s</%sprefix>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.prefix)), input_name='prefix')), namespace_, eol_))
        if self.namespace_prefix is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snamespace_prefix>%s</%snamespace_prefix>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.namespace_prefix)), input_name='namespace_prefix')), namespace_, eol_))
        if self.empty_namespace_prefix is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sempty_namespace_prefix>%s</%sempty_namespace_prefix>%s' % (namespace_, self.gds_format_boolean((self.empty_namespace_prefix), input_name='empty_namespace_prefix'), namespace_, eol_))
        if self.behavior_filename is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbehavior_filename>%s</%sbehavior_filename>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.behavior_filename)), input_name='behavior_filename')), namespace_, eol_))
        if self.properties is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sproperties>%s</%sproperties>%s' % (namespace_, self.gds_format_boolean((self.properties), input_name='properties'), namespace_, eol_))
        if self.subclass_suffix is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssubclass_suffix>%s</%ssubclass_suffix>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.subclass_suffix)), input_name='subclass_suffix')), namespace_, eol_))
        if self.root_element is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sroot_element>%s</%sroot_element>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.root_element)), input_name='root_element')), namespace_, eol_))
        if self.superclass_module is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssuperclass_module>%s</%ssuperclass_module>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.superclass_module)), input_name='superclass_module')), namespace_, eol_))
        if self.auto_super is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sauto_super>%s</%sauto_super>%s' % (namespace_, self.gds_format_boolean((self.auto_super), input_name='auto_super'), namespace_, eol_))
        if self.old_getters_setters is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sold_getters_setters>%s</%sold_getters_setters>%s' % (namespace_, self.gds_format_boolean((self.old_getters_setters), input_name='old_getters_setters'), namespace_, eol_))
        if self.validator_bodies is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%svalidator_bodies>%s</%svalidator_bodies>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.validator_bodies)), input_name='validator_bodies')), namespace_, eol_))
        if self.user_methods is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%suser_methods>%s</%suser_methods>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.user_methods)), input_name='user_methods')), namespace_, eol_))
        if self.no_dates is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sno_dates>%s</%sno_dates>%s' % (namespace_, self.gds_format_boolean((self.no_dates), input_name='no_dates'), namespace_, eol_))
        if self.no_versions is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sno_versions>%s</%sno_versions>%s' % (namespace_, self.gds_format_boolean((self.no_versions), input_name='no_versions'), namespace_, eol_))
        if self.no_process_includes is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sno_process_includes>%s</%sno_process_includes>%s' % (namespace_, self.gds_format_boolean((self.no_process_includes), input_name='no_process_includes'), namespace_, eol_))
        if self.silence is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssilence>%s</%ssilence>%s' % (namespace_, self.gds_format_boolean((self.silence), input_name='silence'), namespace_, eol_))
        if self.namespace_defs is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snamespace_defs>%s</%snamespace_defs>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.namespace_defs)), input_name='namespace_defs')), namespace_, eol_))
        if self.external_encoding is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sexternal_encoding>%s</%sexternal_encoding>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.external_encoding)), input_name='external_encoding')), namespace_, eol_))
        if self.get_encoded is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sget_encoded>%s</%sget_encoded>%s' % (namespace_, self.gds_format_boolean((self.get_encoded), input_name='get_encoded'), namespace_, eol_))
        if self.member_specs is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smember_specs>%s</%smember_specs>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.member_specs)), input_name='member_specs')), namespace_, eol_))
        if self.export_spec is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sexport_spec>%s</%sexport_spec>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.export_spec)), input_name='export_spec')), namespace_, eol_))
        if self.one_file_per_xsd is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sone_file_per_xsd>%s</%sone_file_per_xsd>%s' % (namespace_, self.gds_format_boolean((self.one_file_per_xsd), input_name='one_file_per_xsd'), namespace_, eol_))
        if self.output_directory is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%soutput_directory>%s</%soutput_directory>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.output_directory)), input_name='output_directory')), namespace_, eol_))
        if self.module_suffix is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smodule_suffix>%s</%smodule_suffix>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.module_suffix)), input_name='module_suffix')), namespace_, eol_))
        if self.preserve_cdata_tags is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spreserve_cdata_tags>%s</%spreserve_cdata_tags>%s' % (namespace_, self.gds_format_boolean((self.preserve_cdata_tags), input_name='preserve_cdata_tags'), namespace_, eol_))
        if self.cleanup_name_list is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scleanup_name_list>%s</%scleanup_name_list>%s' % (namespace_, self.gds_encode(self.gds_format_string((quote_xml(self.cleanup_name_list)), input_name='cleanup_name_list')), namespace_, eol_))

    def build(self, node):
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[(-1)]
            self.buildChildren(child, node, nodeName_)

        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'input_schema':
            input_schema_ = child_.text
            input_schema_ = self.gds_validate_string(input_schema_, node, 'input_schema')
            self.input_schema = input_schema_
        else:
            if nodeName_ == 'output_superclass':
                output_superclass_ = child_.text
                output_superclass_ = self.gds_validate_string(output_superclass_, node, 'output_superclass')
                self.output_superclass = output_superclass_
            else:
                if nodeName_ == 'output_subclass':
                    output_subclass_ = child_.text
                    output_subclass_ = self.gds_validate_string(output_subclass_, node, 'output_subclass')
                    self.output_subclass = output_subclass_
                else:
                    if nodeName_ == 'force':
                        sval_ = child_.text
                        if sval_ in ('true', '1'):
                            ival_ = True
                        else:
                            if sval_ in ('false', '0'):
                                ival_ = False
                            else:
                                raise_parse_error(child_, 'requires boolean')
                        ival_ = self.gds_validate_boolean(ival_, node, 'force')
                        self.force = ival_
                    else:
                        if nodeName_ == 'prefix':
                            prefix_ = child_.text
                            prefix_ = self.gds_validate_string(prefix_, node, 'prefix')
                            self.prefix = prefix_
                        else:
                            if nodeName_ == 'namespace_prefix':
                                namespace_prefix_ = child_.text
                                namespace_prefix_ = self.gds_validate_string(namespace_prefix_, node, 'namespace_prefix')
                                self.namespace_prefix = namespace_prefix_
                            else:
                                if nodeName_ == 'empty_namespace_prefix':
                                    sval_ = child_.text
                                    if sval_ in ('true', '1'):
                                        ival_ = True
                                    else:
                                        if sval_ in ('false', '0'):
                                            ival_ = False
                                        else:
                                            raise_parse_error(child_, 'requires boolean')
                                    ival_ = self.gds_validate_boolean(ival_, node, 'empty_namespace_prefix')
                                    self.empty_namespace_prefix = ival_
                                else:
                                    if nodeName_ == 'behavior_filename':
                                        behavior_filename_ = child_.text
                                        behavior_filename_ = self.gds_validate_string(behavior_filename_, node, 'behavior_filename')
                                        self.behavior_filename = behavior_filename_
                                    else:
                                        if nodeName_ == 'properties':
                                            sval_ = child_.text
                                            if sval_ in ('true', '1'):
                                                ival_ = True
                                            else:
                                                if sval_ in ('false', '0'):
                                                    ival_ = False
                                                else:
                                                    raise_parse_error(child_, 'requires boolean')
                                            ival_ = self.gds_validate_boolean(ival_, node, 'properties')
                                            self.properties = ival_
                                        else:
                                            if nodeName_ == 'subclass_suffix':
                                                subclass_suffix_ = child_.text
                                                subclass_suffix_ = self.gds_validate_string(subclass_suffix_, node, 'subclass_suffix')
                                                self.subclass_suffix = subclass_suffix_
                                            else:
                                                if nodeName_ == 'root_element':
                                                    root_element_ = child_.text
                                                    root_element_ = self.gds_validate_string(root_element_, node, 'root_element')
                                                    self.root_element = root_element_
                                                else:
                                                    if nodeName_ == 'superclass_module':
                                                        superclass_module_ = child_.text
                                                        superclass_module_ = self.gds_validate_string(superclass_module_, node, 'superclass_module')
                                                        self.superclass_module = superclass_module_
                                                    else:
                                                        if nodeName_ == 'auto_super':
                                                            sval_ = child_.text
                                                            if sval_ in ('true', '1'):
                                                                ival_ = True
                                                            else:
                                                                if sval_ in ('false',
                                                                             '0'):
                                                                    ival_ = False
                                                                else:
                                                                    raise_parse_error(child_, 'requires boolean')
                                                            ival_ = self.gds_validate_boolean(ival_, node, 'auto_super')
                                                            self.auto_super = ival_
                                                        else:
                                                            if nodeName_ == 'old_getters_setters':
                                                                sval_ = child_.text
                                                                if sval_ in ('true',
                                                                             '1'):
                                                                    ival_ = True
                                                                else:
                                                                    if sval_ in ('false',
                                                                                 '0'):
                                                                        ival_ = False
                                                                    else:
                                                                        raise_parse_error(child_, 'requires boolean')
                                                                ival_ = self.gds_validate_boolean(ival_, node, 'old_getters_setters')
                                                                self.old_getters_setters = ival_
                                                            else:
                                                                if nodeName_ == 'validator_bodies':
                                                                    validator_bodies_ = child_.text
                                                                    validator_bodies_ = self.gds_validate_string(validator_bodies_, node, 'validator_bodies')
                                                                    self.validator_bodies = validator_bodies_
                                                                else:
                                                                    if nodeName_ == 'user_methods':
                                                                        user_methods_ = child_.text
                                                                        user_methods_ = self.gds_validate_string(user_methods_, node, 'user_methods')
                                                                        self.user_methods = user_methods_
                                                                    else:
                                                                        if nodeName_ == 'no_dates':
                                                                            sval_ = child_.text
                                                                            if sval_ in ('true',
                                                                                         '1'):
                                                                                ival_ = True
                                                                            else:
                                                                                if sval_ in ('false',
                                                                                             '0'):
                                                                                    ival_ = False
                                                                                else:
                                                                                    raise_parse_error(child_, 'requires boolean')
                                                                            ival_ = self.gds_validate_boolean(ival_, node, 'no_dates')
                                                                            self.no_dates = ival_
                                                                        else:
                                                                            if nodeName_ == 'no_versions':
                                                                                sval_ = child_.text
                                                                                if sval_ in ('true',
                                                                                             '1'):
                                                                                    ival_ = True
                                                                                else:
                                                                                    if sval_ in ('false',
                                                                                                 '0'):
                                                                                        ival_ = False
                                                                                    else:
                                                                                        raise_parse_error(child_, 'requires boolean')
                                                                                ival_ = self.gds_validate_boolean(ival_, node, 'no_versions')
                                                                                self.no_versions = ival_
                                                                            else:
                                                                                if nodeName_ == 'no_process_includes':
                                                                                    sval_ = child_.text
                                                                                    if sval_ in ('true',
                                                                                                 '1'):
                                                                                        ival_ = True
                                                                                    else:
                                                                                        if sval_ in ('false',
                                                                                                     '0'):
                                                                                            ival_ = False
                                                                                        else:
                                                                                            raise_parse_error(child_, 'requires boolean')
                                                                                    ival_ = self.gds_validate_boolean(ival_, node, 'no_process_includes')
                                                                                    self.no_process_includes = ival_
                                                                                else:
                                                                                    if nodeName_ == 'silence':
                                                                                        sval_ = child_.text
                                                                                        if sval_ in ('true',
                                                                                                     '1'):
                                                                                            ival_ = True
                                                                                        else:
                                                                                            if sval_ in ('false',
                                                                                                         '0'):
                                                                                                ival_ = False
                                                                                            else:
                                                                                                raise_parse_error(child_, 'requires boolean')
                                                                                        ival_ = self.gds_validate_boolean(ival_, node, 'silence')
                                                                                        self.silence = ival_
                                                                                    else:
                                                                                        if nodeName_ == 'namespace_defs':
                                                                                            namespace_defs_ = child_.text
                                                                                            namespace_defs_ = self.gds_validate_string(namespace_defs_, node, 'namespace_defs')
                                                                                            self.namespace_defs = namespace_defs_
                                                                                        else:
                                                                                            if nodeName_ == 'external_encoding':
                                                                                                external_encoding_ = child_.text
                                                                                                external_encoding_ = self.gds_validate_string(external_encoding_, node, 'external_encoding')
                                                                                                self.external_encoding = external_encoding_
                                                                                            else:
                                                                                                if nodeName_ == 'get_encoded':
                                                                                                    sval_ = child_.text
                                                                                                    if sval_ in ('true',
                                                                                                                 '1'):
                                                                                                        ival_ = True
                                                                                                    else:
                                                                                                        if sval_ in ('false',
                                                                                                                     '0'):
                                                                                                            ival_ = False
                                                                                                        else:
                                                                                                            raise_parse_error(child_, 'requires boolean')
                                                                                                    ival_ = self.gds_validate_boolean(ival_, node, 'get_encoded')
                                                                                                    self.get_encoded = ival_
                                                                                                else:
                                                                                                    if nodeName_ == 'member_specs':
                                                                                                        member_specs_ = child_.text
                                                                                                        member_specs_ = self.gds_validate_string(member_specs_, node, 'member_specs')
                                                                                                        self.member_specs = member_specs_
                                                                                                    else:
                                                                                                        if nodeName_ == 'export_spec':
                                                                                                            export_spec_ = child_.text
                                                                                                            export_spec_ = self.gds_validate_string(export_spec_, node, 'export_spec')
                                                                                                            self.export_spec = export_spec_
                                                                                                        else:
                                                                                                            if nodeName_ == 'one_file_per_xsd':
                                                                                                                sval_ = child_.text
                                                                                                                if sval_ in ('true',
                                                                                                                             '1'):
                                                                                                                    ival_ = True
                                                                                                                else:
                                                                                                                    if sval_ in ('false',
                                                                                                                                 '0'):
                                                                                                                        ival_ = False
                                                                                                                    else:
                                                                                                                        raise_parse_error(child_, 'requires boolean')
                                                                                                                ival_ = self.gds_validate_boolean(ival_, node, 'one_file_per_xsd')
                                                                                                                self.one_file_per_xsd = ival_
                                                                                                            else:
                                                                                                                if nodeName_ == 'output_directory':
                                                                                                                    output_directory_ = child_.text
                                                                                                                    output_directory_ = self.gds_validate_string(output_directory_, node, 'output_directory')
                                                                                                                    self.output_directory = output_directory_
                                                                                                                else:
                                                                                                                    if nodeName_ == 'module_suffix':
                                                                                                                        module_suffix_ = child_.text
                                                                                                                        module_suffix_ = self.gds_validate_string(module_suffix_, node, 'module_suffix')
                                                                                                                        self.module_suffix = module_suffix_
                                                                                                                    else:
                                                                                                                        if nodeName_ == 'preserve_cdata_tags':
                                                                                                                            sval_ = child_.text
                                                                                                                            if sval_ in ('true',
                                                                                                                                         '1'):
                                                                                                                                ival_ = True
                                                                                                                            else:
                                                                                                                                if sval_ in ('false',
                                                                                                                                             '0'):
                                                                                                                                    ival_ = False
                                                                                                                                else:
                                                                                                                                    raise_parse_error(child_, 'requires boolean')
                                                                                                                            ival_ = self.gds_validate_boolean(ival_, node, 'preserve_cdata_tags')
                                                                                                                            self.preserve_cdata_tags = ival_
                                                                                                                        else:
                                                                                                                            if nodeName_ == 'cleanup_name_list':
                                                                                                                                cleanup_name_list_ = child_.text
                                                                                                                                cleanup_name_list_ = self.gds_validate_string(cleanup_name_list_, node, 'cleanup_name_list')
                                                                                                                                self.cleanup_name_list = cleanup_name_list_


GDSClassesMapping = {'session': sessionType}
USAGE_TEXT = '\nUsage: python <Parser>.py [ -s ] <in_xml_file>\n'

def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[(-1)]
    rootClass = GDSClassesMapping.get(tag)
    if rootClass is None:
        rootClass = globals().get(tag)
    return (
     tag, rootClass)


def parse(inFileName, silence=False):
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'sessionType'
        rootClass = sessionType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export((sys.stdout),
          0, name_=rootTag, namespacedef_='',
          pretty_print=True)
    return rootObj


def parseEtree(inFileName, silence=False):
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'sessionType'
        rootClass = sessionType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    doc = None
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not silence:
        content = etree_.tostring(rootElement,
          pretty_print=True, xml_declaration=True,
          encoding='utf-8')
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return (
     rootObj, rootElement, mapping, reverse_mapping)


def parseString(inString, silence=False):
    from StringIO import StringIO
    parser = None
    doc = parsexml_(StringIO(inString), parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'sessionType'
        rootClass = sessionType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export((sys.stdout),
          0, name_=rootTag, namespacedef_='')
    return rootObj


def parseLiteral(inFileName, silence=False):
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'sessionType'
        rootClass = sessionType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    doc = None
    if not silence:
        sys.stdout.write('#from generateds_gui_session import *\n\n')
        sys.stdout.write('import generateds_gui_session as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral((sys.stdout), 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    main()
__all__ = [
 'sessionType']