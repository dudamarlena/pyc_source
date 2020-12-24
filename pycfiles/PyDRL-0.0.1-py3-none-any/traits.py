# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\traits102\traits.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
from __future__ import nested_scopes
from types import NoneType, IntType, LongType, FloatType, ComplexType, StringType, UnicodeType, ListType, TupleType, DictType, FunctionType, ClassType, MethodType, InstanceType, TypeType, BooleanType
from trait_base import SequenceTypes, Undefined, Self, trait_editors, class_of, TraitNotifier
from trait_errors import TraitError, DelegationError
from trait_handlers import TraitHandler, TraitReadOnly, TraitInstance, TraitFunction, TraitType, TraitEnum, TraitComplex, TraitMap, TraitString, AnyValue, TraitThisClass
from trait_delegates import TraitGetterSetter, TraitDelegate
from trait_notifiers import InstanceTraitNotifier, ClassTraitNotifier
ConstantTypes = (
 NoneType, IntType, LongType, FloatType, ComplexType,
 StringType, UnicodeType)
PythonTypes = (
 StringType, UnicodeType, IntType, LongType,
 FloatType, ComplexType, ListType, TupleType,
 DictType, FunctionType, MethodType, ClassType,
 InstanceType, TypeType, NoneType)
TypeTypes = (
 StringType, UnicodeType, IntType, LongType,
 FloatType, ComplexType, ListType, TupleType,
 DictType, BooleanType)
ClassTypes = (
 ClassType, TypeType)
CallableTypes = (
 FunctionType, MethodType)
CopyTypes = (
 ListType, DictType)
try:
    False
except NameError:
    False, True = (0, 1)

class Trait():

    def __init__(self, default_value, *value_type, **keywords):
        setter = None
        is_getter_setter = isinstance(default_value, TraitGetterSetter)
        if is_getter_setter:
            getter = default_value
            default_value = Undefined
        else:
            getter = self
        if len(value_type) == 0 and type(default_value) in SequenceTypes:
            default_value, value_type = default_value[0], default_value
        if len(value_type) == 0:
            if is_getter_setter:
                setter = getter
            elif isinstance(default_value, Trait):
                dic = default_value.__dict__.copy()
                dic.update(keywords)
                keywords = dic
            elif isinstance(default_value, TraitHandler):
                setter = default_value
                default_value = None
            else:
                typeValue = type(default_value)
                if typeValue is ClassType:
                    if default_value is TraitThisClass:
                        setter = TraitThisClass()
                        default_value = None
                    else:
                        setter = TraitInstance(default_value)
                        default_value = None
                elif typeValue is InstanceType:
                    setter = TraitInstance(default_value.__class__)
                elif typeValue is StringType:
                    setter = TraitString(keywords)
                elif typeValue in TypeTypes:
                    setter = TraitType(typeValue)
                elif type(typeValue) is TypeType:
                    setter = TraitInstance(default_value)
                    default_value = None
                else:
                    setter = TraitInstance(default_value.__class__)
        else:
            enum = []
            other = []
            map = {}
            self.do_list(value_type, enum, map, other)
            if default_value is None and len(enum) == 1 and enum[0] is None and len(other) == 1 and isinstance(other[0], TraitInstance):
                enum = []
            if len(enum) > 0:
                other.append(TraitEnum(enum))
            if len(map) > 0:
                other.append(TraitMap(map))
            if len(other) == 0:
                setter = TraitHandler()
            elif len(other) == 1:
                setter = other[0]
                if isinstance(setter, TraitGetterSetter):
                    getter = setter
                elif isinstance(setter, Trait):
                    dic = setter.__dict__.copy()
                    dic.update(keywords)
                    dic['default_value'] = default_value
                    keywords = dic
                elif default_value is None and isinstance(setter, TraitInstance):
                    setter.allow_none()
            else:
                setter = TraitComplex(other)
            self.default_value = default_value
            self.getter = getter
            self.setter = setter
            for name, value in keywords.items():
                setattr(self, name, value)

        if setter is not None and getattr(setter, 'metadata', None) is not None:
            for name, value in setter.metadata().items():
                setattr(self, name, value)

        return

    def __getattr__(self, name):
        if name[0:2] == '__':
            raise AttributeError, "%s instance has no attribute '%s'" % (
             self.__class__.__name__, name)
        return

    def do_list(self, list, enum, map, other):
        for item in list:
            if item in PythonTypes:
                other.append(TraitType(item))
            else:
                typeItem = type(item)
                if typeItem in ConstantTypes:
                    enum.append(item)
                elif typeItem in SequenceTypes:
                    self.do_list(item, enum, map, other)
                elif typeItem is DictType:
                    map.update(item)
                elif typeItem in CallableTypes:
                    other.append(TraitFunction(item))
                elif item is TraitThisClass:
                    other.append(TraitThisClass())
                elif isinstance(item, TraitHandler) or isinstance(item, TraitGetterSetter) or isinstance(item, Trait):
                    other.append(item)
                elif typeItem in ClassTypes:
                    other.append(TraitInstance(item))
                else:
                    other.append(TraitHandler())

    def getattr(self, object, name, value):
        if value is Self:
            return object
        if type(value) not in CopyTypes:
            return object.__setattr__(name, value)
        if type(value) is ListType:
            return object.__setattr__(name, value[:])
        return object.__setattr__(name, value.copy())

    def get_editor(self):
        if self.editor is None:
            try:
                self.editor = self.setter.get_editor(self)
            except:
                pass

        return self.editor


class PythonTrait(Trait):

    def __init__(self):
        self.default_value = None
        self.getter = self
        self.setter = self
        return

    def getattr(self, object, name, value):
        raise AttributeError, "%s instance has no attribute '%s'" % (
         object.__class__.__name__, name)

    def setattr(self, object, name, value, default):
        object.__dict__[name] = value
        return value


class MappedTrait(Trait):

    def __init__(self):
        self.default_value = None
        self.getter = self
        self.setter = AnyValue
        return

    def getattr(self, object, name, value):
        getattr(object, name[:-1])
        return object.__dict__[name]


Disallow = TraitDelegate()
ReadOnly = Trait(Undefined, TraitReadOnly())
DefaultPythonTrait = PythonTrait()
TheMappedTrait = MappedTrait()

class SimpleTest():

    def __init__(self, value):
        self.value = value

    def __call__(self, test):
        return test == self.value


class HasTraits():
    __traits__ = {'*': DefaultPythonTrait}

    def __init__(self, **traits):
        for name, value in traits.items():
            setattr(self, name, value)

    def __delattr__(self, name):
        try:
            del self.__dict__[name]
            self.__getattr__(name)
        except KeyError:
            return

    def __getattr__(self, name):
        try:
            trait = self.__traits__[name]
            getattr = trait.getter.getattr
        except (AttributeError, KeyError):
            trait = self._trait(name)
            getattr = trait.getter.getattr

        try:
            return getattr(self, name, trait.default_value)
        except DelegationError as excp:
            raise DelegationError, excp
        except TraitError as excp:
            raise TraitError, '%s %s' % (str(excp)[:-1],
             'as the default value. The trait must be assigned a valid value before being used.')

    def __setattr__(self, name, value):
        try:
            trait = self.__traits__[name]
            return trait.setter.setattr(self, name, value, trait.default_value)
        except (AttributeError, KeyError):
            trait = self._trait(name)
            try:
                return trait.setter.setattr(self, name, value, trait.default_value)
            except TraitError as excp:
                excp.set_desc(trait.desc)
                raise TraitError, excp

        except TraitError as excp:
            excp.set_desc(trait.desc)
            raise TraitError, excp

    def __call__(self, showHelp=0):
        names = self._trait_names()
        if len(names) == 0:
            return ''
        result = []
        pad = max([ len(x) for x in names ]) + 1
        maxval = 78 - pad
        names.sort()
        for name in names:
            try:
                value = repr(getattr(self, name)).replace('\n', '\\n')
                if len(value) > maxval:
                    value = '%s...%s' % (value[:(maxval - 2) // 2],
                     value[-((maxval - 3) // 2):])
            except:
                value = '<undefined>'

            lname = (name + ':').ljust(pad)
            if showHelp:
                result.append('%s %s\n   The value must be %s.' % (
                 lname, value, self._base_trait(name).setter.info()))
            else:
                result.append('%s %s' % (lname, value))

        print ('\n').join(result)

    def set(self, **traits):
        for name, value in traits.items():
            setattr(self, name, value)

        return self

    def reset_traits(self, traits=None):
        unresetable = []
        if traits is None:
            traits = self._trait_names()
        for name in traits:
            try:
                delattr(self, name)
            except AttributeError:
                unresetable.append(name)

        return unresetable

    def clone_traits(self, other, traits=None):
        unassignable = []
        if traits is None:
            traits = self._trait_names()
        for name in traits:
            try:
                setattr(self, name, getattr(other, name))
            except:
                unassignable.append(name)

        return unassignable

    def traits(self, **metadata):
        result = []
        for meta_name, meta_eval in metadata.items():
            if type(meta_eval) is not FunctionType:
                metadata[meta_name] = SimpleTest(meta_eval)

        for name in self._trait_names():
            trait = self._trait(name)
            for meta_name, meta_eval in metadata.items():
                if not meta_eval(getattr(trait, meta_name)):
                    break
            else:
                result.append(name)

        return result

    def edit_traits(self, traits=None):
        trait_editors().TraitSheetDialog(self, traits)

    def configure_traits(self, filename=None, edit=True, traits=None):
        if filename is not None:
            fd = None
            try:
                import cPickle
                fd = open(filename, 'rb')
                self.clone_traits(cPickle.Unpickler(fd).load())
            except:
                if fd is not None:
                    fd.close()

        if edit:
            try:
                clone = self.__class__()
                clone.clone_traits(self)
            except:
                clone = None

            app = trait_editors().TraitSheetApp(self, traits)
            if not app.save_ok and clone is not None:
                self.clone_traits(clone)
            elif filename is not None and app.save_ok:
                fd = None
                try:
                    import cPickle
                    fd = open(filename, 'wb')
                    cPickle.Pickler(fd, True).dump(self)
                except:
                    if fd is not None:
                        fd.close()
                    return False

        return True

    def editable_traits(self):
        try:
            return self.__editable_traits__
        except:
            names = self._trait_names()
            names.sort()
            return names

    def add_trait(self, name, trait):
        self.__traits__[name] = trait
        if name[-1:] == '*':
            self._init_class_list()

    def get_trait(self, name):
        return self._trait(name)

    def sync_trait(self, trait_name, object, alias=None, mutual=True):
        if alias is None:
            alias = trait_name
        self.on_trait_change(lambda value: setattr(object, alias, value), trait_name)
        if mutual:
            object.on_trait_change(lambda value: setattr(self, trait_name, value), alias)
        return

    def on_trait_change(self, handler, trait_name=None, remove=False):
        trait_name = trait_name or 'anytrait'
        dict = self.__dict__
        notifiers = dict.get(TraitNotifier, None)
        if remove:
            if notifiers is not None:
                notifiers.remove(handler, trait_name)
            return
        if notifiers is None:
            dict[TraitNotifier] = notifiers = InstanceTraitNotifier(self, self.__class__.__dict__.get(TraitNotifier))
            notifiers.reset_trait_value(self)
        notifiers.add(handler, trait_name)
        return

    def defer_trait_change(self, defer=True):
        self._object_notifier().defer_trait_change(self, defer)

    def _object_notifier(self):
        notifier = self.__dict__.get(TraitNotifier)
        if notifier is not None:
            return notifier
        else:
            return self._class_notifier()

    def _notifier_for(self, name):
        return self._class_notifier().notifier_for(name)

    def _event_notifier_for(self, name):
        return self._class_notifier().event_notifier_for(name)

    def _class_notifier(self):
        cls = self.__class__
        notifier = cls.__dict__.get(TraitNotifier)
        if notifier is None:
            notifier = ClassTraitNotifier(cls)
            setattr(cls, TraitNotifier, notifier)
        return notifier

    def _reset_trait_value(self):
        self._object_notifier().reset_trait_value(self)

    def _set_trait_value(self, object, name, value, default):
        self._reset_trait_value()
        return self._set_trait_value(object, name, value, default)

    def _set_event_value(self, object, name, value, default):
        self._reset_trait_value()
        return self._set_event_value(object, name, value, default)

    def _trait_names(self):
        return [ x for x in self.__traits__.keys() if x[-1:] not in '*_' and x[:1] != '_'
               ]

    def _trait(self, name):
        trait = self.__traits__.get(name)
        if isinstance(trait, Trait):
            return trait
        else:
            traits = self.__traits__
            if trait is None:
                class_list = traits.get('**')
                if class_list is None:
                    self._init_class_list()
                    return self._trait(name)
                if name[-1:] == '_':
                    trait = self._trait(name[:-1])
                    setter = trait.setter
                    if isinstance(setter, TraitDelegate):
                        traits[name] = trait
                        return trait
                    if isinstance(setter, TraitHandler) and setter.is_mapped():
                        try:
                            traits[name] = trait = Trait(setter.map.get(trait.default_value), setter.reverse())
                        except:
                            traits[name] = trait = TheMappedTrait

                        return trait
                for cls in class_list:
                    if cls == name[:len(cls)]:
                        trait = traits[(cls + '*')]
                        break

            else:
                trait = Trait(trait)
            traits[name] = trait
            return trait

    def _base_trait(self, name):
        trait = self._trait(name)
        if isinstance(trait.setter, TraitDelegate):
            return trait.setter.base_trait(self, name)
        return trait

    def _init_class_list(self):
        traits = self.__traits__
        class_list = traits.get('**')
        if class_list is None:
            traits = {}
            self._inherit(self.__class__, traits)
            self.__class__.__traits__ = traits
        class_list = []
        trait = traits.get('*')
        if trait is None:
            traits['*'] = trait = DefaultPythonTrait
        else:
            if not isinstance(trait, Trait):
                traits['*'] = trait = Trait(trait)
            traits['__*'] = DefaultPythonTrait
            for key, trait in traits.items():
                if key[-1:] == '*':
                    class_list.append(key[:-1])
                    if not isinstance(trait, Trait):
                        traits[key] = Trait(trait)

        class_list.sort(lambda x, y: len(y) - len(x))
        traits['**'] = class_list
        return

    def _inherit(self, cls, traits):
        has_traits = cls is HasTraits
        if not has_traits:
            for base in cls.__bases__:
                has_traits |= self._inherit(base, traits)

        if has_traits:
            traits.update(cls.__traits__)
        return has_traits


class _MetaTraits(type):

    def __new__(cls, name, bases, classdict):
        traits = classdict.get('__traits__')
        for name, value in classdict.items():
            if isinstance(value, Trait):
                if traits is None:
                    classdict['__traits__'] = traits = {}
                traits[name] = value
                del classdict[name]

        return super(_MetaTraits, cls).__new__(cls, name, bases, classdict)


class HasObjectTraits(HasTraits, object):
    __metaclass__ = _MetaTraits


class HasDynamicTraits(HasTraits):

    def __init__(self, **traits):
        if self.__traits__.get('**') is None:
            self._init_class_list()
        self.__traits__ = self.__traits__.copy()
        HasTraits.__init__(self, **traits)
        return


class HasDynamicObjectTraits(HasDynamicTraits, object):
    __metaclass__ = _MetaTraits


class TraitProxy(HasDynamicTraits):

    def __init__(self, object, *trait_names):
        HasDynamicTraits.__init__(self)
        self._object = object
        delegate = TraitDelegate('_object', True)
        for trait_name in trait_names:
            self.add_trait(trait_name, delegate)

    def anytrait_changed(self, trait_name, old, new):
        setattr(self._object, trait_name, new)


import trait_handlers
trait_handlers.Trait = Trait
import trait_delegates
trait_delegates.HasTraits = HasTraits