# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/useragentutils/operating_system.py
# Compiled at: 2013-01-06 02:01:41
from base_product import BaseProduct
from manufacturer import Manufacturer
from device_type import DeviceType
from utilities import EnumValue

class OperatingSystem(BaseProduct):
    required = [
     'deviceType']
    WINDOWS = EnumValue(manufacturer=Manufacturer.MICROSOFT, parent=None, versionId=1, name='Windows', aliases=[
     'Windows'], exclude=[
     'Palm'], deviceType=DeviceType.COMPUTER, versionRegexString=None)
    WINDOWS_7 = EnumValue(manufacturer=Manufacturer.MICROSOFT, parent=WINDOWS, versionId=21, name='Windows 7', aliases=[
     'Windows NT 6.1'], exclude=None, deviceType=DeviceType.COMPUTER, versionRegexString=None)
    WINDOWS_VISTA = EnumValue(manufacturer=Manufacturer.MICROSOFT, parent=WINDOWS, versionId=20, name='Windows Vista', aliases=[
     'Windows NT 6'], exclude=None, deviceType=DeviceType.COMPUTER, versionRegexString=None)
    WINDOWS_2000 = EnumValue(manufacturer=Manufacturer.MICROSOFT, parent=WINDOWS, versionId=15, name='Windows 2000', aliases=[
     'Windows NT 5.0'], exclude=None, deviceType=DeviceType.COMPUTER, versionRegexString=None)
    WINDOWS_XP = EnumValue(manufacturer=Manufacturer.MICROSOFT, parent=WINDOWS, versionId=10, name='Windows XP', aliases=[
     'Windows NT 5'], exclude=None, deviceType=DeviceType.COMPUTER, versionRegexString=None)
    WINDOWS_MOBILE7 = EnumValue(manufacturer=Manufacturer.MICROSOFT, parent=WINDOWS, versionId=51, name='Windows Mobile 7', aliases=[
     'Windows Phone OS 7'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    WINDOWS_MOBILE = EnumValue(manufacturer=Manufacturer.MICROSOFT, parent=WINDOWS, versionId=50, name='Windows Mobile', aliases=[
     'Windows CE'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    WINDOWS_98 = EnumValue(manufacturer=Manufacturer.MICROSOFT, parent=WINDOWS, versionId=5, name='Windows 98', aliases=[
     'Windows 98', 'Win98'], exclude=[
     'Palm'], deviceType=DeviceType.COMPUTER, versionRegexString=None)
    ANDROID = EnumValue(manufacturer=Manufacturer.GOOGLE, parent=None, versionId=0, name='Android', aliases=[
     'Android'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    ANDROID4 = EnumValue(manufacturer=Manufacturer.GOOGLE, parent=ANDROID, versionId=4, name='Android 4.x', aliases=[
     'Android 4', 'Android-4'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    ANDROID4_TABLET = EnumValue(manufacturer=Manufacturer.GOOGLE, parent=ANDROID4, versionId=40, name='Android 4.x Tablet', aliases=[
     'Xoom', 'Transformer'], exclude=None, deviceType=DeviceType.TABLET, versionRegexString=None)
    ANDROID3_TABLET = EnumValue(manufacturer=Manufacturer.GOOGLE, parent=ANDROID, versionId=30, name='Android 3.x Tablet', aliases=[
     'Android 3'], exclude=None, deviceType=DeviceType.TABLET, versionRegexString=None)
    ANDROID2 = EnumValue(manufacturer=Manufacturer.GOOGLE, parent=ANDROID, versionId=2, name='Android 2.x', aliases=[
     'Android 2'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    ANDROID2_TABLET = EnumValue(manufacturer=Manufacturer.GOOGLE, parent=ANDROID2, versionId=20, name='Android 2.x Tablet', aliases=[
     'Kindle Fire', 'GT-P1000', 'SCH-I800'], exclude=None, deviceType=DeviceType.TABLET, versionRegexString=None)
    ANDROID1 = EnumValue(manufacturer=Manufacturer.GOOGLE, parent=ANDROID, versionId=1, name='Android 1.x', aliases=[
     'Android 1'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    WEBOS = EnumValue(manufacturer=Manufacturer.HP, parent=None, versionId=11, name='WebOS', aliases=[
     'webOS'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    PALM = EnumValue(manufacturer=Manufacturer.HP, parent=None, versionId=10, name='PalmOS', aliases=[
     'Palm'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    IOS = EnumValue(manufacturer=Manufacturer.APPLE, parent=None, versionId=2, name='iOS', aliases=[
     'like Mac OS X'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    iOS5_IPHONE = EnumValue(manufacturer=Manufacturer.APPLE, parent=IOS, versionId=42, name='iOS 5 (iPhone)', aliases=[
     'iPhone OS 5'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    iOS4_IPHONE = EnumValue(manufacturer=Manufacturer.APPLE, parent=IOS, versionId=41, name='iOS 4 (iPhone)', aliases=[
     'iPhone OS 4'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    MAC_OS_X_IPAD = EnumValue(manufacturer=Manufacturer.APPLE, parent=IOS, versionId=50, name='Mac OS X (iPad)', aliases=[
     'iPad'], exclude=None, deviceType=DeviceType.TABLET, versionRegexString=None)
    MAC_OS_X_IPHONE = EnumValue(manufacturer=Manufacturer.APPLE, parent=IOS, versionId=40, name='Mac OS X (iPhone)', aliases=[
     'iPhone'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    MAC_OS_X_IPOD = EnumValue(manufacturer=Manufacturer.APPLE, parent=IOS, versionId=30, name='Mac OS X (iPod)', aliases=[
     'iPod'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    MAC_OS_X = EnumValue(manufacturer=Manufacturer.APPLE, parent=None, versionId=10, name='Mac OS X', aliases=[
     'Mac OS X', 'CFNetwork'], exclude=None, deviceType=DeviceType.COMPUTER, versionRegexString=None)
    MAC_OS = EnumValue(manufacturer=Manufacturer.APPLE, parent=None, versionId=1, name='Mac OS', aliases=[
     'Mac'], exclude=None, deviceType=DeviceType.COMPUTER, versionRegexString=None)
    MAEMO = EnumValue(manufacturer=Manufacturer.NOKIA, parent=None, versionId=2, name='Maemo', aliases=[
     'Maemo'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    BADA = EnumValue(manufacturer=Manufacturer.SAMSUNG, parent=None, versionId=2, name='Bada', aliases=[
     'Bada'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    GOOGLE_TV = EnumValue(manufacturer=Manufacturer.GOOGLE, parent=None, versionId=100, name='Android (Google TV)', aliases=[
     'GoogleTV'], exclude=None, deviceType=DeviceType.DMR, versionRegexString=None)
    KINDLE = EnumValue(manufacturer=Manufacturer.AMAZON, parent=None, versionId=1, name='Linux (Kindle)', aliases=[
     'Kindle'], exclude=None, deviceType=DeviceType.TABLET, versionRegexString=None)
    KINDLE3 = EnumValue(manufacturer=Manufacturer.AMAZON, parent=KINDLE, versionId=30, name='Linux (Kindle 3)', aliases=[
     'Kindle/3'], exclude=None, deviceType=DeviceType.TABLET, versionRegexString=None)
    KINDLE2 = EnumValue(manufacturer=Manufacturer.AMAZON, parent=KINDLE, versionId=20, name='Linux (Kindle 2)', aliases=[
     'Kindle/2'], exclude=None, deviceType=DeviceType.TABLET, versionRegexString=None)
    LINUX = EnumValue(manufacturer=Manufacturer.OTHER, parent=None, versionId=2, name='Linux', aliases=[
     'Linux', 'CamelHttpStream'], exclude=None, deviceType=DeviceType.COMPUTER, versionRegexString=None)
    SYMBIAN = EnumValue(manufacturer=Manufacturer.SYMBIAN, parent=None, versionId=1, name='Symbian OS', aliases=[
     'Symbian', 'Series60'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    SYMBIAN9 = EnumValue(manufacturer=Manufacturer.SYMBIAN, parent=SYMBIAN, versionId=20, name='Symbian OS 9.x', aliases=[
     'SymbianOS/9', 'Series60/3'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    SYMBIAN8 = EnumValue(manufacturer=Manufacturer.SYMBIAN, parent=SYMBIAN, versionId=15, name='Symbian OS 8.x', aliases=[
     'SymbianOS/8', 'Series60/2.6', 'Series60/2.8'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    SYMBIAN7 = EnumValue(manufacturer=Manufacturer.SYMBIAN, parent=SYMBIAN, versionId=10, name='Symbian OS 7.x', aliases=[
     'SymbianOS/7'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    SYMBIAN6 = EnumValue(manufacturer=Manufacturer.SYMBIAN, parent=SYMBIAN, versionId=5, name='Symbian OS 6.x', aliases=[
     'SymbianOS/6'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    SERIES40 = EnumValue(manufacturer=Manufacturer.NOKIA, parent=None, versionId=1, name='Series 40', aliases=[
     'Nokia6300'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    SONY_ERICSSON = EnumValue(manufacturer=Manufacturer.SONY_ERICSSON, parent=None, versionId=1, name='Sony Ericsson', aliases=[
     'SonyEricsson'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    SUN_OS = EnumValue(manufacturer=Manufacturer.SUN, parent=None, versionId=1, name='SunOS', aliases=[
     'SunOS'], exclude=None, deviceType=DeviceType.COMPUTER, versionRegexString=None)
    PSP = EnumValue(manufacturer=Manufacturer.SONY, parent=None, versionId=1, name='Sony Playstation', aliases=[
     'Playstation'], exclude=None, deviceType=DeviceType.GAME_CONSOLE, versionRegexString=None)
    WII = EnumValue(manufacturer=Manufacturer.NINTENDO, parent=None, versionId=1, name='Nintendo Wii', aliases=[
     'Wii'], exclude=None, deviceType=DeviceType.GAME_CONSOLE, versionRegexString=None)
    BLACKBERRY = EnumValue(manufacturer=Manufacturer.BLACKBERRY, parent=None, versionId=1, name='BlackBerryOS', aliases=[
     'BlackBerry'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    BLACKBERRY7 = EnumValue(manufacturer=Manufacturer.BLACKBERRY, parent=BLACKBERRY, versionId=7, name='BlackBerry 7', aliases=[
     'Version/7'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    BLACKBERRY6 = EnumValue(manufacturer=Manufacturer.BLACKBERRY, parent=BLACKBERRY, versionId=6, name='BlackBerry 6', aliases=[
     'Version/6'], exclude=None, deviceType=DeviceType.MOBILE, versionRegexString=None)
    BLACKBERRY_TABLET = EnumValue(manufacturer=Manufacturer.BLACKBERRY, parent=None, versionId=100, name='BlackBerry Tablet OS', aliases=[
     'RIM Tablet OS'], exclude=None, deviceType=DeviceType.TABLET, versionRegexString=None)
    ROKU = EnumValue(manufacturer=Manufacturer.ROKU, parent=None, versionId=1, name='Roku OS', aliases=[
     'Roku'], exclude=None, deviceType=DeviceType.DMR, versionRegexString=None)
    UNKNOWN = EnumValue(manufacturer=Manufacturer.OTHER, parent=None, versionId=1, name='Unknown', aliases=[], exclude=None, deviceType=DeviceType.UNKNOWN, versionRegexString=None)