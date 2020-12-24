# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/acting.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 65584 bytes
"""acting.py action module

"""
import time, struct
from collections import deque, Mapping
from functools import wraps
import inspect, copy
try:
    from itertools import izip
except ImportError:
    izip = zip

from ..aid.sixing import *
from .globaling import AUX, MOOT, INDENT_ADD, ScheduleNames, TRANSIT, ActionSubContextNames
from ..aid.odicting import odict
from ..aid.classing import metaclassify, nonStringIterable
from ..aid.aiding import nameToPath
from . import excepting
from . import registering
from . import storing
from . import framing
from ..aid.consoling import getConsole
console = getConsole()

class Act(object):
    __doc__ = ' Container class for actor resolve time initialization and runtime operation '
    __slots__ = ('frame', 'context', 'act', 'actor', 'registrar', 'inits', 'ioinits',
                 'parms', 'prerefs', 'human', 'count', 'inode')

    def __init__(self, frame=None, context=None, act=None, actor=None, registrar=None, inits=None, ioinits=None, parms=None, prerefs=None, human='', count=0, inode=None, **kwa):
        """
        Initialization method for instance.

        Attributes:
            .frame = ref to Frame holding this Act
            .context = name string of actioning context set when added to frame
            .act = ref to super Act if self is embedded in another Act such as Need
            .actor = ref to Actor instance or actor name to be resolved
                    call performs instances method action
            .registrar = ref to Actor class holding .Registry
            .parms = dictionary of keyword arguments for Actor instance call
            .inits = dictionary of arguments to Actor.__init__()
            .ioinits = dictionary of arguments to Actor._initio()
            .prerefs = dictionary of init, ioinit, and parm refs to resolve
            .human = human friendly version of action declaration
            .count = line count in floscript of action declaration
            .inode = actor level inode for ioinits if any

        Share path resolution
            act.resolve aggregates ioinits from registry,  act.ioinits, and act.prerefs
            act.resolve calls .actor._initio with ionits as parameters to get iois
            then for each ioi act.resolve calls .resolvePath to get share or node
            and then assigns share/node to to attribute/parameter of .actor

        """
        (super(Act, self).__init__)(**kwa)
        self.frame = frame
        self.context = context
        self.act = act
        self.actor = actor
        self.registrar = registrar or Actor
        self.parms = parms if parms is not None else odict()
        self.inits = inits if inits else None
        self.ioinits = ioinits if ioinits else None
        self.prerefs = prerefs if prerefs else None
        self.human = human
        self.count = count
        self.inode = inode

    def clone(self):
        """ Return clone of self in support of framer cloning
            clones is dict whose items keys are original framer names
            and values are duples of (original,clone) framer references
        """
        if isinstance(self.frame, framing.Frame):
            msg = "CloneError: Attempting to clone resolved frame link  '{0}'.".format(self.frame.name)
            raise excepting.CloneError(msg)
        else:
            if self.act:
                msg = "CloneError: Attempting to clone resolved act link  '{0}'.".format(self.act)
                raise excepting.CloneError(msg)
            if isinstance(self.actor, Actor):
                msg = "CloneError: Attempting to clone resolved actor  '{0}'.".format(self.actor.name)
                raise excepting.CloneError(msg)
        clone = copy.deepcopy(self)
        return clone

    def __call__(self):
        """ Define act as callable object """
        return (self.actor)(**self.parms)

    def expose(self):
        """ Show attributes"""
        console.terse('Act Actor {0} Parms {1} in Frame {2} Context {3} SuperAct {4}\n'.format(self.actor, self.parms, self.frame, self.context, self.act))
        if self.actor:
            self.actor._expose()

    def resolve(self, **kwa):
        """ Resolve .frame attribute and .actor. Cause .actor to resolve its parms """
        if self.act:
            self.frame = self.act.frame
            self.context = self.act.context
        self.frame = framing.resolveFrame((self.frame), who=('Act for {0}'.format(self.actor)),
          desc="act's",
          human=(self.human),
          count=(self.count))
        if not isinstance(self.actor, Actor):
            actor, inits, ioinits, parms = self.registrar.__fetch__(self.actor)
            if self.prerefs:
                for src, fields in self.prerefs.get('inits', {}).items():
                    src = self.resolvePath(ipath=src, warn=True)
                    if not fields:
                        fields = self._prepareSrcFields(src, fields)
                    for field in fields:
                        if field in src:
                            inits[field] = src[field]

            inits.update(self.inits or odict())
            if 'name' not in inits:
                inits['name'] = self.actor
            inits['store'] = self.frame.store
            inits['act'] = self
            self.actor = actor = actor(**inits)
            if self.prerefs:
                for src, fields in self.prerefs.get('parms', {}).items():
                    src = self.resolvePath(ipath=src, warn=True)
                    if not fields:
                        fields = self._prepareSrcFields(src, fields)
                    for field in fields:
                        if field in src:
                            parms[field] = src[field]

            parms.update(self.parms or odict())
            self.inode = (self.ioinits or odict()).get('inode', ioinits.get('inode', self.inode))
            if self.inode is not None:
                if not isinstance(self.inode, basestring):
                    raise ValueError("Nonstring inode '{0}'".format(self.inode))
            if self.inode:
                if not self.inode.endswith('.'):
                    self.inode = '{0}.'.format(self.inode)
            rioinits = odict(ioinits)
            if self.prerefs:
                if 'ioinits' in self.prerefs:
                    if self.inode is None:
                        self.inode = ''
                    for src, fields in self.prerefs['ioinits'].items():
                        src = self.resolvePath(ipath=src, warn=True)
                        if not fields:
                            fields = self._prepareSrcFields(src, fields)
                        for field in fields:
                            if field in src and field != 'inode':
                                ioinits[field] = src[field]

            ioinits.update(self.ioinits or odict())
            for key, val in rioinits.items():
                if key in ioinits and not isinstance(ioinits[key], Mapping) and isinstance(val, Mapping):
                    val = val.copy()
                    val['ipath'] = ioinits[key]
                    ioinits[key] = val

            if ioinits:
                iois = actor._initio(ioinits)
                if iois:
                    for key, ioi in iois.items():
                        if key == 'inode':
                            share = actor._resolvePath(ipath='', ival=(ioi.get('ival')),
                              iown=(ioi.get('iown')))
                        else:
                            share = actor._resolvePath(ipath=(ioi['ipath']), ival=(ioi.get('ival')),
                              iown=(ioi.get('iown')))
                        if actor._Parametric:
                            if key in parms:
                                msg = 'ResolveError: Parm and Ioi with same name'
                                raise excepting.ResolveError(msg, key, self, self.human, self.count)
                            parms[key] = share
                        else:
                            if hasattr(actor, key):
                                msg = 'ResolveError: Attribute and Ioi with same name'
                                raise excepting.ResolveError(msg, key, self, self.human, self.count)
                            setattr(actor, key, share)

            self.parms = parms
            self.parms.update((self.actor._resolve)(**self.parms))
            (self.actor._prepare)(**self.parms)

    def resolvePath(self, ipath, ival=None, iown=None, warn=False):
        """
        Returns resolved Share or Node instance from ipath
        ipath may be path name of share or node
        or reference to Share or Node instance

        This method resolves inline pathname strings into share and node references
        at resolve time.

        ival is optional value for share
        iown is optional ownership if True then overwrite if exists
               otherwise do not overwrite

        if warn then will complain if the share is created.

        When ipath is empty then resolvePath returns the effective context node
        path given by .inode and nested frame inodes and framer inodes

        It allows for substitution into ipath of
        inode, framer,  main framer, frame, main frame, or actor relative names.
        So that lexically relative pathnames can
        be dynamically resolved in support of framer cloning.
        It assumes that any implied variants have been reconciled.
        If .actor is not yet instantiated then raises exception if ipath
           uses actor relative addressing. This may occur for init prerefs.

        When ipath is a string:  (not a Node or Share reference)
            the following syntax is used:

            If the path name starts with a leading '.' dot then path name is
            fully reconciled and no contextual substitutions are to be applied.

            If the path name begins with 'me' then the path is framer inode relative

            Otherwise make subsitutions in pathname strings that begin
            with 'framer.'
                Substitute for special path part 'framer' with names of 'me' or 'main'
                Substitute for special path part 'frame' with names  of 'me' or 'main'
                Substitute for special path part 'actor' with name of 'me'

                'me' indicates substitute the current framer, frame, or actor name
                respectively.

                'main' indicates substitute the current .main.frame.name or
                .main.frame.framer.name respectively obtained from aux .main link

        If ipath ends with a '.' then it resolves to a node
        Otherwise if not trailing dot it resolves to a share

        When  ipath is a pathname string that resolves to a Share and ival is not None
        Then ival is used to initialize the share values.
            ival should be a share initializer:
               valid initializers are:
                   a dict of fields and values
                   a list of duples, each a (key, value) item

            If own is True then .update(ival) is used
            Otherwise .create(ival) is used

        Requires that:
           self.store exist

           The following have already been resolved:
               self.frame
               self.frame.framer
               self.frame.framer.main
               self.frame.framer.main.framer

           If actor relative addressing is used then:
              self.actor is resolved
              self.actor.name is not empty

        Any actor could have ioinits saved for them in their ._act  Act
        If ionits exist then then an inode should be part of the ioinits
        Currently only the Do verb actors have ioinits. The inode is one of them.
        The ioinits come from two sources. The registry and the do verb per and for
        clauses

        _act.ioinits are the do and per clauses
        registry ioints are from the Actor.Ionints class variable

        So the .inode attribute indicates if the ipath being resolved is for
        an ioinit or not.  If .inode is None it is not for an ioinit.
        Otherwise even if .inode is "" then ipath comes from ioinit and
        path resolution should handle inode logic.

        This would puts all the framer inode prepend
        logic in one place and make it easier to climb the  frame and aux outline
        """
        if not (isinstance(ipath, storing.Share) or isinstance(ipath, storing.Node)):
            parts = ipath.split('.') if ipath else []
            noded = True if not parts else False
            if not parts or parts and parts[0]:
                if not self.frame:
                    raise excepting.ResolveError('ResolveError: Missing frame context to resolve relative pathname.', ipath, self, self.human, self.count)
                elif not self.frame.framer:
                    raise excepting.ResolveError('ResolveError: Missing framer context to resolve relative pathname.', ipath, self.frame, self.human, self.count)
                else:
                    framer = self.frame.framer
                    fparts = framer.inode.rstrip('.').split('.') if framer.inode else []
                    main = framer.main
                    mainer = main.framer if main else None
                    while mainer and (not fparts or fparts[0] not in ('', 'framer')):
                        if fparts:
                            if fparts[0] == 'me':
                                del fparts[0]
                        else:
                            while main and (not fparts or fparts[0] not in ('', 'framer')):
                                if main.inode:
                                    fparts = main.inode.rstrip('.').split('.') + fparts
                                    if fparts:
                                        if fparts[0] == 'me':
                                            del fparts[0]
                                            break
                                main = main.over

                            if fparts:
                                if fparts[0] in ('', 'framer'):
                                    break
                            if mainer.inode:
                                fparts = mainer.inode.rstrip('.').split('.') + fparts
                        main = mainer.main
                        mainer = main.framer if main else None

                    if fparts:
                        if fparts[0] == 'me':
                            del fparts[0]
                    frame = self.frame
                    oparts = frame.inode.rstrip('.').split('.') if frame.inode else []
                    while frame and (not oparts or oparts[0] not in ('', 'framer')):
                        if oparts:
                            if oparts[0] == 'me':
                                del oparts[0]
                                break
                        frame = frame.over
                        if frame and frame.inode:
                            oparts = frame.inode.rstrip('.').split('.') + oparts

                    if self.inode is not None:
                        if not parts or parts[0] not in ('framer', 'me'):
                            iparts = self.inode.rstrip('.').split('.') if self.inode else []
                            if not iparts:
                                if not oparts:
                                    if not fparts:
                                        iparts = 'framer.me.frame.me.actor.me'.split('.')
                            parts = iparts + parts
                    if not parts or parts[0] not in ('', 'framer'):
                        if parts:
                            if parts[0] == 'me':
                                del parts[0]
                        else:
                            parts = oparts + parts
                        if not parts or parts[0] not in ('', 'framer'):
                            parts = fparts + parts
            if parts:
                if parts[0]:
                    if parts[0] == 'framer':
                        if parts[1] == 'me':
                            parts[1] = self.frame.framer.name
                        else:
                            if parts[1] == 'main':
                                if not self.frame.framer.main:
                                    raise excepting.ResolveError('ResolveError: Missing main framer context to resolve relative pathname.', ipath, self.frame.framer, self.human, self.count)
                                parts[1] = self.frame.framer.main.framer.name
                        if len(parts) >= 3:
                            if parts[2] == 'frame':
                                if parts[3] == 'me':
                                    parts[3] = self.frame.name
                                else:
                                    if parts[3] == 'main':
                                        if not self.frame.framer.main:
                                            raise excepting.ResolveError('ResolveError: Missing main frame context to resolve relative pathname.', ipath, self.frame.framer, self.human, self.count)
                                        parts[3] = self.frame.framer.main.name
                                if len(parts) >= 5:
                                    if parts[4] == 'actor':
                                        if parts[5] == 'me':
                                            if not isinstance(self.actor, Actor) or not self.actor.name:
                                                raise excepting.ResolveError('ResolveError: Unresolved actor context to resolve relative pathname.', ipath, self, self.human, self.count)
                                            parts[5:6] = nameToPath(self.actor.name).lstrip('.').rstrip('.').split('.')
                            elif parts[2] == 'actor':
                                if parts[3] == 'me':
                                    if not isinstance(self.actor, Actor) or not self.actor.name:
                                        raise excepting.ResolveError('ResolveError: Unresolved actor context to resolve relative pathname.', ipath, self, self.human, self.count)
                                    parts[3:4] = nameToPath(self.actor.name).lstrip('.').rstrip('.').split('.')
            ipath = '.'.join(parts)
            if noded:
                if ipath:
                    if not ipath.endswith('.'):
                        ipath = '{0}.'.format(ipath)
            if not self.frame.store:
                raise excepting.ResolveError('ResolveError: Missing store context to resolve relative pathname.', ipath, self, self.human, self.count)
            if ipath.endswith('.'):
                ipath = self.frame.store.createNode(ipath.rstrip('.'))
                if warn:
                    console.profuse("     Warning: Non-existent node '{0}' ... creating anyway\n".format(ipath))
            else:
                ipath = self.frame.store.create(ipath)
                if ival is not None:
                    if iown:
                        ipath.update(ival)
                    else:
                        ipath.create(ival)
                if warn:
                    console.profuse("     Warning: Non-existent node '{0}' ... creating anyway\n".format(ipath))
        return ipath

    def _prepareSrcFields(self, src, fields):
        """
        Prepares and verifys list field names fields in share src
           handles default conditions when fields is empty

           src is share
           fields is list of field names

        """
        if not fields:
            if src:
                if 'value' in src:
                    fields = [
                     'value']
                else:
                    fields = src.keys()
            else:
                fields = [
                 'value']
        return fields


class Nact(Act):
    __doc__ = ' Negating Act used for actor needs to give Not Need\n    '
    __slots__ = ('frame', 'context', 'act', 'actor', 'registrar', 'parms', 'inits',
                 'ioinits', 'human', 'count')

    def __init__(self, **kwa):
        (super(Nact, self).__init__)(**kwa)

    def __call__(self):
        """Define act as callable object
           Negate the output
        """
        return not (self.actor)(**self.parms)

    def expose(self):
        """ Show attributes """
        console.terse('Nact Actor {0} Parms {1} in Frame {2} Context {3} SuperAct {4}\n'.format(self.actor, self.parms, self.frame, self.context, self.act))
        if self.actor:
            self.actor._expose()


class SideAct(Act):
    __doc__ = " Anciliary act to a main Act/Actor used to call a different 'action' method\n        of the Main act.actor in support of combined activity such as restarting\n        an action.\n\n        SideActs are created in the .resolve method of an Actor and assume that\n        all attributes and parms have already been resolved.\n\n        Unique Attributes:\n            .action = name of method to call in .actor\n    "
    __slots__ = 'action'

    def __init__(self, action='', **kwa):
        """ Initialization method for instance. """
        (super(SideAct, self).__init__)(**kwa)
        self.action = action

    def __call__(self):
        """ Define call method named .action of .actor """
        return (getattr(self.actor, self.action))(**self.parms)

    def resolve(self, **kwa):
        """ Assumes all has been resolved.
            Check for valid action
        """
        if not isinstance(self.actor, Actor):
            msg = 'ResolveError: Unresolved actor'
            raise excepting.ResolveError(msg, self.actor, self)
        else:
            if not self.action:
                msg = 'ResolveError: Empty action'
                raise excepting.ResolveError(msg, self.action, self, self.human, self.count)
            msg = getattr(self.actor, self.action, None) or 'ResolveError: Missing action in actor'
            raise excepting.ResolveError(msg, self.action, self, self.human, self.count)


def actify(name, base=None, registry=None, inits=None, ioinits=None, parms=None, parametric=None):
    """ Parametrized decorator function that converts the decorated function
        into an Actor sub class with .action method and with class name that
        is name and registers the new subclass in the registry under name as
        a subclass of base. The default base is Actor.

        The parameters  registry, parametric, inits, ioinits, and parms if provided,
        are used to create the class attributes for the new subclass

    """
    base = base or Actor
    if not issubclass(base, Actor):
        msg = "Base class '{0}' not subclass of Actor".format(base)
        raise excepting.RegisterError(msg)
    attrs = odict()
    if registry:
        attrs['Registry'] = odict()
    if parametric is not None:
        attrs['_Parametric'] = True if parametric else False
    if inits:
        attrs['Inits'] = odict(inits)
    if ioinits:
        attrs['Ioinits'] = odict(ioinits)
    if parms:
        attrs['Parms'] = odict(parms)
    cls = type(name, (base,), attrs)

    def implicit(func):

        @wraps(func)
        def inner(*pa, **kwa):
            return func(*pa, **kwa)

        cls.action = inner
        return inner

    return implicit


actorify = actify

@metaclassify(registering.RegisterType)
class Actor(object):
    __doc__ = ' Actor Base Class\n        Has Actor specific Registry of classes\n    '
    Registry = odict()
    Inits = odict()
    Ioinits = odict()
    Parms = odict()
    _Parametric = True
    __slots__ = ('name', 'store', '_act')

    def __init__(self, name='', store=None, act=None, **kwa):
        """
        Initialization method for instance.

        Instance attributes
            .name = name string for Actor variant in class Registry
            .store = reference to shared data Store
            ._act = reference to containing Act

        If subclass has init need to call super
        super(SubClassName, self).__init__(**kwa)

        """
        self.name = name
        if store is not None:
            if not isinstance(store, storing.Store):
                raise ValueError('Not store {0}'.format(store))
            self.store = store
        self._act = act

    def __call__(self, **kwa):
        """ run .action  """
        return (self.action)(**kwa)

    def action(self, **kwa):
        """Action called by Actor. Should override in subclass."""
        console.profuse('Actioning {0} in {1} of {2} with {3}\n'.format(self.name, self._act.frame.name, self._act.frame.framer.name, str(kwa)))

    def _expose(self):
        """Show Actor."""
        console.terse('Actor {0}'.format(self.name))

    def _resolve(self, **kwa):
        """ Return updated parms
            Extend in subclass to resolve specific kwa items that are links or
            share refs and update parms
        """
        parms = odict()
        return parms

    def _initio(self, ioinits):
        """
        Compute initializations for ioflo shares from ioinits (odict or item list)

        The 'inode' item in ioinits is special. Act.resolve extracts 'inode' from
        ioinits and assigns to ._act.inode before ._initio is called.

        This implements a generic Actor interface protocol for associating the
        io data flow shares to the Actor.

        The ._act.inode attribute holds the pathname string of the default
        data store node where shares associated with the Actor instance may
        be placed when relative addressing is used.
        It is also the default data store context
        for share references by Doer iois. The inode on an actor my be set
        explicitly in the Ioinit class variable or in the actify (doify) decorator
        or by the via clause of a Doer

        The values of the items in the **kwa argument may be either strings or
        mappings

        For each key,val in ioinits.items() there are the following 2 forms for val:

        1- string:
           ipath = pathnamestring
        2- dict of items (mapping) of form:
            {
                ipath: "pathnamestring", (optional)
                ival: initial value, (optional)
                iown: truthy, (optional)
            }

        In either case, three init values are produced, these are:
            ipath, ival, iown,
        Missing init values from ipath, ival, iown will be assigned a
        default value as per the rules below:

        For each ioinits item (key, val) besides the inode
            key is the name of the associated instance attribute or action parm.
            Extract ipath, ival, iown from val

            Shares are initialized with mappings passed into share.create or
            share.update. So to assign ival to share.value pass into share.create
            or share.update a mapping of the form {'value': ival} whereas
            passing in an empty mapping does nothing.

            If ipath not provided
                ipath is the default path inode.key
            Else ipath is provided
                If ipath starts with dot "." Then absolute path
                Else ipath does not start with dot "." Then relative path from inode

                If ipath ends with dot Then the path is to a node not share
                        node ref is created and remaining init values are ignored

            If ival not provided
                 set ival to empty mapping which when passed to share.create
                 will not change share.value
            Else ival provided
                If ival is an empty Mapping Then
                    assign a shallow copy of ival to share.value by passing
                    in {value: ival (copy)} to share.create/.update
                Else If ival is a non-string iterable and not a mapping
                    assign a shallow copy of ival to share.value by passing
                    in {value: ival (copy)} to share.create/.update
                Else If ival is a non-empty Mapping Then
                    Each item in ival is assigned as a field, value pair in the share
                    by passing ival directly into share.create or share.update
                    This means there is no way to init a share.value to a non empty mapping
                    It is possible to init a share.value to an empty mapping see below
                Else
                    assign ival to share.value by by passing
                    in {value: ival} to share.create or share.update

            Create share with pathname given by ipath

            If iown Then
                init share with ival value using update
            Else
                init share with ival value using create ((change if not exist))

        """
        ioinits = odict(ioinits)
        if self._act.inode is None:
            self._act.inode = ''
        iois = odict()
        ioi = odict(ipath=(self._act.inode))
        iois['inode'] = ioi
        for key, val in ioinits.items():
            if key == 'inode':
                pass
            else:
                if val is None:
                    val = ''
                else:
                    if isinstance(val, basestring):
                        ipath = val
                        iown = None
                        ival = odict()
                    else:
                        if isinstance(val, Mapping):
                            ipath = val.get('ipath', '')
                            iown = val.get('iown')
                            if 'ival' not in val:
                                ival = odict()
                            else:
                                ival = val['ival']
                                if isinstance(ival, Mapping):
                                    if not ival:
                                        ival = odict(value=(copy.copy(ival)))
                                else:
                                    if nonStringIterable(ival):
                                        ival = odict(value=(copy.copy(ival)))
                                    else:
                                        ival = odict(value=ival)
                        else:
                            raise ValueError("Bad ioinit for key '{0}' with value '{1}'".format(key, val))
                if not ipath:
                    ipath = key
                ioi = odict(ipath=ipath, ival=ival, iown=iown)
                iois[key] = ioi

        return iois

    def _prepare(self, **kwa):
        """ Base method to be overriden in sub classes. Perform post initio setup
            after all parms and ioi parms or attributes have been created
            kwa usually parms.

            If one is using this method consider refactoring into two different
            behaviors
        """
        pass

    def _resolvePath(self, ipath, ival=None, iown=None, warn=False):
        """ Returns resolved Share or Node instance from ipath
            Calls self._act.resolvePath()
            See doc string from Act.resolvePath for detailed description of
            functionality

            Requires that
               self._act exist
        """
        if not (isinstance(ipath, storing.Share) or isinstance(ipath, storing.Node)):
            if not self._act:
                raise excepting.ResolveError('ResolveError: Missing act context to resolve relative pathname.', ipath, self, self._act.human, self._act.count)
            ipath = self._act.resolvePath(ipath=ipath, ival=ival,
              iown=iown,
              warn=warn)
        return ipath

    def _prepareDstFields(self, srcFields, dst, dstFields):
        """
        Prepares  for a transfer of data
           from srcFields
           to dstFields in dst
        Handles default conditions when fields are empty
            srcFields is list of field names
            dst is share
            dstFields is list of field names

        Ensure Builder.prepareDataDstFields is similar
        """
        if not dstFields:
            if 'value' in dst:
                dstFields = [
                 'value']
            else:
                dstFields = srcFields
        self._verifyShareFields(dst, dstFields)
        if len(srcFields) != len(dstFields):
            msg = 'ResolveError: Unequal number of source = {0} and destination = {2} fields'.format(srcFields, dstFields)
            raise excepting.ResolveError(msg, self.name, '', self._act.human, self._act.count)
        for dstField, srcField in izip(dstFields, srcFields):
            if dstField != srcField and srcField != 'value':
                console.profuse("     Warning: Field names mismatch. '{0}' in {1} from '{2}' ... creating anyway".format(dstField, dst.name, srcField))

        for field in dstFields:
            if field not in dst:
                console.profuse("     Warning: Transfer into non-existent field '{0}' in share {1} ... creating anyway\n".format(field, dst.name))
                dst[field] = None

        return dstFields

    def _prepareSrcDstFields(self, src, srcFields, dst, dstFields):
        """
        Prepares and verifys a transfer of data
           from srcFields in src
           to dstFields in dst
        Handles default conditions when fields are empty
           src and dst are shares
           srcFields and dstFields are lists

        Ensure Builder.prepareSrcDstFields is the same
        """
        if not srcFields:
            if src:
                if 'value' in src:
                    srcFields = [
                     'value']
                else:
                    if dstFields:
                        srcFields = dstFields
                    else:
                        srcFields = src.keys()
            else:
                srcFields = [
                 'value']
        else:
            self._verifyShareFields(src, srcFields)
            if not dstFields:
                if 'value' in dst:
                    dstFields = [
                     'value']
                else:
                    dstFields = srcFields
            self._verifyShareFields(dst, dstFields)
            if len(srcFields) != len(dstFields):
                msg = 'ResolveError: Unequal number of fields, source = {0} and destination={1)'.format(srcFields, dstFields)
                raise excepting.ResolveError(msg, self.name, '', self._act.human, self._act.count)
        for dstField, srcField in izip(dstFields, srcFields):
            if dstField != srcField and srcField != 'value':
                console.profuse("     Warning: Field names mismatch. '{0}' in {1} from '{2}' in {3}  ... creating anyway".format(dstField, dst.name, srcField, src.name))

        for field in srcFields:
            if field not in src:
                console.profuse("     Warning: Transfer from non-existent field '{0}' in share {1} ... creating anyway".format(field, src.name))
                src[field] = None

        for field in dstFields:
            if field not in dst:
                console.profuse("     Warning: Transfer into non-existent field '{0}' in share {1} ... creating anyway\n".format(field, dst.name))
                dst[field] = None

        return (
         srcFields, dstFields)

    def _verifyShareFields(self, share, fields):
        """
        Verify that updating fields in share won't violate the
           condition that when a share has field == 'value'
           it will be the only field

           fields is list of field names
           share is  share

        Raises exception if condition would be violated

        Ensure Builder.verifyShareFields is same
        """
        if len(fields) > 1:
            if 'value' in fields:
                msg = "ResolveError: Field = 'value' within fields = '{0}'".format(fields)
                raise excepting.ResolveError(msg, self.name, '', self._act.human, self._act.count)
        if share:
            for field in fields:
                if field not in share and ('value' in share or field == 'value'):
                    msg = "ResolveError: Candidate field '{0}' when fields = '{1}' exist".format(field, share.keys())
                    raise excepting.ResolveError(msg, self.name, '', self._act.human, self._act.count)


class Interrupter(Actor):
    __doc__ = "\n    Interrupter Actor Class\n    Interrupter is a base clase for all actor classes that interrupt normal precur\n    processing and result in a change in the frame or the frame processing.\n\n    This class must be subclassed. This is a convenience so can either use\n      isinstance to test\n\n    Specifically an Interrupter's action() method returns truthy when its action\n    interrupts the normal frame processing.\n\n    Examples are:\n    Transiters which interrupt by changing to a new frame\n    Suspenders which interrupt when the conditional aux condition is true and\n       further processing of the frame and sub frames is stopped\n    "

    def __init__(self, **kw):
        (super(Interrupter, self).__init__)(**kw)
        self._tracts = []


class Transiter(Interrupter):
    __doc__ = 'Transiter Interrupter Class\n       Transiter  is a special actor that performs transitions between frames\n\n       Parameters\n            needs = list of Act objects that are exit needs for this trans\n            near = source frame of trans\n            far = target frame of trans\n            human = text version of transition\n\n    '

    def _resolve(self, needs, near, far, human, **kwa):
        parms = (super(Transiter, self)._resolve)(**kwa)
        if near == 'me':
            near = self._act.frame
        parms['near'] = near = framing.resolveFrame(near, who=(self.name),
          desc='near',
          human=(self._act.human),
          count=(self._act.count))
        if far == 'next':
            if not isinstance(near.next_, framing.Frame):
                raise excepting.ResolveError('ResolveError: Bad next frame', near.name, near.next_, self._act.human, self._act.count)
            far = near.next_
        else:
            if far == 'me':
                far = near
        far = framing.resolveFrame(far, who=(self.name),
          desc='far',
          human=(self._act.human),
          count=(self._act.count))
        parms['far'] = far
        for act in needs:
            act.act = self._act
            act.resolve()
            self._tracts.extend(act.actor._tracts)
            del act.actor._tracts[:]

        return parms

    def action(self, needs, near, far, human, **kw):
        """Action called by Actor  """
        framer = near.framer
        console.profuse('Attempt segue from {0} to {1}\n'.format(near.name, far.name))
        for act in needs:
            if not act():
                return

        console.profuse('     active outline: {0}\n'.format([frame.name for frame in framer.actives]))
        console.profuse('     far outline: {0}\n'.format([frame.name for frame in far.outline]))
        exits, enters, reexens = framing.Framer.ExEn(framer.actives, far)
        if not framer.checkEnter(enters, exits):
            return
        else:
            msg = 'To: {0}<{1} at {2} Via: {3} ({4}) From: {5} after {6:0.3f}\n'.format(framer.name, far.human, round(framer.store.stamp, 6), near.name, human, framer.human, framer.elapsed)
            console.terse(msg)
            console.profuse('     exits: {0}\n'.format([frame.name for frame in exits]))
            console.profuse('     enters: {0}\n'.format([frame.name for frame in enters]))
            console.profuse('     reexens: {0}\n'.format([frame.name for frame in reexens]))
            for act in self._tracts:
                act()

            framer.exit(exits)
            framer.rexit(reexens[:])
            framer.renter(reexens)
            framer.enter(enters)
            framer.activate(active=far)
            return far

    def _expose(self):
        """      """
        console.terse('Transiter {0}\n'.format(self.name))


class Suspender(Interrupter):
    __doc__ = 'Suspender Interrupter Class\n       Suspender  is a special actor that performs a conditional auxiliary\n          which truncates the active outline effectively suspended the truncated\n          frames\n\n       Parameters\n            needs = list of Act objects that are exit needs for this trans\n            main = source frame of trans\n            aux = target frame of trans\n            human = text version of transition\n\n    '

    def __init__(self, **kw):
        (super(Suspender, self).__init__)(**kw)

    def _resolve(self, needs, main, aux, human, **kwa):
        parms = (super(Suspender, self)._resolve)(**kwa)
        if main == 'me':
            main = self._act.frame
        parms['main'] = main = framing.resolveFrame(main, who=main,
          desc='main',
          human=(self._act.human),
          count=(self._act.count))
        parms['aux'] = aux = framing.resolveFramer(aux, who=(main.name),
          desc='aux',
          contexts=[
         AUX],
          human=(self._act.human),
          count=(self._act.count))
        for act in needs:
            act.act = self._act
            act.resolve()
            self._tracts.extend(act.actor._tracts)
            del act.actor._tracts[:]

        deActParms = odict(aux=aux)
        deAct = SideAct(actor=self, parms=deActParms,
          action='deactivize',
          human=(self._act.human),
          count=(self._act.count))
        self._act.frame.addExact(deAct)
        console.profuse('{0}Added exact {1} SideAct for {2} with {3} in {4}\n'.format(INDENT_ADD, 'deactivize', self.name, deAct.parms, self._act.frame.name))
        deAct.resolve()
        return parms

    def action(self, needs, main, aux, human, **kw):
        """Action called by Actor  """
        framer = main.framer
        if aux.done:
            console.profuse('Attempt segue from {0} to aux {1}\n'.format(main.name, aux.name))
            for act in needs:
                if not act():
                    return

            if aux.main and aux.main is not self._act.frame:
                console.concise("    Invalid aux '{0}' in use by another frame '{1}'\n".format(aux.name, aux.main.name))
                return
            else:
                if not aux.checkStart():
                    return
                else:
                    msg = 'To: {0} in {1}<{2} at {3} Via: {4} ({5}) From: {6} after {7:0.3f}\n'.format(aux.name, framer.name, main.headHuman, round(framer.store.stamp, 6), main.name, human, framer.human, framer.elapsed)
                    console.terse(msg)
                    for act in self._tracts:
                        act()

                    if aux.original:
                        aux.main = main
                    aux.enterAll()
                    aux.recur()
                    if aux.done:
                        self.deactivate(aux)
                        return
                framer.change(main.head, main.headHuman)
                return aux
        if not aux.done:
            aux.segue()
            aux.recur()
            if aux.done:
                self.deactivate(aux)
                framer.reactivate()
                return
            else:
                return aux

    def _expose(self):
        """      """
        console.terse('Suspender {0}\n'.format(self.name))

    def deactivize(self, aux, **kwa):
        """ If not aux.done Then force deactivate. Used in exit action."""
        if not aux.done:
            console.profuse('{0} deactivate {1}\n'.format(self.name, aux.name))
            self.deactivate(aux)

    def deactivate(self, aux):
        """Called by deactivator actor to cleanly exit      """
        console.profuse('Deactivating {0}\n'.format(aux.name))
        aux.exitAll()
        if aux.original:
            aux.main = None


class Printer(Actor):
    __doc__ = 'Printor Actor Class\n\n       Printer is a special actor that just prints to console its message\n\n    '

    def action(self, message, **kw):
        """Action called by Actor
        """
        console.terse('*** {0} ***\n'.format(message))

    def _expose(self):
        """   """
        console.terse('Printer {0}\n'.format(self.name))


class Marker(Actor):
    __doc__ = ' Base class that sets up mark in provided share reference'


class MarkerUpdate(Marker):
    __doc__ = ' MarkerUpdate Class\n\n        MarkerUpdate is a special actor that acts on a share to mark the update by\n            saving a copy of the last stamp\n\n        MarkerUpdate works with NeedUpdate which does the comparison against the marked stamp.\n\n        Builder at parse time when it encounters an NeedUpdate,\n        creates the mark in the share and creates the appropriate MarkerUpdate\n    '

    def action(self, share, marker, **kwa):
        """ Update mark in share
            Where share is reference to share and marker is unique name key of mark in
                share.marks odict
            Updates mark.stamp

            only one mark per marker per share is needed
        """
        console.profuse('{0} mark {1} in {2} on {3}\n'.format(self.name, share.name, marker, 'update'))
        mark = share.marks.get(marker)
        if mark:
            mark.stamp = self.store.stamp
            if self._act.context == ActionSubContextNames[TRANSIT]:
                mark.used = mark.stamp

    def _expose(self):
        """   """
        console.terse('MarkerUpdate {0}\n'.format(self.name))


class MarkerChange(Marker):
    __doc__ = ' MarkerChange Class\n\n        MarkerChange is a special actor that acts on a share to mark save a copy\n        of the data in the mark for the share.\n\n        MarkerChange works with NeedChange which does the comparison with the mark\n\n        Builder at parse time when it encounters a NeedChange,\n        creates the mark in the share and creates the appropriate marker\n    '

    def action(self, share, marker, **kwa):
        """ Update mark in share
            Where share is reference to share and marker is unique name key of mark in
                share.marks odict
            Updates mark.data

            only one mark per marker per share is needed
        """
        console.profuse('{0} mark {1} in {2} on {3}\n'.format(self.name, share.name, marker, 'change'))
        mark = share.marks.get(marker)
        if mark:
            mark.data = storing.Data(share.items())

    def _expose(self):
        """   """
        console.terse('MarkerChange {0}\n'.format(self.name))


class Rearer(Actor):
    __doc__ = '\n    Rearer Actor Class\n    Rearer is a special actor that clones a moot framer at runtime\n\n       Parameters\n            original = moot framer to be cloned\n            clone = name of clone\n            schedule = schedule kind of clone\n            frame = frame to put auxiliary clone in\n\n    '

    def _resolve(self, original, clone, schedule, frame, **kwa):
        parms = (super(Rearer, self)._resolve)(**kwa)
        parms['original'] = original = framing.resolveFramer(original, who=(self.name),
          desc='original',
          contexts=[
         MOOT],
          human=(self._act.human),
          count=(self._act.count))
        if schedule not in [AUX]:
            msg = "ResolveError: Invalid schedule '{0}' for cloneof '{1}'".format(ScheduleNames.get(schedule, schedule), original.name)
            raise excepting.ResolveError(msg=msg, name=(self.name),
              value=schedule,
              human=(self._act.human),
              count=(self._act.count))
        else:
            if schedule == AUX:
                parms['framer'] = framer = framing.resolveFramer((self._act.frame.framer), who=(self._act.frame.name),
                  desc='rear aux clone',
                  contexts=[],
                  human=(self._act.human),
                  count=(self._act.count))
                if frame == 'me':
                    msg = "ResolveError: Invalid frame 'me' for reared clone."
                    raise excepting.ResolveError(msg, name=clone,
                      value=(self.name),
                      human=(self._act.human),
                      count=(self._act.count))
                parms['frame'] = frame = framing.resolveFrameOfFramer(frame, framer,
                  who=(self._act.frame.name),
                  desc='rear aux clone',
                  human=(self._act.human),
                  count=(self._act.count))
                if clone != 'mine':
                    msg = "ResolveError: Aux insular clone name must be 'mine' not '{0}'".format(clone)
                    raise excepting.ResolveError(msg, name=clone,
                      value=(self.name),
                      human=(self._act.human),
                      count=(self._act.count))
            else:
                msg = "ResolveError: Invalid insular clone schedule '{0}' for {1}.".format(schedule, original)
                raise excepting.ResolveError(msg, name=clone,
                  value=(self.name),
                  human=(self._act.human),
                  count=(self._act.count))
        return parms

    def action(self, original, clone, schedule, frame, framer, **kw):
        """
        Action called by Actor

        Parameters:
           original is resolved original moot framer to be cloned
           clone is clone tag (not used currently)
           schedule is clone schedule
           frame is resolved frame for reared clone
           framer is resolved framer for frame for reared clone

        """
        console.profuse("         Cloning '{0}' as '{1}' be '{2}'\n".format(original.name, clone, ScheduleNames.get(schedule, schedule)))
        if schedule == AUX:
            if frame in self._act.frame.outline:
                console.terse("         Error: Cannot rear clone in own '{0}' outline. {1} in line {2}\n".format(frame.name, self._act.human, self._act.count))
                return
            tag = framer.newAuxTag(base=(original.tag))
            name = '_'.join((framer.surname, tag))
            console.terse("         Rearing original '{0}' as aux insular clone '{1}' in Frame '{2}' in Framer '{3}'\n".format(original.name, name, frame.name, framer.name))
            clone = original.clone(name=name, tag=tag, schedule=schedule)
            clone.original = False
            clone.insular = True
            clone.razeable = True
            framer.auxes[tag] = clone
            frame.addAux(clone)
            clone.main = frame
            self.store.house.presolvables.append(clone)
            self.store.house.presolvePresolvables()
            self.store.house.resolveResolvables()


class Razer(Actor):
    __doc__ = '\n    Razer Actor Class\n    Razer is a special actor that destroys a  framer clone at runtime\n\n       Parameters\n            who = auxiliary clones to be destroyed\n            frame = frame holding clones to be destroyed\n\n    '

    def _resolve(self, who, frame, **kwa):
        parms = (super(Razer, self)._resolve)(**kwa)
        parms['framer'] = framer = framing.resolveFramer((self._act.frame.framer), who=(self._act.frame.name),
          desc='rear aux clone',
          contexts=[],
          human=(self._act.human),
          count=(self._act.count))
        if frame == 'me':
            frame = self._act.frame
        parms['frame'] = frame = framing.resolveFrameOfFramer(frame, framer,
          who=(self._act.frame.name),
          desc='rear aux clone',
          human=(self._act.human),
          count=(self._act.count))
        return parms

    def action(self, who, frame, framer, **kw):
        """
        Action called by Actor

        Parameters:
           who is string describing which aux(es) to raze
           frame is frame with auxes to raze
           framer is framer of frame with auxes to raze
        """
        razeables = []
        if who == 'all':
            for aux in frame.auxes:
                if aux.insular and aux.razeable:
                    razeables.append(aux)

        else:
            if who == 'first':
                for aux in frame.auxes:
                    if aux.insular:
                        if aux.razeable:
                            razeables.append(aux)
                            break

            else:
                if who == 'last':
                    for aux in reversed(frame.auxes):
                        if aux.insular:
                            if aux.razeable:
                                razeables.append(aux)
                                break

        for aux in razeables:
            console.concise("         Razing '{0}' in '{1}'\n".format(who, frame.name))
            aux.prune()
            frame.auxes.remove(aux)
            if aux.tag in framer.auxes:
                del framer.auxes[aux.tag]