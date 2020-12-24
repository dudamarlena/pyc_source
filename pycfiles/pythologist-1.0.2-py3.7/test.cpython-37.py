# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pythologist/test.py
# Compiled at: 2019-01-19 14:12:07
# Size of source mod 2**32: 6240 bytes
import json
from collections import namedtuple
import pandas as pd
Result = namedtuple('Result', ['result', 'count', 'total', 'about'])

class InFormCellFrameTest:

    def __init__(self, icf):
        self._icf = icf.copy()

    def check_overlapping_samples(self):
        samples = self._icf.groupby(['sample']).apply(lambda x: x['folder'].unique().shape[0])
        result = 'PASS'
        about = []
        count = 0
        total = 0
        for sample in samples.index:
            total += 1
            if samples[sample] > 1:
                result = 'FAIL'
                count += 1
                about.append(sample + ' present in ' + str(samples[sample]) + ' folders')

        if result == 'PASS':
            [
             'samples are unique to each folder and are not repeated in different folders.']
        return Result(result=result, count=count, total=total, about=('; '.join(about)))

    def check_overlapping_frames(self):
        frames = self._icf.groupby(['sample', 'frame']).apply(lambda x: x['folder'].unique().shape[0])
        result = 'PASS'
        about = []
        count = 0
        total = 0
        for frame in frames.index:
            total += 1
            if frames[frame] > 1:
                result = 'FAIL'
                count += 1
                about.append(str(frame) + ' present in ' + str(frames[frame]) + ' folders')

        if result == 'PASS':
            about = [
             'sample/frames are unique to each folder and are not repeated in different folders.']
        return Result(result=result, count=count, total=total, about=('; '.join(about)))

    def check_scored_stain_consistency(self):
        scored = set(self._icf.scored_stains)
        frames = self._icf.groupby(['folder', 'sample', 'frame']).apply(lambda x: x['frame_stains'].unique())
        total = 0
        count = 0
        result = 'PASS'
        about = []
        for frame in frames.index:
            for entry in [json.loads(x) for x in frames[frame]]:
                for tissue in entry.keys():
                    stains = list(entry[tissue].keys())
                    total += 1
                    if len(scored - set(stains)) > 0:
                        result = 'FAIL'
                        count += 1
                        about.append('frame ' + str(frame) + ' is missing stain(s) ' + str(scored - set(stains)))

        if result == 'PASS':
            about = [
             'The same stains are present on all frames.']
        return Result(result=result, count=count, total=total, about=('; '.join(about)))

    def check_phenotype_consistency(self):
        total = 0
        count = 0
        result = 'PASS'
        about = []
        frames = self._icf.groupby(['folder', 'sample', 'frame']).apply(lambda x: x['phenotypes_present'].unique())
        all_phenotypes = set(self._icf.phenotypes)
        for frame in frames.index:
            for entry in [json.loads(x) for x in frames[frame]]:
                total += 1
                if len(all_phenotypes - set(entry)) > 0:
                    count += 1
                    result = 'FAIL'
                    about.append(str(frame) + ' frame is missing phenotype ' + str(all_phenotypes - set(entry)))

        if result == 'PASS':
            about = [
             'The same phenotypes are present on all frames.']
        return Result(result=result, count=count, total=total, about=('; '.join(about)))

    def check_tissue_consistency(self):
        total = 0
        count = 0
        result = 'PASS'
        about = []
        frames = self._icf.groupby(['folder', 'sample', 'frame']).apply(lambda x: list(x['tissues_present'].unique()))
        all_tissues = set(self._icf.tissues)
        for frame in frames.index:
            for entry in [list(json.loads(x).keys()) for x in frames[frame]]:
                total += 1
                if len(all_tissues - set(entry)) > 0:
                    count += 1
                    result = 'FAIL'
                    about.append(str(frame) + ' frame is missing tissue ' + str(all_tissues - set(entry)))

        if result == 'PASS':
            about = [
             'The same tissues are present on all frames.']
        return Result(result=result, count=count, total=total, about=('; '.join(about)))

    def check_scored_stain_compartment(self):
        frames = self._icf.groupby(['folder', 'sample', 'frame']).apply(lambda x: x['frame_stains'].unique())
        rows = []
        for frame in frames.index:
            for entry in [json.loads(x) for x in frames[frame]]:
                for tissue in entry.keys():
                    stains = entry[tissue].keys()
                    for stain in stains:
                        compartment = entry[tissue][stain]['compartment']
                        rows.append(pd.Series(dict(zip([
                         'folder', 'sample', 'frame', 'tissue', 'stain', 'compartment'], list(frame) + [tissue, stain, compartment]))))

        df = pd.DataFrame(rows)
        stains = df.groupby(['stain', 'compartment']).apply(lambda x: [x['folder'], x['sample'], x['frame']]).reset_index().rename(columns={0: 'frames'})
        counts = stains.groupby(['stain']).apply(lambda x: x['compartment'].unique().shape[0])
        total = 0
        count = 0
        about = []
        result = 'PASS'
        for stain in counts.index:
            total += 1
            if counts[stain] > 1:
                count += 1
                about.append(stain + ' is scored from different components')
                result = 'FAIL'

        if result == 'PASS':
            about = [
             'Stains are scored from the same compartment across all frames.']
        return Result(result=result, count=count, total=total, about=('; '.join(about)))