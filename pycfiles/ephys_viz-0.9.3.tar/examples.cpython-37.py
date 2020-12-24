# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ephys-viz/generated/ephys_viz/ephys_viz/widgets/TimeseriesView/examples.py
# Compiled at: 2019-11-15 11:26:28
# Size of source mod 2**32: 823 bytes
import spikeextractors as se, ephys_viz as ev

class examples:

    @classmethod
    def toy_example(cls):
        recording, sorting = se.example_datasets.toy_example()
        return ev.TimeseriesView(title='Ephys recording from SpikeExtractors toy example',
          recording=recording)