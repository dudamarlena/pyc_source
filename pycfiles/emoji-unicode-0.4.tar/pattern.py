# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esteban/PycharmProjects/emoji-awesome/emoji_unicode/pattern.py
# Compiled at: 2015-11-18 15:42:07
from __future__ import unicode_literals
CODE_POINTS = b'©®‼⁉™ℹ↔-↙↩-↪⌚-⌛⌨⏏⏩-⏳⏸-⏺Ⓜ▪-▫▶◀◻-◾☀-☄☎☑☔-☕☘☝☠☢-☣☦☪☮-☯☸-☺♈-♓♠♣♥-♦♨♻♿⚒-⚔⚖-⚗⚙⚛-⚜⚠-⚡⚪-⚫⚰-⚱⚽-⚾⛄-⛅⛈⛎-⛏⛑⛓-⛔⛩-⛪⛰-⛵⛷-⛺⛽✂✅✈-✍✏✒✔✖✝✡✨✳-✴❄❇❌❎❓-❕❗❣-❤➕-➗➡➰➿⤴-⤵⬅-⬇⬛-⬜⭐⭕〰〽㊗㊙🀄🃏🅰-🅱🅾-🅿🆎🆑-🆚🇦-🇿🈁-🈂🈚🈯🈲-🈺🉐-🉑🌀-🌡🌤-🎓🎖-🎗🎙-🎛🎞-🏰🏳-🏵🏷-📽📿-🔽🕉-🕎🕐-🕧🕯-🕰🕳-🕹🖇🖊-🖍🖐🖕-🖖🖥🖨🖱-🖲🖼🗂-🗄🗑-🗓🗜-🗞🗡🗣🗨🗯🗳🗺-🙏🚀-🛅🛋-🛐🛠-🛥🛩🛫-🛬🛰🛳🤐-🤘🦀-🦄🧀'
TXT_VARIATION = b'︎'
EMO_VARIATION = b'️'
FITZ_MODIFIER = b'🏻-🏿'
KC_MODIFIER = b'⃣'
ZWJ = b'\u200d'
FLAGS = b'🇦-🇿'
KEY_CAPS = b'0-9\\*#'
RE_PATTERN_TEMPLATE = b'(?P<emoji>(?:(?:[%(key_caps)s](?:%(emo_variation)s)?%(kc_modifier)s)|(?:[%(flags)s]){2}|(?:[%(emojis)s])(?!%(txt_variation)s))(?:(?:(?:%(emo_variation)s)?(?:[%(fitz_modifier)s]))|(?:(?:%(emo_variation)s)?(?:[%(zwj)s])(?:.)){1,4}|(?:%(emo_variation)s))?)' % {b'emojis': CODE_POINTS, 
   b'txt_variation': TXT_VARIATION, 
   b'emo_variation': EMO_VARIATION, 
   b'fitz_modifier': FITZ_MODIFIER, 
   b'zwj': ZWJ, 
   b'flags': FLAGS, 
   b'kc_modifier': KC_MODIFIER, 
   b'key_caps': KEY_CAPS}