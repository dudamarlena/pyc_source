# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/Divmod-release/Imaginary/imaginary/text.py
# Compiled at: 2006-09-13 05:36:49
import pprint
from epsilon import structlike

class _unset(object):

    def __nonzero__(self):
        return False


unset = _unset()

class AttributeSet(structlike.record('bold underline reverseVideo blink fg bg', bold=False, underline=False, reverseVideo=False, blink=False, fg='9', bg='9')):
    """
    @ivar bold: True, False, or unset, indicating whether characters
    with these attributes will be bold, or if boldness should be
    inherited from the previous setting.

    @ivar underline: Similar to C{bold} but indicating the underlined
    state of characters.

    @ivar reverseVideo: Similar to C{bold} but indicating whether
    reverse video should be applied.

    @ivar blink: Similar to C{bold} but indicating whether foreground
    material should blink.

    @ivar fg: An integer between 0 and 9 inclusive or unset.
    Integer values indicate a color setting for the foreground,
    whereas unset indicates foreground color should be inherited from
    the previous settings.

    @ivar bg: Like C{fg} but for background color.
    """

    def __init__(self, *a, **kw):
        super(AttributeSet, self).__init__(*a, **kw)
        assert self.fg is unset or self.fg in '012345679'
        assert self.bg is unset or self.bg in '012345679'
        assert self.bold is unset or self.bold in (True, False)
        assert self.underline is unset or self.underline in (True, False)
        assert self.reverseVideo is unset or self.reverseVideo in (True, False)
        assert self.blink is unset or self.blink in (True, False)

    def __repr__(self):
        return '%s(%s)' % (
         self.__class__.__name__,
         (', ').join([ ('=').join((k, str(v))) for (k, v) in zip(self.__names__, self) if v is not unset
            ]))

    def __len__(self):
        return 6

    def __getitem__(self, index):
        return [
         self.bold, self.underline, self.reverseVideo, self.blink, self.fg, self.bg][index]

    def __setitem__(self, index, value):
        setattr(self, ['bold', 'underline', 'reverseVideo', 'blink', 'fg', 'bg'][index], value)

    def clone(self):
        return self.__class__(*self)

    def update(self, other):
        for i in range(len(self)):
            if other[i] is not unset:
                self[i] = other[i]

        return self

    _flags = {'bold': '1', 'underline': '4', 'reverseVideo': '7', 'blink': '5'}

    def toVT102(self, state):
        passive = []
        active = []
        reset = False
        for attr in ('bold', 'underline', 'reverseVideo', 'blink'):
            was = getattr(state, attr)
            willBe = getattr(self, attr)
            if was is unset:
                if willBe is unset:
                    pass
                elif willBe:
                    active.append(self._flags[attr])
                else:
                    reset = True
            elif was:
                if willBe is unset:
                    passive.append(self._flags[attr])
                elif willBe:
                    passive.append(self._flags[attr])
                else:
                    reset = True
            elif willBe is unset:
                pass
            elif willBe:
                active.append(self._flags[attr])

        for (x, attr) in (('3', 'fg'), ('4', 'bg')):
            was = getattr(state, attr)
            willBe = getattr(self, attr)
            if was is unset:
                if willBe is unset:
                    pass
                elif willBe == '9':
                    pass
                else:
                    active.append(x + willBe)
            elif was == '9':
                if willBe is unset:
                    pass
                elif willBe == '9':
                    pass
                else:
                    active.append(x + willBe)
            elif willBe is unset:
                passive.append(x + was)
            elif willBe == '9':
                reset = True
            elif willBe == was:
                passive.append(x + was)
            else:
                active.append(x + willBe)

        if reset:
            active.extend(passive)
            active.insert(0, '0')
        if active:
            return '\x1b[' + (';').join(active) + 'm'
        return ''


class AttributeStack(object):

    def __init__(self, initialAttributes):
        self._stack = [
         initialAttributes]

    def __repr__(self):
        return pprint.pformat(self._stack)

    def __len__(self):
        return len(self._stack)

    def push(self, attrs):
        self._stack.append(self.get().clone().update(attrs))

    def duptop(self):
        self._stack.append(self.get().clone())

    def update(self, attrs):
        self.get().update(attrs)

    def pop(self):
        return self._stack.pop()

    def get(self):
        return self._stack[(-1)]


class fg:
    pass


class bg:
    pass


neutral = AttributeSet(unset, unset, unset, unset, unset, unset)
for (cls, attr) in [(fg, 'fg'),
 (
  bg, 'bg')]:
    for (n, color) in enumerate(['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']):
        value = neutral.clone()
        setattr(value, attr, str(n))
        setattr(cls, color, value)

    cls.normal = neutral.clone()
    setattr(cls.normal, attr, '9')

del n
del cls
del attr
del color
for attr in ('bold', 'blink', 'reverseVideo', 'underline'):
    value = neutral.clone()
    setattr(value, attr, True)
    locals()[attr] = value

def flatten(dag, currentAttrs=None, useColors=True):
    """
    Serialize a tree of strings and terminal codes to an iterable of strings,
    ready to be written to your favorite terminal device.

    @type currentAttrs: L{AttributeSet}
    @param currentAttrs: The current set of attributes.

    @param useColors: If False, terminal codes will be left out.
    """
    if currentAttrs is None:
        if not useColors:
            currentAttrs = AttributeSet()
        else:
            raise TypeError('currentAttrs is required when useColors is False')
    attrs = AttributeStack(currentAttrs)
    attrs.duptop()
    stack = [
     iter(dag)]
    dirty = False
    while stack:
        try:
            obj = stack[(-1)].next()
        except StopIteration:
            stack.pop()
            attrs.pop()
            if len(attrs):
                if useColors:
                    dirty = bool(attrs.get().toVT102(currentAttrs))
        else:
            if isinstance(obj, AttributeSet):
                attrs.update(obj)
                if useColors:
                    dirty = bool(attrs.get().toVT102(currentAttrs))
            elif isinstance(obj, (str, unicode)):
                if obj:
                    if dirty:
                        if useColors:
                            yield attrs.get().toVT102(currentAttrs)
                        currentAttrs = attrs.get().clone()
                        dirty = False
                    yield obj
            else:
                try:
                    newIter = iter(obj)
                except TypeError:
                    if dirty:
                        if useColors:
                            yield attrs.get().toVT102(currentAttrs)
                        currentAttrs = attrs.get().clone()
                        dirty = False
                    yield obj
                else:
                    stack.append(newIter)
                    attrs.duptop()

    if dirty and len(attrs):
        if useColors:
            yield attrs.get().toVT102(currentAttrs)
    return


__all__ = [
 'fg', 'bg',
 'flatten']