# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_traits.py
# Compiled at: 2013-12-08 17:19:04
from pytest import raises
from mio.errors import AttributeError, TypeError

def test_basic_trait(mio, capfd):
    mio.eval('\n        TGreeting = Trait clone() do (\n            hello = method(\n                print("Hello", self getGreeting())\n            )\n        )\n\n        World = Object clone() do (\n            use(TGreeting)\n\n            greeting = "World!"\n\n            getGreeting = method(\n               self greeting\n            )\n\n            setGreeting = method(aGreeting,\n                self greeting = aGreeting\n            )\n        )\n    ')
    mio.eval('World hello()')
    out, err = capfd.readouterr()
    assert out == 'Hello World!\n'
    mio.eval('World setGreeting("John")')
    mio.eval('World hello()')
    out, err = capfd.readouterr()
    assert out == 'Hello John\n'


def test_basic_trait2(mio, capfd):
    mio.eval('\n        TGreeting = Trait clone() do (\n            hello = method(\n                print("Hello", self getGreeting())\n            )\n        )\n\n        World = Object clone() do (\n            use(TGreeting)\n\n            greeting = "World!"\n\n            getGreeting = method(\n               self greeting\n            )\n\n            setGreeting = method(aGreeting,\n                self greeting = aGreeting\n            )\n        )\n    ')
    mio.eval('World hello()')
    out, err = capfd.readouterr()
    assert out == 'Hello World!\n'
    mio.eval('World setGreeting("John")')
    mio.eval('World hello()')
    out, err = capfd.readouterr()
    assert out == 'Hello John\n'
    with raises(TypeError):
        mio.eval('World use(TGreeting)', reraise=True)


def test_invalid(mio):
    mio.eval('TGreetable = Object clone()')
    with raises(TypeError):
        mio.eval('Object clone() use(TGreetable)', reraise=True)


def test_state(mio):
    mio.eval('TGreetable = Trait clone()')
    with raises(TypeError):
        mio.eval('TGreetable greeting = "World!"', reraise=True)


def test_requirements(mio):
    mio.eval('\n        TGreetable = Trait clone() do(\n            requires("greeting")\n        )\n    ')
    mio.eval('TGreetable requirements()') == ['greeting']


def test_requires(mio):
    mio.eval('\n        TGreetable = Trait clone() do(\n            requires("greeting")\n        )\n    ')
    with raises(TypeError):
        mio.eval('Object clone() use(TGreetable)', reraise=True)


def test_resolution(mio):
    mio.eval('\n        TFoo = Trait clone() do(\n            foo = method("foo")\n        )\n        TBar = Trait clone() do(\n            foo = method("foo")\n        )\n    ')
    with raises(TypeError):
        mio.eval('Object clone() use(TFoo) use(TBar)', reraise=True)


def test_resolution2(mio):
    mio.eval('\n        TFoo = Trait clone() do(\n            foo = method("foo")\n        )\n        TBar = Trait clone() do(\n            foo = method("foo")\n        )\n    ')
    mio.eval('Foo = Object clone() use(TFoo) use(TBar, {"foo": "bar"})')
    assert mio.eval('Foo hasTrait(TFoo)')
    assert mio.eval('Foo hasTrait(TBar)')
    assert mio.eval('Foo behaviors') == ['foo', 'bar']


def test_resolution_deltrait(mio):
    mio.eval('\n        TFoo = Trait clone() do(\n            foo = method("foo")\n        )\n        TBar = Trait clone() do(\n            foo = method("foo")\n        )\n    ')
    mio.eval('Foo = Object clone() use(TFoo) use(TBar, {"foo": "bar"})')
    assert mio.eval('Foo hasTrait(TFoo)')
    assert mio.eval('Foo hasTrait(TBar)')
    assert mio.eval('Foo behaviors') == ['foo', 'bar']
    mio.eval('Foo delTrait(TFoo)')
    assert not mio.eval('Foo hasTrait(TFoo)')
    assert mio.eval('Foo behaviors') == ['bar']
    mio.eval('Foo delTrait(TBar)')
    assert not mio.eval('Foo hasTrait(TBar)')
    assert mio.eval('Foo behaviors') == []


def test_adapt(mio):
    mio.eval('TGreetable = Trait clone()')
    assert mio.eval('World = Object clone() adapt(TGreetable) hasTrait(TGreetable)')


def test_hasTrait(mio):
    mio.eval('\n        TGreetable = Trait clone()\n        World = Object clone() do (\n            use(TGreetable)\n        )\n    ')
    assert mio.eval('World hasTrait(TGreetable)')


def test_hasTrait2(mio):
    mio.eval('\n        TGreetable = Trait clone()\n        World = Object clone() do (\n            use(TGreetable)\n        )\n    ')
    assert mio.eval('World hasTrait(TGreetable)')
    assert mio.eval('World clone() hasTrait(TGreetable)')


def test_delTrait(mio):
    mio.eval('\n        TGreetable = Trait clone()\n        World = Object clone() do (\n            use(TGreetable)\n        )\n    ')
    assert mio.eval('World hasTrait(TGreetable)')
    mio.eval('World delTrait(TGreetable)')
    assert mio.eval('World behaviors') == []
    assert not mio.eval('World hasTrait(TGreetable)')


def test_delTrait2(mio, capfd):
    mio.eval('\n        TGreetable = Trait clone() do (\n            hello = method(\n                print("Hello World!")\n            )\n        )\n\n        World = Object clone() do (\n            use(TGreetable)\n        )\n    ')
    assert mio.eval('World hasTrait(TGreetable)')
    assert mio.eval('World behaviors') == ['hello']
    assert mio.eval('World hello()').value is None
    out, err = capfd.readouterr()
    assert out == 'Hello World!\n'
    mio.eval('World delTrait(TGreetable)')
    assert mio.eval('World behaviors') == []
    assert not mio.eval('World hasTrait(TGreetable)')
    with raises(AttributeError):
        mio.eval('World hello()', reraise=True)
    return


def test_delTrait3(mio, capfd):
    mio.eval('\n        TGreetable = Trait clone() do (\n            hello = method(\n                print("Hello World!")\n            )\n        )\n\n        World = Object clone() do (\n            use(TGreetable)\n        )\n    ')
    assert mio.eval('World hasTrait(TGreetable)')
    assert mio.eval('World behaviors') == ['hello']
    assert mio.eval('World hello()').value is None
    out, err = capfd.readouterr()
    assert out == 'Hello World!\n'
    mio.eval('World delTrait(TGreetable)')
    assert mio.eval('World behaviors') == []
    assert not mio.eval('World hasTrait(TGreetable)')
    with raises(TypeError):
        mio.eval('World delTrait(TGreetable)', reraise=True)
    return


def test_traits(mio):
    mio.eval('\n        TGreetable = Trait clone()\n        World = Object clone() do (\n            use(TGreetable)\n        )\n    ')
    TGreetable = mio.eval('TGreetable')
    assert mio.eval('World traits') == [TGreetable]


def test_behaviors(mio, capfd):
    mio.eval('\n        TGreetable = Trait clone() do (\n            hello = method(\n                print("Hello World!")\n            )\n        )\n\n        World = Object clone() do (\n            use(TGreetable)\n        )\n    ')
    assert mio.eval('World hello()').value is None
    out, err = capfd.readouterr()
    assert out == 'Hello World!\n'
    assert mio.eval('World behaviors') == ['hello']
    return


def test_del_behavior(mio, capfd):
    mio.eval('\n        TGreetable = Trait clone() do (\n            hello = method(\n                print("Hello World!")\n            )\n        )\n\n        World = Object clone() do (\n            use(TGreetable)\n        )\n    ')
    assert mio.eval('World hello()').value is None
    out, err = capfd.readouterr()
    assert out == 'Hello World!\n'
    assert mio.eval('World behaviors') == ['hello']
    mio.eval('World del("hello")')
    with raises(AttributeError):
        mio.eval('World hello()', reraise=True)
    assert mio.eval('World behaviors') == []
    return