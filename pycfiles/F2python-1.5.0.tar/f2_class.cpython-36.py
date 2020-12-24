# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thibault/Work/Recherche/F2/F2Python/F2/f2_class.py
# Compiled at: 2017-04-05 17:17:14
# Size of source mod 2**32: 21935 bytes
"""
F2 Database Interface
---------------------

Definition of class    F 2 _ C l a s s, 

Th. Estier
version 1.2 - june 2005
   --
   written after the original Ada version from 1989-1990, Th. Estier, CUI Geneva.
"""
from . import OFF, metadict
from . import f2_object
F2_NULL = f2_object.F2_NULL
theObject = f2_object.theObject
F2_Object = f2_object.F2_Object
debug = True

class F2_Class(F2_Object):
    __doc__ = 'an F2 object belonging to class CLASS hierarchy'

    def __str__(self):
        return '<%s.%s>' % (OFF.className[self._klass], OFF.className[self._rank])

    def __call__(self, _select={}, _where=None, **selectors):
        """apply an F2 object's selection among instances of a class. """
        selectors.update(_select)
        for k in selectors.keys():
            if type(k) is not str:
                raise f2_object.F2TypeError('F2 class selection: %s uncorrect selector (must be str)' % k)

        if self.is_AtomClass():
            candidates = [
             theObject(metadict.atomClass, self._rank)]
            return f2_object.F2_Object_list(candidates)
        else:
            if self.is_TupleClass():
                thisClass_state_attr = theObject(metadict.Attribute, OFF.classStateAttr[self._rank])
            else:
                raise f2_object.F2TypeError("F2 class %s can't be selected" % self)
            alive_state_ranks = OFF.db_root[thisClass_state_attr._rank].keys()
            if len(selectors) == 0:
                candidates_objs = [theObject(self._rank, x) for x in alive_state_ranks]
            else:
                first_sel, first_val = list(selectors.items())[0]
                first_attr = self._attribute_of(first_sel, self._rank)
                if isinstance(first_val, list) and len(first_val) > 0 and isinstance(first_val[0], F2_Object):
                    check_val = [x._rank for x in first_val]
                else:
                    if isinstance(first_val, F2_Object):
                        check_val = first_val._rank
                    else:
                        check_val = first_val
                    if check_val == F2_NULL:
                        first_attr_keys = list(OFF.db_root[first_attr].keys())
                        candidates_objs = [theObject(self._rank, x) for x in alive_state_ranks if x not in first_attr_keys]
                    else:
                        candidates_objs = [theObject(self._rank, x) for x in OFF.db_root[first_attr].find(check_val)]
                        candidates_objs = [obj for obj in candidates_objs if obj.exist_in(thisClass_state_attr)]
                    for other_sel, other_val in list(selectors.items())[1:]:
                        candidates_objs = [obj for obj in candidates_objs if obj._getattr(other_sel) == other_val]

            if callable(_where):
                candidates_objs = [obj for obj in candidates_objs if _where(obj)]
            return f2_object.F2_Object_list(candidates_objs)

    def root(self):
        """return the specialization root of this class, = self when self is a root."""
        rootC = self._rank
        while OFF.stateSubClass[rootC] != F2_NULL:
            rootC = OFF.superClass[rootC]

        return theClass(rootC)

    def direct_attributes(self):
        """return direct attributes"""
        candidates = OFF.domainClass.find(self._rank)
        return f2_object.F2_Object_list([theObject(metadict.Attribute, a) for a in candidates if OFF.stateAttribute[a] != F2_NULL])

    def all_attributes(self):
        """return all attributes, inherited or not"""
        all_attrs = []
        my_root_rank = self.root()._rank
        this_class_rank = self._rank
        while this_class_rank != my_root_rank:
            all_attrs[:0] = theClass(this_class_rank).direct_attributes()
            this_class_rank = OFF.superClass[this_class_rank]

        result = theClass(this_class_rank).direct_attributes() + all_attrs
        return f2_object.F2_Object_list(result)

    def all_subclasses(self):
        """return all subclasses of this class."""
        candidates = OFF.superClass.find(self._rank)
        direct_subcs = [theClass(c) for c in candidates if OFF.stateSubClass[c] != F2_NULL]
        result = direct_subcs
        for c in direct_subcs:
            result.extend(c.all_subclasses())

        return f2_object.F2_Object_list(result)

    def is_SubClass(self):
        """true when self is instance of SubClass"""
        return OFF.stateSubClass[self._rank] != F2_NULL

    def is_AtomClass(self):
        """true when self is instance of AtomClass"""
        return OFF.stateAtomClass[self._rank] != F2_NULL

    def is_TupleClass(self):
        """true when self is instance of TupleClass"""
        return OFF.stateTupleClass[self._rank] != F2_NULL

    def _initial_segment(self, new_rank):
        """set the initial null values into current segment of self attributes
         (this method is normally not used outside of this module)"""
        state_attr = OFF.classStateAttr[self._rank]
        off_state_attr = OFF.db_root[state_attr]
        if off_state_attr[new_rank] == F2_NULL:
            off_state_attr[new_rank] = 0
            for attr in self.direct_attributes():
                if attr._rank != state_attr:
                    attr_storage = OFF.db_root[attr._rank]
                    attr_storage[new_rank] = F2_NULL
                    OFF.db_root[attr._rank] = attr_storage

    def _new_oid(self, root_class):
        """build a new OID for an object of this (root-)class"""
        return OFF.new_db_oid()

    def create(self, **attr_values):
        """build a new instance for this class."""
        if not self.is_TupleClass():
            raise AssertionError('F2_Class.create(): cannot create an instance in class %s.' % self)
        elif not (self.makesValidKeys)(**attr_values):
            raise AssertionError('F2_Class.create(): duplicate key in %s.' % list(attr_values.items()))
        root_class = self.root()
        new_oid = self._new_oid(root_class)
        future_obj = theObject(self._rank, new_oid)
        (future_obj.pre_create)(**attr_values)
        root_class._initial_segment(new_oid)
        curr = self
        while curr != root_class:
            curr._initial_segment(new_oid)
            curr = theClass(OFF.superClass[curr._rank])

        for attr_name, attr_value in attr_values.items():
            future_obj._assign(attr_name, attr_value, previous=F2_NULL)

        (self.storeValidKeys)(future_obj, **attr_values)
        (future_obj.post_create)(**attr_values)
        return future_obj

    def enter(self, an_object, **attr_values):
        """take an existing object, enter this (sub-)class."""
        if not isinstance(an_object, F2_Object):
            raise AssertionError("F2_Class.enter(): can't apply to %s." % an_object)
        else:
            if not self.is_TupleClass():
                raise AssertionError('F2_Class.enter(): %s entering a non-tupleclass' % an_object)
            else:
                assert (self.makesValidKeys)(**attr_values), 'F2_Class.create(): duplicate key in %s.' % list(attr_values.items())
                his_class = theClass(an_object)
                his_root = his_class.root()
                assert his_root == self.root(), "F2_Class.enter(): %s can't enter into %s hierarchy" % self.root()
            assert an_object.exist_in(his_root), 'F2_Class.enter(): %s does not exist.' % an_object
        an_object = theObject(self._rank, an_object._rank)
        (an_object.pre_enter)(**attr_values)
        curr = self
        while curr != his_root and not an_object.exist_in(curr):
            curr._initial_segment(an_object._rank)
            curr = theClass(OFF.superClass[curr._rank])

        for attr_name, attr_value in attr_values.items():
            an_object._assign(attr_name, attr_value, previous=F2_NULL)

        (self.storeValidKeys)(an_object, **attr_values)
        (an_object.post_enter)(**attr_values)
        return an_object

    def leave(self, an_object):
        """forces an object to leave this class (and hence to leave all sub-classes)."""
        if not isinstance(an_object, F2_Object):
            raise AssertionError("F2_Class.leave(): can't apply to %s." % an_object)
        else:
            assert self.is_TupleClass(), 'F2_Class.leave(): %s trying to leave a non-tupleclass' % an_object
            classesToExit = self.all_subclasses() + [self]
            classesToExit = [c for c in classesToExit if an_object.exist_in(c)]
            if debug:
                print('%s.leave(%s): will have to _kill from following classes:' % (self, an_object))
                for c in classesToExit:
                    print('  -', c)

        old_attr_vals = {}
        for c in classesToExit:
            casted_obj = F2_Object(c._rank, an_object._rank)
            for a in c.direct_attributes():
                a_name = a.attributeName
                old_attr_vals[a_name] = getattr(casted_obj, a_name)

            casted_obj.pre_leave()

        for c in classesToExit:
            c._kill(F2_Object(c._rank, an_object._rank))

        for c in classesToExit:
            casted_obj = F2_Object(c._rank, an_object._rank)
            (casted_obj.post_leave)(**old_attr_vals)

        if self.is_SubClass():
            return theObject(OFF.superClass[self._rank], an_object._rank)
        else:
            return F2_Object(self._rank, F2_NULL)

    def _kill(self, an_object):
        """remove an_object from self collection: sets this segment's state attribute to F2_NULL"""
        state_attr_rank = OFF.classStateAttr[self._rank]
        ref_counter = an_object.current_reference(state_attr_rank)
        if ref_counter == F2_NULL:
            return
        if debug:
            print('%s._kill(%s): 1) removing references to referred objects, direct_attributes() are:' % (self, an_object))
            for a in self.direct_attributes():
                print('  ', a.attributeName)

        for a in self.direct_attributes():
            if a._rank != state_attr_rank:
                attrName = a.attributeName
                previous_value = an_object._getattr(attrName)
                an_object._assign(attrName, F2_NULL, previous_value)

        if debug:
            print('%s._kill(%s): 2) checking referencing objects.' % (self, an_object))
        if ref_counter > 0:
            referringAttributes = OFF.rangeClass.find(self._rank)
            if debug:
                print('  found %d referring attributes:' % len(referringAttributes))
            for attr in referringAttributes:
                minCard = OFF.minCard[attr]
                domainClass = OFF.domainClass[attr]
                attr_store = OFF.db_root[attr]
                if debug:
                    print('   -', OFF.attributeName[attr], 'domainClass = ', theClass(domainClass))
                referers = attr_store.find(an_object._rank)
                for ref in referers:
                    obj_ref = F2_Object(domainClass, ref)
                    if obj_ref.exist_object():
                        currentValue = attr_store[ref]
                        if isinstance(currentValue, list):
                            if len(currentValue) <= minCard:
                                theClass(domainClass).leave(obj_ref)
                            else:
                                changedValue = currentValue[:]
                                changedValue.remove(an_object._rank)
                                attr_store[ref] = changedValue
                        elif minCard != F2_NULL:
                            if minCard >= 1:
                                theClass(domainClass).leave(obj_ref)
                        else:
                            attr_store[ref] = F2_NULL

        attr_storage = OFF.db_root[state_attr_rank]
        attr_storage[an_object._rank] = F2_NULL
        OFF.db_root[state_attr_rank] = attr_storage

    def makesValidKeys(self, **attr_values):
        """check that this combination of attr_values is valid with present keys,
           return True only when all Keys are OK with this combination"""
        if not OFF.db_root['F2_Signature']['bootstrap_is_ongoing']:
            from . import f2_key
            keyList = f2_key.keysOfThisClass(self)
            for k in keyList:
                if not k.checkAttrValInKey(attr_values):
                    return False

        return True

    def storeValidKeys(self, curr_obj, **attr_values):
        """store valid tuple of values in key store of each key."""
        if not OFF.db_root['F2_Signature']['bootstrap_is_ongoing']:
            from . import f2_key
            keyList = f2_key.keysOfThisClass(self)
            for k in keyList:
                k.pushValuesInKey(attr_values, curr_obj)

    def post_create(self, **attr_values):
        """action trigged directly after creation of a new F2 Class: if its a tuple Class, make a state attribute."""
        if self.is_TupleClass():
            self._make_state_attribute()

    def pre_enter(self, **attr_values):
        """supplemental pre-conditions before entering a subclass of class CLASS."""
        enters_into_class = theClass(self._klass)
        if enters_into_class == theClass(metadict.subClass):
            if 'superClass' not in list(attr_values.keys()):
                raise f2_object.F2ValueError('SubClass.enter(%s): superClass not defined.' % self.className)
            else:
                superC = attr_values['superClass']
                if not (isinstance(superC, F2_Class) and superC.is_TupleClass()):
                    raise f2_object.F2ValueError('SubClass.enter(%s): superClass incorrect.' % self.className)
                if superC in self.all_subclasses():
                    raise f2_object.F2ValueError("SubClass.enter(%s): can't create a cycle in hierarchy." % self.className)

    def post_enter(self, **attr_values):
        """actions trigged directly after entering a subclass of CLASS:
           - if its TupleClass : confirm presence of a state attribute for this class,
           - if its SubClass : confirm class belongship of every object."""
        enters_into_class = theClass(self._klass)
        if enters_into_class == theClass(metadict.tupleClass):
            if not self.classStateAttribute:
                self._make_state_attribute()
        if enters_into_class == theClass(metadict.subClass):
            cSa = self.classStateAttribute
            for oid, obj_state in OFF.db_root[cSa._rank].items():
                if obj_state != F2_NULL:
                    self._confirm_exist(F2_Object(self._rank, oid))

    def pre_assign(self, name, old_val, new_val):
        """called before an attribute of class CLASS or TupleClass or SubClass or AtomClass, is assigned."""
        if name == 'superClass':
            if not new_val:
                raise f2_object.F2ValueError("%s.superClass = '?': Null not allowed here." % self.className)
            else:
                if self.root() != new_val.root():
                    raise f2_object.F2ValueError('%s.superClass = %s: not in same subclass tree.' % (self.className, new_val.className))
                if new_val in self.all_subclasses():
                    raise f2_object.F2ValueError("%s.superClass = %s: can't create a cycle in hierarchy." % (self.className, new_val.className))
        if name == 'className':
            pass

    def post_assign(self, name, old_val, new_val):
        """called after an attribute of class CLASS or TupleClass or SubClass or AtomClass, is assigned."""
        if name == 'superClass':
            cSa = self.classStateAttribute
            for oid, obj_state in OFF.db_root[cSa._rank].items():
                if obj_state != F2_NULL:
                    new_val._confirm_exist(F2_Object(self._klass, oid))

    def post_leave(self, **old_attr_values):
        """redefinable trigger, called immediately AFTER an object leaves a sub-class (or a class)"""
        exits_from_class = theClass(self._klass)
        if exits_from_class == theClass(metadict.subClass):
            if 'superClass' in list(old_attr_values.keys()):
                old_super_class = old_attr_values['superClass']
                if old_super_class:
                    if old_super_class.exist_object():
                        old_root = old_super_class.root()
                        if old_root:
                            if old_root.exist_in(theClass(metadict.tupleClass)):
                                cSa = old_root.classStateAttribute
                                for oid, obj_state in OFF.db_root[cSa._rank].items():
                                    if obj_state != F2_NULL:
                                        old_root.leave(F2_Object(old_root._klass, oid))

    def _make_state_attribute(self):
        """build a state attribute for this class"""
        classAttr = theClass(metadict.Attribute)
        newStateAttr = classAttr.create(attributeName=('state' + self.className), domainClass=self,
          rangeClass=(theClass(metadict.entityState)),
          minCard=1,
          maxCard=1,
          visibility=0)
        self.classStateAttribute = newStateAttr

    def _confirm_exist(self, an_object):
        """confirm existence of an_object in sub-class self, and in all its superclasses"""
        an_object = F2_Object(self._rank, an_object._rank)
        curr = self
        curr_root = curr.root()
        curr_root._initial_segment(an_object._rank)
        while curr != curr_root:
            curr._initial_segment(an_object._rank)
            curr = theClass(OFF.superClass[curr._rank])


def theClass(class_designator, db_designator=None):
    """theClass takes 3 forms: 
        - theClass(class_name [, database]) : class_name is a string, database (if provided) is an F2_Object of class Database
        - theClass(f2_object) : the class of this object, 
        - theClass(class_rank) : the internal rank of this class (reserved to low level, don't use)"""
    if isinstance(class_designator, str):
        classlist = OFF.className.find(class_designator)
        classlist = [c for c in classlist if OFF.stateCLASS[c] != F2_NULL]
        if classlist:
            if len(classlist) == 1:
                return F2_Class(metadict.CLASS, classlist[0])
            if db_designator:
                while classlist:
                    cl = F2_Class(metadict.CLASS, classlist.pop())
                    dbOfThisCl = cl._getattr('db')
                    if dbOfThisCl:
                        if dbOfThisCl == db_designator:
                            return cl

                raise f2_object.ClassDesignationError('name %s is ambiguous or inexistent in database %s' % (class_designator, db_designator))
            raise f2_object.ClassDesignationError('name %s is ambiguous' % class_designator)
        else:
            raise f2_object.ClassDesignationError('no F2 Class with name %s.' % class_designator)
    else:
        if isinstance(class_designator, F2_Object):
            return F2_Class(metadict.CLASS, class_designator._klass)
        if isinstance(class_designator, int):
            return F2_Class(metadict.CLASS, class_designator)
        raise f2_object.F2TypeError('no F2 Class designated by type %s.' % type(class_designator))


f2_object._RegisterPythonClass(metadict.CLASS, F2_Class)