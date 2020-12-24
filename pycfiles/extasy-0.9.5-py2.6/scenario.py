# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\extasy\step_definitions\scenario.py
# Compiled at: 2010-11-20 06:10:24
import extasy
from extasy import *

@Given('I run "$title" scenario of "$story" story')
@When('I run "$title" scenario of "$story" story')
@Then('I run "$title" scenario of "$story" story')
def run(context, title, story):
    ok = extasy.runner.run_story_scenario(story, scenario=title)
    if not ok:
        raise StepFailure('Fail running "%s" scenario of "%s" story' % (title, story))