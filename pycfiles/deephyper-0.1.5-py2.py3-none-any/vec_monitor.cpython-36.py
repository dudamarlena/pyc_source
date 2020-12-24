# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/vec_monitor.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1768 bytes
from . import VecEnvWrapper
from deephyper.search.nas.baselines.bench.monitor import ResultsWriter
import numpy as np, time
from collections import deque

class VecMonitor(VecEnvWrapper):

    def __init__(self, venv, filename=None, keep_buf=0):
        VecEnvWrapper.__init__(self, venv)
        self.eprets = None
        self.eplens = None
        self.epcount = 0
        self.tstart = time.time()
        if filename:
            self.results_writer = ResultsWriter(filename, header={'t_start': self.tstart})
        else:
            self.results_writer = None
        self.keep_buf = keep_buf
        if self.keep_buf:
            self.epret_buf = deque([], maxlen=keep_buf)
            self.eplen_buf = deque([], maxlen=keep_buf)

    def reset(self):
        obs = self.venv.reset()
        self.eprets = np.zeros(self.num_envs, 'f')
        self.eplens = np.zeros(self.num_envs, 'i')
        return obs

    def step_wait(self):
        obs, rews, dones, infos = self.venv.step_wait()
        self.eprets += rews
        self.eplens += 1
        newinfos = []
        for i, (done, ret, eplen, info) in enumerate(zip(dones, self.eprets, self.eplens, infos)):
            info = info.copy()
            if done:
                epinfo = {'r':ret, 
                 'l':eplen,  't':round(time.time() - self.tstart, 6)}
                info['episode'] = epinfo
                if self.keep_buf:
                    self.epret_buf.append(ret)
                    self.eplen_buf.append(eplen)
                self.epcount += 1
                self.eprets[i] = 0
                self.eplens[i] = 0
                if self.results_writer:
                    self.results_writer.write_row(epinfo)
            newinfos.append(info)

        return (obs, rews, dones, newinfos)