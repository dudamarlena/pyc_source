# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_transitions_with_pop_recipe.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 4851 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 2.5, s, t 3, s, t 5, s, t 5.5, dt 0.016, s, q'
tags = 'transitions with pop, unschedule, schedule, on_enter, on_exit'
import cocos
import cocos.director as director
from cocos.actions import *
from cocos.layer import *
from cocos.scenes import *
t0 = 0.0
time_x = 0.0
scene1 = None
scene2 = None
scene3 = None
stage = None
last_current_scene = 123

def report(t):
    global scene1
    global scene2
    print('\nscene change')
    print('time:%4.3f' % t)
    print('len(director.scene_stack):', len(director.scene_stack))
    current_scene = director.scene
    if current_scene is None:
        s_scene = 'None'
    elif current_scene is scene1:
        s_scene = 'scene1'
    elif current_scene is scene2:
        s_scene = 'scene2'
    else:
        s_scene = 'transition scene'
    print('current scene:', s_scene, current_scene)


def sequencer(dt):
    global last_current_scene
    global stage
    global time_x
    time_x += dt
    if last_current_scene != director.scene:
        last_current_scene = director.scene
        report(time_x)
    if stage == 'run scene1' and time_x > 2.0:
        stage = 'transition to scene2'
        print('\n%4.3f begin %s' % (time_x, stage))
        director.push(FadeTransition(scene2, 0.5))
    elif stage == 'transition to scene2' and time_x > 5.0:
        stage = 'transition to the top scene in the stack'
        print('\n%4.3f begin %s' % (time_x, stage))
        director.replace(FadeTransitionWithPop(director.scene_stack[0], 0.5))


class FadeTransitionWithPop(FadeTransition):

    def finish(self):
        director.pop()


class ZoomTransitionWithPop(ZoomTransition):

    def finish(self):
        director.pop()


class FlipX3DTransitionWithPop(FlipX3DTransition):

    def finish(self):
        director.pop()


TransitionWithPop = "\nTransitionWithPop recipe\n\nWhile you can apply any cocos transition scene to the scene changes\ndirector.run\ndirector.replace\ndirector.push\n\nthey are not builtin scene transitions to apply when doing director.pop\n\nBut is easy to implement in your app with the following recipe:\n\n    1. select one of the stock scene transitions, to be found in\n       cocos/scenes/transitions.py, say ZzzTransition\n\n    2. define a subclass\n        class ZzzTransitionWithPop(ZzzTransition):\n            def finish():\n                director.pop()\n\n    3. instead of director.pop(), use\n            director.replace( ZzzTransitionWithPop(\n                              director.scene_stack[0], <other params>))\n       where <other params> are the ones needed in the original transition,\n       excluding the 'dst' argument\n\n"
description = "\n    A demo for the recipe TransitionWithPop, which shows how to replace a dry\n    director.pop() with a more appealing transition to the same scene.\n    There is a short multiline string in the code telling the recipe.\n\n    Along the time you will see :\n\n    around t=0.000 : scene1 shows (screen full green)\n    around t=2.000 : begins normal transition to scene2 (director.push(...))\n    around t=2.500 : transitions ends, scene2 in full view (screen full violet)\n    around t=5.000 : starts transition with pop\n    around t=5.500 : transition ends, scene1 in full view (screen full green)\n\n    In the console a report about current scene and director.scene_stack changes\n    The final scene should be scene1 and len(director.scene_stack) should be the\n    same as before the first transition initiated; that's 0 for cocos rev>1066\n    "

class TestScene(cocos.scene.Scene):

    def on_enter(self):
        super(TestScene, self).on_enter()
        self.schedule(sequencer)

    def on_exit(self):
        self.unschedule(sequencer)


def main():
    global scene1
    global scene2
    global stage
    print(description)
    print('\nactual timeline:')
    director.init(resizable=True)
    scene1 = TestScene()
    scene1.add(ColorLayer(80, 160, 32, 255))
    scene2 = TestScene()
    scene2.add(ColorLayer(120, 32, 120, 255))
    stage = 'before director.run'
    print('\n%4.3f %s' % (0.0, stage))
    report(0)
    stage = 'run scene1'
    print('\n%4.3f begin %s' % (0.0, stage))
    director.run(scene1)


if __name__ == '__main__':
    main()
# global scene3 ## Warning: Unused global
# global t0 ## Warning: Unused global