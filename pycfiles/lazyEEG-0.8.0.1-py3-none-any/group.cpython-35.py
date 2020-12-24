# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Coding\py\IPython Notebooks\experiment\chunking\LazyEEG\group.py
# Compiled at: 2017-04-14 17:56:12
# Size of source mod 2**32: 6464 bytes
from .default import *
from . import parameter

def parsing(container):
    if type(container) == str:
        container = [
         container]

    def plus_minus(text):
        text = '+' + text.replace(' ', '')
        mix = re.findall('[\\+\\-][^\\+\\-]+', text)
        plus, minus = [], []
        for c in mix:
            if c[0] == '+':
                plus.append(c[1:])
            elif c[0] == '-':
                minus.append(c[1:])

        if plus == []:
            plus = slice(None)
        return {'+': plus, '-': minus}

    def divide_batch(batch):
        batch_frame = []
        for scene in batch.split(','):
            if ':' in scene:
                name, scene = scene.split(':')
                name = name.strip()
            else:
                name = scene
            batch_frame.append((name.strip(),
             [plus_minus(group) for group in scene.split('&')]))

        return batch_frame

    try:
        container_frame = []
        for board in container:
            if type(board) is str:
                board += '@' * (2 - board.count('@'))
                cond_batch, chan_batch, timespan = board.split('@')
            elif type(board) is dict:
                cond_batch = board.get('Cond', default='')
                chan_batch = board.get('Chan', default='')
                timespan = board.get('Time', default='')
            cond_batch_frame = divide_batch(cond_batch)
            chan_batch_frame = divide_batch(chan_batch)
            if timespan.strip() == '':
                timespan_frame = slice(None)
            else:
                ts = [i for i in re.compile('[,~\\:]').split(timespan)]
                if len(ts) == 1:
                    ts.append(ts[0])
                timespan_frame = pd.timedelta_range(start=ts[0], end=ts[1], freq='1ms')
            container_frame.append((cond_batch_frame, chan_batch_frame, timespan_frame))

    except:
        raise ValueError('unsupported text format')

    return container_frame


def extract(data, container_script, name):
    container_frame = parsing(container_script)
    container_data = []
    for board_frame in container_frame:
        cond_batch, chan_batch, timespan = board_frame
        title = name
        if len(chan_batch) > 1 or chan_batch[0][0] != '':
            title += ', ' + ','.join([scene_name for scene_name, scene in chan_batch])
        if type(timespan) is not slice:
            title += ', %d-%dms' % (timespan.microseconds[0] // 1000, timespan.microseconds[(-1)] // 1000)
        cond_scene_names = []
        batch_data = []
        for (cond_scene_name, cond_scene), (chan_scene_name, chan_scene) in itertools.product(cond_batch, chan_batch):
            cond_scene_names.append(cond_scene_name)
            signs = []
            scene_data = []
            for cond_group_idx, cond_group in enumerate(cond_scene):
                for chan_group_idx, chan_group in enumerate(chan_scene):
                    for cond_sign, chan_sign in itertools.product(['+', '-'], ['+', '-']):
                        scene_data.append(data.loc[(ids[:, cond_group[cond_sign], :, chan_group[chan_sign]], ids[:, timespan])])
                        signs += [(cond_group_idx, cond_sign, chan_group_idx, chan_sign)] * len(scene_data[(-1)])

            scene_data = pd.concat(scene_data)
            raw_channel_index = scene_data.index.get_level_values('channel')
            if len(chan_batch) == 1 and chan_batch[0][0] == '':
                multindex = [(subject, cond_scene_name, trial, channel, cond_group_idx, cond_sign, chan_group_idx, chan_sign) for (subject, condition, trial, channel), (cond_group_idx, cond_sign, chan_group_idx, chan_sign) in zip(scene_data.index, signs)]
            else:
                multindex = [(subject, cond_scene_name, trial, chan_scene_name, cond_group_idx, cond_sign, chan_group_idx, chan_sign) for (subject, condition, trial, channel), (cond_group_idx, cond_sign, chan_group_idx, chan_sign) in zip(scene_data.index, signs)]
            scene_data.index = pd.MultiIndex.from_tuples(multindex, names=[
             *scene_data.index.names, 'cond_group', 'cond_sign', 'chan_group', 'chan_sign'])
            if len(cond_scene) == 1 and len(chan_scene) == 1:
                scene_data.index = scene_data.index.droplevel(['cond_group', 'chan_group'])
            batch_data.append(scene_data)

        batch_data = pd.concat(batch_data)
        batch_data.sort_index(inplace=True)
        batch_data = batch_data.reindex(cond_scene_names, level='condition')
        batch_data.name = title
        yield [
         title, batch_data]