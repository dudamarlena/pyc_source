# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/trim/interior/plain/test/testDetecting.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 2146 bytes


def TestBox():
    """           """
    storing.Store.Clear()
    doing.Doer.Clear()
    store = storing.Store(name='Test')
    print('\nTesting Box Position Detector')
    detector = DetectorPositionBox(name='detectorPositionBox', store=store, group='detector.position.box',
      input='state.position',
      parms=dict(track=0.0, north=(-50.0), east=0.0, length=10000,
      width=2000))
    store.expose()
    detector._expose()
    print('')
    input = store.fetch('state.position').update(north=9950.0, east=0.0)
    detector.action()
    detector._expose()
    print('')
    input = store.fetch('state.position').update(north=9949.0, east=0.0)
    detector.action()
    detector._expose()
    print('')
    input = store.fetch('state.position').update(north=9951, east=0.0)
    detector.action()
    detector._expose()
    print('')
    input = store.fetch('state.position').update(north=9900.0, east=500.0)
    detector.action()
    detector._expose()
    input = store.fetch('state.position').update(north=1000.0, east=2000.0)
    detector.action()
    detector._expose()
    input = store.fetch('state.position').update(north=1000.0, east=(-2000.0))
    detector.action()
    detector._expose()
    input = store.fetch('state.position').update(north=11000.0, east=500.0)
    detector.action()
    detector._expose()
    input = store.fetch('state.position').update(north=11000.0, east=2000.0)
    detector.action()
    detector._expose()
    input = store.fetch('state.position').update(north=11000.0, east=(-2000.0))
    detector.action()
    detector._expose()
    input = store.fetch('state.position').update(north=(-1000.0), east=2000.0)
    detector.action()
    detector._expose()
    input = store.fetch('state.position').update(north=(-1000.0), east=(-2000.0))
    detector.action()
    detector._expose()


def Test():
    """Module Common self test

    """
    pass


if __name__ == '__main__':
    Test()