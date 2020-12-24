# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dbryan/.virtualenvs/ssg/lib/python3.4/site-packages/salt_state_graph/test_graph.py
# Compiled at: 2015-08-03 01:04:07
# Size of source mod 2**32: 775 bytes
import os, salt_state_graph
test_folder = os.path.join(os.path.dirname(__file__), 'testdata')

def test_graph():
    """
    Use our example data to see that the dot output produced matches what we
    expect.
    """
    examples = set([os.path.join(test_folder, f.split('.')[0]) for f in os.listdir(test_folder)])
    for e in examples:
        with open(e + '.dot') as (f):
            expect = ''.join(sorted([l.strip() for l in f.readlines()]))
        with open(e + '.json') as (f):
            g = salt_state_graph.Graph(f)
            got = ''.join(sorted(g.render('dot').splitlines()))
            assert got.strip() == expect.strip()