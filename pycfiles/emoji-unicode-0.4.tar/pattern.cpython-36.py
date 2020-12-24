# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esteban/PycharmProjects/emoji-unicode/emoji_unicode/pattern.py
# Compiled at: 2017-10-10 17:02:27
# Size of source mod 2**32: 3949 bytes
from __future__ import unicode_literals
CODE_POINTS = '©®‼⁉™ℹ↔-↙↩-↪⌚-⌛⌨⏏⏩-⏳⏸-⏺Ⓜ▪-▫▶◀◻-◾☀-☄☎☑☔-☕☘☝☠☢-☣☦☪☮-☯☸-☺♀♂♈-♓♠♣♥-♦♨♻♿⚒-⚗⚙⚛-⚜⚠-⚡⚪-⚫⚰-⚱⚽-⚾⛄-⛅⛈⛎⛏⛑⛓-⛔⛩-⛪⛰-⛵⛷-⛺⛽✂✅✈-✉✊-✋✌-✍✏✒✔✖✝✡✨✳-✴❄❇❌❎❓-❕❗❣-❤➕-➗➡➰➿⤴-⤵⬅-⬇⬛-⬜⭐⭕〰〽㊗㊙🀄🃏🅰-🅱🅾🅿🆎🆑-🆚🇦-🇿🈁-🈂🈚🈯🈲-🈺🉐-🉑🌀-🌠🌡🌤-🌬🌭-🌯🌰-🌵🌶🌷-🍼🍽🍾-🍿🎀-🎓🎖-🎗🎙-🎛🎞-🎟🎠-🏄🏅🏆-🏊🏋-🏎🏏-🏓🏔-🏟🏠-🏰🏳-🏵🏷🏸-🏿🐀-🐾🐿👀👁👂-📷📸📹-📼📽📿🔀-🔽🕉-🕊🕋-🕎🕐-🕧🕯-🕰🕳-🕹🕺🖇🖊-🖍🖐🖕-🖖🖤🖥🖨🖱-🖲🖼🗂-🗄🗑-🗓🗜-🗞🗡🗣🗨🗯🗳🗺🗻-🗿😀😁-😐😑😒-😔😕😖😗😘😙😚😛😜-😞😟😠-😥😦-😧😨-😫😬😭😮-😯😰-😳😴😵-🙀🙁-🙂🙃-🙄🙅-🙏🚀-🛅🛋-🛏🛐🛑-🛒🛠-🛥🛩🛫-🛬🛰🛳🛴-🛶\U0001f6f7-\U0001f6f8🤐-🤘🤙-🤞\U0001f91f🤠-🤧\U0001f928-\U0001f92f🤰\U0001f931-\U0001f932🤳-🤺🤼-🤾🥀-🥅🥇-🥋\U0001f94c🥐-🥞\U0001f95f-\U0001f96b🦀-🦄🦅-🦑\U0001f992-\U0001f997🧀\U0001f9d0-\U0001f9e6'
TXT_VARIATION = '︎'
EMO_VARIATION = '️'
FITZ_MODIFIER = '🏻-🏿'
KC_MODIFIER = '⃣'
ZWJ = '\u200d'
FLAGS = '🇦-🇿'
KEY_CAPS = '0-9\\*#'
RE_PATTERN_TEMPLATE = '(?P<emoji>(?:(?:[%(key_caps)s](?:%(emo_variation)s)?%(kc_modifier)s)|(?:[%(flags)s]){2}|(?:[%(emojis)s])(?!%(txt_variation)s))(?:(?:(?:%(emo_variation)s)?(?:[%(fitz_modifier)s]))|(?:(?:%(emo_variation)s)?(?:[%(zwj)s])(?:.)){1,4}|(?:%(emo_variation)s))?)' % {'emojis':CODE_POINTS, 
 'txt_variation':TXT_VARIATION, 
 'emo_variation':EMO_VARIATION, 
 'fitz_modifier':FITZ_MODIFIER, 
 'zwj':ZWJ, 
 'flags':FLAGS, 
 'kc_modifier':KC_MODIFIER, 
 'key_caps':KEY_CAPS}