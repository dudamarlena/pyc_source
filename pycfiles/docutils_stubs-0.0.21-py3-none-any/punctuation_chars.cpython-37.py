# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/utils/punctuation_chars.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 6364 bytes
import sys, re, unicodedata
openers = '"\'(<\\[{༺༼᚛⁅⁽₍〈❨❪❬❮❰❲❴⟅⟦⟨⟪⟬⟮⦃⦅⦇⦉⦋⦍⦏⦑⦓⦕⦗⧘⧚⧼⸢⸤⸦⸨〈《「『【〔〖〘〚〝〝﴾︗︵︷︹︻︽︿﹁﹃﹇﹙﹛﹝（［｛｟｢«‘“‹⸂⸄⸉⸌⸜⸠‚„»’”›⸃⸅⸊⸍⸝⸡‛‟'
closers = '"\')>\\]}༻༽᚜⁆⁾₎〉❩❫❭❯❱❳❵⟆⟧⟩⟫⟭⟯⦄⦆⦈⦊⦌⦎⦐⦒⦔⦖⦘⧙⧛⧽⸣⸥⸧⸩〉》」』】〕〗〙〛〞〟﴿︘︶︸︺︼︾﹀﹂﹄﹈﹚﹜﹞）］｝｠｣»’”›⸃⸅⸊⸍⸝⸡‛‟«‘“‹⸂⸄⸉⸌⸜⸠‚„'
delimiters = '\\-/:֊¡·¿;·՚-՟։־׀׃׆׳״؉؊،؍؛؞؟٪-٭۔܀-܍߷-߹࠰-࠾।॥॰෴๏๚๛༄-༒྅࿐-࿔၊-၏჻፡-፨᐀᙭᙮᛫-᛭᜵᜶។-៖៘-៚᠀-᠊᥄᥅᧞᧟᨞᨟᪠-᪦᪨-᪭᭚-᭠᰻-᰿᱾᱿᳓‐-‗†-‧‰-‸※-‾⁁-⁃⁇-⁑⁓⁕-⁞⳹-⳼⳾⳿⸀⸁⸆-⸈⸋⸎-⸛⸞⸟⸪-⸮⸰⸱、-〃〜〰〽゠・꓾꓿꘍-꘏꙳꙾꛲-꛷꡴-꡷꣎꣏꣸-꣺꤮꤯꥟꧁-꧍꧞꧟꩜-꩟꫞꫟꯫︐-︖︙︰-︲﹅﹆﹉-﹌﹐-﹒﹔-﹘﹟-﹡﹣﹨﹪﹫！-＃％-＇＊，-／：；？＠＼｡､･'
if sys.maxunicode >= 1114111:
    delimiters += '𐄀𐄁𐎟𐏐𐡗𐤟𐤿𐩐-𐩘𐩿𐬹-𐬿𑂻𑂼𑂾-𑃁𒑰-𒑳'
closing_delimiters = '\\\\.,;!?'
quote_pairs = {'»':'»', 
 '‘':'‚', 
 '’':'’', 
 '‚':'‘’', 
 '“':'„', 
 '„':'“”', 
 '”':'”', 
 '›':'›'}

def match_chars(c1, c2):
    """Test whether `c1` and `c2` are a matching open/close character pair.

    Matching open/close pairs are at the same position in
    `punctuation_chars.openers` and `punctuation_chars.closers`.
    The pairing of open/close quotes is ambiguous due to  different
    typographic conventions in different languages,
    so we test for additional matches stored in `quote_pairs`.
    """
    try:
        i = openers.index(c1)
    except ValueError:
        return False
    else:
        return c2 == closers[i] or c2 in quote_pairs.get(c1, '')