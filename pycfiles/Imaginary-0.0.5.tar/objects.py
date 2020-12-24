# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/Divmod-release/Imaginary/imaginary/objects.py
# Compiled at: 2009-06-29 01:03:17
from __future__ import division
import math
from zope.interface import implements
from twisted.python import reflect, components
from epsilon import structlike
from axiom import item, attributes
from imaginary import iimaginary, eimaginary, text as T, events, language
from imaginary.enhancement import Enhancement as _Enhancement

def merge(d1, *dn):
    """
    da = {a: [1, 2]}
    db = {b: [3]}
    dc = {b: [5], c: [2, 4]}
    merge(da, db, dc)
    da == {a: [1, 2], b: [3, 5], c: [2, 4]}
    """
    for d in dn:
        for (k, v) in d.iteritems():
            d1.setdefault(k, []).extend(v)


class Points(item.Item):
    max = attributes.integer(doc='\n    Maximum number of points.\n    ', allowNone=False)
    current = attributes.integer(doc='\n    Current number of points.\n    ', allowNone=False)

    def __init__(self, **kw):
        if 'max' in kw and 'current' not in kw:
            kw['current'] = kw['max']
        super(Points, self).__init__(**kw)

    def __cmp__(self, other):
        return cmp(self.current, other)

    def __str__(self):
        return '%d/%d' % (self.current, self.max)

    def __repr__(self):
        d = {'class': reflect.qual(self.__class__), 'current': self.current, 
           'max': self.max}
        return '%(class)s(%(max)d, %(current)d)' % d

    def increase(self, amount):
        return self.modify(amount)

    def decrease(self, amount):
        return self.modify(-amount)

    def modify(self, amount):
        self.current = max(min(self.current + amount, self.max), 0)
        return self.current


class Thing(item.Item):
    implements(iimaginary.IThing, iimaginary.IVisible)
    weight = attributes.integer(doc='\n    Units of weight of this object.\n    ', default=1, allowNone=False)
    location = attributes.reference(doc='\n    Direct reference to the location of this object\n    ')
    portable = attributes.boolean(doc='\n    Whether this can be picked up, pushed around, relocated, etc\n    ', default=True, allowNone=False)
    name = attributes.text(doc='\n    The name of this object.\n    ', allowNone=False)
    description = attributes.text(doc='\n    What this object looks like.\n    ', default='')
    gender = attributes.integer(doc='\n    The grammatical gender of this thing.  One of L{language.Gender.MALE},\n    L{language.Gender.FEMALE}, or L{language.Gender.NEUTER}.\n    ', default=language.Gender.NEUTER, allowNone=False)
    proper = attributes.boolean(doc='\n    Whether my name is a proper noun.\n    ', default=False, allowNone=False)

    def destroy(self):
        if self.location is not None:
            iimaginary.IContainer(self.location).remove(self)
        self.deleteFromStore()
        return

    def links(self):
        d = {self.name.lower(): [self]}
        if self.location is not None:
            merge(d, {self.location.name: [self.location]})
        for pup in self.powerupsFor(iimaginary.ILinkContributor):
            merge(d, pup.links())

        return d

    thing = property(lambda self: self)
    _ProviderStackElement = structlike.record('distance stability target proxies')

    def findProviders(self, interface, distance):
        seen = {}
        visited = {self: True}
        facet = interface(self, None)
        initialProxies = list(self.powerupsFor(iimaginary.IProxy))
        locationProxies = set()
        if self.location is not None:
            locationProxies.update(set(self.location.powerupsFor(iimaginary.ILocationProxy)))
        if facet is not None:
            seen[self] = True
            proxiedFacet = self._applyProxies(locationProxies, initialProxies, facet, interface)
            if proxiedFacet is not None:
                yield proxiedFacet
        stabilityHelper = 1
        descendTo = [
         self._ProviderStackElement(distance, 0, self, initialProxies)]
        while descendTo:
            element = descendTo.pop()
            distance, target, proxies = element.distance, element.target, element.proxies
            links = target.links().items()
            links.sort()
            for (linkName, linkedThings) in links:
                for linkedThing in linkedThings:
                    if distance:
                        if linkedThing not in visited:
                            visited[linkedThing] = True
                            stabilityHelper += 1
                            locationProxies.update(set(linkedThing.powerupsFor(iimaginary.ILocationProxy)))
                            proxies = proxies + list(linkedThing.powerupsFor(iimaginary.IProxy))
                            descendTo.append(self._ProviderStackElement(distance - 1, stabilityHelper, linkedThing, proxies))
                    facet = interface(linkedThing, None)
                    if facet is not None and linkedThing not in seen:
                        seen[linkedThing] = True
                        proxiedFacet = self._applyProxies(locationProxies, proxies, facet, interface)
                        if proxiedFacet is not None:
                            yield proxiedFacet

            descendTo.sort()

        return

    def _applyProxies(self, locationProxies, proxies, obj, interface):
        for proxy in locationProxies:
            if iimaginary.IContainer(proxy.thing).contains(obj.thing) or proxy.thing is obj.thing:
                obj = proxy.proxy(obj, interface)
                if obj is None:
                    return

        for proxy in proxies:
            obj = proxy.proxy(obj, interface)
            if obj is None:
                return

        return obj

    def proxiedThing(self, thing, interface, distance):
        for prospectiveFacet in self.findProviders(interface, distance):
            if prospectiveFacet.thing is thing:
                return prospectiveFacet

        raise eimaginary.ThingNotFound(thing)

    def search(self, distance, interface, name):
        """
        Retrieve game objects answering to the given name which provide the
        given interface and are within the given distance.

        @type distance: C{int}
        @param distance: How many steps to traverse (note: this is wrong, it
        will become a real distance-y thing with real game-meaning someday).

        @param interface: The interface which objects within the required range
        must be adaptable to in order to be returned.

        @type name: C{str}
        @param name: The name of the stuff.

        @return: An iterable of L{iimaginary.IThing} providers which are found.
        """
        extras = []
        container = iimaginary.IContainer(self.location, None)
        if container is not None:
            potentialExit = container.getExitNamed(name, None)
            if potentialExit is not None:
                try:
                    potentialThing = self.proxiedThing(potentialExit.toLocation, interface, distance)
                except eimaginary.ThingNotFound:
                    pass
                else:
                    yield potentialThing
        if name == 'me' or name == 'self':
            facet = interface(self, None)
            if facet is not None:
                extras.append(self)
        if name == 'here' and self.location is not None:
            facet = interface(self.location, None)
            if facet is not None:
                extras.append(self.location)
        for res in self.findProviders(interface, distance):
            if res.thing in extras:
                yield res
            elif res.thing.knownAs(name):
                yield res

        return

    def moveTo(self, where, arrivalEventFactory=None):
        """
        @see: L{iimaginary.IThing.moveTo}.
        """
        if where is self.location:
            return
        else:
            oldLocation = self.location
            if oldLocation is not None:
                events.DepartureEvent(oldLocation, self).broadcast()
            if where is not None:
                where = iimaginary.IContainer(where)
                if oldLocation is not None and not self.portable:
                    raise eimaginary.CannotMove(self, where)
                where.add(self)
                if arrivalEventFactory is not None:
                    arrivalEventFactory(self).broadcast()
            if oldLocation is not None:
                iimaginary.IContainer(oldLocation).remove(self)
            return

    def knownAs(self, name):
        """
        Return C{True} if C{name} might refer to this L{Thing}, C{False} otherwise.

        XXX - See #2604.
        """
        name = name.lower()
        mine = self.name.lower()
        return name == mine or name in mine.split()

    def visualize(self):
        container = iimaginary.IContainer(self.thing, None)
        if container is not None:
            exits = list(container.getExits())
        else:
            exits = ()
        return language.DescriptionConcept(self.name, self.description, exits, self.powerupsFor(iimaginary.IDescriptionContributor))


components.registerAdapter(lambda thing: language.Noun(thing).nounPhrase(), Thing, iimaginary.IConcept)
OPPOSITE_DIRECTIONS = {'north': 'south', 
   'west': 'east', 
   'northwest': 'southeast', 
   'northeast': 'southwest'}
for (k, v) in OPPOSITE_DIRECTIONS.items():
    OPPOSITE_DIRECTIONS[v] = k

class Exit(item.Item):
    fromLocation = attributes.reference(doc='\n    Where this exit leads from.\n    ', allowNone=False, whenDeleted=attributes.reference.CASCADE, reftype=Thing)
    toLocation = attributes.reference(doc='\n    Where this exit leads to.\n    ', allowNone=False, whenDeleted=attributes.reference.CASCADE, reftype=Thing)
    name = attributes.text(doc='\n    What this exit is called/which direction it is in.\n    ', allowNone=False)
    sibling = attributes.reference(doc='\n    The reverse exit object, if one exists.\n    ')

    def link(cls, a, b, forwardName, backwardName=None):
        if backwardName is None:
            backwardName = OPPOSITE_DIRECTIONS[forwardName]
        me = cls(store=a.store, fromLocation=a, toLocation=b, name=forwardName)
        him = cls(store=b.store, fromLocation=b, toLocation=a, name=backwardName)
        me.sibling = him
        him.sibling = me
        return

    link = classmethod(link)

    def destroy(self):
        if self.sibling is not None:
            self.sibling.deleteFromStore()
        self.deleteFromStore()
        return

    def conceptualize(self):
        return language.ExpressList(['the exit to ', language.Noun(self.toLocation).nounPhrase()])


components.registerAdapter(lambda exit: exit.conceptualize(), Exit, iimaginary.IConcept)

class Containment(object):
    """Functionality for containment to be used as a mixin in Powerups.
    """
    implements(iimaginary.IContainer, iimaginary.IDescriptionContributor, iimaginary.ILinkContributor)
    powerupInterfaces = (iimaginary.IContainer, iimaginary.ILinkContributor,
     iimaginary.IDescriptionContributor)
    capacity = None
    closed = False

    def contains(self, other):
        for child in self.getContents():
            if other is child:
                return True
            cchild = iimaginary.IContainer(child, None)
            if cchild is not None and cchild.contains(other):
                return True

        return False

    def getContents(self):
        if self.thing is None:
            return []
        else:
            return self.store.query(Thing, Thing.location == self.thing)

    def add(self, obj):
        if self.closed:
            raise eimaginary.Closed(self, obj)
        containedWeight = self.getContents().getColumn('weight').sum()
        if containedWeight + obj.weight > self.capacity:
            raise eimaginary.DoesntFit(self, obj)
        assert self.thing is not None
        obj.location = self.thing
        return

    def remove(self, obj):
        if self.closed:
            raise eimaginary.Closed(self, obj)
        if obj.location is self.thing:
            obj.location = None
        return

    def getExits(self):
        return self.store.query(Exit, Exit.fromLocation == self.thing)

    def getExitNames(self):
        return self.getExits().getColumn('name')

    _marker = object()

    def getExitNamed(self, name, default=_marker):
        result = self.store.findUnique(Exit, attributes.AND(Exit.fromLocation == self.thing, Exit.name == name), default=default)
        if result is self._marker:
            raise KeyError(name)
        return result

    def links(self):
        d = {}
        if not self.closed:
            for ob in self.getContents():
                merge(d, ob.links())

        for exit in self.getExits():
            merge(d, {exit.name: [exit.toLocation]})

        return d

    def conceptualize(self):
        return ExpressSurroundings(self.getContents())


class ExpressSurroundings(language.ItemizedList):

    def concepts(self, observer):
        return [ iimaginary.IConcept(o) for o in super(ExpressSurroundings, self).concepts(observer) if o is not observer
               ]


class Container(item.Item, Containment, _Enhancement):
    """A generic powerup that implements containment."""
    capacity = attributes.integer(doc='\n    Units of weight which can be contained.\n    ', allowNone=False, default=1)
    closed = attributes.boolean(doc='\n    Indicates whether the container is currently closed or open.\n    ', allowNone=False, default=False)
    thing = attributes.reference(doc='\n    The object this container powers up.\n    ')


class ExpressCondition(language.BaseExpress):
    implements(iimaginary.IConcept)

    def vt102(self, observer):
        return [
         [
          T.bold, T.fg.yellow, language.Noun(self.original.thing).shortName().plaintext(observer)],
         ' is ',
         [
          T.bold, T.fg.red, self.original._condition(), '.']]


class Actable(object):
    implements(iimaginary.IActor, iimaginary.IEventObserver)
    powerupInterfaces = (iimaginary.IActor, iimaginary.IEventObserver, iimaginary.IDescriptionContributor)
    experience = 0
    level = 0
    CONDITIONS = ('dead', 'dying', 'incapacitated', 'mortally wounded', 'injured',
                  'bleeding', 'shaken up', 'fine', 'chipper', 'great')

    def conceptualize(self):
        return ExpressCondition(self)

    def _condition(self):
        if self.hitpoints.current == 0:
            return self.CONDITIONS[0]
        ratio = self.hitpoints.current / self.hitpoints.max
        idx = int(ratio * (len(self.CONDITIONS) - 2))
        return self.CONDITIONS[(idx + 1)]

    def send(self, *event):
        if len(event) != 1 or isinstance(event[0], (str, tuple)):
            event = events.Success(actor=self.thing, actorMessage=event)
        else:
            event = event[0]
        self.prepare(event)()

    def prepare(self, concept):
        """
        Implement L{iimaginary.IEventObserver.prepare} to prepare C{concept}
        with this L{Actable}'s C{intelligence}, if it has one; otherwise,
        return a callable that does nothing.
        """
        intelligence = self.getIntelligence()
        if intelligence is not None:
            return intelligence.prepare(concept)
        else:
            return lambda : None

    def gainExperience(self, amount):
        experience = self.experience + amount
        level = int(math.log(experience) / math.log(2))
        evt = None
        if level > self.level:
            evt = events.Success(actor=self.thing, actorMessage=(
             'You gain ', level - self.level, ' levels!\n'))
        elif level < self.level:
            evt = events.Success(actor=self.thing, actorMessage=(
             'You lose ', self.level - level, ' levels!\n'))
        self.level = level
        self.experience = experience
        if evt is not None:
            self.send(evt)
        return


class Actor(item.Item, Actable, _Enhancement):
    hitpoints = attributes.reference(doc='\n    ')
    stamina = attributes.reference(doc='\n    ')
    strength = attributes.reference(doc='\n    ')
    _ephemeralIntelligence = attributes.inmemory(doc='\n    Maybe the L{IEventObserver} associated with this actor, generally a\n    L{wiring.player.Player} instance.\n    ')
    _enduringIntelligence = attributes.reference(doc='\n    Maybe the persistent L{IEventObserver} associated with this actor.\n    Generally used with NPCs.\n    ')
    thing = attributes.reference(doc='\n    The L{IThing} that this is installed on.\n    ')
    level = attributes.integer(doc="\n    Don't you hate level-based games?  They're so stupid.\n    ", default=0, allowNone=False)
    experience = attributes.integer(doc='\n    XP!  Come on, you know what this is.\n    ', default=0, allowNone=False)

    def __init__(self, **kw):
        super(Actor, self).__init__(**kw)
        if self.hitpoints is None:
            self.hitpoints = Points(store=self.store, max=100)
        if self.stamina is None:
            self.stamina = Points(store=self.store, max=100)
        if self.strength is None:
            self.strength = Points(store=self.store, max=100)
        return

    def activate(self):
        self._ephemeralIntelligence = None
        return

    def setEphemeralIntelligence(self, intelligence):
        """
        Set the ephemeral intelligence, generally one representing a PC's user
        interface.
        """
        if self._enduringIntelligence:
            raise ValueError('Tried setting an ephemeral intelligence %r when an enduring intelligence %r already existed' % (
             intelligence, self._enduringIntelligence))
        self._ephemeralIntelligence = intelligence

    def setEnduringIntelligence(self, intelligence):
        """
        Set the enduring intelligence, generally one representing an NPC's AI.
        """
        if self._ephemeralIntelligence:
            raise ValueError('Tried setting an enduring intelligence %r when an ephemeral intelligence %r already existed' % (
             intelligence, self._ephemeralIntelligence))
        self._enduringIntelligence = intelligence

    def getIntelligence(self):
        """
        Get the current intelligence, be it ephemeral or enduring.
        """
        if self._ephemeralIntelligence is not None:
            return self._ephemeralIntelligence
        else:
            return self._enduringIntelligence


class LocationLighting(item.Item, _Enhancement):
    implements(iimaginary.ILocationProxy)
    powerupInterfaces = (iimaginary.ILocationProxy,)
    candelas = attributes.integer(doc='\n    The luminous intensity in candelas.\n\n    See U{http://en.wikipedia.org/wiki/Candela}.\n    ', default=100, allowNone=False)
    thing = attributes.reference()

    def getCandelas(self):
        """
        Sum the candelas of all light sources within a limited distance from
        the location this is installed on and return the result.
        """
        sum = 0
        for candle in self.thing.findProviders(iimaginary.ILightSource, 1):
            sum += candle.candelas

        return sum

    def proxy(self, facet, interface):
        if interface is iimaginary.IVisible:
            if self.getCandelas():
                return facet
            else:
                if facet.thing is self.thing:
                    return _DarkLocationProxy(self.thing)
                return
        return facet


class _DarkLocationProxy(structlike.record('thing')):
    implements(iimaginary.IVisible)

    def visualize(self):
        return language.DescriptionConcept('Blackness', 'You cannot see anything because it is very dark.')


class LightSource(item.Item, _Enhancement):
    implements(iimaginary.ILightSource)
    powerupInterfaces = (iimaginary.ILightSource,)
    candelas = attributes.integer(doc='\n    The luminous intensity in candelas.\n\n    See U{http://en.wikipedia.org/wiki/Candela}.\n    ', default=1, allowNone=False)
    thing = attributes.reference()