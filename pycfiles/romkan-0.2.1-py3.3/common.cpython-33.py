# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/romkan/common.py
# Compiled at: 2013-02-25 16:57:33
# Size of source mod 2**32: 24956 bytes
from __future__ import unicode_literals
from .version import __version__
import re
try:
    from functools import cmp_to_key
except ImportError:

    def cmp_to_key(mycmp):
        """Convert a cmp= function into a key= function"""

        class K(object):
            __slots__ = [
             'obj']

            def __init__(self, obj):
                self.obj = obj

            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0

            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0

            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0

            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0

            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0

            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0

            __hash__ = None

        return K


KUNREITAB = "ァ       xa      ア       a       ィ       xi      イ       i       ゥ       xu\nウ       u       ヴ       vu      ヴァ      va      ヴィ      vi      ヴェ      ve\nヴォ      vo      ェ       xe      エ       e       ォ       xo      オ       o \n\nカ       ka      ガ       ga      キ       ki      キャ      kya     キュ      kyu \nキョ      kyo     ギ       gi      ギャ      gya     ギュ      gyu     ギョ      gyo \nク       ku      グ       gu      ケ       ke      ゲ       ge      コ       ko\nゴ       go \n\nサ       sa      ザ       za      シ       si      シャ      sya     シュ      syu \nショ      syo     シェ    sye\nジ       zi      ジャ      zya     ジュ      zyu     ジョ      zyo \nス       su      ズ       zu      セ       se      ゼ       ze      ソ       so\nゾ       zo \n\nタ       ta      ダ       da      チ       ti      チャ      tya     チュ      tyu \nチョ      tyo     ヂ       di      ヂャ      dya     ヂュ      dyu     ヂョ      dyo \nティ    ti\n\nッ       xtu \nッヴ      vvu     ッヴァ     vva     ッヴィ     vvi \nッヴェ     vve     ッヴォ     vvo \nッカ      kka     ッガ      gga     ッキ      kki     ッキャ     kkya \nッキュ     kkyu    ッキョ     kkyo    ッギ      ggi     ッギャ     ggya \nッギュ     ggyu    ッギョ     ggyo    ック      kku     ッグ      ggu \nッケ      kke     ッゲ      gge     ッコ      kko     ッゴ      ggo     ッサ      ssa \nッザ      zza     ッシ      ssi     ッシャ     ssya \nッシュ     ssyu    ッショ     ssyo    ッシェ     ssye\nッジ      zzi     ッジャ     zzya    ッジュ     zzyu    ッジョ     zzyo\nッス      ssu     ッズ      zzu     ッセ      sse     ッゼ      zze     ッソ      sso \nッゾ      zzo     ッタ      tta     ッダ      dda     ッチ      tti     ッティ  tti\nッチャ     ttya    ッチュ     ttyu    ッチョ     ttyo    ッヂ      ddi \nッヂャ     ddya    ッヂュ     ddyu    ッヂョ     ddyo    ッツ      ttu \nッヅ      ddu     ッテ      tte     ッデ      dde     ット      tto     ッド      ddo \nッドゥ  ddu\nッハ      hha     ッバ      bba     ッパ      ppa     ッヒ      hhi \nッヒャ     hhya    ッヒュ     hhyu    ッヒョ     hhyo    ッビ      bbi \nッビャ     bbya    ッビュ     bbyu    ッビョ     bbyo    ッピ      ppi \nッピャ     ppya    ッピュ     ppyu    ッピョ     ppyo    ッフ      hhu     ッフュ  ffu\nッファ     ffa     ッフィ     ffi     ッフェ     ffe     ッフォ     ffo \nッブ      bbu     ップ      ppu     ッヘ      hhe     ッベ      bbe     ッペ    ppe\nッホ      hho     ッボ      bbo     ッポ      ppo     ッヤ      yya     ッユ      yyu \nッヨ      yyo     ッラ      rra     ッリ      rri     ッリャ     rrya \nッリュ     rryu    ッリョ     rryo    ッル      rru     ッレ      rre \nッロ      rro \n\nツ       tu      ヅ       du      テ       te      デ       de      ト       to\nド       do      ドゥ    du\n\nナ       na      ニ       ni      ニャ      nya     ニュ      nyu     ニョ      nyo \nヌ       nu      ネ       ne      ノ       no \n\nハ       ha      バ       ba      パ       pa      ヒ       hi      ヒャ      hya \nヒュ      hyu     ヒョ      hyo     ビ       bi      ビャ      bya     ビュ      byu \nビョ      byo     ピ       pi      ピャ      pya     ピュ      pyu     ピョ      pyo \nフ       hu      ファ      fa      フィ      fi      フェ      fe      フォ      fo\nフュ    fu\nブ       bu      プ       pu      ヘ       he      ベ       be      ペ       pe\nホ       ho      ボ       bo      ポ       po \n\nマ       ma      ミ       mi      ミャ      mya     ミュ      myu     ミョ      myo \nム       mu      メ       me      モ       mo \n\nャ       xya     ヤ       ya      ュ       xyu     ユ       yu      ョ       xyo\nヨ       yo\n\nラ       ra      リ       ri      リャ      rya     リュ      ryu     リョ      ryo \nル       ru      レ       re      ロ       ro \n\nヮ       xwa     ワ       wa      ウィ    wi      ヰ wi      ヱ       we      ウェ      we\nヲ       wo      ウォ    wo      ン n \n\nン     n'\nディ   dyi\nー     -\nチェ    tye\nッチェ     ttye\nジェ      zye\n"
KUNREITAB_H = "ぁ      xa      あ      a      ぃ      xi      い      i      ぅ      xu\nう      u      う゛      vu      う゛ぁ      va      う゛ぃ      vi       う゛ぇ      ve\nう゛ぉ      vo      ぇ      xe      え      e      ぉ      xo      お      o \n\nか      ka      が      ga      き      ki      きゃ      kya      きゅ      kyu \nきょ      kyo      ぎ      gi      ぎゃ      gya      ぎゅ      gyu      ぎょ      gyo \nく      ku      ぐ      gu      け      ke      げ      ge      こ      ko\nご      go \n\nさ      sa      ざ      za      し      si      しゃ      sya      しゅ      syu \nしょ      syo      じ      zi      じゃ      zya      じゅ      zyu      じょ      zyo \nす      su      ず      zu      せ      se      ぜ      ze      そ      so\nぞ      zo \n\nた      ta      だ      da      ち      ti      ちゃ      tya      ちゅ      tyu \nちょ      tyo      ぢ      di      ぢゃ      dya      ぢゅ      dyu      ぢょ      dyo \n\nっ      xtu \nっう゛      vvu      っう゛ぁ      vva      っう゛ぃ      vvi \nっう゛ぇ      vve      っう゛ぉ      vvo \nっか      kka      っが      gga      っき      kki      っきゃ      kkya \nっきゅ      kkyu      っきょ      kkyo      っぎ      ggi      っぎゃ      ggya \nっぎゅ      ggyu      っぎょ      ggyo      っく      kku      っぐ      ggu \nっけ      kke      っげ      gge      っこ      kko      っご      ggo      っさ      ssa \nっざ      zza      っし      ssi      っしゃ      ssya \nっしゅ      ssyu      っしょ      ssyo \nっじ      zzi      っじゃ      zzya      っじゅ      zzyu      っじょ      zzyo \nっす      ssu      っず      zzu      っせ      sse      っぜ      zze      っそ      sso \nっぞ      zzo      った      tta      っだ      dda      っち      tti \nっちゃ      ttya      っちゅ      ttyu      っちょ      ttyo      っぢ      ddi \nっぢゃ      ddya      っぢゅ      ddyu      っぢょ      ddyo      っつ      ttu \nっづ      ddu      って      tte      っで      dde      っと      tto      っど      ddo \nっは      hha      っば      bba      っぱ      ppa      っひ      hhi \nっひゃ      hhya      っひゅ      hhyu      っひょ      hhyo      っび      bbi \nっびゃ      bbya      っびゅ      bbyu      っびょ      bbyo      っぴ      ppi \nっぴゃ      ppya      っぴゅ      ppyu      っぴょ      ppyo      っふ      hhu \nっふぁ      ffa      っふぃ      ffi      っふぇ      ffe      っふぉ      ffo \nっぶ      bbu      っぷ      ppu      っへ      hhe      っべ      bbe      っぺ    ppe\nっほ      hho      っぼ      bbo      っぽ      ppo      っや      yya      っゆ      yyu \nっよ      yyo      っら      rra      っり      rri      っりゃ      rrya \nっりゅ      rryu      っりょ      rryo      っる      rru      っれ      rre \nっろ      rro \n\nつ      tu      づ      du      て      te      で      de      と      to\nど      do \n\nな      na      に      ni      にゃ      nya      にゅ      nyu      にょ      nyo \nぬ      nu      ね      ne      の      no \n\nは      ha      ば      ba      ぱ      pa      ひ      hi      ひゃ      hya \nひゅ      hyu      ひょ      hyo      び      bi      びゃ      bya      びゅ      byu \nびょ      byo      ぴ      pi      ぴゃ      pya      ぴゅ      pyu      ぴょ      pyo \nふ      hu      ふぁ      fa      ふぃ      fi      ふぇ      fe      ふぉ      fo \nぶ      bu      ぷ      pu      へ      he      べ      be      ぺ      pe\nほ      ho      ぼ      bo      ぽ      po \n\nま      ma      み      mi      みゃ      mya      みゅ      myu      みょ      myo \nむ      mu      め      me      も      mo \n\nゃ      xya      や      ya      ゅ      xyu      ゆ      yu      ょ      xyo\nよ      yo\n\nら      ra      り      ri      りゃ      rya      りゅ      ryu      りょ      ryo \nる      ru      れ      re      ろ      ro \n\nゎ      xwa      わ      wa      ゐ      wi      ゑ      we\nを      wo      ん      n \n\nん     n'\nでぃ   dyi\nー     -\nちぇ    tye\nっちぇ      ttye\nじぇ      zye\n"
HEPBURNTAB = "ァ      xa      ア       a       ィ       xi      イ       i       ゥ       xu\nウ       u       ヴ       vu      ヴァ      va      ヴィ      vi      ヴェ      ve\nヴォ      vo      ェ       xe      エ       e       ォ       xo      オ       o\n        \n\nカ       ka      ガ       ga      キ       ki      キャ      kya     キュ      kyu\nキョ      kyo     ギ       gi      ギャ      gya     ギュ      gyu     ギョ      gyo\nク       ku      グ       gu      ケ       ke      ゲ       ge      コ       ko\nゴ       go      \n\nサ       sa      ザ       za      シ       shi     シャ      sha     シュ      shu\nショ      sho     シェ    she\nジ       ji      ジャ      ja      ジュ      ju      ジョ      jo\nス       su      ズ       zu      セ       se      ゼ       ze      ソ       so\nゾ       zo\n\nタ       ta      ダ       da      チ       chi     チャ      cha     チュ      chu\nチョ      cho     ヂ       di      ヂャ      dya     ヂュ      dyu     ヂョ      dyo\nティ    ti\n\nッ       xtsu    \nッヴ      vvu     ッヴァ     vva     ッヴィ     vvi     \nッヴェ     vve     ッヴォ     vvo     \nッカ      kka     ッガ      gga     ッキ      kki     ッキャ     kkya    \nッキュ     kkyu    ッキョ     kkyo    ッギ      ggi     ッギャ     ggya    \nッギュ     ggyu    ッギョ     ggyo    ック      kku     ッグ      ggu     \nッケ      kke     ッゲ      gge     ッコ      kko     ッゴ      ggo     ッサ      ssa\nッザ      zza     ッシ      sshi    ッシャ     ssha    \nッシュ     sshu    ッショ     ssho    ッシェ  sshe\nッジ      jji     ッジャ     jja     ッジュ     jju     ッジョ     jjo     \nッス      ssu     ッズ      zzu     ッセ      sse     ッゼ      zze     ッソ      sso\nッゾ      zzo     ッタ      tta     ッダ      dda     ッチ      cchi    ッティ  tti\nッチャ     ccha    ッチュ     cchu    ッチョ     ccho    ッヂ      ddi     \nッヂャ     ddya    ッヂュ     ddyu    ッヂョ     ddyo    ッツ      ttsu    \nッヅ      ddu     ッテ      tte     ッデ      dde     ット      tto     ッド      ddo\nッドゥ  ddu\nッハ      hha     ッバ      bba     ッパ      ppa     ッヒ      hhi     \nッヒャ     hhya    ッヒュ     hhyu    ッヒョ     hhyo    ッビ      bbi     \nッビャ     bbya    ッビュ     bbyu    ッビョ     bbyo    ッピ      ppi     \nッピャ     ppya    ッピュ     ppyu    ッピョ     ppyo    ッフ      ffu     ッフュ  ffu\nッファ     ffa     ッフィ     ffi     ッフェ     ffe     ッフォ     ffo     \nッブ      bbu     ップ      ppu     ッヘ      hhe     ッベ      bbe     ッペ      ppe\nッホ      hho     ッボ      bbo     ッポ      ppo     ッヤ      yya     ッユ      yyu\nッヨ      yyo     ッラ      rra     ッリ      rri     ッリャ     rrya    \nッリュ     rryu    ッリョ     rryo    ッル      rru     ッレ      rre     \nッロ      rro     \n\nツ       tsu     ヅ       du      テ       te      デ       de      ト       to\nド       do      ドゥ    du\n\nナ       na      ニ       ni      ニャ      nya     ニュ      nyu     ニョ      nyo\nヌ       nu      ネ       ne      ノ       no      \n\nハ       ha      バ       ba      パ       pa      ヒ       hi      ヒャ      hya\nヒュ      hyu     ヒョ      hyo     ビ       bi      ビャ      bya     ビュ      byu\nビョ      byo     ピ       pi      ピャ      pya     ピュ      pyu     ピョ      pyo\nフ       fu      ファ      fa      フィ      fi      フェ      fe      フォ      fo\nフュ    fu\nブ       bu      プ       pu      ヘ       he      ベ       be      ペ       pe\nホ       ho      ボ       bo      ポ       po      \n\nマ       ma      ミ       mi      ミャ      mya     ミュ      myu     ミョ      myo\nム       mu      メ       me      モ       mo\n\nャ       xya     ヤ       ya      ュ       xyu     ユ       yu      ョ       xyo\nヨ       yo      \n\nラ       ra      リ       ri      リャ      rya     リュ      ryu     リョ      ryo\nル       ru      レ       re      ロ       ro      \n\nヮ       xwa     ワ       wa      ウィ    wi      ヰ wi      ヱ       we      ウェ    we\nヲ       wo      ウォ    wo      ン n       \n\nン     n'\nディ   di\nー     -\nチェ    che\nッチェ     cche\nジェ      je\n"
HEPBURNTAB_H = "ぁ      xa      あ      a      ぃ      xi      い      i      ぅ      xu\nう      u      う゛      vu      う゛ぁ      va      う゛ぃ      vi      う゛ぇ      ve\nう゛ぉ      vo      ぇ      xe      え      e      ぉ      xo      お      o\n\n\nか      ka      が      ga      き      ki      きゃ      kya      きゅ      kyu\nきょ      kyo      ぎ      gi      ぎゃ      gya      ぎゅ      gyu      ぎょ      gyo\nく      ku      ぐ      gu      け      ke      げ      ge      こ      ko\nご      go      \n\nさ      sa      ざ      za      し      shi      しゃ      sha      しゅ      shu\nしょ      sho      じ      ji      じゃ      ja      じゅ      ju      じょ      jo\nす      su      ず      zu      せ      se      ぜ      ze      そ      so\nぞ      zo\n\nた      ta      だ      da      ち      chi      ちゃ      cha      ちゅ      chu\nちょ      cho      ぢ      di      ぢゃ      dya      ぢゅ      dyu      ぢょ      dyo\n\nっ      xtsu      \nっう゛      vvu      っう゛ぁ      vva      っう゛ぃ      vvi      \nっう゛ぇ      vve      っう゛ぉ      vvo      \nっか      kka      っが      gga      っき      kki      っきゃ      kkya      \nっきゅ      kkyu      っきょ      kkyo      っぎ      ggi      っぎゃ      ggya      \nっぎゅ      ggyu      っぎょ      ggyo      っく      kku      っぐ      ggu      \nっけ      kke      っげ      gge      っこ      kko      っご      ggo      っさ      ssa\nっざ      zza      っし      sshi      っしゃ      ssha      \nっしゅ      sshu      っしょ      ssho      \nっじ      jji      っじゃ      jja      っじゅ      jju      っじょ      jjo      \nっす      ssu      っず      zzu      っせ      sse      っぜ      zze      っそ      sso\nっぞ      zzo      った      tta      っだ      dda      っち      cchi      \nっちゃ      ccha      っちゅ      cchu      っちょ      ccho      っぢ      ddi      \nっぢゃ      ddya      っぢゅ      ddyu      っぢょ      ddyo      っつ      ttsu      \nっづ      ddu      って      tte      っで      dde      っと      tto      っど      ddo\nっは      hha      っば      bba      っぱ      ppa      っひ      hhi      \nっひゃ      hhya      っひゅ      hhyu      っひょ      hhyo      っび      bbi      \nっびゃ      bbya      っびゅ      bbyu      っびょ      bbyo      っぴ      ppi      \nっぴゃ      ppya      っぴゅ      ppyu      っぴょ      ppyo      っふ      ffu      \nっふぁ      ffa      っふぃ      ffi      っふぇ      ffe      っふぉ      ffo      \nっぶ      bbu      っぷ      ppu      っへ      hhe      っべ      bbe      っぺ      ppe\nっほ      hho      っぼ      bbo      っぽ      ppo      っや      yya      っゆ      yyu\nっよ      yyo      っら      rra      っり      rri      っりゃ      rrya      \nっりゅ      rryu      っりょ      rryo      っる      rru      っれ      rre      \nっろ      rro      \n\nつ      tsu      づ      du      て      te      で      de      と      to\nど      do      \n\nな      na      に      ni      にゃ      nya      にゅ      nyu      にょ      nyo\nぬ      nu      ね      ne      の      no      \n\nは      ha      ば      ba      ぱ      pa      ひ      hi      ひゃ      hya\nひゅ      hyu      ひょ      hyo      び      bi      びゃ      bya      びゅ      byu\nびょ      byo      ぴ      pi      ぴゃ      pya      ぴゅ      pyu      ぴょ      pyo\nふ      fu      ふぁ      fa      ふぃ      fi      ふぇ      fe      ふぉ      fo\nぶ      bu      ぷ      pu      へ      he      べ      be      ぺ      pe\nほ      ho      ぼ      bo      ぽ      po      \n\nま      ma      み      mi      みゃ      mya      みゅ      myu      みょ      myo\nむ      mu      め      me      も      mo\n\nゃ      xya      や      ya      ゅ      xyu      ゆ      yu      ょ      xyo\nよ      yo      \n\nら      ra      り      ri      りゃ      rya      りゅ      ryu      りょ      ryo\nる      ru      れ      re      ろ      ro      \n\nゎ      xwa      わ      wa      ゐ      wi      ゑ      we\nを      wo      ん      n      \n\nん     n'\nでぃ   dyi\nー     -\nちぇ    che\nっちぇ      cche\nじぇ      je\n"

def pairs(arr, size=2):
    for i in range(0, len(arr) - 1, size):
        yield arr[i:i + size]


KANROM = {}
ROMKAN = {}
for pair in pairs(re.split('\\s+', KUNREITAB + HEPBURNTAB)):
    kana, roma = pair
    KANROM[kana] = roma
    ROMKAN[roma] = kana

ROMKAN.update({'du': 'ヅ',  'di': 'ヂ',  'fu': 'フ',  'ti': 'チ',  'wi': 'ウィ', 
 'we': 'ウェ',  'wo': 'ヲ'})
_len_cmp = lambda x: -len(x)
ROMPAT = re.compile('|'.join(sorted(ROMKAN.keys(), key=_len_cmp)))
_kanpat_cmp = lambda x, y: (len(y) > len(x)) - (len(y) < len(x)) or (len(KANROM[x]) > len(KANROM[x])) - (len(KANROM[x]) < len(KANROM[x]))
KANPAT = re.compile('|'.join(sorted(KANROM.keys(), key=cmp_to_key(_kanpat_cmp))))
KUNREI = [y for x, y in pairs(re.split('\\s+', KUNREITAB))]
HEPBURN = [y for x, y in pairs(re.split('\\s+', HEPBURNTAB))]
KUNPAT = re.compile('|'.join(sorted(KUNREI, key=_len_cmp)))
HEPPAT = re.compile('|'.join(sorted(HEPBURN, key=_len_cmp)))
TO_HEPBURN = {}
TO_KUNREI = {}
for kun, hep in zip(KUNREI, HEPBURN):
    TO_HEPBURN[kun] = hep
    TO_KUNREI[hep] = kun

TO_HEPBURN.update({'ti': 'chi'})
KANROM_H = {}
ROMKAN_H = {}
for pair in pairs(re.split('\\s+', KUNREITAB_H + HEPBURNTAB_H)):
    kana, roma = pair
    KANROM_H[kana] = roma
    ROMKAN_H[roma] = kana

ROMKAN_H.update({'du': 'づ',  'di': 'ぢ',  'fu': 'ふ',  'ti': 'ち',  'wi': 'うぃ', 
 'we': 'うぇ',  'wo': 'を'})
_len_cmp = lambda x: -len(x)
ROMPAT_H = re.compile('|'.join(sorted(ROMKAN_H.keys(), key=_len_cmp)))
_kanpat_cmp = lambda x, y: (len(y) > len(x)) - (len(y) < len(x)) or (len(KANROM_H[x]) > len(KANROM_H[x])) - (len(KANROM_H[x]) < len(KANROM_H[x]))
KANPAT_H = re.compile('|'.join(sorted(KANROM_H.keys(), key=cmp_to_key(_kanpat_cmp))))
KUNREI_H = [y for x, y in pairs(re.split('\\s+', KUNREITAB_H))]
HEPBURN_H = [y for x, y in pairs(re.split('\\s+', HEPBURNTAB_H))]
KUNPAT_H = re.compile('|'.join(sorted(KUNREI_H, key=_len_cmp)))
HEPPAT_H = re.compile('|'.join(sorted(HEPBURN_H, key=_len_cmp)))
TO_HEPBURN_H = {}
TO_KUNREI_H = {}
for kun, hep in zip(KUNREI_H, HEPBURN_H):
    TO_HEPBURN_H[kun] = hep
    TO_KUNREI_H[hep] = kun

TO_HEPBURN_H.update({'ti': 'chi'})

def normalize_double_n(str):
    """
    Normalize double n.
    """
    str = re.sub('nn', "n'", str)
    str = re.sub("n'(?=[^aiueoyn]|$)", 'n', str)
    return str


def to_katakana(str):
    """
    Convert a Romaji (ローマ字) to a Katakana (片仮名).
    """
    str = str.lower()
    str = normalize_double_n(str)
    tmp = ROMPAT.sub(lambda x: ROMKAN[x.group(0)], str)
    return tmp


def to_hiragana(str):
    """
    Convert a Romaji (ローマ字) to a Hiragana (平仮名).
    """
    str = str.lower()
    str = normalize_double_n(str)
    tmp = ROMPAT_H.sub(lambda x: ROMKAN_H[x.group(0)], str)
    return tmp


def to_kana(str):
    """
    Convert a Romaji (ローマ字) to a Katakana (片仮名). (same as to_katakana)
    """
    return to_katakana(str)


def to_hepburn(str):
    """
    Convert a Kana (仮名) or a Kunrei-shiki Romaji (訓令式ローマ字) to a Hepburn Romaji (ヘボン式ローマ字).
    """
    tmp = str
    tmp = KANPAT.sub(lambda x: KANROM[x.group(0)], tmp)
    tmp = KANPAT_H.sub(lambda x: KANROM_H[x.group(0)], tmp)
    tmp = re.sub("n'(?=[^aeiuoyn]|$)", 'n', tmp)
    if tmp == str:
        tmp = tmp.lower()
        tmp = normalize_double_n(tmp)
        tmp = KUNPAT.sub(lambda x: TO_HEPBURN[x.group(0)], tmp)
    return tmp


def to_kunrei(str):
    """
    Convert a Kana (仮名) or a Hepburn Romaji (ヘボン式ローマ字) to a Kunrei-shiki Romaji (訓令式ローマ字).
    """
    tmp = str
    tmp = KANPAT.sub(lambda x: KANROM[x.group(0)], tmp)
    tmp = KANPAT_H.sub(lambda x: KANROM_H[x.group(0)], tmp)
    tmp = re.sub("n'(?=[^aeiuoyn]|$)", 'n', tmp)
    tmp = tmp.lower()
    tmp = normalize_double_n(tmp)
    tmp = HEPPAT.sub(lambda x: TO_KUNREI[x.group(0)], tmp)
    return tmp


def to_roma(str):
    """
    Convert a Kana (仮名) to a Hepburn Romaji (ヘボン式ローマ字).
    """
    tmp = str
    tmp = KANPAT.sub(lambda x: KANROM[x.group(0)], tmp)
    tmp = KANPAT_H.sub(lambda x: KANROM_H[x.group(0)], tmp)
    tmp = re.sub("n'(?=[^aeiuoyn]|$)", 'n', tmp)
    return tmp


def is_consonant(str):
    """
    Return a MatchObject if a Latin letter is a consonant in Japanese.
    Return None otherwise.
    """
    str = str.lower()
    return re.match('[ckgszjtdhfpbmyrwxn]', str)


def is_vowel(str):
    """
    Return a MatchObject if a Latin letter is a vowel in Japanese.
    Return None otherwise.
    """
    str = str.lower()
    return re.match('[aeiou]', str)


def expand_consonant(str):
    """
    Expand consonant to its related moras.
    Example: 'sh' => ['sha', 'she', 'shi', 'sho', 'shu']
    """
    str = str.lower()
    return sorted([mora for mora in ROMKAN.keys() if re.match('^%s.$' % str, mora)])