# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/jptel/jptel.py
# Compiled at: 2019-03-29 13:51:42
# Size of source mod 2**32: 3247 bytes
from typing import Dict
import re
from . import data
from .exception import InvalidCharacterException, InvalidTelephoneNumberException
number_and_hyphen_regexp = re.compile('^[−ー0-9０-９-]+$')
telephone_number_regexp = re.compile('^[0-9０-９]{10,11}$')
telephone_number_with_hyphen_regex = re.compile('^[0-9０-９]{2,4}[−ー-][0-9０-９]{2,4}[−ー-][0-9０-９]{3,4}$')
_translate_table = str.maketrans({'０':'0', 
 '１':'1', 
 '２':'2', 
 '３':'3', 
 '４':'4', 
 '５':'5', 
 '６':'6', 
 '７':'7', 
 '８':'8', 
 '９':'9', 
 'ー':'-', 
 '−':'-'})

def generate_dict(number: str, area_code_length: int, city_code_length: int) -> Dict[(str, str)]:
    total_code_length = area_code_length + city_code_length
    if len(number) < total_code_length:
        raise InvalidTelephoneNumberException
    return {'area_code':number[:area_code_length], 
     'city_code':number[area_code_length:total_code_length], 
     'subscriber_code':number[total_code_length:]}


def zenkaku_to_hankaku(number: str) -> str:
    return number.translate(_translate_table)


def extract_number(src: str) -> str:
    """全角半角やハイフンが混じった文字列を半角数字のみの文字列にして返す"""
    m = number_and_hyphen_regexp.fullmatch(src)
    if not m:
        raise InvalidCharacterException
    return zenkaku_to_hankaku(m.string).replace('-', '')


def split(src: str) -> Dict[(str, str)]:
    """入力された文字列を辞書形式に分割して返す"""
    number = extract_number(src)
    for codes in [data.area_code_5, data.area_code_4, data.area_code_3, data.area_code_2]:
        for code in codes:
            if number.startswith(code):
                area_code_length = len(code)
                city_code_length = data.TOTAL_CODE_LENGTH - area_code_length
                return generate_dict(number, area_code_length, city_code_length)

    for code in data.freedial_code:
        if number.startswith(code):
            return generate_dict(number, data.FREEDIAL_CODE_PREFIX_LENGTH, data.FREEDIAL_CODE_LENGTH)

    for code in data.mobile_code:
        if number.startswith(code):
            return generate_dict(number, data.MOBILE_CODE_PREFIX_LENGTH, data.MOBILE_CODE_LENGTH)

    for code in data.other_code:
        if number.startswith(code):
            return generate_dict(number, data.OTHER_CODE_PREFIX_LENGTH, data.OTHER_CODE_LENGTH)

    raise InvalidTelephoneNumberException


def validate(src: str) -> bool:
    if not telephone_number_regexp.fullmatch(src):
        if not telephone_number_with_hyphen_regex.fullmatch(src):
            return False
    try:
        split(src)
    except (InvalidTelephoneNumberException, InvalidTelephoneNumberException):
        return False
    else:
        return True


def normalize(src: str) -> str:
    """入力された文字列をハイフン区切りの電話番号にして返す"""
    number = extract_number(src)
    code = split(number)
    return '{}-{}-{}'.format(code['area_code'], code['city_code'], code['subscriber_code'])