# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/devel/grandma/demo/test_demo_app.py
# Compiled at: 2011-10-03 11:38:27
import unittest
from grandma.grandma import t_ways
from demo_app import run_app

def oracle_demo_app(**args):
    """Demo the use of an oracle"""
    return True


def check_single_testcase(args):
    """Helper function calling demo app and oracle"""
    res = run_app(**args)
    ocl = oracle_demo_app(**args)
    assert res == ocl


def test_wussy():
    """This is a very weak test since it only contains a single sample set of parameters."""
    check_single_testcase({'font': 'arial', 'bold': True, 'italic': False, 'strikethrough': True, 
       'underline': True, 'color': 'black', 'size': 'xLarge'})


def test_powerfull():
    """Demonstrate application of combinatorial testing."""
    spec = {'font': [
              'arial', 'tahoma', 'brushScript', 'monotypeCorsive'], 
       'bold': [
              True, False], 
       'italic': [
                True, False], 
       'strikethrough': [
                       True, False], 
       'underline': [
                   True, False], 
       'color': [
               'black', 'yellow', 'white', 'blue', 'red', 'green'], 
       'size': [
              'small', 'nominal', 'large', 'xLarge', 'xxLarge', 'xxxLarge', 'ridiculouslyLarge']}
    incompats = [{'font': ['brushScript', 'monotypeCorsive'], 'italic': False, 'bold': True}, {'font': 'monotypeCorsive', 'italic': True, 'bold': False}]
    reqs = []
    for t in t_ways(spec, 5, incompats=incompats, reqs=reqs):
        print 'test: ' + str(t)
        yield (check_single_testcase, t)