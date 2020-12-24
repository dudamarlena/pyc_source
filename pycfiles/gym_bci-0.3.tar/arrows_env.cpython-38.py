# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yeison/Development/gcpds/gym-bci/notebooks/gym_bci/envs/arrows_env.py
# Compiled at: 2019-11-23 16:29:28
# Size of source mod 2**32: 5417 bytes
from gym import Env
import logging, random, matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot
from matplotlib.widgets import Button

class ArrowsEnv(Env):
    __doc__ = ''
    metadata = {'render.modes': ['human']}

    def __str__(self):
        """"""
        return 'Arrows Environment'

    def __init__(self):
        """"""
        self.environ_config = {'maintain':4000, 
         'min_delay':200, 
         'max_delay':800, 
         'button_start':False}
        logging.info(f"Environment selected: {self}")
        matplotlib.use('TkAgg', warn=False, force=True)
        matplotlib.rcParams['toolbar'] = 'None'
        matplotlib.rcParams['axes.linewidth'] = 0
        fig = pyplot.figure('Motor Imagery')
        pyplot.style.use('dark_background')
        fig.set_facecolor('k')
        self._no_ticks()
        pyplot.axis('equal')
        pyplot.ion()

    def _no_ticks(self):
        """"""
        pyplot.xticks([])
        pyplot.yticks([])
        pyplot.xlim(-0.4, 0.8)
        pyplot.ylim(-0.5, 0.5)

    def _build_button_start(self):
        """"""
        pyplot.style.use('ggplot')
        pyplot.cla()
        self._no_ticks()
        w, h = (0.25, 0.1)
        self.btn_start_ax = pyplot.axes([0.5 - w / 2, 0.5 - h / 2, w, h], label='start')
        self.btn_start = Button((self.btn_start_ax), 'Start', color='C5', hovercolor='C5')
        self._continue = False
        self.btn_start.on_clicked(self._set_continue)
        pyplot.pause(1e-17)
        pyplot.draw()
        while True:
            pyplot.pause(0.01)
            if self._continue:
                self.btn_start_ax.set_visible(False)
                pyplot.pause(1e-17)
                pyplot.cla()
                pyplot.subplot(111)
                break

    def _set_continue(self, *args, **kwargs):
        self._continue = True

    def _maintain(self):
        """"""
        self._no_ticks()
        pyplot.draw()
        pyplot.pause(self.environ_config['maintain'] / 1000)

    def _rest(self):
        """"""
        pyplot.cla()
        self._no_ticks()
        pyplot.pause(random.randint(self.environ_config['min_delay'], self.environ_config['max_delay']) / 1000)

    def _action_right(self):
        """"""
        c = random.randint(0, 9)
        pyplot.arrow(0, 0, 0.2, 0, fc=f"C{c}", ec=f"C{c}", head_width=0.3, head_length=0.2, linewidth=30)

    def _action_left(self):
        """"""
        c = random.randint(0, 9)
        pyplot.arrow(0.4, 0, (-0.2), 0, fc=f"C{c}", ec=f"C{c}", head_width=0.3, head_length=0.2, linewidth=30)

    def _action_up(self):
        """"""
        c = random.randint(0, 9)
        pyplot.arrow(0.2, (-0.2), 0, 0.2, fc=f"C{c}", ec=f"C{c}", head_width=0.3, head_length=0.2, linewidth=30)

    def _action_down(self):
        """"""
        c = random.randint(0, 9)
        pyplot.arrow(0.2, 0.2, 0, (-0.2), fc=f"C{c}", ec=f"C{c}", head_width=0.3, head_length=0.2, linewidth=30)

    def _action_east(self):
        """"""
        self._action_right()

    def _action_west(self):
        """"""
        self._action_right()

    def _action_north(self):
        """"""
        self._action_up()

    def _action_south(self):
        """"""
        self._action_down()

    def step(self, action):
        """"""
        self.render(action)

    def reset(self, **kwargs):
        """"""
        self.environ_config.update(kwargs)
        if self.environ_config['button_start']:
            self._build_button_start()

    def render(self, action, mode='human', close=False):
        """"""
        getattr(self, f"_action_{action.lower()}")()
        self._maintain()
        self._rest()

    def close(self):
        """"""
        pyplot.close()