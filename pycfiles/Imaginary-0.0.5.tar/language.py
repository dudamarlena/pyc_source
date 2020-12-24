# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/Divmod-release/Imaginary/imaginary/language.py
# Compiled at: 2008-05-04 18:35:09
"""

Textual formatting for game objects.

"""
import types
from zope.interface import implements
from twisted.python.components import registerAdapter
from epsilon import structlike
from imaginary import iimaginary, iterutils, text as T

class Gender(object):
    """
    enum!
    """
    MALE = 1
    FEMALE = 2
    NEUTER = 3


class Noun(object):
    """
    This is a language wrapper around a Thing.

    It is separated into its own class for two reasons:

     - You should try to keep your game-logic self-contained and avoid
       polluting it with lots of constant strings, so that porting to new
       interfaces (text prototype -> isometric final implementation) is easy.
       It's easier to read the code that way and make changes to the logic even
       if you don't want to move to a different interface.

     - It would be nice if text games could be internationalized by separating
       the formatting logic from the game logic.  In an extreme case, it would
       be SUPER-COOL if people could be playing the same game in french and
       english on the same server, simply by changing a setting on their
       client.
    """

    def __init__(self, thing):
        self.thing = thing

    def shortName(self):
        return ExpressString(self.thing.name)

    def nounPhrase(self):
        if self.thing.proper:
            return self.shortName()
        return ExpressList([self.indefiniteArticle(), self.shortName()])

    def definiteNounPhrase(self):
        if self.thing.proper:
            return self.shortName()
        return ExpressList([self.definiteArticle(), self.shortName()])

    def indefiniteArticle(self):
        if self.thing.name[0].lower() in 'aeiou':
            return 'an '
        return 'a '

    def definiteArticle(self):
        return 'the '

    def heShe(self):
        """
        Return the personal pronoun for the wrapped thing.
        """
        x = {Gender.MALE: 'he', Gender.FEMALE: 'she'}.get(self.thing.gender, 'it')
        return ExpressString(x)

    def himHer(self):
        """
        Return the objective pronoun for the wrapped thing.
        """
        x = {Gender.MALE: 'him', Gender.FEMALE: 'her'}.get(self.thing.gender, 'it')
        return ExpressString(x)

    def hisHer(self):
        """
        Return a possessive pronoun that cannot be used after 'is'.
        """
        x = {Gender.MALE: 'his', Gender.FEMALE: 'her'}.get(self.thing.gender, 'its')
        return ExpressString(x)


def flattenWithoutColors(vt102):
    return T.flatten(vt102, useColors=False)


class BaseExpress(object):
    implements(iimaginary.IConcept)

    def __init__(self, original):
        self.original = original

    def plaintext(self, observer):
        return flattenWithoutColors(self.vt102(observer))


class DescriptionConcept(structlike.record('name description exits others', description='', exits=(), others=())):
    """
    A concept which is expressed as the description of a Thing as well as
    any concepts which power up that thing for IDescriptionContributor.

    Concepts will be ordered by the C{preferredOrder} class attribute.
    Concepts not named in this list will appear last in an unpredictable
    order.
    """
    implements(iimaginary.IConcept)
    preferredOrder = [
     'ExpressCondition',
     'ExpressClothing',
     'ExpressSurroundings']

    def plaintext(self, observer):
        return flattenWithoutColors(self.vt102(observer))

    def vt102(self, observer):
        exits = ''
        if self.exits:
            exits = [
             T.bold, T.fg.green, '( ',
             [
              T.fg.normal, T.fg.yellow,
              iterutils.interlace(' ', (exit.name for exit in self.exits))],
             ' )', '\n']
        description = self.description or ''
        if description:
            description = (
             T.fg.green, self.description, '\n')
        descriptionConcepts = []
        for pup in self.others:
            descriptionConcepts.append(pup.conceptualize())

        def index(c):
            try:
                return self.preferredOrder.index(c.__class__.__name__)
            except ValueError:
                return len(self.preferredOrder)

        descriptionConcepts.sort(key=index)
        descriptionComponents = []
        for c in descriptionConcepts:
            s = c.vt102(observer)
            if s:
                descriptionComponents.extend([s, '\n'])

        if descriptionComponents:
            descriptionComponents.pop()
        return [
         [
          T.bold, T.fg.green, '[ ', [T.fg.normal, self.name], ' ]\n'],
         exits,
         description,
         descriptionComponents]


class ExpressNumber(BaseExpress):
    implements(iimaginary.IConcept)

    def vt102(self, observer):
        return str(self.original)


class ExpressString(BaseExpress):
    implements(iimaginary.IConcept)

    def __init__(self, original, capitalized=False):
        self.original = original
        self._cap = capitalized

    def vt102(self, observer):
        if self._cap:
            return self.original[:1].upper() + self.original[1:]
        return self.original

    def capitalizeConcept(self):
        return ExpressString(self.original, True)


class ExpressList(BaseExpress):
    implements(iimaginary.IConcept)

    def concepts(self, observer):
        return map(iimaginary.IConcept, self.original)

    def vt102(self, observer):
        return [ x.vt102(observer) for x in self.concepts(observer) ]

    def capitalizeConcept(self):
        return Sentence(self.original)


class Sentence(ExpressList):

    def vt102(self, observer):
        o = self.concepts(observer)
        if o:
            o[0] = o[0].capitalizeConcept()
        return [ x.vt102(observer) for x in o ]

    def capitalizeConcept(self):
        return self


registerAdapter(ExpressNumber, int, iimaginary.IConcept)
registerAdapter(ExpressNumber, long, iimaginary.IConcept)
registerAdapter(ExpressString, str, iimaginary.IConcept)
registerAdapter(ExpressString, unicode, iimaginary.IConcept)
registerAdapter(ExpressList, list, iimaginary.IConcept)
registerAdapter(ExpressList, tuple, iimaginary.IConcept)
registerAdapter(ExpressList, types.GeneratorType, iimaginary.IConcept)

class ItemizedList(BaseExpress):
    implements(iimaginary.IConcept)

    def __init__(self, listOfConcepts):
        self.listOfConcepts = listOfConcepts

    def concepts(self, observer):
        return self.listOfConcepts

    def vt102(self, observer):
        return ExpressList(itemizedStringList(self.concepts(observer))).vt102(observer)

    def capitalizeConcept(self):
        listOfConcepts = self.listOfConcepts[:]
        if listOfConcepts:
            listOfConcepts[0] = iimaginary.IConcept(listOfConcepts[0]).capitalizeConcept()
        return ItemizedList(listOfConcepts)


def itemizedStringList(desc):
    if len(desc) == 1:
        yield desc[0]
    elif len(desc) == 2:
        yield desc[0]
        yield ' and '
        yield desc[1]
    elif len(desc) > 2:
        for ele in desc[:-1]:
            yield ele
            yield ', '

        yield 'and '
        yield desc[(-1)]