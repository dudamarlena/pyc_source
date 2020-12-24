# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asyncee/python-obscene-words-filter/obscene_words_filter/conf.py
# Compiled at: 2017-01-24 07:20:43
from __future__ import unicode_literals
import re
from .regexp import build_good_phrase, build_bad_phrase
bad_words = [
 build_bad_phrase(b'п еи з д'),
 build_bad_phrase(b'х у йёуяию'),
 build_bad_phrase(b'о х у е втл'),
 build_bad_phrase(b'п и д оеа р'),
 build_bad_phrase(b'п и д р'),
 build_bad_phrase(b'её б а нклт'),
 build_bad_phrase(b'у её б оа нтк'),
 build_bad_phrase(b'её б л аои'),
 build_bad_phrase(b'в ы её б'),
 build_bad_phrase(b'е б ё т'),
 build_bad_phrase(b'св ъь еёи б'),
 build_bad_phrase(b'б л я'),
 build_bad_phrase(b'г оа в н'),
 build_bad_phrase(b'м у д а кч'),
 build_bad_phrase(b'г ао н д о н'),
 build_bad_phrase(b'ч м оы'),
 build_bad_phrase(b'д е р ь м'),
 build_bad_phrase(b'ш л ю х'),
 build_bad_phrase(b'з ао л у п'),
 build_bad_phrase(b'м ао н д'),
 build_bad_phrase(b'с у ч а р'),
 build_bad_phrase(b'д ао л б ао её б')]
bad_words_re = re.compile((b'|').join(bad_words), re.IGNORECASE | re.UNICODE)
good_words = [
 build_good_phrase(b'х л е б а л оа'),
 build_good_phrase(b'с к и п и д а р'),
 build_good_phrase(b'к о л е б а н и яей'),
 build_good_phrase(b'з ао к оа л е б а лт'),
 build_good_phrase(b'р у б л я'),
 build_good_phrase(b'с т е б е л ь'),
 build_good_phrase(b'с т р а х о в к ауи'),
 b'([о][с][к][о][Р][б][л][я]([т][ь])*([л])*([е][ш][ь])*)',
 b'([в][л][ю][б][л][я](([т][ь])([с][я])*)*(([е][ш][ь])([с][я])*)*)',
 b'((([п][о][д])*([з][а])*([п][е][р][е])*)*[с][т][р][а][х][у]([й])*([с][я])*([е][ш][ь])*([е][т])*)',
 b'([м][е][б][е][л][ь]([н][ы][й])*)',
 b'([Уу][Пп][Оо][Тт][Рр][Ее][Бб][Лл][Яя]([Тт][Ьь])*([Ее][Шш][Ьь])*([Яя])*([Лл])*)',
 b'([Ии][Сс][Тт][Рр][Ее][Бб][Лл][Яя]([Тт][Ьь])*([Ее][Шш][Ьь])*([Яя])*([Лл])*)',
 b'([Сс][Тт][Рр][Аа][Хх]([Аа])*)']
good_words_re = re.compile((b'|').join(good_words), re.IGNORECASE | re.UNICODE)