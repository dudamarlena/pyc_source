# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/tests/test_check.py
# Compiled at: 2019-03-22 02:52:30
# Size of source mod 2**32: 9822 bytes
"""
-------------------------------------------------

    File Name:        /Users/jackdeng/code/Python/paramspy/tests/test_check.py

    Description:      test for checker

    Author:           dlwxxxdlw@gmail.com

    Date:             2019-03-10-14:11:45

    Version:          v1.0

    Lastmodified:     2019-03-10 by Jack Deng

-------------------------------------------------
"""
import re, pytest
try:
    from loguru import logger
except ImportError:
    from logging import getLogger
    logger = getLogger(__name__)

from paramspy import Checker, CheckFailed, RuleNotMatch, TypeNotMatch, ParamNotFound

def test_not_match():
    target = [
     {'username':'dlwxxxdlw', 
      'password':'zxvxcgweg', 
      'phone':'1234567890%$^'},
     {'username':'', 
      'password':'zxvxcgweg', 
      'phone':'1234567890%$^', 
      'gender':'alian'},
     {'password':'zxvxcgweg', 
      'phone':'18934554354', 
      'age':'35'},
     {'username':'dlwxxxdlw', 
      'password':'zxvxcgweg', 
      'phone':'18934554354', 
      'age':12}]
    try:
        res = Checker([
         (
          'username', (str,), 'WORD'),
         (
          'password', (str,), 'WORD'),
         (
          'phone', (int,), 'NUMBER'),
         [
          'gender', 'female', ['female', 'male', 'secret']],
         [
          'age', None, (int,), lambda x: int(x) > 18]]).check(target)
    except CheckFailed as check_err:
        try:
            logger.error('{}'.format(check_err))
            logger.error('error string \n{}'.format(check_err.get_excstr()))
            logger.warning('default rules {}'.format(Checker.default_rules()))
        finally:
            check_err = None
            del check_err

    try:
        res = Checker([
         [
          'username', None, 'WORD'],
         [
          'password', None, 'WORD'],
         ('phone', 'NUMBER'),
         [
          'gender', 'female']]).check(target)
    except CheckFailed as check_err:
        try:
            logger.error('{}'.format(check_err))
        finally:
            check_err = None
            del check_err


def test_param_not_found_value():
    target = {'username':'dlwxxxdlw', 
     'password':'zxvxcgweg'}
    try:
        res = Checker([
         [
          'username', None, 'WORD'],
         [
          'password', None, 'WORD'],
         ('phone', 'NUMBER'),
         [
          'gender', 'female']]).check(target)
    except CheckFailed as check_err:
        try:
            logger.error('{}'.format(check_err))
        finally:
            check_err = None
            del check_err


def test_default_value():
    target = {'username':'dlwxxxdlw', 
     'password':'zxvxcgweg'}
    target1 = {'username':'dlwxxxdlw', 
     'password':'zxvxcgweg', 
     'gender':'alien'}
    try:
        res = Checker([
         [
          'username', None, 'WORD'],
         [
          'password', None, 'WORD'],
         [
          'gender', 'female']]).check(target)
        logger.debug(res)
        res1 = Checker([
         [
          'username', None, 'WORD'],
         [
          'password', None, 'WORD'],
         [
          'gender', 'female', str, ['male', 'female']]]).check(target1)
    except CheckFailed as check_err:
        try:
            logger.error('{}'.format(check_err))
        finally:
            check_err = None
            del check_err


def test_multi_rule_not_match():
    target = {'username':'dlwxxxdlw', 
     'password':'zxvxcgweg', 
     'phone':'1234567890%$^', 
     'email':'heheeheheda'}
    try:
        res = Checker([
         [
          'username', None, 'WORD'],
         [
          'password', None, 'WORD'],
         [
          'phone', None, int, 'NUMBER'],
         (
          'gender', ['female', 'male']),
         [
          'email', None, 'EMAIL']]).check(target)
    except CheckFailed as check_err:
        try:
            logger.error(check_err)
        finally:
            check_err = None
            del check_err


def test_all_match():
    target = {'username':'dlwxxxdlw', 
     'password':'zxvxcgweg', 
     'phone':1234567890, 
     'email':'heheeheheda@gmail.com'}
    try:
        res = Checker([
         [
          'username', None, 'WORD'],
         [
          'password', None, 'WORD'],
         [
          'phone', None, int, 'NUMBER'],
         [
          'gender', 'female'],
         [
          'email', None, 'EMAIL']]).check(target)
        logger.debug(res)
    except CheckFailed as check_err:
        try:
            logger.error(check_err)
        finally:
            check_err = None
            del check_err


def test_custom_regex():
    target = [
     {'username':'dlwxxxdlw', 
      'password':'zxvxcgweg', 
      'phone':13889232341, 
      'email':'heheeheheda@gmail.com'},
     {'username':'dlwxxxdlw', 
      'password':'zxvxcgweg', 
      'phone':'1234567890', 
      'email':'heheeheheda@gmail.com'}]
    try:
        res = Checker([
         [
          'username', None, 'WORD'],
         [
          'password', None, 'WORD'],
         [
          'phone', None, (int, str), re.compile('^(138|181)')],
         [
          'gender', 'female'],
         [
          'email', None, 'EMAIL']]).check(target)
        logger.debug(res)
    except CheckFailed as check_err:
        try:
            logger.error(check_err)
            logger.error(check_err.get_excstr())
        finally:
            check_err = None
            del check_err


def test_custom_list_rule():
    target = [{'username':'dlwxxxdlw', 
      'password':'zxvxcgweg', 
      'phone':12345456790, 
      'gender':'male', 
      'email':'heheeheheda@gmail.com'},
     {'username':'dlwxxxdlw', 
      'password':'zxvxcgweg', 
      'phone':'12345456790', 
      'gender':'alien', 
      'email':'heheeheheda@gmail.com'}]
    try:
        res = Checker([
         [
          'username', None, 'WORD'],
         [
          'password', None, 'WORD'],
         [
          'phone', None, (int,)],
         [
          'gender', None, ['female', 'male', 'secret']],
         [
          'email', None, 'EMAIL']]).check(target)
        logger.debug('{}'.format(res))
    except CheckFailed as check_err:
        try:
            logger.error('{}'.format(check_err))
        finally:
            check_err = None
            del check_err


def test_value_not_allowed():
    target = {'username':'dlwxxxdlw', 
     'password':'zxvxcgweg', 
     'phone':'1234567890', 
     'gender':'female', 
     'email':'heheeheheda@gmail.com'}
    try:
        res = Checker([
         (
          'username', (str,), 'WORD'),
         (
          'password', (str,), 'WORD'),
         (
          'phone', str, 'NUMBER'),
         [
          'email', None, 'EMAIL']]).check(target)
        logger.debug('{}'.format(res))
    except CheckFailed as check_err:
        try:
            logger.error('{}'.format(check_err))
        finally:
            check_err = None
            del check_err


def test_list_data():
    target = [{'username':'dlwxxxdlw', 
      'password':'zxvxcgweg', 
      'phone':'1234567890', 
      'gender':'female', 
      'email':'heheeheheda@gmail.com'},
     {'username':'dlwxxxdlw', 
      'phone':1234567890, 
      'gender':'female', 
      'email':'heheeheheda@gmail.com'},
     {'username':123456, 
      'password':'zxvxcgweg', 
      'phone':'1234567890', 
      'email':'bademail'}]
    try:
        res = Checker([
         (
          'username', str, 'WORD'),
         (
          'password', str, 'WORD'),
         (
          'phone', int, 'NUMBER'),
         [
          'gender', 'secret'],
         (
          'email', str, 'EMAIL')]).check(target)
        logger.debug('{}'.format(res))
    except CheckFailed as check_err:
        try:
            logger.error('{}'.format(check_err))
        finally:
            check_err = None
            del check_err


def test_no_rule():
    target = [
     {'username':'dlwxxxdlw', 
      'password':'zxvxcgweg', 
      'phone':'1234567890', 
      'gender':'female', 
      'email':'heheeheheda@gmail.com'},
     {'username':'dlwxxxdlw', 
      'phone':1234567890, 
      'gender':'female', 
      'email':'heheeheheda@gmail.com'},
     {'username':123456, 
      'password':'zxvxcgweg', 
      'phone':'1234567890', 
      'email':'bademail'}]
    try:
        res = Checker([
         'username',
         'password',
         'phone',
         'gender',
         'email']).check(target)
        logger.debug('{}'.format(res))
    except CheckFailed as check_err:
        try:
            logger.error('{}'.format(check_err))
        finally:
            check_err = None
            del check_err


def test_for_lambda():
    target = [
     {'age':25, 
      'height':180},
     {'age':'35', 
      'height':'190'},
     {'age': '35'}]
    try:
        res = Checker([
         (
          'age', (int, str), lambda x: int(x) > 10),
         [
          'height', 170, (int,), lambda y: int(y) < 170]]).check(target)
    except CheckFailed as check_err:
        try:
            logger.error(check_err)
            logger.error(check_err.get_excstr())
        finally:
            check_err = None
            del check_err


def test_raise_first():
    target = [
     {'age':25, 
      'height':180},
     {'age':'35', 
      'height':'190'},
     {'age': '35'}]
    try:
        res = Checker([
         (
          'age', (int, str), lambda x: int(x) > 10),
         [
          'height', 170, (int,), lambda y: int(y) < 170]]).check(target,
          raise_first=True)
    except CheckFailed as check_err:
        try:
            logger.error(check_err)
        finally:
            check_err = None
            del check_err