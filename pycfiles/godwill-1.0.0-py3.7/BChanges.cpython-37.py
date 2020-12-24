# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/gwill/changes/BChanges.py
# Compiled at: 2019-03-26 03:00:17
# Size of source mod 2**32: 4529 bytes
import random
from gwill.conf.GuaCi import *
import sys
from gwill.data.gua_ci.gwill_solution import solution_dict
seed_list = []
if len(sys.argv) > 1:
    for seed in sys.argv[1:]:
        seed_list.append(seed)

    print('the seed is: %s ', seed_list)

def godwill():
    bc = BChanges()
    yoyo = []
    for seed in seed_list:
        yoyo.append(bc.yoyo(int(seed)))

    while len(yoyo) < 6:
        yoyo.append(bc.yoyo(0))

    gwill = 'i_' + str(int(yoyo[0]) & 1) + str(int(yoyo[1]) & 1) + str(int(yoyo[2]) & 1) + str(int(yoyo[3]) & 1) + str(int(yoyo[4]) & 1) + str(int(yoyo[5]) & 1)
    gwill_name = gua_ci[gwill]
    print('##########################################################################################################################################')
    print(gwill_name)
    gwill_solution = solution_dict[gwill]
    print(gwill_solution)
    print('##########################################################################################################################################')


class BChanges(object):

    def __init__(self):
        pass

    def yoyo(self, seed):
        if seed == 0:
            seed = 10
        sky, land, human = self.chaos(49, seed)
        sky, land, human = self.change(sky, land, human)
        grass = sky + land
        sky, land, human = self.chaos(grass, seed)
        sky, land, human = self.change(sky, land, human)
        grass = sky + land
        sky, land, human = self.chaos(grass, seed)
        sky, land, human = self.change(sky, land, human)
        grass = sky + land
        return grass / 4

    def change(self, sky, land, human):
        sky_change = sky % 4
        land_change = land % 4
        if sky_change == 0:
            sky_change = 4
        sky = sky - sky_change
        human = human + sky_change
        if land_change == 0:
            land_change = 4
        land = land - land_change
        human = human + land_change
        return (sky, land, human)

    def chaos(self, grass, seed):
        sky = random.randrange(1, grass, seed)
        land = grass - sky - 1
        human = 1
        return (sky, land, human)

    def drawYo(self, yo, pen, x, y):
        if yo == 0:
            pen.penup()
            pen.goto(x, y)
            pen.pendown()
            pen.forward(200)
        else:
            pen.penup()
            pen.goto(x, y)
            pen.pendown()
            pen.forward(90)
            pen.penup()
            pen.goto(x + 20, y)
            pen.pendown()
            pen.forward(90)