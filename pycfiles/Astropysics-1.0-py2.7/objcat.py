# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astropysics/objcat.py
# Compiled at: 2013-11-27 17:30:36
"""

======================================================
objcat -- flexible, dynamically updated object catalog
======================================================

The :mod:`objcat` module contains classes and functions for generating catalogs
of objects. This catalog is unique in that it stores source information and can
dynamical deriv quantities that are dynamically updated as their sources are
changed. It also provides mechanisms for safely saving these object catalogss in
a database, and someday soon will include a web interface to interact with the
catalog via the internet.

Fundamentally, the catalog should be thought of as a tree (`this kind
<http://en.wikipedia.org/wiki/Tree_(data_structure)>`_, rather than `this one
<http://en.wikipedia.org/wiki/Tree>`_) of :class:`FieldNode` objects. Normally,
a :class:`Catalog` object acts as the root.

todo:add examples!

Classes and Inheritance Structure
---------------------------------

.. inheritance-diagram:: astropysics.objcat
   :parts: 1

Module API
----------

"""
from __future__ import division, with_statement
from .constants import pi
from .utils import add_docs_and_sig as _add_docs_and_sig
import numpy as np
from collections import deque
try:
    from abc import ABCMeta
    from abc import abstractmethod
    from abc import abstractproperty
    from collections import Sequence, MutableSequence
except ImportError:
    abstractmethod = lambda x: x
    abstractproperty = property
    ABCMeta = type

    class MutableSequence(object):
        __slots__ = ('__weakref__', )


    class Sequence(object):
        __slots__ = ('__weakref__', )


class CycleError(Exception):
    """
    This exception indicates a cycle was detected in some graph-like structure
    """

    def __init__(self, message):
        super(CycleError, self).__init__(message)


class CycleWarning(Warning):
    """
    This warning indicates a cycle was detected in some graph-like structure
    """

    def __init__(self, message):
        super(CycleWarning, self).__init__(message)


class SourceDataError(Exception):
    """
    This exception indicates a problem occured while trying to retrieve
    external Source-related data
    """

    def __init__(self, message):
        super(SourceDataError, self).__init__(message)


class CatalogNode(object):
    """
    This object is the superclass for all elements/nodes of a catalog with both
    parents and children.

    This is an abstract class that must have its initializer overriden.

    *Subclassing*
        * Subclasses must call super(Subclass,self).__init__(parent) in their
          __init__

    """
    __metaclass__ = ABCMeta
    __slots__ = ('_parent', '_children', '__weakref__')

    @abstractmethod
    def __init__(self, parent):
        self._children = []
        self._parent = None
        if parent is not None:
            self.parent = parent
        return

    def __getstate__(self):
        return {'_parent': self._parent, '_children': self._children}

    def __setstate__(self, d):
        self._parent = d['_parent']
        self._children = d['_children']

    def _cycleCheck(self, source):
        """
        call this from a child object with the child as the Source to check
        for cycles in the graph
        """
        if source is self:
            raise CycleError('cycle detected in graph assignment attempt')
        if self._parent is None:
            return
        else:
            return self.parent._cycleCheck(source)
            return

    def _getParent(self):
        return self._parent

    def _setParent(self, val):
        if val is not None:
            val._cycleCheck(self)
            val._children.append(self)
        if self._parent is not None:
            for i, c in enumerate(self._parent._children):
                if c is self:
                    break
            else:
                raise ValueError('Node ' + str(self) + " not in parent's children! This should be impossible.")

            del self._parent._children[i]
        self._parent = val
        return

    parent = property(_getParent, _setParent)

    @property
    def children(self):
        return tuple(self._children)

    def reorderChildren(self, neworder, inverseinds=False):
        """
        Change the order of the children

        :param neworder:
            Must be one of:
                * 'reverse'
                    Flip the order of the children
                * Array-like with integer values
                    Specifies the new order of the children. (e.g. to reorder
                    [a,b,c] to [c,a,b], neworder would be [2,0,1])
                * A callable
                    Reorders the children as per the :meth:`sort` list method,
                    using the callable as the `cmp` argument - it is called as
                    cmp(node1,node2) and should return -1 if node1<node2, 0 if
                    equal, or 1 if node1>node2.
                * None
                    Reorders as per standard python list sorting

        :param inverseinds:
            If True and `neworder` is integer array-like, does inverse
            reordering (e.g. if `neworder` is [2,0,1] and the children are
            [c,a,b] ,the children are reordered to [a,b,c]).  Otherwise,
            has no effect.
        """
        if neworder == 'reverse':
            self._children.reverse()
        elif callable(neworder):
            self._children.sort()
        elif callable(neworder):
            self._children.sort(cmp=neworder)
        else:
            neworder = np.array(neworder, copy=False).ravel()
            if len(neworder) != len(self._children):
                raise ValueError('input sequence does not have correct number of elements')
            if np.unique(neworder).size != neworder.size:
                raise ValueError('input sequence has repeats')
            if inverseinds:
                neworder = argsort(neworder)
            self._children[:] = np.array(self._children, dtype=object)[neworder]

    def addChild(self, node):
        """
        Adds a node as a child of this node.  Note that this will replace the
        added node's current parent (if any)
        """
        if not isinstance(node, FieldNode):
            raise ValueError('children must be FieldNodes')
        node.parent = self

    def removeChild(self, node):
        """
        Removes the requested child from this node, leaving it an orphan (i.e.
        it's parent is None)

        If child is not present, a ValueError will be raised
        """
        if node not in self:
            raise ValueError('requested child not present in this node')
        node.parent = None
        return

    @property
    def nnodes(self):
        """
        this gives the number of total nodes at this point in the tree
        (including self - e.g. a leaf in the tree returns 1)
        """
        return sum([ c.nnodes for c in self._children ], 1)

    def idstr(self):
        """
        a string uniquely identifying the object in its catalog heirarchy
        """
        if self.parent is None:
            return 'Root@' + hex(id(self))
        else:
            obj = self
            i = j = 0
            while obj.parent is not None:
                i += 1
                obj = obj.parent

            assert obj.parent is None, 'Catalog has no root!'
            for c in self.parent.children:
                if self is c:
                    break
                j += 1

            return ('{0}/{1}/{2}').format(i, j, obj.idstr())
            return

    def visit(self, func, traversal='postorder', filter=False, includeself=True):
        """
        This function walks through the object and all its children, executing
        func(:class:`CatalogNode`) and returning a list of the return values

        :param func: The function to call as ``func(node)`` on each node.
        :type func: a callable

        :param traversal:
            The traversal order of the tree - can be:

            * 'preorder'
            * 'postorder'
            * an integer indicating at which index the root should be evaluated
              (pre/post are 0/-1)
            * a float between -1 and 1 indicating where the root should be evaluated
              as a fraction
            * 'level'/'breathfirst'
            * None:only visit this Node

        :param filter:
            Sets a filter to control which nodes are visited. Can be:

            * False
                process and return all values
            * A callable
                is called as g(node) and if it returns False, the node will not
                be processed nor put in the list (also ignores anything that
                returns None)
            * any other
                If the node returns this value on processing, it will not be
                included in the returned list.

        :param includeself:
            If False, the function will not visit the node itself (only the
            sub-trees)
        :type includeself: bool

        :returns: A list with the return values of `visitfunc` at each visited node.

        """
        if callable(filter):
            oldfunc = func

            def func(*args, **kwargs):
                if filter(args[0]):
                    return oldfunc(*args, **kwargs)
                else:
                    return
                    return

            filterval = None
        else:
            filterval = filter
        if type(traversal) is int:
            retvals = []
            doroot = True
            for i, c in enumerate(self._children):
                if i == traversal and includeself:
                    retvals.append(func(self))
                    doroot = False
                retvals.extend(c.visit(func, traversal))

            if doroot and includeself:
                retvals.append(func(self))
        elif type(traversal) is float:
            retvals = []
            doroot = True
            travi = int(traversal * self._children)
            for i, c in enumerate(self._children):
                if i == travi and includeself:
                    retvals.append(func(self))
                    doroot = False
                retvals.extend(c.visit(func, traversal))

            if doroot and includeself:
                retvals.append(func(self))
        elif traversal == 'postorder':
            retvals = []
            for c in self._children:
                retvals.extend(c.visit(func, traversal))

            if includeself:
                retvals.append(func(self))
        elif traversal == 'preorder':
            retvals = self.visit(func, 0, filter, includeself)
        elif traversal == 'level' or traversal == 'breadthfirst':
            retvals = []
            q = deque()
            if includeself:
                q.append(self)
            while len(q) > 0:
                elem = q.popleft()
                retvals.append(func(elem))
                q.extend(elem._children)

        elif traversal is None:
            retvals = [
             func(self)]
        else:
            raise ValueError('unrecognized traversal type')
        if filterval is not False:
            retvals = [ v for v in retvals if v is not filterval ]
        return retvals

    def save(self, file, savechildren=True, **kwargs):
        """
        save this node as a file with the given name or file-like object

        if savechildren is True, the entire subtree will be saved, if False,
        just this node

        Note that the parent and everything above this point will NOT be
        saved (when reloaded the parent will be None)

        extra kwargs are passed into utils.fpickle
        """
        from .utils import fpickle
        oldpar = self._parent
        self._parent = None
        oldchildren = self._children
        if not savechildren:
            self._children = []
        try:
            fpickle(self, file, **kwargs)
        finally:
            self._parent = oldpar
            self._children = oldchildren

        return

    @staticmethod
    def load(file):
        """
        Load a previously saved :class:`CatalogNode`.

        :param file:
            A file name or file-like object for a file storing a pickled
            :class:`CatalogNode`.

        :raises TypeError: If `file` does not contain a :class:`CatalogNode`.
        """
        import cPickle as pickle
        if isinstance(file, basestring):
            fn = file
            with open(fn, 'r') as (f):
                res = pickle.load(f)
        else:
            fn = file.name
            res = pickle.load(file)
        if not isinstance(res, CatalogNode):
            raise TypeError('File %s does not contain a CatalogNode' % fn)
        return res


def save(node, file, savechildren=True):
    """
    save the specified node as a file with the given name or file-like object

    if savechildren is True, the entire subtree will be saved, if False,
    just this node

    Note that the parent and everything above this point will NOT be
    saved (when reloaded the parent will be None)
    """
    return node.save(file, savechildren)


load = CatalogNode.load

class ActionNode(CatalogNode):
    """
    This object is the superclass for nodes of a catalog that perform an action
    but do not store data. Thus, they have a parent, but no children.

    *Subclassing*

    * If :meth:`__init__` is overridden in a subclass,
      :meth:`ActionNode.__init__` must be called.
    * Subclasses must override the abstract :meth:`_doAction` method to define
      the action for the node. The first argument should be the node to act on.
      Additional arguments (passed on from :meth:`__call__` should be documented
      in the class docstring.

    If an action is desired without inserting the :class:`ActionNode` into the
    graph, the following method is typically used::

        output = SomeActionClass(None,param1=foo,param2=bar)(targetnode)

    """
    __metaclass__ = ABCMeta

    def __init__(self, parent, name=None):
        """
        :param parent: The parent of this node or None for no parent.
        :param name:
            The name of this node or None to use a default based on the class
            name.
        """
        CatalogNode.__init__(self, parent)
        if name:
            self.name = name
        else:
            self.name = self.__class__.__name__ + ' node'
        self._children = tuple()

    def __call__(self, node=None, *args, **kwargs):
        """
        Call this object to perform the action of this node.

        :param node:
            The node this action is to operate on, or None to use this node's
            parent.

        Additional arguments or keyword arguments are particular to a given node
        class - see the class docstring for details.
        """
        if node is None:
            node = self.parent
        return self._doAction(node, *args, **kwargs)

    @abstractmethod
    def _doAction(self, node, *args, **kwargs):
        """
        Subclasses must override this method to actionally perform the action
        this node expects. Whatever it returns will be returned by `__call__`
        """
        raise NotImplementedError

    def __getstate__(self):
        d = super(ActionNode, self).__getstate__()
        d.update(self.__dict__)
        return d

    def __setstate__(self, d):
        super(ActionNode, self).__setstate__(d)
        for k, v in d.iteritems():
            if not hasattr(self, k):
                self.__dict__[k] = v


class FieldNode(CatalogNode, Sequence):
    """
    A node in the catalog that has Fields.

    Note that for these subclasses, attribute access (e.g. node.fieldname)
    accesses the Field object, while mapping or sequence-style access
    (e.g node['fieldname'] or node[1])  directly accesses the current value
    of the field (or None if there is no value).  This means that
    iterating over the object will also give values.  To iterate over
    the Field objects, use the fields() method.

    Further, setting an attribute (e.g. node['fieldname'] = value) has different
    behavior depending on the type of the input value:

    * an integer i: sets the current value for that field to the ith entry in
      the field
    * a string: sets the current value to the entry that has the provided source
      name
    * a tuple (string,value): sets the field entry for the source named by the
      string to the value, and sets that source as the current value
    * a tuple (string,(value,lerr[,uerr]): sets the field entry for the source
      named by the string to the value and sets the errors for that entry, and
      sets that source as the current value
    """
    __slots__ = (
     '_fieldnames',)

    def __init__(self, parent, **kwargs):
        """
        Create a new fieldNode with the provided `parent`.

        kwargs are assigned as node values as self[kwargkey] = kwargvalue
        """
        CatalogNode.__init__(self, parent)
        self._fieldnames = []
        for k, v in kwargs.iteritems():
            self[k] = v

    def __getstate__(self):
        d = super(FieldNode, self).__getstate__()
        d['_fieldnames'] = self._fieldnames
        for n in self._fieldnames:
            val = getattr(self, n)
            d[n] = val

        return d

    def __setstate__(self, d):
        super(FieldNode, self).__setstate__(d)
        self._fieldnames = d['_fieldnames']
        for n in self._fieldnames:
            fi = d[n]
            setattr(self, n, fi)
            fi.node = self

    def addField(self, field):
        if isinstance(field, basestring):
            field = Field(field)
        elif not isinstance(field, Field):
            raise ValueError('input value is not a Field')
        if field.name in self._fieldnames:
            raise ValueError('Field name "%s" already present' % field.name)
        setattr(self, field.name, field)
        if field.node is not None:
            raise ValueError('a Field can only reside in one Node')
        field.node = self
        self._fieldnames.append(field.name)
        return

    def delField(self, fieldname):
        try:
            self._fieldnames.remove(fieldname)
            if hasattr(self.__class__, fieldname):
                setattr(self, fieldname, None)
            else:
                delattr(self, fieldname)
        except ValueError:
            raise KeyError('Field "%s" not found' % fieldname)

        return

    def fields(self):
        """
        this yields an iterator over all of the Field objects (rather than
        their values, as regular sequence access does)
        """
        for n in self._fieldnames:
            yield getattr(self, n)

    def __str__(self):
        return 'FieldNode with fields %s' % self._fieldnames

    def getFieldString(self, sep='\n'):
        """
        Generate a string with field:value pairs for all fields using
        sep as the seperator between the strings
        """
        strs = []
        for f in self.fields():
            try:
                strs.append(f.name + ':' + str(f()))
            except IndexError:
                strs.append(f.name + ' empty')

        return sep.join(strs)

    def __cmp__(self, other):
        try:
            return cmp(list(self), list(other))
        except TypeError:
            return 1

    def __len__(self):
        return len(self._fieldnames)

    def __contains__(self, key):
        return key in self._fieldnames

    def __getitem__(self, key):
        iserr = issrc = False
        if key not in self._fieldnames:
            try:
                if isinstance(key, basestring):
                    if key.endswith('_src'):
                        key = key[:-4]
                        issrc = True
                    elif key.endswith('_err'):
                        key = key[:-4]
                        iserr = True
                    else:
                        raise IndexError
                else:
                    key = self._fieldnames[key]
            except (IndexError, TypeError):
                raise IndexError('Field "%s" not found' % key)

        try:
            if iserr:
                return getattr(self, key).currenterror
            else:
                if issrc:
                    return getattr(self, key).currentsource
                return getattr(self, key)()

        except IndexError:
            return

        return

    def __setitem__(self, key, val):
        if key not in self._fieldnames:
            try:
                key = self._fieldnames[key]
            except (IndexError, TypeError):
                raise IndexError('Field "%s" not found' % key)

        field = getattr(self, key)
        field.currentobj = val

    def __delitem__(self, key):
        self.delField(key)

    @property
    def fieldnames(self):
        return tuple(self._fieldnames)

    @property
    def values(self):
        vals = []
        for f in self.fields():
            try:
                vals.append(f.currentobj.value)
            except IndexError:
                vals.append('')

        return tuple(vals)

    @property
    def sourcenames(self):
        vals = []
        for f in self.fields():
            try:
                vals.append(str(f.currentobj.source))
            except IndexError:
                vals.append('')

        return tuple(vals)

    @property
    def fielddict(self):
        vals = {}
        for f in self.fields():
            try:
                vals[f.name] = (
                 str(f.currentobj.source), f.currentobj.value)
            except IndexError:
                vals[f.name] = None

        return vals

    def setToSource(self, src, missing='skip'):
        """
        Sets a string or :class:`Source` object passed in as the `src` argument
        as the current source for the requested FieldNode and it's subtree.

        `missing` can be:

        * 'raise'/'exception'
            raise a ValueError if there is no value with that source
        * 'warn'
            give a warning if the value is missing
        * 'skip'
            do nothing

        """
        if not isinstance(src, Source) and src != 'derived':
            src = Source(src)
        if callable(missing):
            action = missing
        else:
            if missing == 'skip':

                def action(src, f, node):
                    return

            elif missing == 'raise' or missing == 'exception':

                def action(src, f, node):
                    raise ValueError('could not find src %s in field %s and node %s' % (src, f, node))

            elif missing == 'warn':
                from warnings import warn

                def action(src, f, node):
                    warn('could not find src %s in field %s and node %s' % (src, f, node))

            else:
                raise ValueError('invalid missing action')
            for f in self.fields():
                if src in f:
                    f.currentobj = src
                else:
                    action(src, f, self)

    @staticmethod
    def setToSourceAtNode(node, src, missing='skip', traversal='postorder', siblings=False):
        """
        Sets a string or :class:`Source` object passed in as the `src` argument
        as the current source for the requested FieldNode and it's subtree.

        `missing` can be:

        * 'raise'/'exception'
            raise a ValueError if there is no value with that source
        * 'warn'
            give a warning if the value is missing
        * 'skip'
            do nothing

        `traversal` is the type of traversal to perform on the subtree. See
        :meth:`FieldNode.visit` for values.

        If `siblings` is True, the function applies to all the children of this
        :class:`FieldNode's<FieldNode>` parent.
        """
        if isinstance(node, FieldNode):
            if siblings and node.parent is not None:
                node = node.parent
                includeself = False
            else:
                includeself = True

            def f(node):
                if hasattr(node, 'setToSource'):
                    node.setToSource(src, missing)
                    return node

            return node.visit(f, traversal=traversal, includeself=includeself, filter=None)
        else:
            vals = []
            for n in node:
                vals.extend(FieldNode.setToSourceAtNode(n, src, missing, traversal, siblings))

            return vals
            return

    @_add_docs_and_sig(setToSourceAtNode)
    def setToSourceAtSelf(self, *args, **kwargs):
        """
        Sets the given src string or Source object as the current source for
        this FieldNode and it's subtree. Based on
        :meth:`FieldNode.setToSourceAtNode` :

        {docstr:setToSourceAtNode}
        """
        return FieldNode.setToSourceAtNode(self, *args, **kwargs)

    def getFieldValueNodes(self, fieldname, value):
        """
        Searches through the tree and returns all nodes for which a particular
        field name has the requested value
        """
        return FieldName.getFieldValueNodesAtNode(self, fieldname, value)

    @staticmethod
    def extractFieldAtNode(node, fieldnames, traversal='postorder', filter=False, missing=0, converter=None, sources=False, errors=False, asrec=False, includeself=True):
        """
        This will walk through the tree starting from the :class:`FieldNode`
        given by the `node` argument and generate an :class:`array
        <numpy.ndarray>` of values for the specified fieldname.

        :param node: The node from which to extract fields.
        :type node: a :class:`FieldNode` object
        :param fieldnames:  Can be:

            * A single field name string.
            * A sequence of fieldnames strings.
            * A comma-seperated string of field names.

        :param traversal: see :meth:`CatalogNode.visit`
        :param filter: see :meth:`CatalogNode.visit`
        :param missing:
            Determines the behavior in the event that a field is not present (or
            a non :class:`FieldNode` is encountered) it can be:

            * 'exception'
                raise an exception if the field is missing
            * 'skip'
                do not include this object in the final array.  If `fieldnames`
                references more than one field, only the first field will be
                used to determine if the node is skipped.
            * 'mask'
                put 0 in the array location and return a mask of missing values as
                the second return value
            * 'masked'
                return numpy.ma.MaskedArray objects instead of arrays, with the
                missing values masked
            * any other
                fill any missing entries with this value

        :param converter:
            A function that is applied to the data before being added to the
            array (or None to perform no conversion).
        :type converter: callable or None
        :param sources:
            Determines if a sequence of sources should be returned - if False,
            only the array is returned. If True, the sources will be returned as
            described below. By default, string representations of the sources
            are returned. If it is set to 'object', the actual :class:`Source`
            objects will be returned instead.
        :type sources: bool or string value 'object'
        :param errors:
            If True, the errors will be returned (see return values below).
        :type errors: bool
        :param asrec:
            Is True, a :class:`record array <numpy.recarray>` is generated
            instead of a regular :class:`array <numpy.ndarray>`. It can
            optionally specify the numpy data type of the values, if it is a
            sequence of size matching the number of fields, an equivalent
            comma-seperated string, or a dictionary mapping fieldnames to
            dtypes. Otherwise, the dtypes are inferred from the extracted
            arrays.
        :type asrec: bool
        :param includeself: If True, this node itself will be included.
        :type includeself: bool

        :returns:
            If `missing` is 'mask', the below return values that are wrapped as
            a (returnval,mask) tuple. If errors are returned, they are
            (uppererror,lowererror) arrays, i.e. +/- . Can be:

            * a :class:`record array<numpy.recarray>` if `asrec` is True
            * an f x N :class:`array<numpy.ndarray>` of values if `sources` and
              `errors` are False
            * (values,errors,sources) if `sources` and `errors` are True
            * (values,sources) if `sources` are True and `errors` are False
            * (values,errors) if `errors` are True and `sources` are False

        """
        from functools import partial
        if missing in ('exception', 'raise', 'skip', 'mask', 'masked'):
            missingval = 0
        else:
            missingval = missing
        if isinstance(fieldnames, basestring):
            if ',' in fieldnames:
                fieldnames = fieldnames.split(',')
            else:
                fieldnames = [
                 fieldnames]
        if converter is None:
            if missing == 'exception' or missing == 'raise':

                def visitfunc(node, fieldname):
                    try:
                        return node[fieldname]
                    except AttributeError as e:
                        args = list(e.args)
                        args[0] = "Node %s has no field '%s'" % (node.idstr(), fieldname)
                        e.args = tuple(args)
                        e.message = args[0]
                        raise

            else:

                def visitfunc(node, fieldname):
                    try:
                        return node[fieldname]
                    except (KeyError, IndexError, TypeError, AttributeError):
                        return missingval

        else:
            if missing == 'exception' or missing == 'raise':

                def visitfunc(node, fieldname):
                    try:
                        return converter(node[fieldname])
                    except AttributeError as e:
                        args = list(e.args)
                        args[0] = "Node %s has no field '%s'" % (node.idstr(), fieldname)
                        e.args = tuple(args)
                        e.message = args[0]
                        raise

            else:

                def visitfunc(node, fieldname):
                    try:
                        return converter(node[fieldname])
                    except (KeyError, IndexError, TypeError, AttributeError):
                        return missingval

            def maskfunc(node, fieldname):
                try:
                    node[fieldname]
                    return True
                except (KeyError, IndexError, TypeError, AttributeError):
                    return False

            if filter is not False and not callable(filter):

                def maskfilter(node, fieldname):
                    return visitfunc(node, fieldname) != filter

            else:
                maskfilter = filter
            lsts = []
            masks = []
            maskfilterp = maskfilter
            for fn in fieldnames:
                lsts.append(node.visit(partial(visitfunc, fieldname=fn), traversal=traversal, filter=filter, includeself=includeself))
                if filter is not False and not callable(filter):
                    maskfilterp = partial(maskfilter, fieldname=fn)
                masks.append(node.visit(partial(maskfunc, fieldname=fn), traversal=traversal, filter=maskfilterp, includeself=includeself))

            lsts = [ np.array(l) for l in lsts ]
            lsts = [ np.array(a.ravel()[0], dtype=object) if a.shape == tuple() else a for a in lsts ]
            if missing == 'skip':
                m = np.array(masks[0])
                lsts = [ a[m] for a in lsts ]
            if sources:

                def srcfunc(node, fieldname):
                    try:
                        return getattr(node, fieldname).currentobj.source
                    except (KeyError, IndexError, TypeError, AttributeError):
                        return

                    return

                if filter is not False and not callable(filter):
                    srcs = [ node.visit(partial(srcfunc, fieldname=fn), traversal=traversal, filter=partial(maskfilter, fieldname=fn), includeself=includeself) for fn in fieldnames ]
                else:
                    srcs = [ node.visit(partial(srcfunc, fieldname=fn), traversal=traversal, filter=filter, includeself=includeself) for fn in fieldnames ]
                if sources != 'object':
                    srcs = [ [ str(s) for s in f ] for f in srcs ]
            if errors:

                def errfunc(node, fieldname):
                    try:
                        return getattr(node, fieldname).currentobj.errors
                    except (KeyError, IndexError, TypeError, AttributeError) as e:
                        return (0, 0)

                if filter is not False and not callable(filter):
                    errs = [ node.visit(partial(errfunc, fieldname=fn), traversal=traversal, filter=partial(maskfilter, fieldname=fn), includeself=includeself) for fn in fieldnames ]
                else:
                    errs = [ node.visit(partial(errfunc, fieldname=fn), traversal=traversal, filter=maskfilter, includeself=includeself) for fn in fieldnames ]
            if asrec:
                from operator import isMappingType, isSequenceType
                if asrec is True:
                    asrec = {}
                else:
                    if isinstance(asrec, basestring):
                        asrec = asrec.split(',')
                    if isMappingType(asrec):
                        for fn in fieldnames:
                            if fn not in asrec:
                                asrec[fn] = None

                    else:
                        if isSequenceType(asrec):
                            if len(asrec) != len(fieldnames):
                                raise ValueError('asrec sequence does not match fieldnames')
                            asrec = dict(zip(fieldnames, asrec))
                        else:
                            raise ValueError('invalid asrec entry')
                        ralists = []
                        newfnms = []
                        for i, (fnm, lst, msk) in enumerate(zip(fieldnames, lsts, masks)):
                            newfnms.append(fnm)
                            ralists.append(np.array(lst, dtype=asrec[fnm]))
                            if errors:
                                errarr = np.array(errs[i], dtype=asrec[fnm])
                                newfnms.append(fnm + '_lerr')
                                ralists.append(errarr[:, 0])
                                newfnms.append(fnm + '_uerr')
                                ralists.append(errarr[:, 1])
                            if sources:
                                newfnms.append(fnm + '_src')
                                ralists.append(srcs[i])
                            if missing == 'mask':
                                newfnms.append(fnm + '_mask')
                                ralists.append(msk)

                    res = np.rec.fromarrays(ralists, names=newfnms)
                    if missing == 'masked':
                        return np.ma.MaskedArray(res, ~np.array(msk))
                return res
            else:
                arr = np.array(lsts, dtype=object)
                if errors:
                    errmsk = np.array([ [ 2 * [err == (0, 0)] for err in fi ] for fi in errs ])
                    errs = np.array(errs)
                if len(arr) == 1:
                    arr = arr[0]
                    masks = masks[0]
                    if sources:
                        srcs = srcs[0]
                    if errors:
                        errs = errs[0]
                if missing == 'mask':
                    res = (
                     arr, np.array(masks))
                else:
                    if missing == 'masked':
                        res = np.ma.MaskedArray(arr, ~np.array(masks))
                        if errors:
                            errs = np.ma.MaskedArray(errs, errmsk)
                    else:
                        if missing == 'skip':
                            if sources:
                                srcs = srcs[m]
                            if errors:
                                errs = errs[m]
                            res = arr
                        else:
                            res = arr
                        if sources and errors:
                            return (res, errs, srcs)
                    if sources:
                        return (res, srcs)
                if errors:
                    return (res, errs)
            return res
        return

    @_add_docs_and_sig(extractFieldAtNode)
    def extractField(self, *args, **kwargs):
        """
        Walk through the tree starting from this object.

        If the kwarg `siblings` is set to True, this will also extract the
        siblings (e.g. the parent subtree, except for the parent itself), and
        this overwrites `includeself`.

        The other arguments are for :meth:`FieldNode.extractFieldAtNode` :

        {docstr:extractFieldAtNode}
        """
        sib = kwargs.pop('siblings', False)
        if sib and self.parent is not None:
            if len(args) < 6:
                kwargs['includeself'] = False
            else:
                args[5] = False
            return FieldNode.extractFieldAtNode(self.parent, *args, **kwargs)
        else:
            return FieldNode.extractFieldAtNode(self, *args, **kwargs)
            return

    @staticmethod
    def getFieldValueNodesAtNode(node, fieldname, value, visitkwargs={}):
        """
        Searches through the tree and returns all nodes for which a particular
        field name has the requested value
        """

        def visitfunc(node):
            if hasattr(node, fieldname):
                v = getattr(node, fieldname)
                if callable(v) and v() == value:
                    return node

        visitkwargs['filter'] = None
        return node.visit(visitfunc, **visitkwargs)


class Field(MutableSequence):
    """
    This class represents an attribute/characteristic/property of the
    FieldNode it is associated with.  It stores the current value
    as well as all the other possible values.

    The values, sources, and default properties will return the actual values
    contained in the FieldValues, while :attr:`currentobj` and iterating
    over the Field will return FieldValue objects.  Calling the
    Field (no arguments) will return the current value itself

    usedef specified if the default should be set -- if True, defaultval will
    be used, if None, a None defaultval will be ignored but any other
    will be recognizd, and if False, no default will be set
    """
    __slots__ = ('_name', '_type', '_vals', '_nodewr', '_notifywrs', '_units', '_descr')

    def __init__(self, name=None, type=None, defaultval=None, usedef=None, descr=None, units=None):
        """
        The field should have a name, and can optionally be given a type.  If the
        name is None, it will be inferred from the node it is placed inside.
        """
        self._name = name
        self._vals = []
        self._type = type
        self._notifywrs = None
        self._nodewr = None
        self._units = units
        self._descr = descr
        if usedef or usedef is None and defaultval is not None:
            self.default = defaultval
        return

    _okDVs = set()

    def __getstate__(self):
        prunedvals = []
        for v in self._vals:
            if isinstance(v, DerivedValue):
                if v in Field._okDVs:
                    Field._okDVs.remove(v)
                else:
                    from warnings import warn
                    warn("can't pickle DerivedValue in %s" % self)
            else:
                prunedvals.append(v)

        return {'_name': self._name, '_type': self._type, '_vals': prunedvals, '_units': self._units, 
           '_descr': self._descr}

    def __setstate__(self, d):
        self._name = d['_name']
        self._type = d['_type']
        self._vals = d['_vals']
        if '_units' in d:
            self._units = d['_units']
        else:
            self._units = None
        if '_descr' in d:
            self._descr = d['_descr']
        else:
            self._descr = None
        self._notifywrs = None
        self._nodewr = None
        return

    def __call__(self):
        return self.currentobj.value

    def __len__(self):
        return len(self._vals)

    def __contains__(self, val):
        try:
            self[val]
            return True
        except (KeyError, IndexError):
            return False

    def __str__(self):
        return 'Field %s:[%s]' % (self._name, (', ').join([ str(v) for v in self._vals ]))

    @property
    def currentsource(self):
        return self.currentobj.source

    @property
    def currenterror(self):
        o = self.currentobj
        if hasattr(o, 'errors'):
            return o.errors
        else:
            return (0, 0)

    def strCurr(self):
        """
        returns a string with the current value instead of the list of
        values (the behavior of str(Field_obj)
        """
        try:
            return 'Field %s: %s' % (self.name, self())
        except IndexError:
            return 'Field %s empty' % self.name

    def _checkConvInVal--- This code section failed: ---

 L.1216         0  LOAD_CONST               -1
                3  LOAD_CONST               ('isSequenceType',)
                6  IMPORT_NAME           0  'operator'
                9  IMPORT_FROM           1  'isSequenceType'
               12  STORE_FAST            3  'isSequenceType'
               15  POP_TOP          

 L.1218        16  LOAD_GLOBAL           2  'isinstance'
               19  LOAD_FAST             1  'val'
               22  LOAD_GLOBAL           3  'FieldValue'
               25  CALL_FUNCTION_2       2  None
               28  POP_JUMP_IF_TRUE    205  'to 205'

 L.1219        31  LOAD_GLOBAL           4  'hasattr'
               34  LOAD_FAST             1  'val'
               37  LOAD_CONST               'source'
               40  CALL_FUNCTION_2       2  None
               43  POP_JUMP_IF_FALSE    64  'to 64'
               46  LOAD_GLOBAL           4  'hasattr'
               49  LOAD_FAST             1  'val'
               52  LOAD_CONST               'value'
               55  CALL_FUNCTION_2       2  None
             58_0  COME_FROM            43  '43'
             58_1  COME_FROM            28  '28'
               58  POP_JUMP_IF_FALSE    64  'to 64'

 L.1220        61  JUMP_ABSOLUTE       205  'to 205'

 L.1221        64  LOAD_FAST             3  'isSequenceType'
               67  LOAD_FAST             1  'val'
               70  CALL_FUNCTION_1       1  None
               73  POP_JUMP_IF_FALSE   180  'to 180'
               76  LOAD_GLOBAL           5  'len'
               79  LOAD_FAST             1  'val'
               82  CALL_FUNCTION_1       1  None
               85  LOAD_CONST               2
               88  COMPARE_OP            2  ==
             91_0  COME_FROM            73  '73'
               91  POP_JUMP_IF_FALSE   180  'to 180'

 L.1222        94  LOAD_GLOBAL           2  'isinstance'
               97  LOAD_FAST             1  'val'
              100  LOAD_CONST               1
              103  BINARY_SUBSCR    
              104  LOAD_GLOBAL           6  'tuple'
              107  CALL_FUNCTION_2       2  None
              110  POP_JUMP_IF_FALSE   154  'to 154'
              113  LOAD_FAST             0  'self'
              116  LOAD_ATTR             7  'type'
              119  LOAD_GLOBAL           6  'tuple'
              122  COMPARE_OP            9  is-not
            125_0  COME_FROM           110  '110'
              125  POP_JUMP_IF_FALSE   154  'to 154'

 L.1223       128  LOAD_GLOBAL           8  'ObservedErroredValue'
              131  LOAD_FAST             1  'val'
              134  LOAD_CONST               0
              137  BINARY_SUBSCR    
              138  LOAD_FAST             1  'val'
              141  LOAD_CONST               1
              144  BINARY_SUBSCR    
              145  CALL_FUNCTION_VAR_1     1  None
              148  STORE_FAST            1  'val'
              151  JUMP_ABSOLUTE       202  'to 202'

 L.1225       154  LOAD_GLOBAL           9  'ObservedValue'
              157  LOAD_FAST             1  'val'
              160  LOAD_CONST               0
              163  BINARY_SUBSCR    
              164  LOAD_FAST             1  'val'
              167  LOAD_CONST               1
              170  BINARY_SUBSCR    
              171  CALL_FUNCTION_2       2  None
              174  STORE_FAST            1  'val'
              177  JUMP_ABSOLUTE       205  'to 205'

 L.1227       180  LOAD_GLOBAL          10  'TypeError'
              183  LOAD_CONST               'Input %s not FieldValue-compatible'
              186  LOAD_GLOBAL          11  'str'
              189  LOAD_FAST             1  'val'
              192  CALL_FUNCTION_1       1  None
              195  BINARY_MODULO    
              196  CALL_FUNCTION_1       1  None
              199  RAISE_VARARGS_1       1  None
              202  JUMP_FORWARD          0  'to 205'
            205_0  COME_FROM           202  '202'

 L.1229       205  LOAD_FAST             2  'dosrccheck'
              208  POP_JUMP_IF_FALSE   531  'to 531'

 L.1230       211  LOAD_GLOBAL           2  'isinstance'
              214  LOAD_FAST             2  'dosrccheck'
              217  LOAD_GLOBAL          12  'Source'
              220  CALL_FUNCTION_2       2  None
              223  POP_JUMP_IF_FALSE   278  'to 278'

 L.1231       226  LOAD_FAST             2  'dosrccheck'
              229  STORE_FAST            4  's'

 L.1232       232  LOAD_FAST             1  'val'
              235  LOAD_ATTR            13  'source'
              238  LOAD_FAST             4  's'
              241  COMPARE_OP            3  !=
              244  POP_JUMP_IF_FALSE   417  'to 417'

 L.1233       247  LOAD_GLOBAL          14  'ValueError'
              250  LOAD_CONST               'Input %s does not match expected %s'
              253  LOAD_FAST             1  'val'
              256  LOAD_ATTR            13  'source'
              259  LOAD_FAST             4  's'
              262  BUILD_TUPLE_2         2 
              265  BINARY_MODULO    
              266  CALL_FUNCTION_1       1  None
              269  RAISE_VARARGS_1       1  None
              272  JUMP_ABSOLUTE       417  'to 417'
              275  JUMP_FORWARD        139  'to 417'

 L.1234       278  LOAD_GLOBAL           2  'isinstance'
              281  LOAD_FAST             2  'dosrccheck'
              284  LOAD_GLOBAL          15  'basestring'
              287  CALL_FUNCTION_2       2  None
              290  POP_JUMP_IF_FALSE   351  'to 351'

 L.1235       293  LOAD_GLOBAL          12  'Source'
              296  LOAD_FAST             2  'dosrccheck'
              299  CALL_FUNCTION_1       1  None
              302  STORE_FAST            4  's'

 L.1236       305  LOAD_FAST             1  'val'
              308  LOAD_ATTR            13  'source'
              311  LOAD_FAST             4  's'
              314  COMPARE_OP            3  !=
              317  POP_JUMP_IF_FALSE   417  'to 417'

 L.1237       320  LOAD_GLOBAL          14  'ValueError'
              323  LOAD_CONST               'Input %s does not match expected %s'
              326  LOAD_FAST             1  'val'
              329  LOAD_ATTR            13  'source'
              332  LOAD_FAST             4  's'
              335  BUILD_TUPLE_2         2 
              338  BINARY_MODULO    
              339  CALL_FUNCTION_1       1  None
              342  RAISE_VARARGS_1       1  None
              345  JUMP_ABSOLUTE       417  'to 417'
              348  JUMP_FORWARD         66  'to 417'

 L.1239       351  LOAD_CONST               None
              354  STORE_FAST            4  's'

 L.1240       357  SETUP_LOOP           57  'to 417'
              360  LOAD_FAST             0  'self'
              363  LOAD_ATTR            17  '_vals'
              366  GET_ITER         
              367  FOR_ITER             46  'to 416'
              370  STORE_FAST            5  'v'

 L.1241       373  LOAD_FAST             5  'v'
              376  LOAD_ATTR            13  'source'
              379  LOAD_FAST             1  'val'
              382  LOAD_ATTR            13  'source'
              385  COMPARE_OP            2  ==
              388  POP_JUMP_IF_FALSE   367  'to 367'

 L.1242       391  LOAD_GLOBAL          14  'ValueError'
              394  LOAD_CONST               'value with %s already present in Field'
              397  LOAD_FAST             5  'v'
              400  LOAD_ATTR            13  'source'
              403  BINARY_MODULO    
              404  CALL_FUNCTION_1       1  None
              407  RAISE_VARARGS_1       1  None
              410  JUMP_BACK           367  'to 367'
              413  JUMP_BACK           367  'to 367'
              416  POP_BLOCK        
            417_0  COME_FROM           357  '357'
            417_1  COME_FROM           348  '348'
            417_2  COME_FROM           275  '275'

 L.1244       417  SETUP_EXCEPT         20  'to 440'

 L.1245       420  LOAD_FAST             1  'val'
              423  LOAD_ATTR            18  'checkType'
              426  LOAD_FAST             0  'self'
              429  LOAD_ATTR             7  'type'
              432  CALL_FUNCTION_1       1  None
              435  POP_TOP          
              436  POP_BLOCK        
              437  JUMP_ABSOLUTE       531  'to 531'
            440_0  COME_FROM           417  '417'

 L.1246       440  DUP_TOP          
              441  LOAD_GLOBAL          10  'TypeError'
              444  COMPARE_OP           10  exception-match
              447  POP_JUMP_IF_FALSE   527  'to 527'
              450  POP_TOP          
              451  STORE_FAST            6  'e'
              454  POP_TOP          

 L.1247       455  LOAD_FAST             0  'self'
              458  LOAD_ATTR             7  'type'
              461  LOAD_GLOBAL          19  'float'
              464  COMPARE_OP            2  ==
              467  POP_JUMP_IF_FALSE   521  'to 521'

 L.1248       470  SETUP_EXCEPT         22  'to 495'

 L.1249       473  LOAD_GLOBAL          19  'float'
              476  LOAD_FAST             1  'val'
              479  LOAD_ATTR            20  '_value'
              482  CALL_FUNCTION_1       1  None
              485  LOAD_FAST             1  'val'
              488  STORE_ATTR           20  '_value'
              491  POP_BLOCK        
              492  JUMP_ABSOLUTE       524  'to 524'
            495_0  COME_FROM           470  '470'

 L.1250       495  DUP_TOP          
              496  LOAD_GLOBAL          14  'ValueError'
              499  COMPARE_OP           10  exception-match
              502  POP_JUMP_IF_FALSE   517  'to 517'
              505  POP_TOP          
              506  POP_TOP          
              507  POP_TOP          

 L.1251       508  LOAD_FAST             6  'e'
              511  RAISE_VARARGS_1       1  None
              514  JUMP_ABSOLUTE       524  'to 524'
              517  END_FINALLY      
            518_0  COME_FROM           517  '517'
              518  JUMP_ABSOLUTE       528  'to 528'

 L.1253       521  RAISE_VARARGS_0       0  None
              524  JUMP_ABSOLUTE       531  'to 531'
              527  END_FINALLY      
            528_0  COME_FROM           527  '527'
              528  JUMP_FORWARD          0  'to 531'
            531_0  COME_FROM           528  '528'

 L.1255       531  LOAD_GLOBAL           2  'isinstance'
              534  LOAD_FAST             1  'val'
              537  LOAD_GLOBAL          21  'DerivedValue'
              540  CALL_FUNCTION_2       2  None
              543  POP_JUMP_IF_FALSE   588  'to 588'

 L.1256       546  LOAD_FAST             1  'val'
              549  LOAD_ATTR            22  'field'
              552  LOAD_CONST               None
              555  COMPARE_OP            9  is-not
              558  POP_JUMP_IF_FALSE   576  'to 576'

 L.1257       561  LOAD_GLOBAL          14  'ValueError'
              564  LOAD_CONST               'DerivedValues can only reside in a single field for dependencies'
              567  CALL_FUNCTION_1       1  None
              570  RAISE_VARARGS_1       1  None
              573  JUMP_FORWARD          0  'to 576'
            576_0  COME_FROM           573  '573'

 L.1258       576  LOAD_FAST             0  'self'
              579  LOAD_FAST             1  'val'
              582  STORE_ATTR           22  'field'
              585  JUMP_FORWARD          0  'to 588'
            588_0  COME_FROM           585  '585'

 L.1259       588  LOAD_FAST             1  'val'
              591  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 61

    def notifyValueChange(self, oldvalobject=None, newvalobject=None):
        """
        notifies all registered functions that the value in this
        field has changed

        (see registerNotifier)
        """
        if self._notifywrs is not None:
            deadrefs = []
            for i, wr in enumerate(self._notifywrs):
                callobj = wr()
                if callobj is None:
                    deadrefs.append(i)
                else:
                    callobj(oldvalobject, newvalobject)

            if len(deadrefs) == len(self._notifywrs):
                self._notifywrs = None
            else:
                for i in reversed(deadrefs):
                    del self._notifywrs[i]

        return

    def registerNotifier(self, notifier, checkargs=True):
        """
        this registers a function to be called when the value changes or is
        otherwise rendered invalid.  The notifier will be called as
        notifier(oldvalobj,newvalobj) BEFORE the value change is finalized.
        """
        from weakref import ref
        if not callable(notifier):
            raise TypeError('notifier not a callable')
        if checkargs:
            import inspect
            if len(inspect.getargspec(notifier)[0]) == 2:
                raise TypeError('notifier does not have 2 arguments')
        if self._notifywrs is None:
            self._notifywrs = []
        self._notifywrs.append(ref(notifier))
        return

    def __getitem__(self, key):
        if type(key) is int:
            return self._vals[key]
        else:
            if key is None:
                key = Source(None)
            elif isinstance(key, basestring):
                if 'derived' in key:
                    key = key.replace('derived', '')
                    if key == '':
                        der = 0
                    else:
                        der = int(key)
                    ders = [ v for v in self._vals if isinstance(v, DerivedValue) ]
                    if len(ders) <= der:
                        raise IndexError('field has only %i DerivedValues' % len(ders))
                    return ders[der]
                key = Source(key)
            if isinstance(key, Source):
                for v in self._vals:
                    if v.source == key:
                        return v

                raise KeyError('Field does not have %s' % key)
            else:
                raise TypeError('key not a Source key or index')
            return

    def __setitem__(self, key, val):
        if type(key) is int or key in self:
            i = key if type(key) is int else self._vals.index(self[key])
            if not isinstance(val, FieldValue) and key in self:
                val = (
                 key, val)
            val = self._checkConvInVal(val, dosrccheck=self._vals[i].source)
            if i == 0:
                self.notifyValueChange(self._vals[0], val)
            self._vals[i] = val
        else:
            if isinstance(key, Source):
                s = key
            elif isinstance(key, basestring) or key is None:
                s = Source(key)
            else:
                raise TypeError('specified key not a recognized Source')
            if not isinstance(val, FieldValue):
                val = (
                 s, val)
            val = self._checkConvInVal(val, dosrccheck=True)
            self._vals.append(val)
        return

    def __delitem__(self, key):
        if type(key) is int:
            i = key
        else:
            i = self._vals.index(self[key])
        if i == 0 and self._notifywrs is not None:
            self.notifyValueChange(self._vals[0], self._vals[1] if len(self._vals) > 1 else None)
        del self._vals[i]
        return

    def insert(self, key, val):
        """
        Insert a value into this :class:`Field`.

        :param key: The index or source at which to insert.
        :param val: The :class:`FieldValue` to add.
        """
        checktype = key if isinstance(key, Source) else True
        val = self._checkConvInVal(val, dosrccheck=checktype)
        self._nocheckinsert(key, val)

    def _nocheckinsert(self, key, val):
        if type(key) is int:
            i = key
        else:
            i = self._vals.index(self[key])
        if i == 0 and self._notifywrs is not None:
            self.notifyValueChange(val, self._vals[0] if len(self._vals) > 0 else None)
        self._vals.insert(i, val)
        return

    @property
    def name(self):
        return self._name

    @property
    def units(self):
        """
        The units of this :class:`Field`.
        """
        return self._units

    @property
    def description(self):
        """
        The description of this :class:`Field`.
        """
        return self._descr

    def _getNode(self):
        if self._nodewr is None:
            return
        else:
            return self._nodewr()

    def _setNode(self, val):
        if val is None:
            self._nodewr = None
        else:
            from weakref import ref
            self._nodewr = ref(val)
        for d in self.derived:
            d.sourcenode = val

        return

    node = property(_getNode, _setNode, doc='the node to which this Field belongs')

    @property
    def type(self):
        """
        Selects the type to enforce for this field. if None, no type-checking
        will be performed if a numpy dtype, the value must be an array matching
        the dtype can also be a sequence of types (accepts all) or a function
        that will be called directly on the function that returns True if the
        type is valid.
        """
        return self._type

    def _getDefault(self):
        return self[None].value

    def _setDefault(self, val):
        self[None] = val
        return

    def _delDefault(self):
        del self[None]
        return

    default = property(_getDefault, _setDefault, _delDefault, '\n    The default value is the FieldValue that has a the None Source -\n    this property is the default value itself, not the fieldValue object\n    ')

    def _getCurr(self):
        try:
            return self._vals[0]
        except IndexError:
            raise IndexError('Field %s empty' % self._name)

    def _setCurr(self, val):
        oldcurr = self._vals[0] if len(self._vals) > 0 else None
        try:
            i = self._vals.index(self[val])
            valobj = self._vals.pop(i)
        except (KeyError, IndexError, TypeError):
            valobj = self._checkConvInVal(val, dosrccheck=False)
            if valobj.source in self:
                del self[valobj.source]

        self.notifyValueChange(oldcurr, valobj)
        self._vals.insert(0, valobj)
        return

    currentobj = property(_getCurr, _setCurr)

    @property
    def values(self):
        return [ v() for v in self._vals ]

    @property
    def sources(self):
        return [ v.source for v in self._vals ]

    @property
    def sourcenames(self):
        return [ str(v.source) for v in self._vals ]

    @property
    def observed(self):
        """
        returns a list of all the ObservedValue objects except the default
        """
        return [ o for o in self if isinstance(o, ObservedValue) and o.source._str != 'None' ]

    @property
    def derived(self):
        """
        returns a list of all the DerivedValue objects
        """
        return [ o for o in self if isinstance(o, DerivedValue) ]

    @property
    def errors(self):
        return [ v.errors if hasattr(v, 'errors') else (0, 0) for v in self._vals ]


class _SourceMeta(type):

    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        if obj._str in Source._singdict:
            singobj = Source._singdict[obj._str]
            ol = obj.getBibcode()
            sl = singobj.getBibcode()
            if ol is not None and ol != sl:
                if sl is not None:
                    from warnings import warn
                    warn('overwriting location %s with %s in %s' % (sl, ol, singobj))
                singobj._adscode = obj._adscode
        else:
            Source._singdict[obj._str] = obj
        return Source._singdict[obj._str]


class Source(object):
    """
    A source for an observation/measurement/value.  Note that there is always
    only one instance if a source at a given time - any two Sources with the
    same source string are the same object

    The source can optionally include a URL location to look up metadata
    like authors, publication date, etc (location property)

    the constructor string can be of the form 'str/loc' in which case loc will be
    interpreted as the bibcode (see :meth:`setBibcode` for valid forms) if it is
    not specified in the argument. If it is 'str//loc', the loc will not be
    validated (e.g. it is assumed to be a correct ADS abstract code).
    """
    __metaclass__ = _SourceMeta
    __slots__ = ['_str', '_adscode', '__weakref__']
    from weakref import WeakValueDictionary
    _singdict = WeakValueDictionary()
    del WeakValueDictionary

    def __init__(self, src, bibcode=None):
        src = src._str if hasattr(src, '_str') else str(src)
        if bibcode is None and '/' in src:
            srcsp = src.split('/')
            if srcsp[(-2)] == '':
                self._str = ('/').join(srcsp[:-2]).strip()
                self._adscode = srcsp[(-1)].strip()
            else:
                self._str = ('/').join(srcsp[:-1]).strip()
                self.setBibcode(srcsp[(-1)].strip())
        else:
            self._str = src
            self.setBibcode(bibcode)
        return

    def __reduce__(self):
        return (
         Source, (self._str + ('' if self._adscode is None else '//' + self._adscode),))

    def __str__(self):
        return self._str + (' @' + self.getBibcode() if self._adscode is not None else '')

    adsurl = 'adsabs.harvard.edu'
    adstimeout = 1

    def getBibcode(self):
        """
        Returns the ADS_ bibliographic code for this source.

        :returns:
            A string with the ADS_ bibcode or None if no bibcode is defined.
        """
        return self._adscode

    def setBibcode(self, val):
        """
        Sets the ADS_ bibliographic code for this :class:`Source`

        :param val:
            The location reference for this bibcode. It may be any of the
            following:

                * A string of the form 'arxiv: ####.####'
                    The location is an ArXiv article identifier.
                * A string of the form 'astro-ph: ####.####'
                    Same as above.
                * A string of the form 'doi: #.##/###
                    The location is a Digital Object Identifier, commonly used by
                    publishers to uniquely identify publications.
                * A string of the form 'http://www.whatever.com/somewhere'
                    A direct URL to an ADS record.
                *  Any other string
                    Any other form will be interpreted as an ADS bibcode.
                * None
                    The bibcode will be unset, and any ADS-related lookups for
                    this source will fail.

        :raises TypeError: If an improper type is provided for `val`.
        :raises SourceDataError: if the record cannot be located.

        """
        if val is not None:
            if not isinstance(val, basestring):
                raise TypeError('bibcodes must be strings or None')
            if val == '':
                val = None
            else:
                val = self._findADScode(val)
        self._adscode = val
        return

    @staticmethod
    def _findADScode(loc):
        from urllib2 import urlopen, HTTPError, URLError
        from contextlib import closing
        if not Source.adsurl:
            return loc
        else:
            lloc = loc.lower()
            if 'arxiv' in lloc:
                url = 'http://%s/abs/arXiv:%s' % (Source.adsurl, lloc.replace('arxiv:', '').replace('arxiv', '').strip())
            else:
                if 'astro-ph' in lloc:
                    url = 'http://%s/abs/arXiv:%s' % (Source.adsurl, lloc.replace('astro-ph:', '').replace('astro-ph', '').strip())
                elif 'doi' in lloc:
                    url = 'http://%s/doi/%s' % (Source.adsurl, lloc.replace('doi:', '').replace('doi', ''))
                elif 'http' in lloc:
                    url = loc
                else:
                    url = 'http://%s/abs/%s' % (Source.adsurl, loc)
                url += '?data_type=PLAINTEXT'
                try:
                    if Source.adstimeout is None:
                        with closing(urlopen(url)) as (page):
                            for l in page:
                                if 'Bibliographic Code:' in l:
                                    return l.replace('Bibliographic Code:', '').strip()

                    else:
                        with closing(urlopen(url, timeout=Source.adstimeout)) as (page):
                            for l in page:
                                if 'Bibliographic Code:' in l:
                                    return l.replace('Bibliographic Code:', '').strip()

                except HTTPError:
                    raise SourceDataError('Requested location %s does not exist at url %s' % (loc, url))
                except URLError as e:
                    if e.reason == 'timed out':
                        raise SourceDataError('Lookup of Bibliographic code failed due to timeout')
                    raise

            raise SourceDataError('Bibliographic entry for the location %s had no ADS code, or parsing problem' % loc)
            return

    _adsxmlcache = {}

    @staticmethod
    def clearADSCache(adscode=None, disable=False):
        """
        this clears the cache of the specified adscode, or everything, if
        the adscode is None
        """
        if adscode is None:
            Source._adsxmlcache.clear()
        else:
            del Source._adsxmlcache[adscode]
        return

    @staticmethod
    def useADSCache(enable=True):
        """
        This is used to disable or enable the cache for ADS lookups - if the
        enable argument is True, the cache is enable (or unaltered if it
        is already active)) and if it is False, it will be disabled

        note that if the cache is disabled, all entries are lost
        """
        if enable:
            if Source._adsxmlcache is None:
                Source._adsxmlcache = {}
        else:
            Source._adsxmlcache = None
        return

    def _getADSXMLRec(self):
        adscode = self._adscode
        if adscode is None:
            raise SourceDataError('No location provided for additional source data')
        if not Source.adsurl:
            raise SourceDataError('ADS URL not provided, so bibliographic lookup cannot occur.')
        if Source._adsxmlcache is not None and adscode in Source._adsxmlcache:
            xmlrec = Source._adsxmlcache[adscode]
        else:
            from urllib2 import urlopen
            from contextlib import closing
            from xml.dom.minidom import parseString
            with closing(urlopen('http://%s/abs/%s>data_type=XML' % (Source.adsurl, adscode))) as (f):
                xmld = parseString(f.read())
            recs = xmld.getElementsByTagName('record')
            if len(recs) > 1:
                raise SourceDataError('Multiple matching ADS records for code %s' % adscode)
            xmlrec = recs[0]
            if Source._adsxmlcache is not None:
                Source._adsxmlcache[adscode] = xmlrec
        return xmlrec

    def getBibEntry(self):
        """
        Retrieves the BibTeX entry for this :class:`Source`. This data is
        retrieved from ADS_ and thus requires a network connection if it is not
        already cached.

        :raises SourceDataError:
            If no bibcode is defined (see :meth:`setBibcode`).

        :returns: A string with the BibTeX formatted entry for this source.

        """
        from urllib2 import urlopen, URLError
        from contextlib import closing
        if self._adscode is None:
            raise SourceDataError('No location provided for additional source data')
        if not Source.adsurl:
            raise SourceDataError('ADS URL not provided, so bibliographic lookup cannot occur.')
        try:
            if Source.adstimeout is None:
                with closing(urlopen('http://%s/abs/%s>data_type=BIBTEX' % (Source.adsurl, self._adscode))) as (xf):
                    res = xf.read()
            else:
                with closing(urlopen('http://%s/abs/%s>data_type=BIBTEX' % (Source.adsurl, self._adscode), timeout=Source.adstimeout)) as (xf):
                    res = xf.read()
        except URLError as e:
            if e.reason == 'timed out':
                raise SourceDataError('Lookup of Bibliographic code failed due to timeout')
            raise

        return res[res.index('@'):]

    def openADSAbstract(self, opentype=None, **kwargs):
        """
        Opens the ADS abstract for this source in a web browser.

        :param opentype: The type of web browser window to open.  Can be:

            * None
                Uses the :func:`webbrowser.open` function.
            * 'new'
                Uses the :func:`webbrowser.open_new` function.
            * 'tab'
                Uses the :func:`webbrowser.open_new_tab` function.

        Additionaly keyword arguments will be passed into the relevant function.
        """
        import webbrowser
        if opentype is None:
            openfunc = webbrowser.open
        elif opentype == 'new':
            openfunc = webbrowser.open_new
        elif opentype == 'tab':
            openfunc = webbrowser.open_new_tab
        else:
            raise ValueError('invalid opentype in openADSAbstract')
        openfunc(self.adsabs, **kwargs)
        return

    @staticmethod
    def build_bibliography(sources='all', fn=None):
        """
        Generates and returns BibTeX bibliography for :class:`Source` objects.

        :param sources:
            A sequence of :class:`Source` objects or the string 'all' to use all
            :class:`Source` objects.
        :param fn:
            A filename at which to save the BibTeX content, or None to not save.

        :returns:
            bibstr,fail where `bibstr` is a string with the BibTeX content and
            `fail` is a list of :class:`Source` objects for which the lookup failed
            (usually because the :class:`Source` has no bibcode)

        :raises TypeError:
            If `sources` is not a list of :class:`Source` objects or 'all'
        """
        pass

    @property
    def authors(self):
        """
        The author list for this Source as a list of strings
        """
        rec = self._getADSXMLRec()
        return [ e.firstChild.nodeValue for e in rec.getElementsByTagName('author') ]

    @property
    def title(self):
        """
        The publication title for this Source
        """
        rec = self._getADSXMLRec()
        es = rec.getElementsByTagName('title')
        if len(es) != 1:
            raise SourceDataError('Title not found for %s' % self)
        return es[0].firstChild.nodeValue

    @property
    def abstract(self):
        """
        The abstract for this Source
        """
        rec = self._getADSXMLRec()
        es = rec.getElementsByTagName('abstract')
        if len(es) != 1:
            raise SourceDataError('Abstract not found for %s' % self)
        return es[0].firstChild.nodeValue

    @property
    def date(self):
        """
        The publication date of this Source
        """
        rec = self._getADSXMLRec()
        es = rec.getElementsByTagName('pubdate')
        if len(es) != 1:
            raise SourceDataError('Publication date not found for %s' % self)
        return es[0].firstChild.nodeValue

    @property
    def adsabs(self):
        """
        The URL for the ADS abstract of this Source
        """
        rec = self._getADSXMLRec()
        for e in rec.getElementsByTagName('link'):
            if e.attributes['type'].value == 'ABSTRACT':
                urlnodes = e.getElementsByTagName('url')
                if len(urlnodes) == 1:
                    return urlnodes[0].firstChild.nodeValue
                return [ n.firstChild.nodeValue for n in urlnodes ]

        raise SourceDataError('Abstract URL not found for %s' % self)

    @property
    def keywords(self):
        """
        The keywords for this source, and the type of the keywords, if
        present
        """
        rec = self._getADSXMLRec()
        kwn = rec.getElementsByTagName('keywords')[0]
        kws = [ n.firstChild.nodeValue for n in kwn.getElementsByTagName('keyword') ]
        try:
            type = kwn.attributes['type'].value
        except KeyError:
            type = None

        return (
         kws, type)


class FieldValue(object):
    """
    Superclass for values that belong to a field.
    """
    __metaclass__ = ABCMeta
    __slots__ = '_source'

    @abstractmethod
    def __init__(self):
        self._source = None
        return

    def __getstate__(self):
        return {'_source': self._source}

    def __setstate__(self, d):
        self._source = d['_source']

    value = abstractproperty(doc='The value stored by this :class:`FieldValue`')

    def _getSource(self):
        return self._source

    def _setSource(self, val):
        if not (val is None or isinstance(val, Source)):
            try:
                val = Source(val)
            except:
                raise TypeError('Input source is not convertable to a Source object')

        self._source = val
        return

    source = property(_getSource, _setSource, doc='The :class:`Source` for this :class:`FieldValue`')

    def checkType(self, typetocheck):
        """
        ensure that the value of this FieldValue is of the requested Type
        (or None to accept anything).  Any mismatches will throw
        a TypeError
        """
        from .utils import check_type
        check_type(typetocheck, self.value)

    def __call__(self):
        return self.value

    def __str__(self):
        return 'Value %s' % self.value


class ObservedValue(FieldValue):
    """
    This value is an observed or otherwise measured value for the field
    with the associated Source.
    """
    __slots__ = '_value'

    def __init__(self, source, value):
        super(ObservedValue, self).__init__()
        if not isinstance(source, Source):
            source = Source(source)
        self.source = source
        self._value = value

    def __getstate__(self):
        d = super(ObservedValue, self).__getstate__()
        d['_value'] = self._value
        return d

    def __setstate__(self, d):
        super(ObservedValue, self).__setstate__(d)
        self._value = d['_value']

    def __str__(self):
        return '%s:Value %s' % (self.source, self.value)

    @property
    def value(self):
        return self._value


class ObservedErroredValue(ObservedValue):
    """
    This value is an observed value with errorbars

    The value is either (value,err) or (value,uperr,lowerr)
    """
    __slots__ = ('_upperr', '_lowerr')

    def __init__(self, source, value, upperr=None, lowerr=None):
        super(ObservedErroredValue, self).__init__(source, value)
        if upperr is None and lowerr is not None:
            upperr = lowerr
            lowerr = None
        self._upperr = upperr
        self._lowerr = lowerr
        return

    def __getstate__(self):
        d = super(ObservedErroredValue, self).__getstate__()
        d['_upperr'] = self._upperr
        d['_lowerr'] = self._lowerr
        return d

    def __setstate__(self, d):
        super(ObservedErroredValue, self).__setstate__(d)
        self._upperr = d['_upperr']
        self._lowerr = d['_lowerr']

    def __str__(self):
        if self._lowerr is not None:
            return '%s:Value %s +%s -%s' % (self.source, self.value, self._upperr, self._lowerr)
        else:
            return '%s:Value %s +/- %s' % (self.source, self.value, self._upperr)
            return

    def checkType(self, typetocheck):
        """
        ensure that the value and errors are of the requested Type
        (or None to accept anything).  Any mismatches will raise
        a TypeError
        """
        if typetocheck is not None:
            from .utils import check_type
            check_type(typetocheck, self.value)
            if self._upperr is not None:
                check_type(typetocheck, self._upperr)
            if self._lowerr is not None:
                check_type(typetocheck, self._lowerr)
        return

    @property
    def errors(self):
        """
        Errors on the measurement as a uppererror,lowererror tuple, or 0,0
        if no errors are present.
        """
        u, l = self._upperr, self._lowerr
        if u is None and l is None:
            return (0, 0)
        else:
            if l is None:
                return (u, u)
            else:
                return (u, l)

            return

    def hasSymmetricErrors(self):
        return self._upperr == self._lowerr


class DerivedValue(FieldValue):
    """
    A FieldValue that derives its value from a function of other
    :class:`FieldValues<FieldValue>`.

    The values to use as arguments to the function are initially set through the
    default values of the function, and can be either references to fields or
    strings used to locate the dependencies in the catalog tree, using the
    `sourcenode` argument as the current source (see :class:`DependentSource`
    for details of how dependent values are dereferenced)

    Alternatively, the initializer argument `flinkdict` may be a dictionary of
    link values that overrides the defaults from the function.

    if `ferr` is True, the return value of `f` should be a 3-sequence of the
    form (value,uppererror,lowererror), and the arguments of `f` will be passed
    as (depvalue,uerr,lerr) from the source :class:`FieldValues<FieldValue>`.

    The class attribute :attr:`failedvalueaction` determines the action to take
    if a an exception is encountered while deriving the value and can be:

    * 'raise'
        raise an exception (or pass one along)
    * 'warn'
        issue a warning when it occurs, but continue execution with the value
        returned as None
    * 'skip'
        the value will be returned as None but the value will be left invalid
    * 'ignore'
        the value will be returned as None and will be marked valid

    """
    __slots__ = ('_f', '_ferr', '_value', '_errs', '_valid', '_fieldwr')
    failedvalueaction = 'raise'

    def __init__(self, f, sourcenode=None, flinkdict=None, ferr=False):
        """
        `f` is the function to use for deriving the value - must have default
        field links for every argument if `flinkdict` is None.

        `sourcenode` specifies the current node to allow for links to be strings
        instead of explicit references to :class:`Fields<Field>`.

        `flinkdict` maps argument names to links, overriding the default values
        of the arguments of `f`
        """
        import inspect
        if callable(f):
            self._f = f
            self._ferr = ferr
            args, varargs, varkw, defaults = inspect.getargspec(f)
            if varargs or varkw:
                raise TypeError('DerivedValue function cannot have variable numbers of args or kwargs')
            if flinkdict:
                flinkdict = flinkdict.copy()
                if defaults is not None:
                    for a, d in zip(args, defaults):
                        if a not in flinkdict:
                            flinkdict[a] = d

                defaults = [ flinkdict.pop(a) for a in args if a in flinkdict ]
                if len(flinkdict) > 0:
                    raise ValueError('Override link for function arguments in a DerivedValue do not exist:%s' % flinkdict.keys())
            if defaults is None or len(args) != len(defaults):
                raise TypeError('DerivedValue does not have enought initial linkage items')
        else:
            raise TypeError('attempted to initialize a DerivedValue with a non-callable')
        self._valid = False
        self._value = None
        self._errs = None
        self._fieldwr = None
        self._source = DependentSource(defaults, sourcenode, self._invalidateNotifier)
        return

    def __getstate__(self):
        d = super(DerivedValue, self).__getstate__()
        d['_value'] = self._value
        from pickle import PicklingError
        raise PicklingError("DerivedValue can't be pickled because it depends on a function")
        d['_f'] = self._f
        return d

    def __setstate__(self, d):
        super(DerivedValue, self).__setstate__(d)
        self._value = d['_value']
        self._valid = False
        self._fieldwr = None
        self._f = d['_f']
        return

    def __str__(self):
        try:
            return 'Derived Value: %s' % self.value
        except:
            return 'Derived Value: Underivable'

    @property
    def source(self):
        return self._source

    @property
    def flinkdict(self):
        from inspect import getargspec
        args = getargspec(self._f)[0]
        return dict([ t for t in zip(args, self.source.depstrs) ])

    def _getNode(self):
        return self._source.pathnode

    def _setNode(self, val):
        self._source.pathnode = val

    sourcenode = property(_getNode, _setNode, doc='The current location in the Catalog tree')

    def _getField(self):
        if self._fieldwr is None:
            return
        else:
            return self._fieldwr()

    def _setField(self, val):
        if val is None:
            self._notifierwr = None
        else:
            from weakref import ref
            self._fieldwr = ref(val)
        return

    field = property(_getField, _setField, doc='A function like Field.notifyValueChange')

    def checkType(self, typetocheck):
        oldaction = DerivedValue.failedvalueaction
        try:
            DerivedValue.failedvalueaction = 'skip'
            super(DerivedValue, self).checkType(typetocheck)
        finally:
            DerivedValue.failedvalueaction = oldaction

    checkType.__doc__ = FieldValue.checkType.__doc__

    def _invalidateNotifier(self, oldvalobj, newvalobj):
        return self.invalidate()

    __invcyclestack = deque()

    def invalidate(self):
        """
        This marks this derivedValue as incorrect
        """
        if self in DerivedValue.__invcyclestack:
            from warnings import warn
            if self.sourcenode is None:
                cycleloc = self.idstr()
            elif 'name' in self.sourcenode:
                cycleloc = 'Node "%s"' % self.sourcenode['name']
            else:
                cycleloc = 'Node ' + self.sourcenode.idstr()
            if self.field is not None:
                cycleloc += ' in Field %s' % self.field.name
            warn('Setting a DerivedValue that results in a cycle at ' + cycleloc, CycleWarning)
        else:
            try:
                DerivedValue.__invcyclestack.append(self)
                self._valid = False
                if self.field is not None:
                    self.field.notifyValueChange(self, self)
            finally:
                DerivedValue.__invcyclestack.pop()

        return

    @property
    def value(self):
        if self._valid:
            return self._value
        else:
            try:
                deps = self._source.getDeps(geterrs=True)
                if self._ferr:
                    valres = self._f(*deps)
                    self._value = valres[0]
                    self._errs = (valres[1], valres[2])
                else:
                    depvals = [ d[0] for d in deps ]
                    self._value = val = self._f(*depvals)
                    if np.all([ np.all(d[1] == 0) and np.all(d[2] == 0) for d in deps ]):
                        self._errs = (0, 0)
                    else:
                        uerrs = []
                        lerrs = []
                        for i, d in enumerate(deps):
                            depvals[i] += d[1]
                            uerrs.append(self._f(*depvals) - val)
                            depvals[i] -= d[1] + d[2]
                            lerrs.append(val - self._f(*depvals))
                            depvals[i] += d[2]

                        uerr = np.sum(np.power(uerrs, 2)) ** 0.5
                        lerr = np.sum(np.power(lerrs, 2)) ** 0.5
                        self._errs = (uerr, lerr)
                self._valid = True
            except (ValueError, IndexError, CycleError, AttributeError, TypeError) as e:
                if isinstance(e, CycleError) and ' at ' not in e.args[0]:
                    if self.sourcenode is None:
                        cycleloc = ' at ' + self.idstr()
                    else:
                        if 'name' in self.sourcenode:
                            cycleloc = ' at Node ' + self.sourcenode['name']
                        else:
                            cycleloc = ' at Node ' + self.sourcenode.idstr()
                        if self.field is not None:
                            cycleloc += ' Field ' + self.field.name
                    dcs = DependentSource._DependentSource__depcyclestack
                    cyclestr = ('->').join([ '(' + (',').join(ds.depstrs) + ')' for ds in dcs ])
                    e.args = (e.args[0] + cycleloc + ' with Path:->' + cyclestr,)
                    e.message = e.args[0]
                if self.failedvalueaction == 'raise':
                    if len(e.args) == 2 and isinstance(e.args[1], list):
                        fields = [ self._f.func_code.co_varnames[i] for i in e.args[1] ]
                        raise ValueError('Could not get dependent values for field%s %s' % ('s' if len(fields) > 1 else '', fields))
                    else:
                        raise
                elif self.failedvalueaction == 'warn':
                    from warnings import warn
                    if len(e.args) == 2 and isinstance(e.args[1], list):
                        fields = [ self._f.func_code.co_varnames[i] for i in e.args[1] ]
                        warn('Problem getting dependent values for field%s %s' % ('s' if len(fields) > 1 else '', fields))
                    else:
                        warn('Problem encountered while deriving value ' + str(e))
                    self._value = None
                    self._valid = False
                elif self.failedvalueaction == 'skip':
                    self._value = None
                    self._valid = False
                elif self.failedvalueaction == 'ignore':
                    self._value = None
                    self._valid = True
                else:
                    raise ValueError('invalid failedvalueaction')

            return self._value
            return

    @property
    def errors(self):
        v = self.value
        return self._errs


class DependentSource(Source):
    """
    This class holds weak references to the :class:`Field`s that are necessary
    to generate values such as in :class:`DerivedValue`.

    This source must know the :class:`CatalogNode` that it is expected to
    inhabit to properly interpret string codes for fields. Otherwise, the input
    fields must be :class:`Field` objects.

    If locator strings are given to `depfields`, these strings follow a simple
    mini-language to locate their target field.  If they are strings without the
    '-' character, they will simply be treated as names within the same node. If
    a '-' is present, the text before the '-' follows the form "^^^.0.st"
    where a '^' character indicates that the path should go up to the parent of
    the current node, ".0" indicates to go to the first child, and ".st"
    indicates that a `LinkField` with the name 'st' should be followed.  Once
    the correct node is located, the text after the "-" indicates the name of
    the field on that node.

    Thus,'^^^.0.st-field' would go three needs up, into the first child, then
    into the node from a link named 'st', and would return the value of the
    field named "field".
    """
    __slots__ = ('depfieldrefs', 'depstrs', '_pathnoderef', 'notifierfunc')
    _instcount = 0

    def __new__(cls, *args, **kwargs):
        obj = super(DependentSource, cls).__new__(cls)
        DependentSource._instcount += 1
        return obj

    def __noneer(self):
        return

    def __init__(self, depfields, pathnode, notifierfunc=None):
        from weakref import ref
        self._str = 'dependent%i' % DependentSource._instcount
        self._adscode = None
        self.depfieldrefs = depfieldrefs = []
        self.depstrs = depstrs = []
        self.pathnode = pathnode
        self.notifierfunc = notifierfunc
        for f in depfields:
            if isinstance(f, basestring):
                depstrs.append(f)
                depfieldrefs.append(self.__noneer)
            elif isinstance(f, Field):
                depstrs.append(None)
                depfieldrefs.append(ref(f))
                if notifierfunc is not None:
                    f.registerNotifier(notifierfunc)
            elif f is None:
                depstrs.append(None)
                depfieldsrefs.append(self.__noneer)
            else:
                raise ValueError('Unrecognized field code %s' % str(f))

        return

    def __reduce__(self):
        return (
         DependentSource, (self.depstrs, None))

    def __len__(self):
        return len(self.depfieldrefs)

    @property
    def location(self):
        return

    def _getPathnode(self):
        return self._pathnoderef()

    def _setPathnode(self, val):
        from weakref import ref
        if val is None:
            self._pathnoderef = self.__noneer
        else:
            if not isinstance(val, CatalogNode):
                raise TypeError('attemted to set pathnode that is not a CatalogNode')
            self._pathnoderef = ref(val)
        for i, s in enumerate(self.depstrs):
            if s is None:
                self.depfieldrefs[i] = self.__noneer

        return

    pathnode = property(_getPathnode, _setPathnode, doc='The CatalogNode for dereferencing source names')

    @staticmethod
    def _locatestr(s, node):
        """
        this method translates from a string and a location to the actual
        targeted Field

        see :class:`DependentSource` docs for a description of the mini-language
        """
        if '-' not in s:
            return getattr(node, s)
        else:
            sp = s.split('-')
            if len(sp) > 2:
                raise ValueError('locator string has more than one "-" character')
            path, nm = sp
            sp2 = path.split('^')
            lasti = len(sp2) - 1
            for i, subs in enumerate(sp2):
                if subs == '':
                    if i != lasti:
                        node = node.parent
                        if node is None:
                            raise ValueError('locator string leads to empty node')
                else:
                    sp3 = subs.split('.')
                    if len(sp3) > 1:
                        if sp3[0] != '':
                            raise ValueError('name before "." character in locator string')
                        del sp3[0]
                    for subs2 in sp3:
                        if hasattr(node, subs2):
                            try:
                                fi = getattr(node, subs2)
                            except ValueError as e:
                                raise ValueError('locator string has invalid link name "%s"' % subs2, e)

                            if not isinstance(fi, LinkField):
                                raise TypeError('locator string leads to a non-link Field')
                            node = fi()
                        else:
                            try:
                                node = node.children[int(subs2)]
                            except ValueError as e:
                                raise ValueError('locator string has invalid child request "%s"' % subs2, e)

                        if node is None:
                            raise ValueError('locator string leads to broken link')

            return getattr(node, nm)

    def populateFieldRefs(self):
        """
        this relinks all dead weakrefs using the dependancy strings and returns
        all of the references or raises a :exc:`ValueError` if any of the
        strings cannot be dereferenced
        """
        from weakref import ref
        if self.pathnode is None:
            refs = [ wr() for wr in self.depfieldrefs ]
            if None in refs:
                raise ValueError('Missing/dead field(s) cannot be dereferenced without a catalog location', [ i for i, r in enumerate(refs) if r is None ])
        else:
            if not hasattr(self.pathnode, 'fieldnames'):
                raise ValueError('Linked pathnode has no fields or does not exist')
            refs = []
            for i, wrf in enumerate(self.depfieldrefs):
                if wrf() is None:
                    f = self._locatestr(self.depstrs[i], self.pathnode)
                    refs.append(f)
                    self.depfieldrefs[i] = ref(f)
                    if self.notifierfunc is not None:
                        f.registerNotifier(self.notifierfunc)
                else:
                    refs.append(wrf())

        return refs

    __depcyclestack = deque()

    def getDeps(self, geterrs=False):
        """
        gets the values of the dependent field.

        the return value is a list of the values in the fields if geterrs is
        False, or (value,upperr,lowerr) if it is True
        """
        try:
            if self in DependentSource.__depcyclestack:
                DependentSource.__depcyclestack.append(self)
                raise CycleError('Attempting to compute a DerivedValue that results in a cycle')
            else:
                DependentSource.__depcyclestack.append(self)
            fieldvals = [ wr() for wr in self.depfieldrefs ]
            if None in fieldvals:
                fieldvals = self.populateFieldRefs()
            if geterrs:
                fvs = []
                for fi in fieldvals:
                    if hasattr(fi, 'errors'):
                        es = fi.currenterror
                        if es is None:
                            fvs.append((fi(), 0, 0))
                        else:
                            fvs.append((fi(), es[0], es[1]))
                    else:
                        fvs.append((fi(), 0, 0))

                return fvs
            return [ fi() for fi in fieldvals ]
        finally:
            DependentSource.__depcyclestack.pop()

        return


class LinkField(Field):
    """
    A `Field` that only has values that point to other nodes.

    :param str name: A string with the field's name.
    :param class type:
        The type of node that this link can accept. Must be `CatalogNode` or a
        subclass.

    .. note::
        If the current linked node has been removed, calling this will change the
        current object to the next valid link.

    """
    __slots__ = tuple()

    def __init__(self, name=None, type=CatalogNode, units=None, descr=None):
        if not (type is CatalogNode or issubclass(type, CatalogNode)):
            raise TypeError('nodetype must be a CatalogNode or subclass')
        if units is not None:
            raise ValueError('LinkFields cannot have units')
        Field.__init__(self, name, type, defaultval=None, usedef=None, units=units, descr=descr)
        return

    def _checkConvInVal(self, val, dosrccheck=True):
        from operator import isSequenceType
        if isSequenceType(val) and len(val) == 2:
            val = LinkValue(val[0], val[1])
        if not isinstance(val, LinkValue):
            raise TypeError('LinkFields can only take LinkValues')
        val.checkType(self._type)
        return val

    def __call__(self):
        res = self.currentobj.value
        if res is None:
            del self[self.currentobj.source]
            res = self()
        return res


class LinkValue(FieldValue):
    """
    A `FieldValue` that points to a node.
    """
    __slots__ = ('_linkwr', )

    def __init__(self, src, nodeval):
        from weakref import ref
        self._source = src
        self._linkwr = ref(nodeval)

    def checkType(self, type):
        node = self.value
        if not isinstance(node, type):
            raise TypeError('linked node %s does not match expected node type %s' % (node, type))

    @property
    def value(self):
        return self._linkwr()

    def __getstate__(self):
        d = super(LinkValue, self).__getstate__()
        d['_linkwr'] = self._linkwr()
        return d

    def __setstate__(self, d):
        from weakref import ref
        super(LinkValue, self).__setstate__(d)
        self._linkwr = ref(d['_linkwr'])


class Catalog(CatalogNode):
    """
    This class represents a catalog of objects or catalogs.

    A Catalog is essentially a node in the object tree that
    is typically (although not necessarily) the root of the
    catalog tree.

    Iterator access is over the children, as is container testing and
    index access.

    Attributes can also be accessed as catobj[attrname] (this allows
    access to Catalog attributes in the same way as FieldNodes)
    """

    def __init__(self, name='default Catalog', parent=None):
        super(Catalog, self).__init__(parent)
        self.name = name

    def __str__(self):
        return 'Catalog %s' % self.name

    def __contains__(self, key):
        if isinstance(key, basestring):
            return hasattr(self, key)
        else:
            return key in self._children

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._children[key]
        return getattr(self, key)

    def __len__(self):
        return len(self._children)

    def __iter__(self):
        return iter(self._children)

    def isRoot(self):
        return self._parent is None

    @property
    def actionchildren(self):
        return tuple([ c for c in self.children if isinstance(c, ActionNode) ])

    def mergeNode(self, node, skipdup=False, testfunc=None):
        """
        merges the given FieldNode into the catalog by reassigning all of
        it's children to this Catalog

        testfunc is a function that will be called on the node to
        be transferred, and if it is True, the node will be moved, or
        if not it will be left alone.  If it is None, this
        test will be skipped

        if skipdup is True, any nodes that already have an object of the same
        name will not be transferred

        returns the number of objects added
        """
        if testfunc is None:
            testfunc = lambda n: True
        nms = [ n['name'] for n in self.children ]
        i = -1
        countoffset = 1
        for i, c in enumerate(node.children):
            if skipdup and c['name'] in nms or not testfunc(c):
                countoffset -= 1
            else:
                c.parent = self

        return i + countoffset

    def insertInto(self, insertnode):
        """
        Inserts this Catalog into another catalog heirarchy in the place of
        a node `insertnode` . This will replace the current parent, if any.

        :param insertnode:
            The node to insert this :class:`Catalog` in the place of. This
            :class:`Catalog` becomes the parant of `insertnode` .
        :type insertnode: :class:`CatalogNode`
        """
        newparent = insertnode.parent
        ind = newparent.index(insertnode)
        insertnode.parent = self
        self.parent = newparent
        newparent._children.insert(ind, newparent._children.pop())

    @_add_docs_and_sig(FieldNode.extractFieldAtNode)
    def extractField(self, *args, **kwargs):
        """
        Walk through the tree starting from this object and generate an array
        of the values for the requested fieldname if any :class:`FieldNode`s are in this
        :class:`Catalog`.

        The other arguments are for :meth:`FieldNode.extractFieldAtNode` :
        {docstr:extractFieldAtNode}
        """
        kwargs['includeself'] = False
        return FieldNode.extractFieldAtNode(self, *args, **kwargs)

    def getFieldNames(self):
        """
        Searches the Catalog and finds all field names present in the children
        """
        s = set()

        def visfunc(node):
            if hasattr(node, 'fieldnames'):
                s.update(node.fieldnames)

        self.visit(visfunc)
        return s

    def getFieldValueNodes(self, fieldname, value):
        """
        Searches the Catalog and finds all objects with the requested name
        """
        return FieldNode.getFieldValueNodesAtNode(self, fieldname, value, {'includeself': False})

    def locateName(self, name):
        """
        Searches the Catalog and finds all objects with the requested name
        """
        return FieldNode.getFieldValueNodesAtNode(self, 'name', name, {'includeself': False})


class _StructuredFieldNodeMeta(ABCMeta):

    def __new__(mcs, name, bases, dct):
        cls = super(_StructuredFieldNodeMeta, mcs).__new__(mcs, name, bases, dct)
        for k, v in dct.iteritems():
            if isinstance(v, Field):
                if v._name is None:
                    v._name = k
                elif k != v._name:
                    raise ValueError('StructuredFieldNode class %s has conficting                       field names - Node attribute:%s, Field.name:%s' % (name, k, v.name))
            elif isinstance(v, tuple) and len(v) == 2 and isinstance(v[1], Field):
                if v[1]._name is None:
                    v[1]._name = k
                elif k != v[1]._name:
                    raise ValueError('StructuredFieldNode class %s has conficting                       derived field names - Node attribute:%s, Field.name:%s' % (name, k, v[1].name))

        return cls


class StructuredFieldNode(FieldNode):
    """
    This class represents a :class:`FieldNode` in the catalog that follows a
    particular data structure (i.e. a consistent set of :class:`Fields<Field>`).
    It is meant to be subclassed to define generic types of objects in the
    catalog.

    The fields and names are inferred from the class definition and hence the
    class attribute name must match the field name. Any
    :class:`FieldValues<FieldValue>` present in the class objects will be
    ignored.

    The :attr:`checkonload` class attribute determines the action to take if an
    unaltered :class:`StructuredFieldNode` is loaded and found to be
    inconsistent with the current class definition. It may be:

    * False/None/0
        Do no checking.
    * 'warn'
        show a warning when the loaded object is inconsistent with the
        definition
    * 'raise'
        raise a ValueError when the loaded object is inconsistent with the
        definition
    * 'revert'
        silently revert to the current definition if inconsistencies are found
    * 'revertwarn'
        issue a warning, then revert

    """
    __metaclass__ = _StructuredFieldNodeMeta

    @staticmethod
    def __fieldInstanceCheck(x):
        return isinstance(x, Field) or isinstance(x, tuple) and len(x) == 2 and isinstance(x[0], DerivedValue)

    def __init__(self, parent, **kwargs):
        import inspect
        super(StructuredFieldNode, self).__init__(parent)
        self._altered = False
        dvs = []
        for k, v in inspect.getmembers(self.__class__, self.__fieldInstanceCheck):
            if isinstance(v, tuple):
                dv, fi = v
            else:
                fi = v
                dv = None
            if None in fi:
                fobj = fi.__class__(fi.name, type=fi.type, defaultval=fi[None], usedef=True, descr=fi.description, units=fi.units)
            else:
                fobj = fi.__class__(fi.name, type=fi.type, descr=fi.description, units=fi.units)
            setattr(self, k, fobj)
            fobj.node = self
            if dv is not None:
                dvs.append((dv, fobj))
            self._fieldnames.append(k)

        for dv, fobj in dvs:
            dvo = DerivedValue(dv._f, sourcenode=self, flinkdict=dv.flinkdict, ferr=dv._ferr)
            dvo.field = fobj
            fobj._nocheckinsert(0, dvo)

        for k, v in kwargs.iteritems():
            self[k] = v

        return

    def __getstate__(self):
        import inspect
        currderind = {}
        for k, v in inspect.getmembers(self.__class__, self.__fieldInstanceCheck):
            if isinstance(v, tuple):
                n = v[1].name
                if n in self._fieldnames:
                    fi = getattr(self, n)
                    for dv in fi:
                        if hasattr(dv, '_f') and dv._f is v[0]._f:
                            currderind[n] = fi.index(dv)
                            Field._okDVs.add(dv)

        d = super(StructuredFieldNode, self).__getstate__()
        d['_altered'] = self._altered
        d['currderind'] = currderind
        return d

    checkonload = 'warn'

    def __setstate__(self, d):
        import inspect
        self._altered = d['_altered']
        super(StructuredFieldNode, self).__setstate__(d)
        if StructuredFieldNode.checkonload:
            inconsistent = False
            fields = []
        for k, v in inspect.getmembers(self.__class__, self.__fieldInstanceCheck):
            if isinstance(v, tuple):
                n = v[1].name
                if n in self._fieldnames:
                    fi = getattr(self, n)
                    try:
                        ind = d['currderind'][n]
                    except KeyError:
                        from warnings import warn
                        warn('missing current index for structured derived value "%s" - assuming as default' % n)
                        ind = 0

                    if ind > len(fi):
                        ind = len(fi)
                    fi.insert(ind, DerivedValue(v[0]._f, self, v[0].flinkdict, v[0]._ferr))
            if StructuredFieldNode.checkonload:
                fields.append(k)
                if not inconsistent and getattr(self, k) is getattr(self.__class__, k) or not isinstance(getattr(self, k), Field):
                    inconsistent = k

        if StructuredFieldNode.checkonload:
            for k, v in inspect.getmembers(self, lambda x: isinstance(x, Field)):
                if k not in fields:
                    inconsistent = str(k) + ' not in ' + str(fields)
                    break

            if inconsistent is not False:
                if 'raise' in StructuredFieldNode.checkonload:
                    raise ValueError("object %s is not consistent with it's class definition due to %s" % (self, inconsistent))
                if 'warn' in StructuredFieldNode.checkonload or StructuredFieldNode.checkonload is True:
                    from warnings import warn
                    warn("object %s is not consistent with it's class definition due to %s" % (self, inconsistent))
                if 'revert' in StructuredFieldNode.checkonload:
                    self.revert()

    @property
    def alteredstruct(self):
        """
        If True, the object no longer matches the specification given by the
        class.  Note that this will remain True even if the offending fields
        are returned to their correct state.
        """
        return self._altered

    def revert(self):
        """
        Revert this object back to the standard Fields for  the class.
        Any deleted fields will be populated with the class Default Value
        any attributes that match the names of deleted Fields will be
        overwritten

        TODO:test
        """
        import inspect, types
        dvs = []
        fields = []
        for k, v in inspect.getmembers(self.__class__, self.__fieldInstanceCheck):
            if isinstance(v, tuple):
                dv, fi = v
            else:
                fi = v
                dv = None
            fields.append(k)
            if hasattr(self, k) is hasattr(self.__class__, k) or not hasattr(self, k) or not isinstance(getattr(self, k), Field):
                if None in fi:
                    fobj = fi.__class__(fi.name, fi.type, fi.default, True)
                else:
                    fobj = fi.__class__(fi.name, fi.type)
                setattr(self, k, fobj)
                fobj.node = self
                if dv is not None:
                    dvs.append((dv, fobj))

        for k, v in inspect.getmembers(self, lambda x: isinstance(x, Field)):
            if k not in fields:
                delattr(self, k)

        self._fieldnames = fields
        for dv, fobj in dvs:
            fobj.insert(0, DerivedValue(dv._f, self, dv.flinkdict, dv._ferr))

        self._altered = False
        self.addField = types.MethodType(StructuredFieldNode.addField, self, StructuredFieldNode)
        self.delField = types.MethodType(StructuredFieldNode.delField, self, StructuredFieldNode)
        return

    def addField(self, field):
        self._altered = True
        self.addField = super(StructuredFieldNode, self).addField
        self.addField(field)

    def delField(self, fieldname):
        self._altered = True
        self.delField = super(StructuredFieldNode, self).delField
        self.delField(fieldname)


def derivedFieldFunc(f=None, name=None, type=None, defaultval=None, usedef=None, units=None, ferr=False, **kwargs):
    """
    This method is to be used as a function decorator to generate a
    field with a name matching that of the function.  Note that the
    function should NOT have self as the leading argument

    Arguments are the same as for the Field constructor, except that
    leftover kwargs are passed in as links that override the
    defaults of the function.

    The docstring of the function will be taken as the field's
    :attr:`description`.
    """
    if f is None:
        return lambda f: StructuredFieldNode.derivedFieldFunc(f, name, type, defaultval, usedef, units, ferr, **kwargs)
    else:
        if name is None:
            name = f.__name__
        fi = Field(name=name, type=type, defaultval=defaultval, usedef=usedef, units=units, descr=f.__doc__)
        dv = DerivedValue(f, sourcenode=None, flinkdict=kwargs, ferr=ferr)
        return (dv, fi)
        return


StructuredFieldNode.derivedFieldFunc = staticmethod(derivedFieldFunc)

def arrayToNodes(values, source, fields, nodes, errors=None, matcher=None, converters=None, namefield=None, setcurr=True):
    """
    Applies values from an array to CatalogNodes.

    values must be a 2-dimensional array or a 1-dimensional structured array.
    If a 2D array, the first dimension should be the fields, while the
    second dimension should be the nodes to be created.

    source is a Source object or a string that will be converted to a Source
    object

    nodes is either a container of nodes to visit or a CatalogNode
    in which all FieldNodes within will be used as the nodes to visit

    fields is either a sequence of field names (must be at least as long as
    the array's second index dimension) or a mapping from indecies to field
    names or structured array field names to FieldNode field names

    if errors is not None, it should either be an object matching values
    in shape, or a tuple (upper,lower) and will be applied as the errors
    on the values

    matcher is a callable called as matcher(arrayrow,node) - if it returns
    False, the array will be matched to the next node - if True, the array
    values will be applied to the node

    converters  are either a sequence of callables or a mapping from indecies
    to callables or structured array field names to callables that will be
    called on each array element before being added to the FieldNode as
    converter(value).  If errors are provided, the converter will be called
    as converter((value,uerr,lerr)). If converters is None, no converting
    is performed.

    namefield is a field name that will be set to a unique code of the form
    'src-i' where i is element index of the array row (or None to apply
    no name).  It can also be a 2-tuple (name,converter) where converter is
    a callable of the form converter(i) that should return the value to
    apply to the field.
    """
    from operator import isSequenceType, isMappingType
    from inspect import getargspec
    if not isinstance(source, Source):
        source = Source(source)
    if isinstance(nodes, CatalogNode):
        if isinstance(matcher, basestring):
            traversal = matcher
            matcher = None
        else:
            traversal = 'preorder'
        nodes = nodes.visit(lambda n: n, traversal, lambda n: isinstance(n, FieldNode))
    else:
        nodes = list(nodes)
    if isinstance(fields, basestring):
        fields = {0: fields}
    else:
        if not isMappingType(fields):
            fields = dict([ t for t in enumerate(fields) ])
        else:
            fields = dict(fields)
        if converters is None:
            pass
        else:
            if not isMappingType(converters):
                converters = dict([ t for t in enumerate(converters) ])
            else:
                converters = dict(converters)
            array = np.array(values, copy=False).T
            if errors is None:
                lerrors = uerrors = None
            else:
                if isinstance(errors, tuple):
                    uerrors, lerrors = errors
                else:
                    uerrors = errors
                    lerrors = None
                if converters is None:
                    converters = {}
                if array.dtype.names is not None and len(array.shape) == 1:
                    if len(array.shape) != 1:
                        raise ValueError('structured array must be 1d')
                    nms = array.dtype.names
                    for k in fields.keys():
                        if k in nms:
                            fields[nms.index(k)] = fields[k]
                            del fields[k]

                    for k in converters.keys():
                        if k in nms:
                            converters[nms.index(k)] = converters[k]

                else:
                    if len(array.shape) == 1:
                        if len(fields) != 1:
                            raise ValueError('input array is 1D but multiple fields were given')
                        array = array.reshape((array.size, 1))
                        if uerrors is not None:
                            uerrors = np.array(uerrors, copy=False)
                            uerrors = uerrors.reshape((1, uerrors.size))
                        if lerrors is not None:
                            lerrors = np.array(lerrors, copy=False)
                            lerrors = lerrors.reshape((1, lerrors.size))
                    elif array.dtype.names is None and len(array.shape) == 2:
                        if array.shape[1] != len(fields):
                            raise ValueError('first dimension of array does not match number of fields')
                    else:
                        raise ValueError('invalid input array')
                    fieldseq = []
                    for i in range(len(array[0])):
                        if i not in fields:
                            fieldseq.append(None)
                        else:
                            fi = fields[i]
                            fieldseq.append(fi)
                            del fields[i]

                fieldseq = tuple(fieldseq)
                if fields:
                    raise ValueError('fields %s were not found in the array' % fields)
                convseq = []
                for i in range(len(array[0])):
                    if i not in converters:
                        convseq.append(lambda val: val)
                    else:
                        convseq.append(converters[i])

            convseq = tuple(convseq)
            twoargseq = []
            for i, conv in enumerate(convseq):
                if conv is None:
                    twoargseq.append(None)
                elif not callable(conv):
                    raise ValueError('non-callable converter for field %s' % fieldseq[i])
                else:
                    aspec = getargspec(conv)
                    if not aspec[1]:
                        if len(aspec[0]) == 1:
                            twoargseq.append(False)
                        elif len(aspec[0]) == 2:
                            twoargseq.append(True)
                        else:
                            raise ValueError('converter for field %s has wrong number of arguments' % fieldseq[i])

        if matcher is None and len(array) != len(nodes):
            raise ValueError('with no matcher, the number of nodes must match the size of the array')
        for i, a in enumerate(array):
            if matcher is None:
                n = nodes[0]
                del nodes[0]
            else:
                for j, n in enumerate(nodes):
                    if matcher(a, n):
                        break
                else:
                    j = None

                if j is not None:
                    del nodes[j]
                for fi in fieldseq:
                    if fi is not None and fi not in n.fieldnames:
                        n.addField(fi)

                for fiind, v in enumerate(a):
                    if fieldseq[fiind] is not None:
                        fi = getattr(n, fieldseq[fiind])
                        if uerrors is not None and uerrors[fiind] is not None:
                            ue = uerrors[fiind][i]
                            v = (v, ue, ue if lerrors is None else lerrors[fiind][i])
                        if twoargseq[fiind]:
                            fi[source] = convseq[fiind](v, a)
                        else:
                            fi[source] = convseq[fiind](v)
                        if setcurr:
                            fi.currentobj = source

    return


def arrayToCatalog(values, source, fields, parent, errors=None, nodetype=StructuredFieldNode, converters=None, filter=None, namefield=None, nameconv=None, setcurr=True):
    """
    Generates a catalog of nodes from the array of data.

    See ``arrayToNodes`` for values,source,fields, and covnerter arguments.

    parent is the object to use as the parent for all of the nodes (which will
    be returned, a string (in which case a Catalog object will be created
    and returned), or None (return value will be a sequence of nodes)

    nodetype is the class to use to create the nodes (usually a subclass of
    ``StructuredFieldNode``)

    filter is a function that will be called on the array row and if it
    returns True, a node will be created, and if False, that row will be
    skipped

    namefield is the field to use to apply the name of the node from the
    index of the array row.  nameconv can be:

    * None: name field will be set to '<sourcestr>-i'
    * a callable: name field will be set to nameconv(i)
    * a sequence of mapping: name field will be set as nameconv[i]

    if namefiled is None, no name will be applied

    """
    if isinstance(parent, basestring):
        parent = Catalog(parent)
    source = Source(source)
    if namefield:
        if nameconv is None:
            srcstr = source._str.split('/')[0]
            nameconv = lambda i: srcstr + '-' + str(i)
        elif callable(nameconv):
            pass
        else:
            nameseq = nameconv
            nameconv = lambda i: nameseq[i]
    if filter:

        def matcher(arrayrow, node):
            return filter(arrayrow)

    else:
        filter = lambda a: True
        matcher = None
    array = np.array(values, copy=False)
    nodes = []
    for i, a in enumerate(array.T):
        if filter(a):
            n = nodetype(parent=parent)
            nodes.append(n)
            if namefield:
                if namefield not in n:
                    n.addField(namefield)
                nfi = getattr(n, namefield)
                if len(nfi) == 1 and None in nfi:
                    del nfi[None]
                nfi[source] = nameconv(i)

    arrayToNodes(array, source, fields, nodes, errors=errors, converters=converters, matcher=matcher, setcurr=setcurr)
    if parent is None:
        return nodes
    else:
        return parent
        return


class SEDField(Field):
    """
    This field represents the Spectral Energy Distribution of this object -
    e.g. a collection of Spectra or Photometric measurements
    """
    __slots__ = [
     '_maskedsedvals', '_specunits']

    def __init__(self, name='SED', specunits='angstroms', defaultval=None, usedef=None, units=None, type=None, descr=None):
        from .spec import Spectrum, HasSpecUnits
        from .phot import PhotObservation
        super(SEDField, self).__init__(name, descr=descr)
        self._type = (
         Spectrum, PhotObservation)
        self._maskedsedvals = set()
        unittuple = HasSpecUnits.strToUnit(specunits)
        self._specunits = unittuple[0] + '-' + unittuple[1]
        if type is not None and set(type) != set(self._type):
            raise ValueError("SEDFields only accept Spectrum and PhotObservation objects - can't set type")
        if units is not None:
            raise ValueError('SEDFields use non-standard units')
        if defaultval:
            self[None] = defaultval
        return

    def __getstate__(self):
        d = super(SEDField, self).__getstate__()
        d['_maskedsedvals'] = self._maskedsedvals
        d['_specunits'] = self._specunits
        return d

    def __setstate__(self, d):
        super(SEDField, self).__setstate__(d)
        self._maskedsedvals = d['_maskedsedvals']
        self._specunits = d['_specunits']

    def __call__(self):
        return self.getFullSED()

    def __setitem__(self, key, val):
        """
        allow self['source'] = (bands,values) syntax
        """
        from .phot import PhotObservation
        if isinstance(val, tuple) and len(val) == 2:
            return super(SEDField, self).__setitem__(key, PhotObservation(*val))
        else:
            return super(SEDField, self).__setitem__(key, val)

    @property
    def type(self):
        return self._type

    @property
    def default(self):
        return self()

    @property
    def specs(self):
        from .spec import Spectrum
        return [ o for i, o in enumerate(self.values) if isinstance(o, Spectrum) and i not in self._maskedsedvals ]

    @property
    def specsources(self):
        from .spec import Spectrum
        return [ self.sources[i] for i, o in enumerate(self.values) if isinstance(o, Spectrum) and i not in self._maskedsedvals ]

    @property
    def phots(self):
        from .phot import PhotObservation
        return [ o for i, o in enumerate(self.values) if isinstance(o, PhotObservation) and i not in self._maskedsedvals ]

    @property
    def photsources(self):
        from .phot import PhotObservation
        return [ self.sources[i] for i, o in enumerate(self.values) if isinstance(o, PhotObservation) and i not in self._maskedsedvals ]

    def _getUnit(self):
        return self._specunits

    def _setUnit(self, val):
        from .spec import HasSpecUnits
        val = HasSpecUnits.strToUnit(val)
        val = val[0] + '-' + val[1]
        oldu = self._specunits
        try:
            for obj in self:
                if hasattr(obj, 'unit'):
                    obj.specunits = val

            self._specunits = val
        except:
            for obj in self:
                obj.specunits = oldu

            raise

    specunits = property(_getUnit, _setUnit, doc='\n    The units to use in the objects of this SED - see\n    astropysics.spec.HasSpecUnits for valid units\n    ')

    def getMasked(self):
        """
        return a copy of the values masked from the full SED
        """
        return tuple(sorted(self._maskedsedvals))

    def mask(self, val):
        """
        mask the value (either index or source name) to not appear in the
        full SED
        """
        if isinstance(val, int):
            self._maskedsedvals.add(val)
        else:
            self._maskedsedvals.add(self.index(val))

    def unmask(self, val):
        """
        unmask the value (either index or source name) to appear in the
        full SED
        """
        if isinstance(val, int):
            self._maskedsedvals.remove(val)
        else:
            self._maskedsedvals.remove(self.index(val))

    def unmaskAll(self):
        """
        unmask all values (all appear in full SED)
        """
        self._maskedsedvals.clear()

    def getBand(self, bands, asflux=False, asdict=False):
        """
        determines the magnitude or flux in the requested band.

        The first photometric measurement in this SEDField that has
        the band will be used - if not present, it will be computed
        from  the first Spectrum with appropriate overlap.  If none
        of these are found, a ValueError will be raised

        if asflux is True, the result will be returned as a flux -
        otherwise, a magnitude is returned.

        asdict returns a dictionary of results - otherwise, a sequence will
        be returned (or a scalar if only one band is requested)
        """
        from .phot import str_to_bands
        bands = str_to_bands(bands)
        vals = []
        for b, bn in zip(bands, [ b.name for b in bands ]):
            v = None
            for p in self.phots:
                if bn in p.bandnames:
                    i = p.bandnames.index(bn)
                    v = p.flux[i] if asflux else p.mag[i]
                    break

            if v is None:
                for s in self.specs:
                    if b.isOverlapped(s):
                        v = b.computeFlux(s) if asflux else b.computeMag(s)
                        break

            if v is None:
                raise ValueError('could not locate value for band ' % bn)
            vals.append(v)

        if asdict:
            return dict([ (b.name, v) for b, v in zip(bands, vals) ])
        if len(vals) == 1:
            return vals[0]
        else:
            return vals
            return

    def getFullSED(self):
        """
        the generates a astropysics.spec.Spectrum object that represents all
        the information contained in this SEDField
        """
        from .spec import Spectrum
        x = np.array([])
        f = np.array([])
        e = np.array([])
        for s in self.specs:
            x = np.r_[(x, s.x)]
            f = np.r_[(f, s.flux)]
            e = np.r_[(e, s.err)]

        for p in self.phots:
            pf, pe = p.flux, p.fluxerr
            px, pw = p.getBandInfo()
            px = np.tile(px / pw, np.prod(px.shape) / len(p))
            px = px.reshape((len(p), np.prod(px.shape) / len(p)))
            pf = pf.reshape((len(p), np.prod(pf.shape) / len(p)))
            pe = pe.reshape((len(p), np.prod(pe.shape) / len(p)))
            x = np.r_[(x, px.ravel())]
            f = np.r_[(f, pf.ravel())]
            e = np.r_[(e, pe.ravel())]

        return Spectrum(x, f, e, unit=self._specunits)

    def plotSED(self, specerrs=True, photerrs=True, plotbands=True, colors=('b', 'g', 'r', 'r', 'k'), log='', clf=True):
        """
        Generates a plot of the SED of this object.

        colors is a tuple of colors as (spec,phot,specerr,photerr,other)
        """
        from .spec import HasSpecUnits
        from .plotting import _mpl_context
        specs = self.specs
        phots = self.phots
        mxy1 = np.max([ np.max(s.flux) for s in specs ]) if len(specs) > 0 else None
        mxy2 = np.max([ np.max(p.getFluxDensity(self.unit)[0]) for p in phots ]) if len(phots) > 0 else None
        mxy = max(mxy1, mxy2)
        mny1 = np.min([ np.min(s.flux) for s in self.specs ]) if len(specs) > 0 else None
        mny2 = np.min([ np.min(p.getFluxDensity(self.unit)[0]) for p in self.phots ]) if len(phots) > 0 else None
        if mny1 is None:
            mny = mny2
        elif mny2 is None:
            mny = mny1
        else:
            mny = min(mny1, mny2)
        mxx1 = np.max([ np.max(s.x) for s in self.specs ]) if len(specs) > 0 else None
        mxx2 = np.max([ np.max(p.getBandInfo(self.unit)[0]) for p in self.phots ]) if len(phots) > 0 else None
        mxx = max(mxx1, mxx2)
        mnx1 = np.min([ np.min(s.x) for s in self.specs ]) if len(specs) > 0 else None
        mnx2 = np.min([ np.min(p.getBandInfo(self.unit)[0]) for p in self.phots ]) if len(phots) > 0 else None
        if mnx1 is None:
            mnx = mnx2
        elif mnx2 is None:
            mnx = mnx1
        else:
            mny = min(mnx1, mnx2)
        with _mpl_context(clf=clf) as (plt):
            if 'x' in log and 'y' in log:
                plt.loglog()
            else:
                if 'x' in log:
                    plt.semilogx()
                else:
                    if 'y' in log:
                        plt.semilogy()
                    c = (colors[0], colors[2], colors[4], colors[4])
                    for s in specs:
                        s.plot(fmt='-', ploterrs=specerrs, colors=c, clf=False)

                lss = ('--', ':', '-.', '-')
                for i, p in enumerate(phots):
                    if plotbands:
                        if plotbands is True:
                            plotbands = {'bandscaling': (mxy - mny) * 0.5, 'bandoffset': mny}
                        plotbands['ls'] = lss[(i % len(lss))]
                    p.plot(includebands=plotbands, fluxtype='fluxden', unit=self.unit, clf=False, fmt='o', c=colors[1], ecolor=colors[3])

            rngx, rngy = mxx - mnx, mxy - mny
            plt.xlim(mnx - rngx * 0.1, mxx + rngx * 0.1)
            plt.ylim(mny - rngy * 0.1, mxy + rngy * 0.1)
            xl = ('-').join(HasSpecUnits.strToUnit(self.unit)[:2])
            xl = xl.replace('wavelength', '\\lambda')
            xl = xl.replace('frequency', '\\nu')
            xl = xl.replace('energy', 'E')
            xl = xl.replace('angstrom', '\\AA')
            xl = xl.replace('micron', '\\mu m')
            xl = tuple(xl.split('-'))
            plt.xlabel('$%s/{\\rm %s}$' % xl)
            plt.ylabel('$ {\\rm Flux}/({\\rm erg}\\, {\\rm s}^{-1}\\, {\\rm cm}^{-2} {\\rm %s}^{-1})$' % xl[1])
        return


class AstronomicalObject(StructuredFieldNode):
    """
    A :class:`StructuredFieldNode` with the basic fields for an astronomical
    object.
    """
    from .coords import CoordinateSystem as _CSys

    def __init__(self, parent=None, name='default Name'):
        super(AstronomicalObject, self).__init__(parent)
        self.name.default = name

    def __str__(self):
        return 'Object %s' % self.name()

    def __repr__(self):
        return '<%s.%s object "%s" at %s>' % (
         self.__class__.__module__, self.__class__.__name__, self.name(),
         hex(id(self)))

    _fieldorder = ('name', 'loc')
    name = Field('name', basestring)
    loc = Field('loc', _CSys)
    sed = SEDField('sed')


class MatplotAction(ActionNode):
    """
    This :class:`ActionNode` uses :mod:`matplotlib` to generate plots.

    This class is an abstract class, requiring subclasses to implement the
    :meth:`makePlot` method.

    Keyword arguments when this action is called will be used to change the
    value of the object attribute with the same name as the keyword temporarily
    for *only* that call.

    The :attr:`defaultattrs` class variable can be set for a class, and it must
    be a dictionary where the keys are strings. It will be used to initialize
    class variables, where the defaults are given by the values of
    :attr:`defaultattrs` .

    The following example illustrates the use of the of a :class:`MatplotAction`.
    Define the :class:`PlotXY` by doing::

        class PlotXY(MatplotAction):
            defaultattrs = dict(logx=False)

            def makePlot(self,node):
                from numpy import log10

                x,y = node.extractField('x,y')
                if self.logx:
                    x = log10(x)
                scatter(x,y)
                xlabel('x')
                ylabel('y')

    Then, if `c` is a `Catalog` with children that have `x` and `y` fields)::

        PlotXY(c)()

    will produce a plot of x vs y, as well as adding the `PlotXY` object as a
    child of `c`. similarly::

        PlotXY(logx=True)(c)

    Will produce a plot of log(x) vs. y for `c`'s chilren, but will *not* add
    the `PlotXY` object as a child of `c`.

    """
    defaultattrs = {}

    def __init__(self, parent, nodename=None, clf=True, savefile=None, **kwargs):
        """
        :param parent: The parent to assign this node to or None for no parent.
        :param nodename:
            The name of this node or None to use the default derived from the
            class name.
        :param clf: If True, the figure will be cleared before plotting.
        :param savefile:
            A string specifying the file name to save the plot to when the node
            is called. If None, the plot will not be saved.

        Additional keyword can be used to set attributes that have defaults
        given by :attr:`defaultattrs`.
        """
        ActionNode.__init__(self, parent, nodename)
        self.savefile = savefile
        self.clf = clf
        for k, v in self.defaultattrs.iteritems():
            if k in kwargs:
                v = kwargs.pop(k)
            setattr(self, k, v)

        if len(kwargs) > 0:
            raise TypeError(self.__class__.__name__ + ' does not have attributes ' + str(kwargs.keys()))

    def _doAction(self, node=None, **kwargs):
        """
        Creates the matplotlib plot.

        :param node:
            The node this action is associated with, or the parent of this
            :class:`MatplotAction` if None.

        Additional arguments will be passed into `makePlot`
        """
        from matplotlib.pyplot import savefig, clf, title, gca
        if node is None:
            node = self.parent
        oldvars = dict([ (k, getattr(self, k)) for k in kwargs ])
        try:
            for k, v in kwargs.iteritems():
                setattr(self, k, v)

            if self.clf:
                clf()
            self.makePlot(node)
            if gca().get_title() == '':
                title(self.name)
            if self.savefile:
                savefig(self.savefile)
        finally:
            for k, v in oldvars.iteritems():
                setattr(self, k, v)

        return

    @abstractmethod
    def makePlot(self, node):
        """
        This method does the actual plotting.

        :param node: The node this action is associated with.
        """
        raise NotImplementedError


class PlottingAction2D(MatplotAction):
    """
    Generates 2D plots by extracting fields from the catalog for two specified
    variables.
    """

    def __init__(self, parent, xaxisname, yaxisname, nodename='2D Plotting Node', plottype='plot', plotkwargs=None, logify=None, ordering='postorder', filter=False):
        ActionNode.__init__(self, parent, nodename)
        self.xaxisname = xaxisname
        self.yaxisname = yaxisname
        self.plottype = plottype
        self.plotkwargs = plotkwargs
        self.logify = logify
        self.ordering = ordering
        self.filter = filter

    def _doAction(self, node=None):
        """
        Perform the plotting (and saves the plot if :attr:`savefile` is not
        None).

        :param node:
            The node at which to start plotting. If None, the parent will be
            used.

        """
        if node is None:
            node = self.parent
        if isinstance(self.ordering, basestring) and self.ordering.startswith('sort'):
            traversal = 'postorder'
            sort = self.ordering[4:]
        else:
            traversal = self.ordering
            sort = False
        ics = isinstance(node, FieldNode)
        xarr, xerr = FieldNode.extractFieldAtNode(node, self.xaxisname, traversal, missing='masked', filter=self.filter, includeself=ics, errors=True)
        yarr, yerr = FieldNode.extractFieldAtNode(node, self.yaxisname, traversal, missing='masked', filter=self.filter, includeself=ics, errors=True)
        if self.logify:
            if 'x' in self.logify:
                logxarr = np.log10(xarr)
                uxerr, lxerr = xerr.T
                loguxerr = np.log10(xarr + uxerr) - logxarr
                loglxerr = np.log10(xarr - lxerr) + logxarr
                xarr = logxarr
                xerr = np.array((loguxerr, loglxerr)).T
            if 'y' in self.logify:
                logyarr = np.log10(yarr)
                uyerr, lyerr = yerr.T
                loguyerr = np.log10(yarr + uyerr) - logyarr
                loglyerr = np.log10(yarr - lyerr) + logyarr
                yarr = logyarr
                yerr = np.array((loguyerr, loglyerr)).T
        if sort == 'x':
            sorti = np.argsort(xarr)
            xarr = xarr[sorti]
            xerr = xerr[sorti]
            yarr = yarr[sorti]
            yerr = yerr[sorti]
        elif sort == 'y':
            sorti = np.argsort(yarr)
            xarr = xarr[sorti]
            xerr = xerr[sorti]
            yarr = yarr[sorti]
            yerr = yerr[sorti]
        if self.plottype == 'plot':
            from matplotlib.pyplot import plot
            pkwargs = {} if self.plotkwargs is None else self.plotkwargs
            plot(xarr.astype(float), yarr.astype(float), **pkwargs)
        elif self.plottype == 'errorbar':
            from matplotlib.pyplot import errorbar, clf
            pkwargs = {'fmt': 'o'} if self.plotkwargs is None else self.plotkwargs
            if np.all(xerr.mask):
                xerr = None
            else:
                xerr = xerr.filled(0).T.astype(float)[::-1]
            if np.all(yerr.mask):
                yerr = None
            else:
                yerr = yerr.filled(0).T.astype(float)[::-1]
            errorbar(xarr.astype(float), yarr.astype(float), yerr, xerr, **pkwargs)
        elif self.plottype == 'scatter':
            from matplotlib.pyplot import scatter
            pkwargs = {} if self.plotkwargs is None else self.plotkwargs
            scatter(xarr.astype(float), yarr.astype(float), **pkwargs)
        elif self.plottype == 'hist':
            from matplotlib.pyplot import hist
            pkwargs = {} if self.plotkwargs is None else self.plotkwargs
            host(xarr.astype(float), **pkwargs)
        else:
            raise ValueError('invalid plottype ' + str(self.plottype))
        return


class TextTableAction(ActionNode):
    """
    This :class:`ActionNode` generates and returns formatted text tables.

    Calling this action generates the and returns the table, and saves it if
    the :attr:`savefile` attribute is not None:

    :param node:
        The node at which to start plotting. If None, the parent will be
        used.
    :param reorder:
        An array of indicies to change the order of the table before
        writing, or None to use the catalog ordering.
    :type: int array or None

    :returns: A string with the table data

    """

    def __init__(self, parent, arrnames, titles=None, details=None, caption=None, nodename='Table Node', tabformat='ascii', fmt='%.18e', errors=True, logify=None, ordering='postorder', savefile=None):
        ActionNode.__init__(self, parent, nodename)
        self.arrnames = arrnames
        self.titles = titles
        self.details = details
        self.caption = caption
        self.tabformat = tabformat
        self.fmt = fmt
        self.errors = errors
        self.savefile = savefile
        self.logify = logify
        self.ordering = ordering

    def _doAction(self, node=None, reorder=None):
        """
        Generate the table (and saves the if :attr:`savefile` is not None).

        :param node:
            The node at which to start plotting. If None, the parent will be
            used.
        :param reorder:
            An array of indicies to change the order of the table before
            writing, or None to use the catalog ordering.
        :type: int array or None

        :returns: A string with the table data

        """
        from operator import isSequenceType
        if node is None:
            node = self.parent
        storesources = 'source' in self.arrnames
        if self.titles is None:
            titles = self.arrnames
        else:
            titles = self.titles
        if len(titles) != len(self.arrnames):
            raise ValueError('titles do not match arrnames')
        if self.details is not None and len(self.details) != len(self.arrnames):
            raise ValueError('details do not match arrnames')
        if isinstance(self.fmt, basestring):
            fmts = [
             self.fmt] * len(titles)
        else:
            fmts = self.fmt
        if len(fmts) != len(self.arrnames):
            raise ValueError('fmt does not match arrnames')
        if not isSequenceType(self.logify):
            logifys = [
             self.logify] * len(titles)
        else:
            logifys = self.logify
        if len(logifys) != len(self.arrnames):
            raise ValueError('fmt does not match arrnames')
        if isinstance(self.ordering, basestring) and self.ordering.startswith('sort'):
            traversal = 'postorder'
            sort = self.ordering[4:]
        else:
            traversal = self.ordering
            sort = False
        ics = isinstance(node, FieldNode)
        arrs, errs, srcs = [], [], []
        srcmap = {}
        for arrname, logify in zip(self.arrnames, logifys):
            if arrname != 'source':
                arr, err, src = FieldNode.extractFieldAtNode(node, arrname, traversal, missing='masked', includeself=ics, errors=True, sources=True)
                if logify:
                    logarr = np.log10(arr)
                    arrs.append(logarr)
                    uerr, lerr = err.T
                    loguerr = np.log10(arr + uerr) - logarr
                    loglerr = np.log10(arr - lerr) + logarr
                    errs.append(np.array((loguerr, loglerr)).T)
                else:
                    arrs.append(arr)
                    errs.append(err)
                srcs.append(src)

        if storesources:
            srcs = np.array(srcs)
            srcs[srcs.astype('S9') == 'dependent'] = 'None'
            usrcs = np.unique(srcs)
            if 'None' in usrcs:
                usrcs[usrcs == 'None'] = usrcs[0]
                usrcs[0] = 'None'
            else:
                usrcs = np.concatenate((['None'], usrcs))
            srccodes = np.empty(srcs.shape, dtype=int)
            for i, src in enumerate(usrcs):
                srccodes[srcs == src] = i

            ocodes = []
            for code in srccodes.T.ravel():
                if code not in ocodes:
                    ocodes.append(code)

            ocodes.remove(0)
            ocodes.insert(0, 0)
            ocodes = np.array(ocodes)
            srccodes = np.choose(srccodes, np.argsort(ocodes))
            usrcs = usrcs[ocodes]
            srcstrs = []
            for src in srccodes.T:
                lsrc = [ str(s) for s in np.unique(src) ]
                if '0' in lsrc:
                    lsrc.remove('0')
                srcstrs.append((',').join(lsrc))

            sind = self.arrnames.index('source')
            arrs.insert(sind, srcstrs)
            errs.insert(sind, [0] * len(srcstrs))
            srcannotation = [ ' %i) %s' % t for t in enumerate(usrcs) if t[0] != 0 ]
            srcannotation = 'Source Code:' + (',').join(srcannotation) + '.'
        if sort:
            sorti = np.argsort(arrs[int(i)])
            arrs = [ arr[sorti] for arr in arrs ]
        if self.tabformat.startswith('ascii'):
            if self.tabformat[5:] == '':
                sep = ' '
            else:
                sep = self.tabformat[6:-1]
            if self.errors:
                titemp = []
                for ti in titles:
                    titemp.append(ti)
                    titemp.append(ti + '_err')

                titles = titemp
            header = '#' + sep.join(titles)
            lines = [header]
            if self.caption:
                for l in self.caption.split('\n'):
                    lines.append('#' + l)

            if self.details is not None:
                for ti, det in zip(titles, self.details):
                    lines.append('#%s: %s' % (ti, det))

            else:
                if storesources is not None:
                    lines.append('#' + srcannotation)
                if self.errors:
                    erravg = np.sum(errs, axis=-1) / 2.0
                    for i in range(len(arrs[0])):
                        ss = []
                        for arr, err, fmt in zip(arrs, erravg, fmts):
                            ss.append(fmt % arr[i])
                            ss.append(fmt % err[i])

                        lines.append(sep.join(ss))

                else:
                    for i in range(len(arrs[0])):
                        ss = [ fmt % arr[i] if arr[i] is not np.ma.masked else '...' for arr, fmt in zip(arrs, fmts) ]
                        lines.append(sep.join(ss))

            tabtxt = ('\n').join(lines)
        elif self.tabformat == 'latex':
            lines = []
            lines.append('\\begin{table}[htbp]')
            lines.append('\\begin{tabular}{' + ('|').join([' c '] * len(titles)) + '}')
            lines.append((' & ').join(titles) + ' \\\\')
            lines.append('\\hline')
            if self.errors:
                for i in range(len(arrs[0])):
                    ss = []
                    for arr, err, fmt in zip(arrs, errs, fmts):
                        if arr[i] is np.ma.masked:
                            ss.append('\\nodata')
                        else:
                            errsubstrfmt = '^{+' + fmt + '}_{-' + fmt + '}'
                            errsubstr = errsubstrfmt % tuple(err[i])
                            ss.append(fmt % arr[i] + errsubstr)

                    lines.append((' & ').join(ss) + '\\\\')

            else:
                for i in range(len(arrs[0])):
                    ss = [ '\\nodata' if arr[i] is np.ma.masked else fmt % arr[i] for arr, fmt in zip(arrs, fmts) ]
                    lines.append((' & ').join(ss) + ' \\\\')

            lines[-1] = lines[(-1)][:-2]
            lines.append('\\end{tabular}')
            caption = self.caption if self.caption is not None else ''
            if storesources:
                caption += ('. ' if not caption.endswith('.') else ' ') + srcannotation
            if caption != '':
                lines.append('\\caption{' + caption + '}')
            lines.append('\\end{table}')
            tabtxt = ('\n').join(lines)
        elif self.tabformat == 'deluxetable':
            lines = [
             '\\begin{deluxetable*}{' + ('').join(['c'] * len(titles)) + '}']
            lines.append('\\tablecolumns{%i}' % len(titles))
            if self.caption is not None:
                lines.append('\\tablecaption{' + self.caption + '}')
            lines.append('\\tablehead{')
            for i, ti in enumerate(titles):
                tnote = '' if self.details is None else '\\tablenotemark{' + chr(97 + i) + '}'
                lines.append('    \\colhead{' + ti + tnote + '} &')

            lines[-1] = lines[(-1)][:-2]
            lines.append('}')
            lines.append('')
            lines.append('\\startdata')
            lines.append('')
            if self.errors:
                for i in range(len(arrs[0])):
                    ss = []
                    for arr, err, fmt in zip(arrs, errs, fmts):
                        if arr[i] is np.ma.masked:
                            ss.append('\\nodata')
                        else:
                            errsubstrfmt = '^{+' + fmt + '}_{-' + fmt + '}'
                            errsubstr = errsubstrfmt % tuple(err[i])
                            ss.append(fmt % arr[i] + errsubstr)

                    lines.append((' & ').join(ss) + '\\\\')

            else:
                for i in range(len(arrs[0])):
                    ss = [ '\\nodata' if arr[i] is np.ma.masked else fmt % arr[i] for arr, fmt in zip(arrs, fmts) ]
                    lines.append((' & ').join(ss) + ' \\\\')

                lines[-1] = lines[(-1)][:-2]
                lines.append('')
                lines.append('\\enddata')
                lines.append('')
                if self.details is None:
                    if 'source' in self.arrnames:
                        lines.append('')
                        lines.append('\\tablecomments{' + srcannotation + '}')
                for i, det in enumerate(self.details):
                    lines.append('\\tablenotetext{' + chr(97 + i) + '}{' + det + '}')

            lines.append('')
            lines.append('\\end{deluxetable*}')
            tabtxt = ('\n').join(lines)
        else:
            raise ValueError('Unrecognized format ' + str(self.format))
        if self.savefile:
            with open(self.savefile, 'w') as (f):
                f.write(tabtxt)
        return tabtxt


class GraphAction(ActionNode):
    """
    This :class:`ActionNode` will generate a :class:`networkx.DiGraph` object
    representing the node and its children. Note that :mod:`networkx` must be
    installed for this to work.

    When this object is called, it returns a :class:`networkx.DiGraph` object.

    """
    try:
        import pygraphviz
        dldef = 'dot'
    except ImportError:
        from networkx import layout
        dldef = layout.spring_layout
        del layout

    def __init__(self, parent, nodename='Graphing Node', traversal='preorder', drawlayout=dldef, drawkwargs={}, show=False, savefile=None, clf=False):
        ActionNode.__init__(self, parent, nodename)
        self.savefile = savefile
        self.show = show
        self.clf = clf
        self.traversal = traversal
        self.drawlayout = drawlayout
        self.drawkwargs = drawkwargs

    del dldef

    def _doAction(self, node):
        """
        Generate the graph (and save if :attr:`savefile` is not None).

        :param node:
            The node at which to generate the graph. If None, the parent will be
            used.

        :returns: A :class:`networkx.DiGraph` object

        """
        import networkx as nx
        if node is None:
            node = self.parent
        nodeidtopdnode = {}

        def visitfunc(node):
            return (node, None if node.parent is None else (node.parent, node))

        nelist = node.visit(visitfunc, traversal=self.traversal)
        g = nx.DiGraph()
        g.add_node(nelist[0][0])
        for node, edge in nelist[1:]:
            g.add_node(node)
            g.add_edge(edge)

        try:
            if isinstance(self.drawlayout, basestring):
                pos = nx.pygraphviz_layout(g, prog=self.drawlayout)
            elif callable(self.drawlayout):
                pos = self.drawlayout(g)
            else:
                pos = self.drawlayout
            nx.draw(g, pos, **self.drawkwargs)
        except ImportError as e:
            if self.savefile or self.show:
                from warnings import warn
                warn('matplotlib not present, so networkx graph could not be drawn or saved')

        return g


del ABCMeta
del abstractmethod
del abstractproperty
del MutableSequence
del pi
del division