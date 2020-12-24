# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/satellite_initial_positions.py
# Compiled at: 2018-10-25 16:02:42
# Size of source mod 2**32: 369 bytes


def satellite_initial_positions(inputs):
    """
    Calculates the initial x,y,z of each satellite.
    If satellite motion is included, then it gives the locations of the
    satellites at each time during the simulation.

    Going to wait until I have some satellites to deal with to write this.
    """
    time_given = 'time' in inputs.geometry