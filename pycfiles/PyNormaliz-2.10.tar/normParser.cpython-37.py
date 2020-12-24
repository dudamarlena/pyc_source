# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/grammar/normParser.py
# Compiled at: 2019-05-09 11:45:25
# Size of source mod 2**32: 180120 bytes
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as (buf):
        buf.write('\x03悋Ꜫ脳맭䅼㯧瞆奤\x03C')
        buf.write('ʼ\x04\x02\t\x02\x04\x03\t\x03\x04\x04\t\x04\x04\x05\t\x05\x04\x06\t\x06\x04\x07\t\x07')
        buf.write('\x04\x08\t\x08\x04\t\t\t\x04\n\t\n\x04\x0b\t\x0b\x04\x0c\t\x0c\x04\r\t\r\x04\x0e')
        buf.write('\t\x0e\x04\x0f\t\x0f\x04\x10\t\x10\x04\x11\t\x11\x04\x12\t\x12\x04\x13\t\x13')
        buf.write('\x04\x14\t\x14\x04\x15\t\x15\x04\x16\t\x16\x04\x17\t\x17\x04\x18\t\x18\x04\x19')
        buf.write('\t\x19\x04\x1a\t\x1a\x04\x1b\t\x1b\x04\x1c\t\x1c\x04\x1d\t\x1d\x04\x1e\t\x1e')
        buf.write('\x04\x1f\t\x1f\x04 \t \x04!\t!\x04"\t"\x04#\t#\x04$\t$\x04%\t%\x04&\t')
        buf.write("&\x04'\t'\x04(\t(\x04)\t)\x04*\t*\x04+\t+\x03\x02\x03\x02\x05\x02Y\n\x02\x03\x02")
        buf.write('\x03\x02\x07\x02]\n\x02\x0c\x02\x0e\x02`\x0b\x02\x03\x02\x03\x02\x05\x02d\n\x02\x03\x02\x03\x02')
        buf.write('\x07\x02h\n\x02\x0c\x02\x0e\x02k\x0b\x02\x03\x02\x05\x02n\n\x02\x03\x03\x03\x03\x05\x03r\n\x03')
        buf.write('\x03\x03\x03\x03\x05\x03v\n\x03\x03\x03\x03\x03\x05\x03z\n\x03\x03\x03\x03\x03\x05\x03~\n\x03\x03')
        buf.write('\x03\x05\x03\x81\n\x03\x03\x03\x05\x03\x84\n\x03\x03\x03\x05\x03\x87\n\x03\x03')
        buf.write('\x03\x03\x03\x05\x03\x8b\n\x03\x03\x03\x05\x03\x8e\n\x03\x03\x03\x03\x03\x05\x03\x92')
        buf.write('\n\x03\x03\x03\x03\x03\x05\x03\x96\n\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x05\x03\x9d')
        buf.write('\n\x03\x03\x03\x05\x03\xa0\n\x03\x03\x03\x03\x03\x05\x03¤\n\x03\x03\x03\x03\x03\x05')
        buf.write('\x03¨\n\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x05\x03¯\n\x03\x03\x03\x05\x03')
        buf.write('²\n\x03\x03\x03\x03\x03\x05\x03¶\n\x03\x03\x03\x03\x03\x05\x03º\n\x03')
        buf.write('\x03\x03\x03\x03\x03\x03\x05\x03¿\n\x03\x03\x03\x05\x03Â\n\x03\x03\x03\x03\x03\x05')
        buf.write('\x03Æ\n\x03\x03\x03\x03\x03\x05\x03Ê\n\x03\x03\x03\x05\x03Í\n\x03\x05')
        buf.write('\x03Ï\n\x03\x03\x04\x03\x04\x03\x04\x07\x04Ô\n\x04\x0c\x04\x0e\x04×')
        buf.write('\x0b\x04\x05\x04Ù\n\x04\x03\x05\x03\x05\x03\x05\x03\x05\x03\x05\x05\x05à\n\x05')
        buf.write('\x03\x05\x03\x05\x03\x05\x07\x05å\n\x05\x0c\x05\x0e\x05è\x0b\x05\x03\x05\x05\x05')
        buf.write('ë\n\x05\x03\x05\x03\x05\x05\x05ï\n\x05\x03\x05\x05\x05ò\n\x05\x05\x05')
        buf.write('ô\n\x05\x03\x06\x03\x06\x03\x06\x03\x06\x07\x06ú\n\x06\x0c\x06\x0e\x06ý')
        buf.write('\x0b\x06\x03\x06\x03\x06\x03\x06\x03\x06\x03\x06\x03\x06\x07\x06ą\n\x06\x0c\x06\x0e\x06Ĉ')
        buf.write('\x0b\x06\x03\x06\x03\x06\x03\x06\x05\x06č\n\x06\x03\x06\x03\x06\x05\x06đ\n\x06')
        buf.write('\x03\x06\x05\x06Ĕ\n\x06\x05\x06Ė\n\x06\x03\x07\x03\x07\x03\x07\x03\x08\x03\x08\x03')
        buf.write('\x08\x05\x08Ğ\n\x08\x03\x08\x03\x08\x03\t\x03\t\x05\tĤ\n\t\x03\t\x03\t')
        buf.write('\x03\t\x03\t\x05\tĪ\n\t\x03\n\x03\n\x03\n\x03\n\x05\nİ\n\n\x03')
        buf.write('\n\x03\n\x03\n\x07\nĵ\n\n\x0c\n\x0e\nĸ\x0b\n\x03\x0b\x05\x0b')
        buf.write('Ļ\n\x0b\x03\x0b\x03\x0b\x05\x0bĿ\n\x0b\x03\x0b\x03\x0b\x03\x0c\x03')
        buf.write('\x0c\x05\x0cŅ\n\x0c\x03\x0c\x03\x0c\x05\x0cŉ\n\x0c\x03\x0c\x03\x0c\x05\x0cō')
        buf.write('\n\x0c\x03\r\x03\r\x05\rő\n\r\x03\r\x03\r\x05\rŕ\n\r\x03\r\x07')
        buf.write('\rŘ\n\r\x0c\r\x0e\rś\x0b\r\x03\x0e\x03\x0e\x05\x0eş')
        buf.write('\n\x0e\x03\x0e\x03\x0e\x05\x0eţ\n\x0e\x03\x0e\x03\x0e\x03\x0f\x03\x0f\x05')
        buf.write('\x0fũ\n\x0f\x03\x0f\x03\x0f\x05\x0fŭ\n\x0f\x03\x0f\x07\x0fŰ')
        buf.write('\n\x0f\x0c\x0f\x0e\x0fų\x0b\x0f\x03\x10\x03\x10\x03\x10\x03\x10\x03\x10')
        buf.write('\x05\x10ź\n\x10\x03\x10\x05\x10Ž\n\x10\x03\x10\x03\x10\x05\x10Ɓ')
        buf.write('\n\x10\x03\x10\x05\x10Ƅ\n\x10\x03\x11\x03\x11\x03\x12\x03\x12\x05\x12Ɗ')
        buf.write('\n\x12\x03\x12\x03\x12\x03\x12\x03\x12\x05\x12Ɛ\n\x12\x03\x12\x03\x12\x05')
        buf.write('\x12Ɣ\n\x12\x03\x12\x07\x12Ɨ\n\x12\x0c\x12\x0e\x12ƚ\x0b')
        buf.write('\x12\x03\x12\x03\x12\x03\x12\x03\x12\x03\x12\x03\x12\x05\x12Ƣ\n\x12\x03\x12')
        buf.write('\x03\x12\x05\x12Ʀ\n\x12\x03\x12\x07\x12Ʃ\n\x12\x0c\x12\x0e\x12')
        buf.write('Ƭ\x0b\x12\x03\x12\x03\x12\x05\x12ư\n\x12\x03\x13\x03\x13\x03\x13')
        buf.write('\x03\x13\x03\x13\x03\x13\x03\x13\x03\x13\x03\x13\x03\x13\x03\x13\x03\x13\x05\x13ƾ')
        buf.write('\n\x13\x03\x13\x03\x13\x05\x13ǂ\n\x13\x03\x13\x07\x13ǅ\n\x13\x0c')
        buf.write('\x13\x0e\x13ǈ\x0b\x13\x03\x13\x03\x13\x05\x13ǌ\n\x13\x03\x14\x07')
        buf.write('\x14Ǐ\n\x14\x0c\x14\x0e\x14ǒ\x0b\x14\x03\x15\x03\x15\x03\x15\x03')
        buf.write('\x15\x03\x16\x03\x16\x03\x16\x03\x16\x03\x16\x03\x16\x03\x16\x05\x16ǟ\n\x16')
        buf.write('\x03\x16\x03\x16\x05\x16ǣ\n\x16\x03\x16\x03\x16\x05\x16ǧ\n\x16\x03')
        buf.write('\x16\x03\x16\x03\x16\x03\x16\x05\x16ǭ\n\x16\x05\x16ǯ\n\x16\x03\x17')
        buf.write('\x03\x17\x03\x17\x03\x17\x03\x17\x05\x17Ƕ\n\x17\x03\x17\x03\x17\x05\x17Ǻ')
        buf.write('\n\x17\x03\x17\x07\x17ǽ\n\x17\x0c\x17\x0e\x17Ȁ\x0b\x17\x03\x17')
        buf.write('\x03\x17\x05\x17Ȅ\n\x17\x03\x18\x03\x18\x03\x18\x03\x18\x05\x18Ȋ\n')
        buf.write('\x18\x03\x18\x05\x18ȍ\n\x18\x03\x18\x03\x18\x03\x18\x03\x18\x05\x18ȓ')
        buf.write('\n\x18\x03\x18\x05\x18Ȗ\n\x18\x05\x18Ș\n\x18\x03\x18\x03\x18\x05')
        buf.write('\x18Ȝ\n\x18\x03\x18\x03\x18\x05\x18Ƞ\n\x18\x03\x18\x07\x18ȣ')
        buf.write('\n\x18\x0c\x18\x0e\x18Ȧ\x0b\x18\x03\x19\x03\x19\x03\x19\x03\x19\x05\x19')
        buf.write('Ȭ\n\x19\x03\x19\x05\x19ȯ\n\x19\x03\x19\x05\x19Ȳ\n\x19')
        buf.write('\x03\x19\x05\x19ȵ\n\x19\x03\x19\x05\x19ȸ\n\x19\x03\x19\x03\x19\x03')
        buf.write('\x19\x03\x19\x03\x19\x03\x19\x03\x19\x05\x19Ɂ\n\x19\x03\x1a\x03\x1a\x03\x1a')
        buf.write('\x03\x1a\x03\x1a\x03\x1a\x03\x1a\x03\x1a\x05\x1aɋ\n\x1a\x03\x1a\x03\x1a\x05')
        buf.write('\x1aɏ\n\x1a\x03\x1a\x03\x1a\x05\x1aɓ\n\x1a\x03\x1a\x03\x1a\x03\x1a')
        buf.write('\x05\x1aɘ\n\x1a\x03\x1a\x03\x1a\x05\x1aɜ\n\x1a\x03\x1a\x03\x1a\x03')
        buf.write('\x1a\x05\x1aɡ\n\x1a\x03\x1a\x03\x1a\x05\x1aɥ\n\x1a\x03\x1a\x07\x1a')
        buf.write('ɨ\n\x1a\x0c\x1a\x0e\x1aɫ\x0b\x1a\x03\x1b\x03\x1b\x03\x1b\x03\x1b')
        buf.write('\x03\x1b\x05\x1bɲ\n\x1b\x03\x1c\x03\x1c\x03\x1c\x05\x1cɷ\n\x1c\x03')
        buf.write('\x1c\x05\x1cɺ\n\x1c\x03\x1c\x03\x1c\x05\x1cɾ\n\x1c\x03\x1c\x05\x1c')
        buf.write('ʁ\n\x1c\x03\x1c\x03\x1c\x03\x1c\x03\x1c\x07\x1cʇ\n\x1c\x0c\x1c\x0e')
        buf.write('\x1cʊ\x0b\x1c\x03\x1d\x03\x1d\x03\x1d\x03\x1d\x03\x1d\x05\x1dʑ\n')
        buf.write('\x1d\x03\x1e\x03\x1e\x03\x1f\x03\x1f\x03 \x03 \x03!\x03!\x03"\x03"\x03#\x03#\x03$\x03')
        buf.write("$\x03%\x03%\x03&\x03&\x03'\x03'\x03(\x05(ʨ\n(\x03(\x03(\x05(ʬ\n")
        buf.write('(\x03)\x03)\x03)\x05)ʱ\n)\x03*\x03*\x03+\x05+ʶ\n+\x03+\x03+\x05+ʺ')
        buf.write('\n+\x03+\x02\x06\x12.26,\x02\x04\x06\x08\n\x0c\x0e\x10\x12\x14\x16\x18\x1a')
        buf.write('\x1c\x1e "$&(*,.02468:<>@BDFHJLNPRT\x02\x0b\x03\x02\x15')
        buf.write('\x16\x04\x02\x12\x13CC\x04\x02\x04\x05>>\x03\x02AB\x03\x0212\x03\x02/0\x03\x02')
        buf.write('-.\x03\x0238\x03\x02$,\x02̥\x02V\x03\x02\x02\x02\x04Î\x03\x02\x02\x02\x06')
        buf.write('Ø\x03\x02\x02\x02\x08ó\x03\x02\x02\x02\nĕ\x03\x02\x02\x02\x0cė')
        buf.write('\x03\x02\x02\x02\x0eĚ\x03\x02\x02\x02\x10ĩ\x03\x02\x02\x02\x12į\x03')
        buf.write('\x02\x02\x02\x14ĺ\x03\x02\x02\x02\x16ł\x03\x02\x02\x02\x18Ŏ\x03\x02')
        buf.write('\x02\x02\x1aŜ\x03\x02\x02\x02\x1cŦ\x03\x02\x02\x02\x1eŴ\x03\x02\x02')
        buf.write('\x02 ƅ\x03\x02\x02\x02"Ư\x03\x02\x02\x02$ǋ\x03\x02\x02\x02&ǐ')
        buf.write('\x03\x02\x02\x02(Ǔ\x03\x02\x02\x02*Ǯ\x03\x02\x02\x02,ȃ\x03\x02\x02\x02')
        buf.write('.ȗ\x03\x02\x02\x020ɀ\x03\x02\x02\x022Ɋ\x03\x02\x02\x024ɱ')
        buf.write('\x03\x02\x02\x026ʀ\x03\x02\x02\x028ʐ\x03\x02\x02\x02:ʒ\x03\x02\x02')
        buf.write('\x02<ʔ\x03\x02\x02\x02>ʖ\x03\x02\x02\x02@ʘ\x03\x02\x02\x02Bʚ')
        buf.write('\x03\x02\x02\x02Dʜ\x03\x02\x02\x02Fʞ\x03\x02\x02\x02Hʠ\x03\x02\x02\x02')
        buf.write('Jʢ\x03\x02\x02\x02Lʤ\x03\x02\x02\x02Nʧ\x03\x02\x02\x02Pʭ\x03')
        buf.write('\x02\x02\x02Rʲ\x03\x02\x02\x02Tʵ\x03\x02\x02\x02VX\x05\x04\x03\x02WY\t\x02\x02')
        buf.write('\x02XW\x03\x02\x02\x02XY\x03\x02\x02\x02YZ\x03\x02\x02\x02Zi\x07 \x02\x02[]\t\x02\x02\x02\\')
        buf.write('[\x03\x02\x02\x02]`\x03\x02\x02\x02^\\\x03\x02\x02\x02^_\x03\x02\x02\x02_a\x03\x02\x02\x02`^\x03')
        buf.write('\x02\x02\x02ac\x05\x04\x03\x02bd\t\x02\x02\x02cb\x03\x02\x02\x02cd\x03\x02\x02\x02de\x03\x02\x02')
        buf.write('\x02ef\x07 \x02\x02fh\x03\x02\x02\x02g^\x03\x02\x02\x02hk\x03\x02\x02\x02ig\x03\x02\x02\x02ij')
        buf.write('\x03\x02\x02\x02jm\x03\x02\x02\x02ki\x03\x02\x02\x02ln\t\x02\x02\x02ml\x03\x02\x02\x02mn\x03\x02')
        buf.write('\x02\x02n\x03\x03\x02\x02\x02oÏ\x05\x06\x04\x02pr\x05\x06\x04\x02qp\x03\x02\x02\x02qr\x03')
        buf.write('\x02\x02\x02rs\x03\x02\x02\x02sÏ\x05\n\x06\x02tv\x05\x06\x04\x02ut\x03\x02\x02\x02uv')
        buf.write('\x03\x02\x02\x02vw\x03\x02\x02\x02wÏ\x05\x08\x05\x02xz\x05\x06\x04\x02yx\x03\x02\x02\x02')
        buf.write('yz\x03\x02\x02\x02z{\x03\x02\x02\x02{Ï\x05\x0c\x07\x02|~\x05\x06\x04\x02}|\x03\x02\x02')
        buf.write('\x02}~\x03\x02\x02\x02~\x80\x03\x02\x02\x02\x7f\x81\t\x02\x02\x02\x80\x7f')
        buf.write('\x03\x02\x02\x02\x80\x81\x03\x02\x02\x02\x81\x83\x03\x02\x02\x02\x82')
        buf.write('\x84\x05\x0e\x08\x02\x83\x82\x03\x02\x02\x02\x83\x84\x03\x02\x02')
        buf.write('\x02\x84\x86\x03\x02\x02\x02\x85\x87\t\x02\x02\x02\x86\x85')
        buf.write('\x03\x02\x02\x02\x86\x87\x03\x02\x02\x02\x87\x88\x03\x02\x02\x02\x88')
        buf.write('Ï\x058\x1d\x02\x89\x8b\x05\x06\x04\x02\x8a\x89\x03\x02\x02\x02')
        buf.write('\x8a\x8b\x03\x02\x02\x02\x8b\x8d\x03\x02\x02\x02\x8c\x8e\t')
        buf.write('\x02\x02\x02\x8d\x8c\x03\x02\x02\x02\x8d\x8e\x03\x02\x02\x02\x8e\x8f')
        buf.write('\x03\x02\x02\x02\x8f\x91\x05\x10\t\x02\x90\x92\t\x02\x02\x02\x91')
        buf.write('\x90\x03\x02\x02\x02\x91\x92\x03\x02\x02\x02\x92\x93\x03\x02\x02\x02')
        buf.write('\x93\x95\x07\x07\x02\x02\x94\x96\t\x02\x02\x02\x95\x94\x03')
        buf.write('\x02\x02\x02\x95\x96\x03\x02\x02\x02\x96\x97\x03\x02\x02\x02\x97\x98')
        buf.write('\x07\x17\x02\x02\x98\x99\x05\x18\r\x02\x99\x9a\x07\x18\x02\x02\x9a')
        buf.write('Ï\x03\x02\x02\x02\x9b\x9d\x05\x06\x04\x02\x9c\x9b\x03\x02\x02\x02')
        buf.write('\x9c\x9d\x03\x02\x02\x02\x9d\x9f\x03\x02\x02\x02\x9e\xa0\t')
        buf.write('\x02\x02\x02\x9f\x9e\x03\x02\x02\x02\x9f\xa0\x03\x02\x02\x02\xa0¡')
        buf.write('\x03\x02\x02\x02¡£\x05\x10\t\x02¢¤\t\x02\x02\x02£')
        buf.write('¢\x03\x02\x02\x02£¤\x03\x02\x02\x02¤¥\x03\x02\x02\x02')
        buf.write('¥§\x07\x07\x02\x02¦¨\t\x02\x02\x02§¦\x03')
        buf.write('\x02\x02\x02§¨\x03\x02\x02\x02¨©\x03\x02\x02\x02©ª')
        buf.write('\x07\x17\x02\x02ª«\x05\x1c\x0f\x02«¬\x07\x18\x02\x02¬')
        buf.write('Ï\x03\x02\x02\x02\xad¯\x05\x06\x04\x02®\xad\x03\x02\x02\x02')
        buf.write('®¯\x03\x02\x02\x02¯±\x03\x02\x02\x02°²\t')
        buf.write('\x02\x02\x02±°\x03\x02\x02\x02±²\x03\x02\x02\x02²³')
        buf.write('\x03\x02\x02\x02³µ\x05\x10\t\x02´¶\t\x02\x02\x02µ')
        buf.write('´\x03\x02\x02\x02µ¶\x03\x02\x02\x02¶·\x03\x02\x02\x02')
        buf.write('·¹\x07\x07\x02\x02¸º\t\x02\x02\x02¹¸\x03')
        buf.write('\x02\x02\x02¹º\x03\x02\x02\x02º»\x03\x02\x02\x02»¼')
        buf.write('\x05(\x15\x02¼Ï\x03\x02\x02\x02½¿\x05\x06\x04\x02¾')
        buf.write('½\x03\x02\x02\x02¾¿\x03\x02\x02\x02¿Á\x03\x02\x02\x02')
        buf.write('ÀÂ\t\x02\x02\x02ÁÀ\x03\x02\x02\x02ÁÂ\x03')
        buf.write('\x02\x02\x02ÂÃ\x03\x02\x02\x02ÃÌ\x05\x1e\x10\x02Ä')
        buf.write('Æ\t\x02\x02\x02ÅÄ\x03\x02\x02\x02ÅÆ\x03\x02\x02\x02')
        buf.write('ÆÇ\x03\x02\x02\x02ÇÉ\x07\x07\x02\x02ÈÊ\t')
        buf.write('\x02\x02\x02ÉÈ\x03\x02\x02\x02ÉÊ\x03\x02\x02\x02ÊË')
        buf.write('\x03\x02\x02\x02ËÍ\x058\x1d\x02ÌÅ\x03\x02\x02\x02Ì')
        buf.write('Í\x03\x02\x02\x02ÍÏ\x03\x02\x02\x02Îo\x03\x02\x02\x02Î')
        buf.write('q\x03\x02\x02\x02Îu\x03\x02\x02\x02Îy\x03\x02\x02\x02Î}\x03\x02\x02\x02')
        buf.write('Î\x8a\x03\x02\x02\x02Î\x9c\x03\x02\x02\x02Î®\x03')
        buf.write('\x02\x02\x02Î¾\x03\x02\x02\x02Ï\x05\x03\x02\x02\x02ÐÙ')
        buf.write('\x07\x0c\x02\x02ÑÕ\x07\x0b\x02\x02ÒÔ\x07\x0b\x02\x02Ó')
        buf.write('Ò\x03\x02\x02\x02Ô×\x03\x02\x02\x02ÕÓ\x03\x02\x02\x02')
        buf.write('ÕÖ\x03\x02\x02\x02ÖÙ\x03\x02\x02\x02×Õ\x03')
        buf.write('\x02\x02\x02ØÐ\x03\x02\x02\x02ØÑ\x03\x02\x02\x02Ù\x07')
        buf.write('\x03\x02\x02\x02ÚÛ\x07\r\x02\x02Ûô\x05\x10\t\x02Ü')
        buf.write('Ý\x07\r\x02\x02Ýß\x05\x10\t\x02Þà\t\x02\x02')
        buf.write('\x02ßÞ\x03\x02\x02\x02ßà\x03\x02\x02\x02àá')
        buf.write('\x03\x02\x02\x02áæ\x07C\x02\x02âã\x07"\x02\x02ã')
        buf.write('å\x07C\x02\x02äâ\x03\x02\x02\x02åè\x03\x02\x02\x02')
        buf.write('æä\x03\x02\x02\x02æç\x03\x02\x02\x02çñ\x03')
        buf.write('\x02\x02\x02èæ\x03\x02\x02\x02éë\t\x02\x02\x02êé')
        buf.write('\x03\x02\x02\x02êë\x03\x02\x02\x02ëì\x03\x02\x02\x02ì')
        buf.write('î\x07\x1e\x02\x02íï\t\x02\x02\x02îí\x03\x02\x02')
        buf.write('\x02îï\x03\x02\x02\x02ïð\x03\x02\x02\x02ðò')
        buf.write('\x07C\x02\x02ñê\x03\x02\x02\x02ñò\x03\x02\x02\x02ò')
        buf.write('ô\x03\x02\x02\x02óÚ\x03\x02\x02\x02óÜ\x03\x02\x02\x02')
        buf.write('ô\t\x03\x02\x02\x02õö\x07\x0f\x02\x02öû\x07C\x02')
        buf.write('\x02÷ø\x07"\x02\x02øú\x07C\x02\x02ù÷')
        buf.write('\x03\x02\x02\x02úý\x03\x02\x02\x02ûù\x03\x02\x02\x02û')
        buf.write('ü\x03\x02\x02\x02üþ\x03\x02\x02\x02ýû\x03\x02\x02\x02')
        buf.write('þÿ\x07"\x02\x02ÿĖ\x07/\x02\x02Āā\x07')
        buf.write('\x0f\x02\x02āĆ\x07C\x02\x02Ăă\x07"\x02\x02ăą')
        buf.write('\x07C\x02\x02ĄĂ\x03\x02\x02\x02ąĈ\x03\x02\x02\x02Ć')
        buf.write('Ą\x03\x02\x02\x02Ćć\x03\x02\x02\x02ćĉ\x03\x02\x02\x02')
        buf.write('ĈĆ\x03\x02\x02\x02ĉĊ\x07"\x02\x02Ċē\x05')
        buf.write('\x10\t\x02ċč\t\x02\x02\x02Čċ\x03\x02\x02\x02Č')
        buf.write('č\x03\x02\x02\x02čĎ\x03\x02\x02\x02ĎĐ\x07\x1e\x02')
        buf.write('\x02ďđ\t\x02\x02\x02Đď\x03\x02\x02\x02Đđ')
        buf.write('\x03\x02\x02\x02đĒ\x03\x02\x02\x02ĒĔ\x07C\x02\x02ē')
        buf.write('Č\x03\x02\x02\x02ēĔ\x03\x02\x02\x02ĔĖ\x03\x02\x02\x02')
        buf.write('ĕõ\x03\x02\x02\x02ĕĀ\x03\x02\x02\x02Ė\x0b\x03\x02')
        buf.write('\x02\x02ėĘ\x07\x11\x02\x02Ęę\x05\x10\t\x02ę\r')
        buf.write('\x03\x02\x02\x02Ěě\x07\x14\x02\x02ěĝ\x05\x10\t\x02Ĝ')
        buf.write('Ğ\x07\x15\x02\x02ĝĜ\x03\x02\x02\x02ĝĞ\x03\x02\x02')
        buf.write('\x02Ğğ\x03\x02\x02\x02ğĠ\x07!\x02\x02Ġ\x0f\x03\x02')
        buf.write('\x02\x02ġģ\x07C\x02\x02ĢĤ\x05 \x11\x02ģĢ')
        buf.write('\x03\x02\x02\x02ģĤ\x03\x02\x02\x02ĤĪ\x03\x02\x02\x02ĥ')
        buf.write('Ħ\x07\x1b\x02\x02Ħħ\x05\x10\t\x02ħĨ\x07\x1c')
        buf.write('\x02\x02ĨĪ\x03\x02\x02\x02ĩġ\x03\x02\x02\x02ĩĥ')
        buf.write('\x03\x02\x02\x02Ī\x11\x03\x02\x02\x02īĬ\x08\n\x01\x02Ĭİ')
        buf.write('\x07C\x02\x02ĭİ\x07\x12\x02\x02Įİ\x07\x13\x02\x02į')
        buf.write('ī\x03\x02\x02\x02įĭ\x03\x02\x02\x02įĮ\x03\x02\x02\x02')
        buf.write('İĶ\x03\x02\x02\x02ıĲ\x0c\x03\x02\x02Ĳĳ\x07')
        buf.write('"\x02\x02ĳĵ\t\x03\x02\x02Ĵı\x03\x02\x02\x02ĵĸ')
        buf.write('\x03\x02\x02\x02ĶĴ\x03\x02\x02\x02Ķķ\x03\x02\x02\x02ķ')
        buf.write('\x13\x03\x02\x02\x02ĸĶ\x03\x02\x02\x02ĹĻ\t\x02\x02\x02ĺ')
        buf.write('Ĺ\x03\x02\x02\x02ĺĻ\x03\x02\x02\x02Ļļ\x03\x02\x02\x02')
        buf.write('ļľ\x07\x1f\x02\x02ĽĿ\t\x02\x02\x02ľĽ')
        buf.write('\x03\x02\x02\x02ľĿ\x03\x02\x02\x02Ŀŀ\x03\x02\x02\x02ŀ')
        buf.write('Ł\x07\x13\x02\x02Ł\x15\x03\x02\x02\x02łń\x05\x12\n\x02')
        buf.write('ŃŅ\t\x02\x02\x02ńŃ\x03\x02\x02\x02ńŅ\x03')
        buf.write('\x02\x02\x02Ņņ\x03\x02\x02\x02ņň\x07\x1f\x02\x02Ň')
        buf.write('ŉ\t\x02\x02\x02ňŇ\x03\x02\x02\x02ňŉ\x03\x02\x02\x02')
        buf.write('ŉŊ\x03\x02\x02\x02ŊŌ\x05\x10\t\x02ŋō')
        buf.write('\x05\x14\x0b\x02Ōŋ\x03\x02\x02\x02Ōō\x03\x02\x02\x02ō')
        buf.write('\x17\x03\x02\x02\x02Ŏř\x05\x16\x0c\x02ŏő\t\x02\x02\x02Ő')
        buf.write('ŏ\x03\x02\x02\x02Őő\x03\x02\x02\x02őŒ\x03\x02\x02\x02')
        buf.write('ŒŔ\x07!\x02\x02œŕ\t\x02\x02\x02Ŕœ\x03')
        buf.write('\x02\x02\x02Ŕŕ\x03\x02\x02\x02ŕŖ\x03\x02\x02\x02ŖŘ')
        buf.write('\x05\x16\x0c\x02ŗŐ\x03\x02\x02\x02Řś\x03\x02\x02\x02ř')
        buf.write('ŗ\x03\x02\x02\x02řŚ\x03\x02\x02\x02Ś\x19\x03\x02\x02\x02ś')
        buf.write('ř\x03\x02\x02\x02ŜŞ\x05\x12\n\x02ŝş\t\x02\x02')
        buf.write('\x02Şŝ\x03\x02\x02\x02Şş\x03\x02\x02\x02şŠ')
        buf.write('\x03\x02\x02\x02ŠŢ\x07\x03\x02\x02šţ\t\x02\x02\x02Ţ')
        buf.write('š\x03\x02\x02\x02Ţţ\x03\x02\x02\x02ţŤ\x03\x02\x02\x02')
        buf.write('Ťť\x05\x12\n\x02ť\x1b\x03\x02\x02\x02Ŧű\x05\x1a')
        buf.write('\x0e\x02ŧũ\t\x02\x02\x02Ũŧ\x03\x02\x02\x02Ũũ')
        buf.write('\x03\x02\x02\x02ũŪ\x03\x02\x02\x02ŪŬ\x07!\x02\x02ū')
        buf.write('ŭ\t\x02\x02\x02Ŭū\x03\x02\x02\x02Ŭŭ\x03\x02\x02\x02')
        buf.write('ŭŮ\x03\x02\x02\x02ŮŰ\x05\x1a\x0e\x02ůŨ')
        buf.write('\x03\x02\x02\x02Űų\x03\x02\x02\x02űů\x03\x02\x02\x02ű')
        buf.write('Ų\x03\x02\x02\x02Ų\x1d\x03\x02\x02\x02ųű\x03\x02\x02\x02Ŵ')
        buf.write('Ź\x05\x10\t\x02ŵŶ\x07\x17\x02\x02Ŷŷ\x05\x18')
        buf.write('\r\x02ŷŸ\x07\x18\x02\x02Ÿź\x03\x02\x02\x02Źŵ')
        buf.write('\x03\x02\x02\x02Źź\x03\x02\x02\x02źƃ\x03\x02\x02\x02Ż')
        buf.write('Ž\t\x02\x02\x02żŻ\x03\x02\x02\x02żŽ\x03\x02\x02\x02')
        buf.write('Žž\x03\x02\x02\x02žƀ\x07\x1f\x02\x02ſƁ')
        buf.write('\t\x02\x02\x02ƀſ\x03\x02\x02\x02ƀƁ\x03\x02\x02\x02Ɓ')
        buf.write('Ƃ\x03\x02\x02\x02ƂƄ\x05\x10\t\x02ƃż\x03\x02\x02')
        buf.write('\x02ƃƄ\x03\x02\x02\x02Ƅ\x1f\x03\x02\x02\x02ƅƆ\t')
        buf.write('\x04\x02\x02Ɔ!\x03\x02\x02\x02ƇƉ\x07\x06\x02\x02ƈƊ')
        buf.write('\x05\x12\n\x02Ɖƈ\x03\x02\x02\x02ƉƊ\x03\x02\x02\x02Ɗ')
        buf.write('ư\x03\x02\x02\x02Ƌƌ\x07\x06\x02\x02ƌƍ\x07\x19\x02')
        buf.write('\x02ƍƘ\x05\x12\n\x02ƎƐ\x07\x15\x02\x02ƏƎ')
        buf.write('\x03\x02\x02\x02ƏƐ\x03\x02\x02\x02ƐƑ\x03\x02\x02\x02Ƒ')
        buf.write('Ɠ\x07!\x02\x02ƒƔ\x07\x15\x02\x02Ɠƒ\x03\x02\x02\x02')
        buf.write('ƓƔ\x03\x02\x02\x02Ɣƕ\x03\x02\x02\x02ƕƗ\x05')
        buf.write('\x12\n\x02ƖƏ\x03\x02\x02\x02Ɨƚ\x03\x02\x02\x02Ƙ')
        buf.write('Ɩ\x03\x02\x02\x02Ƙƙ\x03\x02\x02\x02ƙƛ\x03\x02\x02\x02')
        buf.write('ƚƘ\x03\x02\x02\x02ƛƜ\x07\x1a\x02\x02Ɯư')
        buf.write('\x03\x02\x02\x02Ɲƞ\x07\x06\x02\x02ƞƟ\x07\x17\x02\x02Ɵ')
        buf.write('ƪ\x05\x12\n\x02ƠƢ\x07\x15\x02\x02ơƠ\x03\x02\x02')
        buf.write('\x02ơƢ\x03\x02\x02\x02Ƣƣ\x03\x02\x02\x02ƣƥ')
        buf.write('\x07!\x02\x02ƤƦ\x07\x15\x02\x02ƥƤ\x03\x02\x02\x02ƥ')
        buf.write('Ʀ\x03\x02\x02\x02ƦƧ\x03\x02\x02\x02ƧƩ\x05\x12\n')
        buf.write('\x02ƨơ\x03\x02\x02\x02ƩƬ\x03\x02\x02\x02ƪƨ')
        buf.write('\x03\x02\x02\x02ƪƫ\x03\x02\x02\x02ƫƭ\x03\x02\x02\x02Ƭ')
        buf.write('ƪ\x03\x02\x02\x02ƭƮ\x07\x18\x02\x02Ʈư\x03\x02\x02')
        buf.write('\x02ƯƇ\x03\x02\x02\x02ƯƋ\x03\x02\x02\x02ƯƝ')
        buf.write('\x03\x02\x02\x02ư#\x03\x02\x02\x02Ʊǌ\x05:\x1e\x02Ʋǌ')
        buf.write('\x05<\x1f\x02Ƴǌ\x05> \x02ƴǌ\x05@!\x02Ƶǌ')
        buf.write('\x05B"\x02ƶǌ\x05D#\x02Ʒǌ\x05F$\x02Ƹǌ')
        buf.write('\x05H%\x02ƹǌ\x05J&\x02ƺƻ\x07\x1b\x02\x02ƻǆ')
        buf.write('\x05$\x13\x02Ƽƾ\x07\x15\x02\x02ƽƼ\x03\x02\x02\x02ƽ')
        buf.write('ƾ\x03\x02\x02\x02ƾƿ\x03\x02\x02\x02ƿǁ\x07!\x02\x02')
        buf.write('ǀǂ\x07\x15\x02\x02ǁǀ\x03\x02\x02\x02ǁǂ')
        buf.write('\x03\x02\x02\x02ǂǃ\x03\x02\x02\x02ǃǅ\x05$\x13\x02Ǆ')
        buf.write('ƽ\x03\x02\x02\x02ǅǈ\x03\x02\x02\x02ǆǄ\x03\x02\x02\x02')
        buf.write('ǆǇ\x03\x02\x02\x02Ǉǉ\x03\x02\x02\x02ǈǆ\x03')
        buf.write('\x02\x02\x02ǉǊ\x07\x1c\x02\x02Ǌǌ\x03\x02\x02\x02ǋ')
        buf.write('Ʊ\x03\x02\x02\x02ǋƲ\x03\x02\x02\x02ǋƳ\x03\x02\x02\x02')
        buf.write('ǋƴ\x03\x02\x02\x02ǋƵ\x03\x02\x02\x02ǋƶ\x03')
        buf.write('\x02\x02\x02ǋƷ\x03\x02\x02\x02ǋƸ\x03\x02\x02\x02ǋƹ')
        buf.write('\x03\x02\x02\x02ǋƺ\x03\x02\x02\x02ǌ%\x03\x02\x02\x02ǍǏ')
        buf.write('\n\x05\x02\x02ǎǍ\x03\x02\x02\x02Ǐǒ\x03\x02\x02\x02ǐ')
        buf.write("ǎ\x03\x02\x02\x02ǐǑ\x03\x02\x02\x02Ǒ'\x03\x02\x02\x02ǒ")
        buf.write('ǐ\x03\x02\x02\x02Ǔǔ\x07A\x02\x02ǔǕ\x05&\x14\x02')
        buf.write('Ǖǖ\x07B\x02\x02ǖ)\x03\x02\x02\x02Ǘǯ\x052\x1a')
        buf.write('\x02ǘǯ\x05"\x12\x02Ǚǚ\x05\x12\n\x02ǚǛ')
        buf.write('\x05"\x12\x02Ǜǯ\x03\x02\x02\x02ǜǞ\x05\x12\n\x02ǝ')
        buf.write('ǟ\t\x02\x02\x02Ǟǝ\x03\x02\x02\x02Ǟǟ\x03\x02\x02\x02')
        buf.write('ǟǠ\x03\x02\x02\x02ǠǢ\x07\x1e\x02\x02ǡǣ')
        buf.write('\t\x02\x02\x02Ǣǡ\x03\x02\x02\x02Ǣǣ\x03\x02\x02\x02ǣ')
        buf.write('Ǥ\x03\x02\x02\x02ǤǦ\x052\x1a\x02ǥǧ\x05"\x12')
        buf.write('\x02Ǧǥ\x03\x02\x02\x02Ǧǧ\x03\x02\x02\x02ǧǯ')
        buf.write('\x03\x02\x02\x02Ǩǩ\x05\x12\n\x02ǩǪ\x05T+\x02Ǫ')
        buf.write('Ǭ\x052\x1a\x02ǫǭ\x05"\x12\x02Ǭǫ\x03\x02')
        buf.write('\x02\x02Ǭǭ\x03\x02\x02\x02ǭǯ\x03\x02\x02\x02ǮǗ')
        buf.write('\x03\x02\x02\x02Ǯǘ\x03\x02\x02\x02ǮǙ\x03\x02\x02\x02Ǯ')
        buf.write('ǜ\x03\x02\x02\x02ǮǨ\x03\x02\x02\x02ǯ+\x03\x02\x02\x02ǰ')
        buf.write('Ǳ\x07\x17\x02\x02ǱȄ\x07\x18\x02\x02ǲǳ\x07\x17')
        buf.write('\x02\x02ǳǾ\x05*\x16\x02ǴǶ\t\x02\x02\x02ǵǴ')
        buf.write('\x03\x02\x02\x02ǵǶ\x03\x02\x02\x02ǶǷ\x03\x02\x02\x02Ƿ')
        buf.write('ǹ\x07!\x02\x02ǸǺ\t\x02\x02\x02ǹǸ\x03\x02\x02\x02')
        buf.write('ǹǺ\x03\x02\x02\x02Ǻǻ\x03\x02\x02\x02ǻǽ\x05')
        buf.write('*\x16\x02Ǽǵ\x03\x02\x02\x02ǽȀ\x03\x02\x02\x02ǾǼ')
        buf.write('\x03\x02\x02\x02Ǿǿ\x03\x02\x02\x02ǿȁ\x03\x02\x02\x02Ȁ')
        buf.write('Ǿ\x03\x02\x02\x02ȁȂ\x07\x18\x02\x02ȂȄ\x03\x02\x02')
        buf.write('\x02ȃǰ\x03\x02\x02\x02ȃǲ\x03\x02\x02\x02Ȅ-\x03\x02')
        buf.write('\x02\x02ȅȆ\x08\x18\x01\x02ȆȘ\x05$\x13\x02ȇȉ')
        buf.write('\x05\x12\n\x02ȈȊ\x07\x15\x02\x02ȉȈ\x03\x02\x02\x02ȉ')
        buf.write('Ȋ\x03\x02\x02\x02ȊȌ\x03\x02\x02\x02ȋȍ\x05"\x12')
        buf.write('\x02Ȍȋ\x03\x02\x02\x02Ȍȍ\x03\x02\x02\x02ȍȘ')
        buf.write('\x03\x02\x02\x02ȎȘ\x05,\x17\x02ȏȐ\x05\x12\n\x02Ȑ')
        buf.write('Ȓ\x05,\x17\x02ȑȓ\x07\x15\x02\x02Ȓȑ\x03\x02\x02')
        buf.write('\x02Ȓȓ\x03\x02\x02\x02ȓȕ\x03\x02\x02\x02ȔȖ')
        buf.write('\x05"\x12\x02ȕȔ\x03\x02\x02\x02ȕȖ\x03\x02\x02\x02Ȗ')
        buf.write('Ș\x03\x02\x02\x02ȗȅ\x03\x02\x02\x02ȗȇ\x03\x02\x02\x02')
        buf.write('ȗȎ\x03\x02\x02\x02ȗȏ\x03\x02\x02\x02ȘȤ\x03')
        buf.write('\x02\x02\x02șț\x0c\x03\x02\x02ȚȜ\t\x02\x02\x02țȚ')
        buf.write('\x03\x02\x02\x02țȜ\x03\x02\x02\x02Ȝȝ\x03\x02\x02\x02ȝ')
        buf.write('ȟ\x07"\x02\x02ȞȠ\t\x02\x02\x02ȟȞ\x03\x02\x02\x02')
        buf.write('ȟȠ\x03\x02\x02\x02Ƞȡ\x03\x02\x02\x02ȡȣ\x05')
        buf.write('.\x18\x04Ȣș\x03\x02\x02\x02ȣȦ\x03\x02\x02\x02ȤȢ')
        buf.write('\x03\x02\x02\x02Ȥȥ\x03\x02\x02\x02ȥ/\x03\x02\x02\x02ȦȤ')
        buf.write('\x03\x02\x02\x02ȧɁ\x05.\x18\x02Ȩȩ\x05.\x18\x02ȩ')
        buf.write('ȫ\x07\x1b\x02\x02ȪȬ\x05> \x02ȫȪ\x03\x02\x02\x02')
        buf.write('ȫȬ\x03\x02\x02\x02ȬȮ\x03\x02\x02\x02ȭȯ\t')
        buf.write('\x02\x02\x02Ȯȭ\x03\x02\x02\x02Ȯȯ\x03\x02\x02\x02ȯȱ')
        buf.write('\x03\x02\x02\x02ȰȲ\x07\x1f\x02\x02ȱȰ\x03\x02\x02\x02ȱ')
        buf.write('Ȳ\x03\x02\x02\x02Ȳȴ\x03\x02\x02\x02ȳȵ\t\x02\x02\x02')
        buf.write('ȴȳ\x03\x02\x02\x02ȴȵ\x03\x02\x02\x02ȵȷ\x03')
        buf.write('\x02\x02\x02ȶȸ\x05> \x02ȷȶ\x03\x02\x02\x02ȷȸ')
        buf.write('\x03\x02\x02\x02ȸȹ\x03\x02\x02\x02ȹȺ\x07\x1c\x02\x02Ⱥ')
        buf.write('Ɂ\x03\x02\x02\x02Ȼȼ\x05.\x18\x02ȼȽ\x07\x1b\x02')
        buf.write('\x02ȽȾ\x05.\x18\x02Ⱦȿ\x07\x1c\x02\x02ȿɁ')
        buf.write('\x03\x02\x02\x02ɀȧ\x03\x02\x02\x02ɀȨ\x03\x02\x02\x02ɀ')
        buf.write('Ȼ\x03\x02\x02\x02Ɂ1\x03\x02\x02\x02ɂɃ\x08\x1a\x01\x02Ƀ')
        buf.write('ɋ\x050\x19\x02ɄɅ\x07\x17\x02\x02ɅɆ\x052')
        buf.write('\x1a\x02Ɇɇ\x07\x18\x02\x02ɇɋ\x03\x02\x02\x02Ɉɉ')
        buf.write('\x07-\x02\x02ɉɋ\x052\x1a\x06Ɋɂ\x03\x02\x02\x02Ɋ')
        buf.write('Ʉ\x03\x02\x02\x02ɊɈ\x03\x02\x02\x02ɋɩ\x03\x02\x02\x02')
        buf.write('ɌɎ\x0c\x05\x02\x02ɍɏ\t\x02\x02\x02Ɏɍ\x03')
        buf.write('\x02\x02\x02Ɏɏ\x03\x02\x02\x02ɏɐ\x03\x02\x02\x02ɐɒ')
        buf.write('\t\x06\x02\x02ɑɓ\t\x02\x02\x02ɒɑ\x03\x02\x02\x02ɒ')
        buf.write('ɓ\x03\x02\x02\x02ɓɔ\x03\x02\x02\x02ɔɨ\x052\x1a')
        buf.write('\x06ɕɗ\x0c\x04\x02\x02ɖɘ\t\x02\x02\x02ɗɖ')
        buf.write('\x03\x02\x02\x02ɗɘ\x03\x02\x02\x02ɘə\x03\x02\x02\x02ə')
        buf.write('ɛ\t\x07\x02\x02ɚɜ\t\x02\x02\x02ɛɚ\x03\x02\x02\x02')
        buf.write('ɛɜ\x03\x02\x02\x02ɜɝ\x03\x02\x02\x02ɝɨ\x05')
        buf.write('2\x1a\x05ɞɠ\x0c\x03\x02\x02ɟɡ\t\x02\x02\x02ɠ')
        buf.write('ɟ\x03\x02\x02\x02ɠɡ\x03\x02\x02\x02ɡɢ\x03\x02\x02\x02')
        buf.write('ɢɤ\t\x08\x02\x02ɣɥ\t\x02\x02\x02ɤɣ\x03')
        buf.write('\x02\x02\x02ɤɥ\x03\x02\x02\x02ɥɦ\x03\x02\x02\x02ɦɨ')
        buf.write('\x052\x1a\x04ɧɌ\x03\x02\x02\x02ɧɕ\x03\x02\x02\x02ɧ')
        buf.write('ɞ\x03\x02\x02\x02ɨɫ\x03\x02\x02\x02ɩɧ\x03\x02\x02\x02')
        buf.write('ɩɪ\x03\x02\x02\x02ɪ3\x03\x02\x02\x02ɫɩ\x03\x02')
        buf.write('\x02\x02ɬɲ\x052\x1a\x02ɭɮ\x052\x1a\x02ɮ')
        buf.write('ɯ\x05T+\x02ɯɰ\x052\x1a\x02ɰɲ\x03\x02\x02\x02')
        buf.write('ɱɬ\x03\x02\x02\x02ɱɭ\x03\x02\x02\x02ɲ5\x03\x02')
        buf.write('\x02\x02ɳɴ\x08\x1c\x01\x02ɴɶ\x054\x1b\x02ɵ')
        buf.write('ɷ\x07\x15\x02\x02ɶɵ\x03\x02\x02\x02ɶɷ\x03\x02\x02')
        buf.write('\x02ɷɹ\x03\x02\x02\x02ɸɺ\x05"\x12\x02ɹɸ')
        buf.write('\x03\x02\x02\x02ɹɺ\x03\x02\x02\x02ɺʁ\x03\x02\x02\x02ɻ')
        buf.write('ɽ\x073\x02\x02ɼɾ\x07\x15\x02\x02ɽɼ\x03\x02\x02')
        buf.write('\x02ɽɾ\x03\x02\x02\x02ɾɿ\x03\x02\x02\x02ɿʁ')
        buf.write('\x056\x1c\x04ʀɳ\x03\x02\x02\x02ʀɻ\x03\x02\x02\x02ʁ')
        buf.write('ʈ\x03\x02\x02\x02ʂʃ\x0c\x03\x02\x02ʃʄ\x05N(\x02ʄ')
        buf.write('ʅ\x056\x1c\x04ʅʇ\x03\x02\x02\x02ʆʂ\x03\x02\x02')
        buf.write('\x02ʇʊ\x03\x02\x02\x02ʈʆ\x03\x02\x02\x02ʈʉ')
        buf.write('\x03\x02\x02\x02ʉ7\x03\x02\x02\x02ʊʈ\x03\x02\x02\x02ʋʑ')
        buf.write('\x056\x1c\x02ʌʍ\x056\x1c\x02ʍʎ\x05P)\x02ʎ')
        buf.write('ʏ\x058\x1d\x02ʏʑ\x03\x02\x02\x02ʐʋ\x03\x02\x02\x02')
        buf.write('ʐʌ\x03\x02\x02\x02ʑ9\x03\x02\x02\x02ʒʓ\x07\x1d\x02')
        buf.write('\x02ʓ;\x03\x02\x02\x02ʔʕ\x079\x02\x02ʕ=\x03\x02\x02\x02ʖ')
        buf.write('ʗ\x07:\x02\x02ʗ?\x03\x02\x02\x02ʘʙ\x07;\x02\x02ʙ')
        buf.write('A\x03\x02\x02\x02ʚʛ\x07<\x02\x02ʛC\x03\x02\x02\x02ʜʝ')
        buf.write('\x07=\x02\x02ʝE\x03\x02\x02\x02ʞʟ\x07>\x02\x02ʟG\x03\x02\x02')
        buf.write('\x02ʠʡ\x07?\x02\x02ʡI\x03\x02\x02\x02ʢʣ\x07@\x02')
        buf.write('\x02ʣK\x03\x02\x02\x02ʤʥ\t\t\x02\x02ʥM\x03\x02\x02\x02ʦ')
        buf.write('ʨ\x07\x15\x02\x02ʧʦ\x03\x02\x02\x02ʧʨ\x03\x02\x02')
        buf.write("\x02ʨʩ\x03\x02\x02\x02ʩʫ\x05L'\x02ʪʬ")
        buf.write('\x07\x15\x02\x02ʫʪ\x03\x02\x02\x02ʫʬ\x03\x02\x02\x02ʬ')
        buf.write("O\x03\x02\x02\x02ʭʮ\x07\x16\x02\x02ʮʰ\x05L'\x02ʯ")
        buf.write('ʱ\x07\x15\x02\x02ʰʯ\x03\x02\x02\x02ʰʱ\x03\x02\x02')
        buf.write('\x02ʱQ\x03\x02\x02\x02ʲʳ\t\n\x02\x02ʳS\x03\x02\x02\x02ʴ')
        buf.write('ʶ\t\x02\x02\x02ʵʴ\x03\x02\x02\x02ʵʶ\x03\x02\x02\x02')
        buf.write('ʶʷ\x03\x02\x02\x02ʷʹ\x05R*\x02ʸʺ\t\x02')
        buf.write('\x02\x02ʹʸ\x03\x02\x02\x02ʹʺ\x03\x02\x02\x02ʺU\x03')
        buf.write('\x02\x02\x02}X^cimquy}\x80\x83\x86\x8a\x8d\x91\x95')
        buf.write('\x9c\x9f£§®±µ¹¾')
        buf.write('ÁÅÉÌÎÕØßæ')
        buf.write('êîñóûĆČĐē')
        buf.write('ĕĝģĩįĶĺľń')
        buf.write('ňŌŐŔřŞŢŨŬ')
        buf.write('űŹżƀƃƉƏƓƘ')
        buf.write('ơƥƪƯƽǁǆǋǐ')
        buf.write('ǞǢǦǬǮǵǹǾȃ')
        buf.write('ȉȌȒȕȗțȟȤȫ')
        buf.write('ȮȱȴȷɀɊɎɒɗ')
        buf.write('ɛɠɤɧɩɱɶɹɽ')
        buf.write('ʀʈʐʧʫʰʵʹ')
        return buf.getvalue()


class normParser(Parser):
    grammarFileName = 'norm.g4'
    atn = ATNDeserializer().deserialize(serializedATN())
    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]
    sharedContextCache = PredictionContextCache()
    literalNames = [
     '<INVALID>', "'->'", "'$latest'", "'$best'", "'?'",
     '<INVALID>', "':='", "'|='", "'&='", '<INVALID>', '<INVALID>',
     '<INVALID>', '<INVALID>', '<INVALID>', '<INVALID>',
     '<INVALID>', '<INVALID>', '<INVALID>', '<INVALID>',
     '<INVALID>', '<INVALID>', '<INVALID>', '<INVALID>',
     '<INVALID>', '<INVALID>', '<INVALID>', '<INVALID>',
     '<INVALID>', '<INVALID>', "':'", "';'", "','", "'.'",
     "'..'", '<INVALID>', '<INVALID>', "'=='", "'!='", "'>='",
     "'<='", "'>'", "'<'", "'~'", "'-'", "'+'", "'*'", "'/'",
     "'**'", "'%'"]
    symbolicNames = [
     '<INVALID>', '<INVALID>', '<INVALID>', '<INVALID>',
     '<INVALID>', 'IMPL', 'CEQ', 'OEQ', 'AEQ', 'SINGLELINE',
     'MULTILINE', 'SPACED_EXPORT', 'EXPORT', 'SPACED_IMPORT',
     'IMPORT', 'SPACED_COMMAND', 'COMMAND', 'ARGOPT', 'SPACED_WITH',
     'WS', 'NS', 'LBR', 'RBR', 'LCBR', 'RCBR', 'LSBR',
     'RSBR', 'NONE', 'AS', 'COLON', 'SEMICOLON', 'COMMA',
     'DOT', 'DOTDOT', 'IN', 'NI', 'EQ', 'NE', 'GE', 'LE',
     'GT', 'LT', 'LK', 'MINUS', 'PLUS', 'TIMES', 'DIVIDE',
     'EXP', 'MOD', 'NOT', 'AND', 'OR', 'XOR', 'IMP', 'EQV',
     'BOOLEAN', 'INTEGER', 'FLOAT', 'STRING', 'PATTERN',
     'UUID', 'URL', 'DATETIME', 'PYTHON_BLOCK', 'BLOCK_END',
     'VARNAME']
    RULE_script = 0
    RULE_statement = 1
    RULE_comments = 2
    RULE_exports = 3
    RULE_imports = 4
    RULE_commands = 5
    RULE_context = 6
    RULE_typeName = 7
    RULE_variable = 8
    RULE_argumentProperty = 9
    RULE_argumentDeclaration = 10
    RULE_argumentDeclarations = 11
    RULE_rename = 12
    RULE_renames = 13
    RULE_typeDeclaration = 14
    RULE_version = 15
    RULE_queryProjection = 16
    RULE_constant = 17
    RULE_code = 18
    RULE_codeExpression = 19
    RULE_argumentExpression = 20
    RULE_argumentExpressions = 21
    RULE_evaluationExpression = 22
    RULE_slicedExpression = 23
    RULE_arithmeticExpression = 24
    RULE_conditionExpression = 25
    RULE_oneLineExpression = 26
    RULE_multiLineExpression = 27
    RULE_none = 28
    RULE_bool_c = 29
    RULE_integer_c = 30
    RULE_float_c = 31
    RULE_string_c = 32
    RULE_pattern = 33
    RULE_uuid = 34
    RULE_url = 35
    RULE_datetime = 36
    RULE_logicalOperator = 37
    RULE_spacedLogicalOperator = 38
    RULE_newlineLogicalOperator = 39
    RULE_conditionOperator = 40
    RULE_spacedConditionOperator = 41
    ruleNames = [
     'script', 'statement', 'comments', 'exports', 'imports',
     'commands', 'context', 'typeName', 'variable', 'argumentProperty',
     'argumentDeclaration', 'argumentDeclarations', 'rename',
     'renames', 'typeDeclaration', 'version', 'queryProjection',
     'constant', 'code', 'codeExpression', 'argumentExpression',
     'argumentExpressions', 'evaluationExpression', 'slicedExpression',
     'arithmeticExpression', 'conditionExpression', 'oneLineExpression',
     'multiLineExpression', 'none', 'bool_c', 'integer_c',
     'float_c', 'string_c', 'pattern', 'uuid', 'url', 'datetime',
     'logicalOperator', 'spacedLogicalOperator', 'newlineLogicalOperator',
     'conditionOperator', 'spacedConditionOperator']
    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    IMPL = 5
    CEQ = 6
    OEQ = 7
    AEQ = 8
    SINGLELINE = 9
    MULTILINE = 10
    SPACED_EXPORT = 11
    EXPORT = 12
    SPACED_IMPORT = 13
    IMPORT = 14
    SPACED_COMMAND = 15
    COMMAND = 16
    ARGOPT = 17
    SPACED_WITH = 18
    WS = 19
    NS = 20
    LBR = 21
    RBR = 22
    LCBR = 23
    RCBR = 24
    LSBR = 25
    RSBR = 26
    NONE = 27
    AS = 28
    COLON = 29
    SEMICOLON = 30
    COMMA = 31
    DOT = 32
    DOTDOT = 33
    IN = 34
    NI = 35
    EQ = 36
    NE = 37
    GE = 38
    LE = 39
    GT = 40
    LT = 41
    LK = 42
    MINUS = 43
    PLUS = 44
    TIMES = 45
    DIVIDE = 46
    EXP = 47
    MOD = 48
    NOT = 49
    AND = 50
    OR = 51
    XOR = 52
    IMP = 53
    EQV = 54
    BOOLEAN = 55
    INTEGER = 56
    FLOAT = 57
    STRING = 58
    PATTERN = 59
    UUID = 60
    URL = 61
    DATETIME = 62
    PYTHON_BLOCK = 63
    BLOCK_END = 64
    VARNAME = 65

    def __init__(self, input, output=sys.stdout):
        super().__init__(input, output)
        self.checkVersion('4.7.2')
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class ScriptContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.StatementContext)
            return self.getTypedRuleContext(normParser.StatementContext, i)

        def SEMICOLON(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.SEMICOLON)
            return self.getToken(normParser.SEMICOLON, i)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_script

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterScript'):
                listener.enterScript(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitScript'):
                listener.exitScript(self)

    def script(self):
        localctx = normParser.ScriptContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_script)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 84
                self.statement()
                self.state = 86
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not _la == normParser.WS:
                    if _la == normParser.NS:
                        self.state = 85
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                    self.state = 88
                    self.match(normParser.SEMICOLON)
                    self.state = 103
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 3, self._ctx)
                    while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                        if _alt == 1:
                            self.state = 92
                            self._errHandler.sync(self)
                            _alt = self._interp.adaptivePredict(self._input, 1, self._ctx)
                            while _alt != 2:
                                if _alt != ATN.INVALID_ALT_NUMBER:
                                    if _alt == 1:
                                        self.state = 89
                                        _la = self._input.LA(1)
                                        if not _la == normParser.WS:
                                            if not _la == normParser.NS:
                                                self._errHandler.recoverInline(self)
                                else:
                                    self._errHandler.reportMatch(self)
                                    self.consume()
                                self.state = 94
                                self._errHandler.sync(self)
                                _alt = self._interp.adaptivePredict(self._input, 1, self._ctx)

                            self.state = 95
                            self.statement()
                            self.state = 97
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if _la == normParser.WS or _la == normParser.NS:
                                self.state = 96
                                _la = self._input.LA(1)
                                if not _la == normParser.WS:
                                    if not _la == normParser.NS:
                                        self._errHandler.recoverInline(self)
                            else:
                                self._errHandler.reportMatch(self)
                                self.consume()
                            self.state = 99
                            self.match(normParser.SEMICOLON)
                        self.state = 105
                        self._errHandler.sync(self)
                        _alt = self._interp.adaptivePredict(self._input, 3, self._ctx)

                    self.state = 107
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.WS or _la == normParser.NS:
                        self.state = 106
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class StatementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def comments(self):
            return self.getTypedRuleContext(normParser.CommentsContext, 0)

        def imports(self):
            return self.getTypedRuleContext(normParser.ImportsContext, 0)

        def exports(self):
            return self.getTypedRuleContext(normParser.ExportsContext, 0)

        def commands(self):
            return self.getTypedRuleContext(normParser.CommandsContext, 0)

        def multiLineExpression(self):
            return self.getTypedRuleContext(normParser.MultiLineExpressionContext, 0)

        def context(self):
            return self.getTypedRuleContext(normParser.ContextContext, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def typeName(self):
            return self.getTypedRuleContext(normParser.TypeNameContext, 0)

        def IMPL(self):
            return self.getToken(normParser.IMPL, 0)

        def LBR(self):
            return self.getToken(normParser.LBR, 0)

        def argumentDeclarations(self):
            return self.getTypedRuleContext(normParser.ArgumentDeclarationsContext, 0)

        def RBR(self):
            return self.getToken(normParser.RBR, 0)

        def renames(self):
            return self.getTypedRuleContext(normParser.RenamesContext, 0)

        def codeExpression(self):
            return self.getTypedRuleContext(normParser.CodeExpressionContext, 0)

        def typeDeclaration(self):
            return self.getTypedRuleContext(normParser.TypeDeclarationContext, 0)

        def getRuleIndex(self):
            return normParser.RULE_statement

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterStatement'):
                listener.enterStatement(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitStatement'):
                listener.exitStatement(self)

    def statement(self):
        localctx = normParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        self._la = 0
        try:
            try:
                self.state = 204
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 29, self._ctx)
                if la_ == 1:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 109
                    self.comments()
                elif la_ == 2:
                    self.enterOuterAlt(localctx, 2)
                    self.state = 111
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.SINGLELINE or _la == normParser.MULTILINE:
                        self.state = 110
                        self.comments()
                    self.state = 113
                    self.imports()
                elif la_ == 3:
                    self.enterOuterAlt(localctx, 3)
                    self.state = 115
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.SINGLELINE or _la == normParser.MULTILINE:
                        self.state = 114
                        self.comments()
                    self.state = 117
                    self.exports()
                elif la_ == 4:
                    self.enterOuterAlt(localctx, 4)
                    self.state = 119
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.SINGLELINE or _la == normParser.MULTILINE:
                        self.state = 118
                        self.comments()
                    self.state = 121
                    self.commands()
                else:
                    if la_ == 5:
                        self.enterOuterAlt(localctx, 5)
                        self.state = 123
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.SINGLELINE or _la == normParser.MULTILINE:
                            self.state = 122
                            self.comments()
                        self.state = 126
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input, 9, self._ctx)
                        if la_ == 1:
                            self.state = 125
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 129
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.SPACED_WITH:
                        self.state = 128
                        self.context()
                    self.state = 132
                    self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not _la == normParser.WS:
                    if _la == normParser.NS:
                        self.state = 131
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                    self.state = 134
                    self.multiLineExpression()
                elif la_ == 6:
                    self.enterOuterAlt(localctx, 6)
                    self.state = 136
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not _la == normParser.SINGLELINE:
                        if _la == normParser.MULTILINE:
                            self.state = 135
                            self.comments()
                        self.state = 139
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 138
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 141
                    self.typeName()
                    self.state = 143
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not _la == normParser.WS:
                        if _la == normParser.NS:
                            self.state = 142
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                            else:
                                self._errHandler.reportMatch(self)
                                self.consume()
                        self.state = 145
                        self.match(normParser.IMPL)
                        self.state = 147
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 146
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 149
                    self.match(normParser.LBR)
                    self.state = 150
                    self.argumentDeclarations()
                    self.state = 151
                    self.match(normParser.RBR)
                elif la_ == 7:
                    self.enterOuterAlt(localctx, 7)
                    self.state = 154
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not _la == normParser.SINGLELINE:
                        if _la == normParser.MULTILINE:
                            self.state = 153
                            self.comments()
                        self.state = 157
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 156
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 159
                    self.typeName()
                    self.state = 161
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not _la == normParser.WS:
                        if _la == normParser.NS:
                            self.state = 160
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                            else:
                                self._errHandler.reportMatch(self)
                                self.consume()
                        self.state = 163
                        self.match(normParser.IMPL)
                        self.state = 165
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 164
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 167
                    self.match(normParser.LBR)
                    self.state = 168
                    self.renames()
                    self.state = 169
                    self.match(normParser.RBR)
                elif la_ == 8:
                    self.enterOuterAlt(localctx, 8)
                    self.state = 172
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not _la == normParser.SINGLELINE:
                        if _la == normParser.MULTILINE:
                            self.state = 171
                            self.comments()
                        self.state = 175
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 174
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 177
                    self.typeName()
                    self.state = 179
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not _la == normParser.WS:
                        if _la == normParser.NS:
                            self.state = 178
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                            else:
                                self._errHandler.reportMatch(self)
                                self.consume()
                        self.state = 181
                        self.match(normParser.IMPL)
                        self.state = 183
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 182
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 185
                    self.codeExpression()
                else:
                    if la_ == 9:
                        self.enterOuterAlt(localctx, 9)
                        self.state = 188
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.SINGLELINE or _la == normParser.MULTILINE:
                            self.state = 187
                            self.comments()
                        self.state = 191
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 190
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 193
                    self.typeDeclaration()
                    self.state = 202
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 28, self._ctx)
                    if la_ == 1:
                        self.state = 195
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if _la == normParser.NS:
                                self.state = 194
                                _la = self._input.LA(1)
                                if not _la == normParser.WS:
                                    if not _la == normParser.NS:
                                        self._errHandler.recoverInline(self)
                                else:
                                    self._errHandler.reportMatch(self)
                                    self.consume()
                            self.state = 197
                            self.match(normParser.IMPL)
                            self.state = 199
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if _la == normParser.WS or _la == normParser.NS:
                                self.state = 198
                                _la = self._input.LA(1)
                                if not _la == normParser.WS:
                                    if not _la == normParser.NS:
                                        self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 201
                        self.multiLineExpression()
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class CommentsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MULTILINE(self):
            return self.getToken(normParser.MULTILINE, 0)

        def SINGLELINE(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.SINGLELINE)
            return self.getToken(normParser.SINGLELINE, i)

        def getRuleIndex(self):
            return normParser.RULE_comments

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterComments'):
                listener.enterComments(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitComments'):
                listener.exitComments(self)

    def comments(self):
        localctx = normParser.CommentsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_comments)
        self._la = 0
        try:
            try:
                self.state = 214
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [normParser.MULTILINE]:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 206
                    self.match(normParser.MULTILINE)
                elif token in [normParser.SINGLELINE]:
                    self.enterOuterAlt(localctx, 2)
                    self.state = 207
                    self.match(normParser.SINGLELINE)
                    self.state = 211
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la == normParser.SINGLELINE:
                        self.state = 208
                        self.match(normParser.SINGLELINE)
                        self.state = 213
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                else:
                    raise NoViableAltException(self)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class ExportsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SPACED_EXPORT(self):
            return self.getToken(normParser.SPACED_EXPORT, 0)

        def typeName(self):
            return self.getTypedRuleContext(normParser.TypeNameContext, 0)

        def VARNAME(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.VARNAME)
            return self.getToken(normParser.VARNAME, i)

        def DOT(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.DOT)
            return self.getToken(normParser.DOT, i)

        def AS(self):
            return self.getToken(normParser.AS, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_exports

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterExports'):
                listener.enterExports(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitExports'):
                listener.exitExports(self)

    def exports(self):
        localctx = normParser.ExportsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_exports)
        self._la = 0
        try:
            try:
                self.state = 241
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 37, self._ctx)
                if la_ == 1:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 216
                    self.match(normParser.SPACED_EXPORT)
                    self.state = 217
                    self.typeName()
                else:
                    if la_ == 2:
                        self.enterOuterAlt(localctx, 2)
                        self.state = 218
                        self.match(normParser.SPACED_EXPORT)
                        self.state = 219
                        self.typeName()
                        self.state = 221
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 220
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 223
                    self.match(normParser.VARNAME)
                    self.state = 228
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la == normParser.DOT:
                        self.state = 224
                        self.match(normParser.DOT)
                        self.state = 225
                        self.match(normParser.VARNAME)
                        self.state = 230
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 239
                    self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 36, self._ctx)
                if la_ == 1:
                    self.state = 232
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not _la == normParser.WS:
                        if _la == normParser.NS:
                            self.state = 231
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                            else:
                                self._errHandler.reportMatch(self)
                                self.consume()
                        self.state = 234
                        self.match(normParser.AS)
                        self.state = 236
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 235
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 238
                    self.match(normParser.VARNAME)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class ImportsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SPACED_IMPORT(self):
            return self.getToken(normParser.SPACED_IMPORT, 0)

        def VARNAME(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.VARNAME)
            return self.getToken(normParser.VARNAME, i)

        def DOT(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.DOT)
            return self.getToken(normParser.DOT, i)

        def TIMES(self):
            return self.getToken(normParser.TIMES, 0)

        def typeName(self):
            return self.getTypedRuleContext(normParser.TypeNameContext, 0)

        def AS(self):
            return self.getToken(normParser.AS, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_imports

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterImports'):
                listener.enterImports(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitImports'):
                listener.exitImports(self)

    def imports(self):
        localctx = normParser.ImportsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_imports)
        self._la = 0
        try:
            try:
                self.state = 275
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 43, self._ctx)
                if la_ == 1:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 243
                    self.match(normParser.SPACED_IMPORT)
                    self.state = 244
                    self.match(normParser.VARNAME)
                    self.state = 249
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 38, self._ctx)
                    while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                        if _alt == 1:
                            self.state = 245
                            self.match(normParser.DOT)
                            self.state = 246
                            self.match(normParser.VARNAME)
                        self.state = 251
                        self._errHandler.sync(self)
                        _alt = self._interp.adaptivePredict(self._input, 38, self._ctx)

                    self.state = 252
                    self.match(normParser.DOT)
                    self.state = 253
                    self.match(normParser.TIMES)
                elif la_ == 2:
                    self.enterOuterAlt(localctx, 2)
                    self.state = 254
                    self.match(normParser.SPACED_IMPORT)
                    self.state = 255
                    self.match(normParser.VARNAME)
                    self.state = 260
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 39, self._ctx)
                    while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                        if _alt == 1:
                            self.state = 256
                            self.match(normParser.DOT)
                            self.state = 257
                            self.match(normParser.VARNAME)
                        self.state = 262
                        self._errHandler.sync(self)
                        _alt = self._interp.adaptivePredict(self._input, 39, self._ctx)

                    self.state = 263
                    self.match(normParser.DOT)
                    self.state = 264
                    self.typeName()
                    self.state = 273
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 42, self._ctx)
                    if la_ == 1:
                        self.state = 266
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if _la == normParser.NS:
                                self.state = 265
                                _la = self._input.LA(1)
                                if not _la == normParser.WS:
                                    if not _la == normParser.NS:
                                        self._errHandler.recoverInline(self)
                                else:
                                    self._errHandler.reportMatch(self)
                                    self.consume()
                            self.state = 268
                            self.match(normParser.AS)
                            self.state = 270
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if _la == normParser.WS or _la == normParser.NS:
                                self.state = 269
                                _la = self._input.LA(1)
                                if not _la == normParser.WS:
                                    if not _la == normParser.NS:
                                        self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 272
                        self.match(normParser.VARNAME)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class CommandsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SPACED_COMMAND(self):
            return self.getToken(normParser.SPACED_COMMAND, 0)

        def typeName(self):
            return self.getTypedRuleContext(normParser.TypeNameContext, 0)

        def getRuleIndex(self):
            return normParser.RULE_commands

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterCommands'):
                listener.enterCommands(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitCommands'):
                listener.exitCommands(self)

    def commands(self):
        localctx = normParser.CommandsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_commands)
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 277
                self.match(normParser.SPACED_COMMAND)
                self.state = 278
                self.typeName()
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class ContextContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SPACED_WITH(self):
            return self.getToken(normParser.SPACED_WITH, 0)

        def typeName(self):
            return self.getTypedRuleContext(normParser.TypeNameContext, 0)

        def COMMA(self):
            return self.getToken(normParser.COMMA, 0)

        def WS(self):
            return self.getToken(normParser.WS, 0)

        def getRuleIndex(self):
            return normParser.RULE_context

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterContext'):
                listener.enterContext(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitContext'):
                listener.exitContext(self)

    def context(self):
        localctx = normParser.ContextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_context)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 280
                self.match(normParser.SPACED_WITH)
                self.state = 281
                self.typeName()
                self.state = 283
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == normParser.WS:
                    self.state = 282
                    self.match(normParser.WS)
                self.state = 285
                self.match(normParser.COMMA)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class TypeNameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VARNAME(self):
            return self.getToken(normParser.VARNAME, 0)

        def version(self):
            return self.getTypedRuleContext(normParser.VersionContext, 0)

        def LSBR(self):
            return self.getToken(normParser.LSBR, 0)

        def typeName(self):
            return self.getTypedRuleContext(normParser.TypeNameContext, 0)

        def RSBR(self):
            return self.getToken(normParser.RSBR, 0)

        def getRuleIndex(self):
            return normParser.RULE_typeName

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterTypeName'):
                listener.enterTypeName(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitTypeName'):
                listener.exitTypeName(self)

    def typeName(self):
        localctx = normParser.TypeNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_typeName)
        self._la = 0
        try:
            try:
                self.state = 295
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [normParser.VARNAME]:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 287
                    self.match(normParser.VARNAME)
                    self.state = 289
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la & -64 == 0:
                        if 1 << _la & (1 << normParser.T__1 | 1 << normParser.T__2 | 1 << normParser.UUID) != 0:
                            self.state = 288
                            self.version()
                elif token in [normParser.LSBR]:
                    self.enterOuterAlt(localctx, 2)
                    self.state = 291
                    self.match(normParser.LSBR)
                    self.state = 292
                    self.typeName()
                    self.state = 293
                    self.match(normParser.RSBR)
                else:
                    raise NoViableAltException(self)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class VariableContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VARNAME(self):
            return self.getToken(normParser.VARNAME, 0)

        def COMMAND(self):
            return self.getToken(normParser.COMMAND, 0)

        def ARGOPT(self):
            return self.getToken(normParser.ARGOPT, 0)

        def variable(self):
            return self.getTypedRuleContext(normParser.VariableContext, 0)

        def DOT(self):
            return self.getToken(normParser.DOT, 0)

        def getRuleIndex(self):
            return normParser.RULE_variable

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterVariable'):
                listener.enterVariable(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitVariable'):
                listener.exitVariable(self)

    def variable(self, _p: int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = normParser.VariableContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 16
        self.enterRecursionRule(localctx, 16, self.RULE_variable, _p)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 301
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [normParser.VARNAME]:
                    self.state = 298
                    self.match(normParser.VARNAME)
                elif token in [normParser.COMMAND]:
                    self.state = 299
                    self.match(normParser.COMMAND)
                elif token in [normParser.ARGOPT]:
                    self.state = 300
                    self.match(normParser.ARGOPT)
                else:
                    raise NoViableAltException(self)
                self._ctx.stop = self._input.LT(-1)
                self.state = 308
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 48, self._ctx)
                while _alt != 2:
                    if _alt != ATN.INVALID_ALT_NUMBER:
                        if _alt == 1:
                            if self._parseListeners is not None:
                                self.triggerExitRuleEvent()
                            _prevctx = localctx
                            localctx = normParser.VariableContext(self, _parentctx, _parentState)
                            self.pushNewRecursionContext(localctx, _startState, self.RULE_variable)
                            self.state = 303
                            if not self.precpred(self._ctx, 1):
                                from antlr4.error.Errors import FailedPredicateException
                                raise FailedPredicateException(self, 'self.precpred(self._ctx, 1)')
                            self.state = 304
                            self.match(normParser.DOT)
                            self.state = 305
                            _la = self._input.LA(1)
                            _la - 16 & -64 == 0 and 1 << _la - 16 & (1 << normParser.COMMAND - 16 | 1 << normParser.ARGOPT - 16 | 1 << normParser.VARNAME - 16) != 0 or 
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 310
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 48, self._ctx)

            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.unrollRecursionContexts(_parentctx)

        return localctx

    class ArgumentPropertyContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COLON(self):
            return self.getToken(normParser.COLON, 0)

        def ARGOPT(self):
            return self.getToken(normParser.ARGOPT, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_argumentProperty

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterArgumentProperty'):
                listener.enterArgumentProperty(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitArgumentProperty'):
                listener.exitArgumentProperty(self)

    def argumentProperty(self):
        localctx = normParser.ArgumentPropertyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_argumentProperty)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 312
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not _la == normParser.WS:
                    if _la == normParser.NS:
                        self.state = 311
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                    self.state = 314
                    self.match(normParser.COLON)
                    self.state = 316
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.WS or _la == normParser.NS:
                        self.state = 315
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 318
                self.match(normParser.ARGOPT)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class ArgumentDeclarationContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variable(self):
            return self.getTypedRuleContext(normParser.VariableContext, 0)

        def COLON(self):
            return self.getToken(normParser.COLON, 0)

        def typeName(self):
            return self.getTypedRuleContext(normParser.TypeNameContext, 0)

        def argumentProperty(self):
            return self.getTypedRuleContext(normParser.ArgumentPropertyContext, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_argumentDeclaration

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterArgumentDeclaration'):
                listener.enterArgumentDeclaration(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitArgumentDeclaration'):
                listener.exitArgumentDeclaration(self)

    def argumentDeclaration(self):
        localctx = normParser.ArgumentDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_argumentDeclaration)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 320
                self.variable(0)
                self.state = 322
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not _la == normParser.WS:
                    if _la == normParser.NS:
                        self.state = 321
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                    self.state = 324
                    self.match(normParser.COLON)
                    self.state = 326
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.WS or _la == normParser.NS:
                        self.state = 325
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 328
                self.typeName()
                self.state = 330
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 53, self._ctx)
                if la_ == 1:
                    self.state = 329
                    self.argumentProperty()
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class ArgumentDeclarationsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def argumentDeclaration(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.ArgumentDeclarationContext)
            return self.getTypedRuleContext(normParser.ArgumentDeclarationContext, i)

        def COMMA(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.COMMA)
            return self.getToken(normParser.COMMA, i)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_argumentDeclarations

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterArgumentDeclarations'):
                listener.enterArgumentDeclarations(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitArgumentDeclarations'):
                listener.exitArgumentDeclarations(self)

    def argumentDeclarations(self):
        localctx = normParser.ArgumentDeclarationsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_argumentDeclarations)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 332
                self.argumentDeclaration()
                self.state = 343
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la & -64 == 0:
                    if 1 << _la & (1 << normParser.WS | 1 << normParser.NS | 1 << normParser.COMMA) != 0:
                        self.state = 334
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 333
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 336
                        self.match(normParser.COMMA)
                        self.state = 338
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 337
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 340
                    self.argumentDeclaration()
                    self.state = 345
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class RenameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variable(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.VariableContext)
            return self.getTypedRuleContext(normParser.VariableContext, i)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_rename

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterRename'):
                listener.enterRename(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitRename'):
                listener.exitRename(self)

    def rename(self):
        localctx = normParser.RenameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_rename)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 346
                self.variable(0)
                self.state = 348
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not _la == normParser.WS:
                    if _la == normParser.NS:
                        self.state = 347
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                    self.state = 350
                    self.match(normParser.T__0)
                    self.state = 352
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.WS or _la == normParser.NS:
                        self.state = 351
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 354
                self.variable(0)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class RenamesContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def rename(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.RenameContext)
            return self.getTypedRuleContext(normParser.RenameContext, i)

        def COMMA(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.COMMA)
            return self.getToken(normParser.COMMA, i)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_renames

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterRenames'):
                listener.enterRenames(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitRenames'):
                listener.exitRenames(self)

    def renames(self):
        localctx = normParser.RenamesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_renames)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 356
                self.rename()
                self.state = 367
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la & -64 == 0:
                    if 1 << _la & (1 << normParser.WS | 1 << normParser.NS | 1 << normParser.COMMA) != 0:
                        self.state = 358
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 357
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 360
                        self.match(normParser.COMMA)
                        self.state = 362
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 361
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 364
                    self.rename()
                    self.state = 369
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class TypeDeclarationContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeName(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.TypeNameContext)
            return self.getTypedRuleContext(normParser.TypeNameContext, i)

        def LBR(self):
            return self.getToken(normParser.LBR, 0)

        def argumentDeclarations(self):
            return self.getTypedRuleContext(normParser.ArgumentDeclarationsContext, 0)

        def RBR(self):
            return self.getToken(normParser.RBR, 0)

        def COLON(self):
            return self.getToken(normParser.COLON, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_typeDeclaration

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterTypeDeclaration'):
                listener.enterTypeDeclaration(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitTypeDeclaration'):
                listener.exitTypeDeclaration(self)

    def typeDeclaration(self):
        localctx = normParser.TypeDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_typeDeclaration)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 370
                self.typeName()
                self.state = 375
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == normParser.LBR:
                    self.state = 371
                    self.match(normParser.LBR)
                    self.state = 372
                    self.argumentDeclarations()
                    self.state = 373
                    self.match(normParser.RBR)
                self.state = 385
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 65, self._ctx)
                if la_ == 1:
                    self.state = 378
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not _la == normParser.WS:
                        if _la == normParser.NS:
                            self.state = 377
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                            else:
                                self._errHandler.reportMatch(self)
                                self.consume()
                        self.state = 380
                        self.match(normParser.COLON)
                        self.state = 382
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 381
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 384
                    self.typeName()
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class VersionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def UUID(self):
            return self.getToken(normParser.UUID, 0)

        def getRuleIndex(self):
            return normParser.RULE_version

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterVersion'):
                listener.enterVersion(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitVersion'):
                listener.exitVersion(self)

    def version(self):
        localctx = normParser.VersionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_version)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 387
                _la = self._input.LA(1)
                if _la & -64 == 0:
                    if not 1 << _la & (1 << normParser.T__1 | 1 << normParser.T__2 | 1 << normParser.UUID) != 0:
                        self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class QueryProjectionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variable(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.VariableContext)
            return self.getTypedRuleContext(normParser.VariableContext, i)

        def LCBR(self):
            return self.getToken(normParser.LCBR, 0)

        def RCBR(self):
            return self.getToken(normParser.RCBR, 0)

        def COMMA(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.COMMA)
            return self.getToken(normParser.COMMA, i)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def LBR(self):
            return self.getToken(normParser.LBR, 0)

        def RBR(self):
            return self.getToken(normParser.RBR, 0)

        def getRuleIndex(self):
            return normParser.RULE_queryProjection

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterQueryProjection'):
                listener.enterQueryProjection(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitQueryProjection'):
                listener.exitQueryProjection(self)

    def queryProjection(self):
        localctx = normParser.QueryProjectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_queryProjection)
        self._la = 0
        try:
            try:
                self.state = 429
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 73, self._ctx)
                if la_ == 1:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 389
                    self.match(normParser.T__3)
                    self.state = 391
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 66, self._ctx)
                    if la_ == 1:
                        self.state = 390
                        self.variable(0)
                elif la_ == 2:
                    self.enterOuterAlt(localctx, 2)
                    self.state = 393
                    self.match(normParser.T__3)
                    self.state = 394
                    self.match(normParser.LCBR)
                    self.state = 395
                    self.variable(0)
                    self.state = 406
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la == normParser.WS or _la == normParser.COMMA:
                        self.state = 397
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS:
                            self.state = 396
                            self.match(normParser.WS)
                        self.state = 399
                        self.match(normParser.COMMA)
                        self.state = 401
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS:
                            self.state = 400
                            self.match(normParser.WS)
                        self.state = 403
                        self.variable(0)
                        self.state = 408
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 409
                    self.match(normParser.RCBR)
                elif la_ == 3:
                    self.enterOuterAlt(localctx, 3)
                    self.state = 411
                    self.match(normParser.T__3)
                    self.state = 412
                    self.match(normParser.LBR)
                    self.state = 413
                    self.variable(0)
                    self.state = 424
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la == normParser.WS or _la == normParser.COMMA:
                        self.state = 415
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS:
                            self.state = 414
                            self.match(normParser.WS)
                        self.state = 417
                        self.match(normParser.COMMA)
                        self.state = 419
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS:
                            self.state = 418
                            self.match(normParser.WS)
                        self.state = 421
                        self.variable(0)
                        self.state = 426
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 427
                    self.match(normParser.RBR)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class ConstantContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def none(self):
            return self.getTypedRuleContext(normParser.NoneContext, 0)

        def bool_c(self):
            return self.getTypedRuleContext(normParser.Bool_cContext, 0)

        def integer_c(self):
            return self.getTypedRuleContext(normParser.Integer_cContext, 0)

        def float_c(self):
            return self.getTypedRuleContext(normParser.Float_cContext, 0)

        def string_c(self):
            return self.getTypedRuleContext(normParser.String_cContext, 0)

        def pattern(self):
            return self.getTypedRuleContext(normParser.PatternContext, 0)

        def uuid(self):
            return self.getTypedRuleContext(normParser.UuidContext, 0)

        def url(self):
            return self.getTypedRuleContext(normParser.UrlContext, 0)

        def datetime(self):
            return self.getTypedRuleContext(normParser.DatetimeContext, 0)

        def LSBR(self):
            return self.getToken(normParser.LSBR, 0)

        def constant(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.ConstantContext)
            return self.getTypedRuleContext(normParser.ConstantContext, i)

        def RSBR(self):
            return self.getToken(normParser.RSBR, 0)

        def COMMA(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.COMMA)
            return self.getToken(normParser.COMMA, i)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def getRuleIndex(self):
            return normParser.RULE_constant

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterConstant'):
                listener.enterConstant(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitConstant'):
                listener.exitConstant(self)

    def constant(self):
        localctx = normParser.ConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_constant)
        self._la = 0
        try:
            try:
                self.state = 457
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [normParser.NONE]:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 431
                    self.none()
                elif token in [normParser.BOOLEAN]:
                    self.enterOuterAlt(localctx, 2)
                    self.state = 432
                    self.bool_c()
                elif token in [normParser.INTEGER]:
                    self.enterOuterAlt(localctx, 3)
                    self.state = 433
                    self.integer_c()
                elif token in [normParser.FLOAT]:
                    self.enterOuterAlt(localctx, 4)
                    self.state = 434
                    self.float_c()
                elif token in [normParser.STRING]:
                    self.enterOuterAlt(localctx, 5)
                    self.state = 435
                    self.string_c()
                elif token in [normParser.PATTERN]:
                    self.enterOuterAlt(localctx, 6)
                    self.state = 436
                    self.pattern()
                elif token in [normParser.UUID]:
                    self.enterOuterAlt(localctx, 7)
                    self.state = 437
                    self.uuid()
                elif token in [normParser.URL]:
                    self.enterOuterAlt(localctx, 8)
                    self.state = 438
                    self.url()
                elif token in [normParser.DATETIME]:
                    self.enterOuterAlt(localctx, 9)
                    self.state = 439
                    self.datetime()
                elif token in [normParser.LSBR]:
                    self.enterOuterAlt(localctx, 10)
                    self.state = 440
                    self.match(normParser.LSBR)
                    self.state = 441
                    self.constant()
                    self.state = 452
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la == normParser.WS or _la == normParser.COMMA:
                        self.state = 443
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS:
                            self.state = 442
                            self.match(normParser.WS)
                        self.state = 445
                        self.match(normParser.COMMA)
                        self.state = 447
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS:
                            self.state = 446
                            self.match(normParser.WS)
                        self.state = 449
                        self.constant()
                        self.state = 454
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 455
                    self.match(normParser.RSBR)
                else:
                    raise NoViableAltException(self)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class CodeContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PYTHON_BLOCK(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.PYTHON_BLOCK)
            return self.getToken(normParser.PYTHON_BLOCK, i)

        def BLOCK_END(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.BLOCK_END)
            return self.getToken(normParser.BLOCK_END, i)

        def getRuleIndex(self):
            return normParser.RULE_code

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterCode'):
                listener.enterCode(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitCode'):
                listener.exitCode(self)

    def code(self):
        localctx = normParser.CodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_code)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 462
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la & -64 == 0:
                    if 1 << _la & (1 << normParser.T__0 | 1 << normParser.T__1 | 1 << normParser.T__2 | 1 << normParser.T__3 | 1 << normParser.IMPL | 1 << normParser.CEQ | 1 << normParser.OEQ | 1 << normParser.AEQ | 1 << normParser.SINGLELINE | 1 << normParser.MULTILINE | 1 << normParser.SPACED_EXPORT | 1 << normParser.EXPORT | 1 << normParser.SPACED_IMPORT | 1 << normParser.IMPORT | 1 << normParser.SPACED_COMMAND | 1 << normParser.COMMAND | 1 << normParser.ARGOPT | 1 << normParser.SPACED_WITH | 1 << normParser.WS | 1 << normParser.NS | 1 << normParser.LBR | 1 << normParser.RBR | 1 << normParser.LCBR | 1 << normParser.RCBR | 1 << normParser.LSBR | 1 << normParser.RSBR | 1 << normParser.NONE | 1 << normParser.AS | 1 << normParser.COLON | 1 << normParser.SEMICOLON | 1 << normParser.COMMA | 1 << normParser.DOT | 1 << normParser.DOTDOT | 1 << normParser.IN | 1 << normParser.NI | 1 << normParser.EQ | 1 << normParser.NE | 1 << normParser.GE | 1 << normParser.LE | 1 << normParser.GT | 1 << normParser.LT | 1 << normParser.LK | 1 << normParser.MINUS | 1 << normParser.PLUS | 1 << normParser.TIMES | 1 << normParser.DIVIDE | 1 << normParser.EXP | 1 << normParser.MOD | 1 << normParser.NOT | 1 << normParser.AND | 1 << normParser.OR | 1 << normParser.XOR | 1 << normParser.IMP | 1 << normParser.EQV | 1 << normParser.BOOLEAN | 1 << normParser.INTEGER | 1 << normParser.FLOAT | 1 << normParser.STRING | 1 << normParser.PATTERN | 1 << normParser.UUID | 1 << normParser.URL | 1 << normParser.DATETIME) != 0 or :
                        self.state = 459
                        _la = self._input.LA(1)
                        if not _la <= 0:
                            if _la == normParser.PYTHON_BLOCK or _la == normParser.BLOCK_END:
                                self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 464
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class CodeExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PYTHON_BLOCK(self):
            return self.getToken(normParser.PYTHON_BLOCK, 0)

        def code(self):
            return self.getTypedRuleContext(normParser.CodeContext, 0)

        def BLOCK_END(self):
            return self.getToken(normParser.BLOCK_END, 0)

        def getRuleIndex(self):
            return normParser.RULE_codeExpression

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterCodeExpression'):
                listener.enterCodeExpression(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitCodeExpression'):
                listener.exitCodeExpression(self)

    def codeExpression(self):
        localctx = normParser.CodeExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_codeExpression)
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 465
                self.match(normParser.PYTHON_BLOCK)
                self.state = 466
                self.code()
                self.state = 467
                self.match(normParser.BLOCK_END)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class ArgumentExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arithmeticExpression(self):
            return self.getTypedRuleContext(normParser.ArithmeticExpressionContext, 0)

        def queryProjection(self):
            return self.getTypedRuleContext(normParser.QueryProjectionContext, 0)

        def variable(self):
            return self.getTypedRuleContext(normParser.VariableContext, 0)

        def AS(self):
            return self.getToken(normParser.AS, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def spacedConditionOperator(self):
            return self.getTypedRuleContext(normParser.SpacedConditionOperatorContext, 0)

        def getRuleIndex(self):
            return normParser.RULE_argumentExpression

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterArgumentExpression'):
                listener.enterArgumentExpression(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitArgumentExpression'):
                listener.exitArgumentExpression(self)

    def argumentExpression(self):
        localctx = normParser.ArgumentExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_argumentExpression)
        self._la = 0
        try:
            try:
                self.state = 492
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 83, self._ctx)
                if la_ == 1:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 469
                    self.arithmeticExpression(0)
                elif la_ == 2:
                    self.enterOuterAlt(localctx, 2)
                    self.state = 470
                    self.queryProjection()
                elif la_ == 3:
                    self.enterOuterAlt(localctx, 3)
                    self.state = 471
                    self.variable(0)
                    self.state = 472
                    self.queryProjection()
                else:
                    if la_ == 4:
                        self.enterOuterAlt(localctx, 4)
                        self.state = 474
                        self.variable(0)
                        self.state = 476
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == normParser.WS or _la == normParser.NS:
                            self.state = 475
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 478
                    self.match(normParser.AS)
                    self.state = 480
                    self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not _la == normParser.WS:
                    if _la == normParser.NS:
                        self.state = 479
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                    self.state = 482
                    self.arithmeticExpression(0)
                    self.state = 484
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.T__3:
                        self.state = 483
                        self.queryProjection()
                elif la_ == 5:
                    self.enterOuterAlt(localctx, 5)
                    self.state = 486
                    self.variable(0)
                    self.state = 487
                    self.spacedConditionOperator()
                    self.state = 488
                    self.arithmeticExpression(0)
                    self.state = 490
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.T__3:
                        self.state = 489
                        self.queryProjection()
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class ArgumentExpressionsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBR(self):
            return self.getToken(normParser.LBR, 0)

        def RBR(self):
            return self.getToken(normParser.RBR, 0)

        def argumentExpression(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.ArgumentExpressionContext)
            return self.getTypedRuleContext(normParser.ArgumentExpressionContext, i)

        def COMMA(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.COMMA)
            return self.getToken(normParser.COMMA, i)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_argumentExpressions

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterArgumentExpressions'):
                listener.enterArgumentExpressions(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitArgumentExpressions'):
                listener.exitArgumentExpressions(self)

    def argumentExpressions(self):
        localctx = normParser.ArgumentExpressionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_argumentExpressions)
        self._la = 0
        try:
            try:
                self.state = 513
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 87, self._ctx)
                if la_ == 1:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 494
                    self.match(normParser.LBR)
                    self.state = 495
                    self.match(normParser.RBR)
                elif la_ == 2:
                    self.enterOuterAlt(localctx, 2)
                    self.state = 496
                    self.match(normParser.LBR)
                    self.state = 497
                    self.argumentExpression()
                    self.state = 508
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la & -64 == 0:
                        if 1 << _la & (1 << normParser.WS | 1 << normParser.NS | 1 << normParser.COMMA) != 0:
                            self.state = 499
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if _la == normParser.WS or _la == normParser.NS:
                                self.state = 498
                                _la = self._input.LA(1)
                                if not _la == normParser.WS:
                                    if not _la == normParser.NS:
                                        self._errHandler.recoverInline(self)
                            else:
                                self._errHandler.reportMatch(self)
                                self.consume()
                            self.state = 501
                            self.match(normParser.COMMA)
                            self.state = 503
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if _la == normParser.WS or _la == normParser.NS:
                                self.state = 502
                                _la = self._input.LA(1)
                                if not _la == normParser.WS:
                                    if not _la == normParser.NS:
                                        self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 505
                        self.argumentExpression()
                        self.state = 510
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 511
                    self.match(normParser.RBR)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class EvaluationExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def constant(self):
            return self.getTypedRuleContext(normParser.ConstantContext, 0)

        def variable(self):
            return self.getTypedRuleContext(normParser.VariableContext, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def queryProjection(self):
            return self.getTypedRuleContext(normParser.QueryProjectionContext, 0)

        def argumentExpressions(self):
            return self.getTypedRuleContext(normParser.ArgumentExpressionsContext, 0)

        def evaluationExpression(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.EvaluationExpressionContext)
            return self.getTypedRuleContext(normParser.EvaluationExpressionContext, i)

        def DOT(self):
            return self.getToken(normParser.DOT, 0)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_evaluationExpression

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterEvaluationExpression'):
                listener.enterEvaluationExpression(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitEvaluationExpression'):
                listener.exitEvaluationExpression(self)

    def evaluationExpression(self, _p: int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = normParser.EvaluationExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 44
        self.enterRecursionRule(localctx, 44, self.RULE_evaluationExpression, _p)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 533
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 92, self._ctx)
                if la_ == 1:
                    self.state = 516
                    self.constant()
                elif la_ == 2:
                    self.state = 517
                    self.variable(0)
                    self.state = 519
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 88, self._ctx)
                    if la_ == 1:
                        self.state = 518
                        self.match(normParser.WS)
                    self.state = 522
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 89, self._ctx)
                    if la_ == 1:
                        self.state = 521
                        self.queryProjection()
                elif la_ == 3:
                    self.state = 524
                    self.argumentExpressions()
                elif la_ == 4:
                    self.state = 525
                    self.variable(0)
                    self.state = 526
                    self.argumentExpressions()
                    self.state = 528
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 90, self._ctx)
                    if la_ == 1:
                        self.state = 527
                        self.match(normParser.WS)
                    self.state = 531
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 91, self._ctx)
                    if la_ == 1:
                        self.state = 530
                        self.queryProjection()
                self._ctx.stop = self._input.LT(-1)
                self.state = 546
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 95, self._ctx)
                while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        if self._parseListeners is not None:
                            self.triggerExitRuleEvent()
                        else:
                            _prevctx = localctx
                            localctx = normParser.EvaluationExpressionContext(self, _parentctx, _parentState)
                            self.pushNewRecursionContext(localctx, _startState, self.RULE_evaluationExpression)
                            self.state = 535
                            if not self.precpred(self._ctx, 1):
                                from antlr4.error.Errors import FailedPredicateException
                                raise FailedPredicateException(self, 'self.precpred(self._ctx, 1)')
                            else:
                                self.state = 537
                                self._errHandler.sync(self)
                                _la = self._input.LA(1)
                                if _la == normParser.WS or _la == normParser.NS:
                                    self.state = 536
                                    _la = self._input.LA(1)
                                    if not _la == normParser.WS:
                                        if not _la == normParser.NS:
                                            self._errHandler.recoverInline(self)
                                    else:
                                        self._errHandler.reportMatch(self)
                                        self.consume()
                            self.state = 539
                            self.match(normParser.DOT)
                            self.state = 541
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if _la == normParser.WS or _la == normParser.NS:
                                self.state = 540
                                _la = self._input.LA(1)
                                if not _la == normParser.WS:
                                    if not _la == normParser.NS:
                                        self._errHandler.recoverInline(self)
                                else:
                                    self._errHandler.reportMatch(self)
                                    self.consume()
                        self.state = 543
                        self.evaluationExpression(2)
                    self.state = 548
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 95, self._ctx)

            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.unrollRecursionContexts(_parentctx)

        return localctx

    class SlicedExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def evaluationExpression(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.EvaluationExpressionContext)
            return self.getTypedRuleContext(normParser.EvaluationExpressionContext, i)

        def LSBR(self):
            return self.getToken(normParser.LSBR, 0)

        def RSBR(self):
            return self.getToken(normParser.RSBR, 0)

        def integer_c(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.Integer_cContext)
            return self.getTypedRuleContext(normParser.Integer_cContext, i)

        def COLON(self):
            return self.getToken(normParser.COLON, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_slicedExpression

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterSlicedExpression'):
                listener.enterSlicedExpression(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitSlicedExpression'):
                listener.exitSlicedExpression(self)

    def slicedExpression(self):
        localctx = normParser.SlicedExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_slicedExpression)
        self._la = 0
        try:
            try:
                self.state = 574
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 101, self._ctx)
                if la_ == 1:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 549
                    self.evaluationExpression(0)
                else:
                    if la_ == 2:
                        self.enterOuterAlt(localctx, 2)
                        self.state = 550
                        self.evaluationExpression(0)
                        self.state = 551
                        self.match(normParser.LSBR)
                        self.state = 553
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input, 96, self._ctx)
                        if la_ == 1:
                            self.state = 552
                            self.integer_c()
                        self.state = 556
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input, 97, self._ctx)
                        if la_ == 1:
                            self.state = 555
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 559
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.COLON:
                        self.state = 558
                        self.match(normParser.COLON)
                    self.state = 562
                    self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not _la == normParser.WS:
                    if _la == normParser.NS:
                        self.state = 561
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                    self.state = 565
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.INTEGER:
                        self.state = 564
                        self.integer_c()
                    self.state = 567
                    self.match(normParser.RSBR)
                elif la_ == 3:
                    self.enterOuterAlt(localctx, 3)
                    self.state = 569
                    self.evaluationExpression(0)
                    self.state = 570
                    self.match(normParser.LSBR)
                    self.state = 571
                    self.evaluationExpression(0)
                    self.state = 572
                    self.match(normParser.RSBR)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class ArithmeticExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def slicedExpression(self):
            return self.getTypedRuleContext(normParser.SlicedExpressionContext, 0)

        def LBR(self):
            return self.getToken(normParser.LBR, 0)

        def arithmeticExpression(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.ArithmeticExpressionContext)
            return self.getTypedRuleContext(normParser.ArithmeticExpressionContext, i)

        def RBR(self):
            return self.getToken(normParser.RBR, 0)

        def MINUS(self):
            return self.getToken(normParser.MINUS, 0)

        def MOD(self):
            return self.getToken(normParser.MOD, 0)

        def EXP(self):
            return self.getToken(normParser.EXP, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def TIMES(self):
            return self.getToken(normParser.TIMES, 0)

        def DIVIDE(self):
            return self.getToken(normParser.DIVIDE, 0)

        def PLUS(self):
            return self.getToken(normParser.PLUS, 0)

        def getRuleIndex(self):
            return normParser.RULE_arithmeticExpression

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterArithmeticExpression'):
                listener.enterArithmeticExpression(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitArithmeticExpression'):
                listener.exitArithmeticExpression(self)

    def arithmeticExpression(self, _p: int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = normParser.ArithmeticExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 48
        self.enterRecursionRule(localctx, 48, self.RULE_arithmeticExpression, _p)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 584
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 102, self._ctx)
                if la_ == 1:
                    self.state = 577
                    self.slicedExpression()
                elif la_ == 2:
                    self.state = 578
                    self.match(normParser.LBR)
                    self.state = 579
                    self.arithmeticExpression(0)
                    self.state = 580
                    self.match(normParser.RBR)
                elif la_ == 3:
                    self.state = 582
                    self.match(normParser.MINUS)
                    self.state = 583
                    self.arithmeticExpression(4)
                self._ctx.stop = self._input.LT(-1)
                self.state = 615
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 110, self._ctx)
                while _alt != 2:
                    if _alt != ATN.INVALID_ALT_NUMBER:
                        if _alt == 1:
                            if self._parseListeners is not None:
                                self.triggerExitRuleEvent()
                            _prevctx = localctx
                            self.state = 613
                            self._errHandler.sync(self)
                            la_ = self._interp.adaptivePredict(self._input, 109, self._ctx)
                            if la_ == 1:
                                localctx = normParser.ArithmeticExpressionContext(self, _parentctx, _parentState)
                                self.pushNewRecursionContext(localctx, _startState, self.RULE_arithmeticExpression)
                                self.state = 586
                                if not self.precpred(self._ctx, 3):
                                    from antlr4.error.Errors import FailedPredicateException
                                    raise FailedPredicateException(self, 'self.precpred(self._ctx, 3)')
                                self.state = 588
                                self._errHandler.sync(self)
                                _la = self._input.LA(1)
                                if _la == normParser.WS or _la == normParser.NS:
                                    self.state = 587
                                    _la = self._input.LA(1)
                                    if not _la == normParser.WS:
                                        if not _la == normParser.NS:
                                            self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 590
                    _la = self._input.LA(1)
                    if not _la == normParser.EXP:
                        if not _la == normParser.MOD:
                            self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 592
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not _la == normParser.WS:
                        if _la == normParser.NS:
                            self.state = 591
                            _la = self._input.LA(1)
                            if not _la == normParser.WS:
                                if not _la == normParser.NS:
                                    self._errHandler.recoverInline(self)
                            else:
                                self._errHandler.reportMatch(self)
                                self.consume()
                        self.state = 594
                        self.arithmeticExpression(4)
                    else:
                        if la_ == 2:
                            localctx = normParser.ArithmeticExpressionContext(self, _parentctx, _parentState)
                            self.pushNewRecursionContext(localctx, _startState, self.RULE_arithmeticExpression)
                            self.state = 595
                            if not self.precpred(self._ctx, 2):
                                from antlr4.error.Errors import FailedPredicateException
                                raise FailedPredicateException(self, 'self.precpred(self._ctx, 2)')
                            self.state = 597
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if _la == normParser.WS or _la == normParser.NS:
                                self.state = 596
                                _la = self._input.LA(1)
                                if not _la == normParser.WS:
                                    if not _la == normParser.NS:
                                        self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 599
                        _la = self._input.LA(1)
                        if not _la == normParser.TIMES:
                            if not _la == normParser.DIVIDE:
                                self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 601
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if _la == normParser.NS:
                                self.state = 600
                                _la = self._input.LA(1)
                                if not _la == normParser.WS:
                                    if not _la == normParser.NS:
                                        self._errHandler.recoverInline(self)
                                else:
                                    self._errHandler.reportMatch(self)
                                    self.consume()
                            self.state = 603
                            self.arithmeticExpression(3)
                        elif la_ == 3:
                            localctx = normParser.ArithmeticExpressionContext(self, _parentctx, _parentState)
                            self.pushNewRecursionContext(localctx, _startState, self.RULE_arithmeticExpression)
                            self.state = 604
                            if not self.precpred(self._ctx, 1):
                                from antlr4.error.Errors import FailedPredicateException
                                raise FailedPredicateException(self, 'self.precpred(self._ctx, 1)')
                            else:
                                self.state = 606
                                self._errHandler.sync(self)
                                _la = self._input.LA(1)
                                if not _la == normParser.WS:
                                    if _la == normParser.NS:
                                        self.state = 605
                                        _la = self._input.LA(1)
                                        if not _la == normParser.WS:
                                            if not _la == normParser.NS:
                                                self._errHandler.recoverInline(self)
                                        else:
                                            self._errHandler.reportMatch(self)
                                            self.consume()
                                    self.state = 608
                                    _la = self._input.LA(1)
                                    if not _la == normParser.MINUS:
                                        if not _la == normParser.PLUS:
                                            self._errHandler.recoverInline(self)
                                else:
                                    self._errHandler.reportMatch(self)
                                    self.consume()
                                self.state = 610
                                self._errHandler.sync(self)
                                _la = self._input.LA(1)
                                if _la == normParser.WS or _la == normParser.NS:
                                    self.state = 609
                                    _la = self._input.LA(1)
                                    if not _la == normParser.WS:
                                        if not _la == normParser.NS:
                                            self._errHandler.recoverInline(self)
                                    else:
                                        self._errHandler.reportMatch(self)
                                        self.consume()
                            self.state = 612
                            self.arithmeticExpression(2)
                    self.state = 617
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 110, self._ctx)

            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.unrollRecursionContexts(_parentctx)

        return localctx

    class ConditionExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arithmeticExpression(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.ArithmeticExpressionContext)
            return self.getTypedRuleContext(normParser.ArithmeticExpressionContext, i)

        def spacedConditionOperator(self):
            return self.getTypedRuleContext(normParser.SpacedConditionOperatorContext, 0)

        def getRuleIndex(self):
            return normParser.RULE_conditionExpression

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterConditionExpression'):
                listener.enterConditionExpression(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitConditionExpression'):
                listener.exitConditionExpression(self)

    def conditionExpression(self):
        localctx = normParser.ConditionExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_conditionExpression)
        try:
            try:
                self.state = 623
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 111, self._ctx)
                if la_ == 1:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 618
                    self.arithmeticExpression(0)
                elif la_ == 2:
                    self.enterOuterAlt(localctx, 2)
                    self.state = 619
                    self.arithmeticExpression(0)
                    self.state = 620
                    self.spacedConditionOperator()
                    self.state = 621
                    self.arithmeticExpression(0)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class OneLineExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def conditionExpression(self):
            return self.getTypedRuleContext(normParser.ConditionExpressionContext, 0)

        def WS(self):
            return self.getToken(normParser.WS, 0)

        def queryProjection(self):
            return self.getTypedRuleContext(normParser.QueryProjectionContext, 0)

        def NOT(self):
            return self.getToken(normParser.NOT, 0)

        def oneLineExpression(self, i: int=None):
            if i is None:
                return self.getTypedRuleContexts(normParser.OneLineExpressionContext)
            return self.getTypedRuleContext(normParser.OneLineExpressionContext, i)

        def spacedLogicalOperator(self):
            return self.getTypedRuleContext(normParser.SpacedLogicalOperatorContext, 0)

        def getRuleIndex(self):
            return normParser.RULE_oneLineExpression

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterOneLineExpression'):
                listener.enterOneLineExpression(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitOneLineExpression'):
                listener.exitOneLineExpression(self)

    def oneLineExpression(self, _p: int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = normParser.OneLineExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 52
        self.enterRecursionRule(localctx, 52, self.RULE_oneLineExpression, _p)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 638
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [normParser.COMMAND, normParser.ARGOPT, normParser.LBR, normParser.LSBR, normParser.NONE, normParser.MINUS, normParser.BOOLEAN, normParser.INTEGER, normParser.FLOAT, normParser.STRING, normParser.PATTERN, normParser.UUID, normParser.URL, normParser.DATETIME, normParser.VARNAME]:
                    self.state = 626
                    self.conditionExpression()
                    self.state = 628
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 112, self._ctx)
                    if la_ == 1:
                        self.state = 627
                        self.match(normParser.WS)
                    self.state = 631
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 113, self._ctx)
                    if la_ == 1:
                        self.state = 630
                        self.queryProjection()
                elif token in [normParser.NOT]:
                    self.state = 633
                    self.match(normParser.NOT)
                    self.state = 635
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.WS:
                        self.state = 634
                        self.match(normParser.WS)
                    self.state = 637
                    self.oneLineExpression(2)
                else:
                    raise NoViableAltException(self)
                self._ctx.stop = self._input.LT(-1)
                self.state = 646
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 116, self._ctx)
                while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        if self._parseListeners is not None:
                            self.triggerExitRuleEvent()
                        _prevctx = localctx
                        localctx = normParser.OneLineExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_oneLineExpression)
                        self.state = 640
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, 'self.precpred(self._ctx, 1)')
                        self.state = 641
                        self.spacedLogicalOperator()
                        self.state = 642
                        self.oneLineExpression(2)
                    self.state = 648
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 116, self._ctx)

            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.unrollRecursionContexts(_parentctx)

        return localctx

    class MultiLineExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def oneLineExpression(self):
            return self.getTypedRuleContext(normParser.OneLineExpressionContext, 0)

        def newlineLogicalOperator(self):
            return self.getTypedRuleContext(normParser.NewlineLogicalOperatorContext, 0)

        def multiLineExpression(self):
            return self.getTypedRuleContext(normParser.MultiLineExpressionContext, 0)

        def getRuleIndex(self):
            return normParser.RULE_multiLineExpression

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterMultiLineExpression'):
                listener.enterMultiLineExpression(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitMultiLineExpression'):
                listener.exitMultiLineExpression(self)

    def multiLineExpression(self):
        localctx = normParser.MultiLineExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_multiLineExpression)
        try:
            try:
                self.state = 654
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 117, self._ctx)
                if la_ == 1:
                    self.enterOuterAlt(localctx, 1)
                    self.state = 649
                    self.oneLineExpression(0)
                elif la_ == 2:
                    self.enterOuterAlt(localctx, 2)
                    self.state = 650
                    self.oneLineExpression(0)
                    self.state = 651
                    self.newlineLogicalOperator()
                    self.state = 652
                    self.multiLineExpression()
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class NoneContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NONE(self):
            return self.getToken(normParser.NONE, 0)

        def getRuleIndex(self):
            return normParser.RULE_none

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterNone'):
                listener.enterNone(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitNone'):
                listener.exitNone(self)

    def none(self):
        localctx = normParser.NoneContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_none)
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 656
                self.match(normParser.NONE)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class Bool_cContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOLEAN(self):
            return self.getToken(normParser.BOOLEAN, 0)

        def getRuleIndex(self):
            return normParser.RULE_bool_c

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterBool_c'):
                listener.enterBool_c(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitBool_c'):
                listener.exitBool_c(self)

    def bool_c(self):
        localctx = normParser.Bool_cContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_bool_c)
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 658
                self.match(normParser.BOOLEAN)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class Integer_cContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(normParser.INTEGER, 0)

        def getRuleIndex(self):
            return normParser.RULE_integer_c

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterInteger_c'):
                listener.enterInteger_c(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitInteger_c'):
                listener.exitInteger_c(self)

    def integer_c(self):
        localctx = normParser.Integer_cContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_integer_c)
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 660
                self.match(normParser.INTEGER)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class Float_cContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FLOAT(self):
            return self.getToken(normParser.FLOAT, 0)

        def getRuleIndex(self):
            return normParser.RULE_float_c

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterFloat_c'):
                listener.enterFloat_c(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitFloat_c'):
                listener.exitFloat_c(self)

    def float_c(self):
        localctx = normParser.Float_cContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_float_c)
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 662
                self.match(normParser.FLOAT)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class String_cContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(normParser.STRING, 0)

        def getRuleIndex(self):
            return normParser.RULE_string_c

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterString_c'):
                listener.enterString_c(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitString_c'):
                listener.exitString_c(self)

    def string_c(self):
        localctx = normParser.String_cContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_string_c)
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 664
                self.match(normParser.STRING)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class PatternContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PATTERN(self):
            return self.getToken(normParser.PATTERN, 0)

        def getRuleIndex(self):
            return normParser.RULE_pattern

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterPattern'):
                listener.enterPattern(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitPattern'):
                listener.exitPattern(self)

    def pattern(self):
        localctx = normParser.PatternContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_pattern)
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 666
                self.match(normParser.PATTERN)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class UuidContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def UUID(self):
            return self.getToken(normParser.UUID, 0)

        def getRuleIndex(self):
            return normParser.RULE_uuid

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterUuid'):
                listener.enterUuid(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitUuid'):
                listener.exitUuid(self)

    def uuid(self):
        localctx = normParser.UuidContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_uuid)
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 668
                self.match(normParser.UUID)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class UrlContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def URL(self):
            return self.getToken(normParser.URL, 0)

        def getRuleIndex(self):
            return normParser.RULE_url

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterUrl'):
                listener.enterUrl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitUrl'):
                listener.exitUrl(self)

    def url(self):
        localctx = normParser.UrlContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_url)
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 670
                self.match(normParser.URL)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class DatetimeContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DATETIME(self):
            return self.getToken(normParser.DATETIME, 0)

        def getRuleIndex(self):
            return normParser.RULE_datetime

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterDatetime'):
                listener.enterDatetime(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitDatetime'):
                listener.exitDatetime(self)

    def datetime(self):
        localctx = normParser.DatetimeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_datetime)
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 672
                self.match(normParser.DATETIME)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class LogicalOperatorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AND(self):
            return self.getToken(normParser.AND, 0)

        def OR(self):
            return self.getToken(normParser.OR, 0)

        def NOT(self):
            return self.getToken(normParser.NOT, 0)

        def XOR(self):
            return self.getToken(normParser.XOR, 0)

        def IMP(self):
            return self.getToken(normParser.IMP, 0)

        def EQV(self):
            return self.getToken(normParser.EQV, 0)

        def getRuleIndex(self):
            return normParser.RULE_logicalOperator

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterLogicalOperator'):
                listener.enterLogicalOperator(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitLogicalOperator'):
                listener.exitLogicalOperator(self)

    def logicalOperator(self):
        localctx = normParser.LogicalOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_logicalOperator)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 674
                _la = self._input.LA(1)
                if _la & -64 == 0:
                    if not 1 << _la & (1 << normParser.NOT | 1 << normParser.AND | 1 << normParser.OR | 1 << normParser.XOR | 1 << normParser.IMP | 1 << normParser.EQV) != 0:
                        self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class SpacedLogicalOperatorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalOperator(self):
            return self.getTypedRuleContext(normParser.LogicalOperatorContext, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def getRuleIndex(self):
            return normParser.RULE_spacedLogicalOperator

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterSpacedLogicalOperator'):
                listener.enterSpacedLogicalOperator(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitSpacedLogicalOperator'):
                listener.exitSpacedLogicalOperator(self)

    def spacedLogicalOperator(self):
        localctx = normParser.SpacedLogicalOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_spacedLogicalOperator)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 677
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == normParser.WS:
                    self.state = 676
                    self.match(normParser.WS)
                self.state = 679
                self.logicalOperator()
                self.state = 681
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == normParser.WS:
                    self.state = 680
                    self.match(normParser.WS)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class NewlineLogicalOperatorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NS(self):
            return self.getToken(normParser.NS, 0)

        def logicalOperator(self):
            return self.getTypedRuleContext(normParser.LogicalOperatorContext, 0)

        def WS(self):
            return self.getToken(normParser.WS, 0)

        def getRuleIndex(self):
            return normParser.RULE_newlineLogicalOperator

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterNewlineLogicalOperator'):
                listener.enterNewlineLogicalOperator(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitNewlineLogicalOperator'):
                listener.exitNewlineLogicalOperator(self)

    def newlineLogicalOperator(self):
        localctx = normParser.NewlineLogicalOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_newlineLogicalOperator)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 683
                self.match(normParser.NS)
                self.state = 684
                self.logicalOperator()
                self.state = 686
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == normParser.WS:
                    self.state = 685
                    self.match(normParser.WS)
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class ConditionOperatorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(normParser.EQ, 0)

        def NE(self):
            return self.getToken(normParser.NE, 0)

        def IN(self):
            return self.getToken(normParser.IN, 0)

        def NI(self):
            return self.getToken(normParser.NI, 0)

        def LT(self):
            return self.getToken(normParser.LT, 0)

        def LE(self):
            return self.getToken(normParser.LE, 0)

        def GT(self):
            return self.getToken(normParser.GT, 0)

        def GE(self):
            return self.getToken(normParser.GE, 0)

        def LK(self):
            return self.getToken(normParser.LK, 0)

        def getRuleIndex(self):
            return normParser.RULE_conditionOperator

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterConditionOperator'):
                listener.enterConditionOperator(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitConditionOperator'):
                listener.exitConditionOperator(self)

    def conditionOperator(self):
        localctx = normParser.ConditionOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_conditionOperator)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 688
                _la = self._input.LA(1)
                if _la & -64 == 0:
                    if not 1 << _la & (1 << normParser.IN | 1 << normParser.NI | 1 << normParser.EQ | 1 << normParser.NE | 1 << normParser.GE | 1 << normParser.LE | 1 << normParser.GT | 1 << normParser.LT | 1 << normParser.LK) != 0:
                        self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    class SpacedConditionOperatorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def conditionOperator(self):
            return self.getTypedRuleContext(normParser.ConditionOperatorContext, 0)

        def WS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.WS)
            return self.getToken(normParser.WS, i)

        def NS(self, i: int=None):
            if i is None:
                return self.getTokens(normParser.NS)
            return self.getToken(normParser.NS, i)

        def getRuleIndex(self):
            return normParser.RULE_spacedConditionOperator

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'enterSpacedConditionOperator'):
                listener.enterSpacedConditionOperator(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, 'exitSpacedConditionOperator'):
                listener.exitSpacedConditionOperator(self)

    def spacedConditionOperator(self):
        localctx = normParser.SpacedConditionOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_spacedConditionOperator)
        self._la = 0
        try:
            try:
                self.enterOuterAlt(localctx, 1)
                self.state = 691
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not _la == normParser.WS:
                    if _la == normParser.NS:
                        self.state = 690
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                    self.state = 693
                    self.conditionOperator()
                    self.state = 695
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == normParser.WS or _la == normParser.NS:
                        self.state = 694
                        _la = self._input.LA(1)
                        if not _la == normParser.WS:
                            if not _la == normParser.NS:
                                self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
            except RecognitionException as re:
                try:
                    localctx.exception = re
                    self._errHandler.reportError(self, re)
                    self._errHandler.recover(self, re)
                finally:
                    re = None
                    del re

        finally:
            self.exitRule()

        return localctx

    def sempred(self, localctx: RuleContext, ruleIndex: int, predIndex: int):
        if self._predicates == None:
            self._predicates = dict()
        else:
            self._predicates[8] = self.variable_sempred
            self._predicates[22] = self.evaluationExpression_sempred
            self._predicates[24] = self.arithmeticExpression_sempred
            self._predicates[26] = self.oneLineExpression_sempred
            pred = self._predicates.get(ruleIndex, None)
            if pred is None:
                raise Exception('No predicate with index:' + str(ruleIndex))
            else:
                return pred(localctx, predIndex)

    def variable_sempred(self, localctx: VariableContext, predIndex: int):
        if predIndex == 0:
            return self.precpred(self._ctx, 1)

    def evaluationExpression_sempred(self, localctx: EvaluationExpressionContext, predIndex: int):
        if predIndex == 1:
            return self.precpred(self._ctx, 1)

    def arithmeticExpression_sempred(self, localctx: ArithmeticExpressionContext, predIndex: int):
        if predIndex == 2:
            return self.precpred(self._ctx, 3)
        if predIndex == 3:
            return self.precpred(self._ctx, 2)
        if predIndex == 4:
            return self.precpred(self._ctx, 1)

    def oneLineExpression_sempred(self, localctx: OneLineExpressionContext, predIndex: int):
        if predIndex == 5:
            return self.precpred(self._ctx, 1)