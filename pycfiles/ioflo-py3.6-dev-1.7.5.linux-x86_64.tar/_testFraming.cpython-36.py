# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/test/_testFraming.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 2613 bytes


def TestFrame():
    """Module Common self test

    """
    import acting, poking, needing, goaling, doing, traiting, fiating, wanting
    try:
        Frame.Clear()
        f1 = Frame(name='Primero')
        f2 = Frame()
        f3 = Frame()
        f1.attach(f2)
        f1.attach(f3)
        f4 = Frame()
        f5 = Frame()
        f2.attach(f4)
        f3.attach(f5)
        Act = acting.Act
        Transact = acting.Transact
        need = acting.need
        goal = acting.goal
        deed = acting.deed
        trait = acting.trait
        spec = acting.spec
        fiat = acting.fiat
        a = Act(action=need, act=(need.checkDepth), parms=dict(depth=5.0))
        f2.beacts.append(a)
        a = Act(action=goal, act=(goal.setDepth), parms=dict(depth=2.0))
        f2.enacts.append(a)
        a = Act(action=trait, act=(trait.useDepth), parms=dict(depth=3.0))
        f2.reacts.append(a)
        a = Act(action=deed, act=(deed.doDepth), parms=dict(depth=1.0))
        f2.reacts.append(a)
        a = Act(action=trait, act=(trait.useDepth), parms=dict(depth=6.0))
        f2.exacts.append(a)
        t = Transact()
        a = Act(action=need, act=(need.checkDepth), parms=dict(depth=4.0))
        t.needs.append(a)
        t.far = f5
        f2.preacts.append(t)
        a = Act(action=deed, act=(deed.doDepth), parms=dict(depth=1.0))
        f2.preacts.append(a)
        t = Transact()
        a = Act(action=need, act=(need.checkDepth), parms=dict(depth=1.5))
        t.needs.append(a)
        t.far = f4
        f5.preacts.append(t)
        f6 = Frame()
        a = Act(action=trait, act=(trait.useDepth), parms=dict(depth=10.0))
        f6.reacts.append(a)
        fr1 = Framer()
        fr1.first = f6
        f3.auxes.append(fr1)
        fr2 = Framer()
        fr2.first = f1
        fr2.runner.send(START)
        for i in xrange(3):
            status = fr2.runner.send(RUN)

    except excepting.ParameterError as ex:
        console.terse(ex)
        raise

    return f1


def Test():
    """Module Common self test

    """
    TestFrame()


if __name__ == '__main__':
    Test()