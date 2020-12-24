# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esteban/PycharmProjects/emoji-unicode/emoji_unicode/pattern.py
# Compiled at: 2016-12-12 12:23:54
# Size of source mod 2**32: 2712 bytes
from __future__ import unicode_literals
CODE_POINTS = '©®‼⁉™ℹ↔-↙↩-↪⌚-⌛⌨⏏⏩-⏳⏸-⏺Ⓜ▪-▫▶◀◻-◾☀-☄☎☑☔-☕☘☝☠☢-☣☦☪☮-☯☸-☺♈-♓♠♣♥-♦♨♻♿⚒-⚔⚖-⚗⚙⚛-⚜⚠-⚡⚪-⚫⚰-⚱⚽-⚾⛄-⛅⛈⛎-⛏⛑⛓-⛔⛩-⛪⛰-⛵⛷-⛺⛽✂✅✈-✍✏✒✔✖✝✡✨✳-✴❄❇❌❎❓-❕❗❣-❤➕-➗➡➰➿⤴-⤵⬅-⬇⬛-⬜⭐⭕〰〽㊗㊙🀄🃏🅰-🅱🅾-🅿🆎🆑-🆚🇦-🇿🈁-🈂🈚🈯🈲-🈺🉐-🉑🌀-🌡🌤-🎓🎖-🎗🎙-🎛🎞-🏰🏳-🏵🏷-📽📿-🔽🕉-🕎🕐-🕧🕯-🕰🕳-🕹🖇🖊-🖍🖐🖕-🖖🖥🖨🖱-🖲🖼🗂-🗄🗑-🗓🗜-🗞🗡🗣🗨🗯🗳🗺-🙏🚀-🛅🛋-🛐🛠-🛥🛩🛫-🛬🛰🛳🤐-🤘🦀-🦄🧀'
TXT_VARIATION = '︎'
EMO_VARIATION = '️'
FITZ_MODIFIER = '🏻-🏿'
KC_MODIFIER = '⃣'
ZWJ = '\u200d'
FLAGS = '🇦-🇿'
KEY_CAPS = '0-9\\*#'
RE_PATTERN_TEMPLATE = '(?P<emoji>(?:(?:[%(key_caps)s](?:%(emo_variation)s)?%(kc_modifier)s)|(?:[%(flags)s]){2}|(?:[%(emojis)s])(?!%(txt_variation)s))(?:(?:(?:%(emo_variation)s)?(?:[%(fitz_modifier)s]))|(?:(?:%(emo_variation)s)?(?:[%(zwj)s])(?:.)){1,4}|(?:%(emo_variation)s))?)' % {'emojis': CODE_POINTS, 
 'txt_variation': TXT_VARIATION, 
 'emo_variation': EMO_VARIATION, 
 'fitz_modifier': FITZ_MODIFIER, 
 'zwj': ZWJ, 
 'flags': FLAGS, 
 'kc_modifier': KC_MODIFIER, 
 'key_caps': KEY_CAPS}