# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/spikeforest2/spikeforest_widgets/generated/spikeforest_widgets/spikeforest_widgets/widgets/TimeseriesView/examples.py
# Compiled at: 2019-12-03 09:46:26
# Size of source mod 2**32: 823 bytes
import spikeextractors as se, ephys_viz as ev

class examples:

    @classmethod
    def toy_example(cls):
        recording, sorting = se.example_datasets.toy_example()
        return ev.TimeseriesView(title='Ephys recording from SpikeExtractors toy example',
          recording=recording)