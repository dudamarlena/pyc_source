# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/LiveChat/browser/emoticons.py
# Compiled at: 2008-07-25 11:17:39
import re
emoticons = {':)': '<img src="++resource++qi.LiveChat.resources/smiley_smile.png" alt=":)" title="Smile" />', ':(': '<img src="++resource++qi.LiveChat.resources/smiley_sad.png" alt=":(" title="Sad" />', '8-)': '<img src="++resource++qi.LiveChat.resources/smiley_cool.png" alt="8)" title="Cool" />', ':D': '<img src="++resource++qi.LiveChat.resources/smiley_lol.png" alt=":D" title="Big grin" />', ':|': '<img src="++resource++qi.LiveChat.resources/smiley_skeptic.png" alt=":|" title="Skeptic" />', ':o': '<img src="++resource++qi.LiveChat.resources/smiley_surprised.png" alt=":o" title="Surprised" />', ':P': '<img src="++resource++qi.LiveChat.resources/smiley_tongue.png" alt=":P" title="Tongue-in-cheek" />', ';)': '<img src="++resource++qi.LiveChat.resources/smiley_wink.png" alt=";)" title="Wink" />', ':-)': '<img src="++resource++qi.LiveChat.resources/smiley_smile.png" alt=":)" title="Smile" />', ':-(': '<img src="++resource++qi.LiveChat.resources/smiley_sad.png" alt=":(" title="Sad" />', ':-D': '<img src="++resource++qi.LiveChat.resources/smiley_lol.png" alt=":D" title="Big grin" />', ':-|': '<img src="++resource++qi.LiveChat.resources/smiley_skeptic.png" alt=":|" title="Skeptic" />', ':-o': '<img src="++resource++qi.LiveChat.resources/smiley_surprised.png" alt=":o" title="Surprised" />', ':-P': '<img src="++resource++qi.LiveChat.resources/smiley_tongue.png" alt=":P" title="Tongue-in-cheek" />', ';-)': '<img src="++resource++qi.LiveChat.resources/smiley_wink.png" alt=";)" title="Wink" />'}
regex = re.compile('(%s)(?!")' % ('|').join(map(re.escape, emoticons.keys())))

def replaceEmoticons(text):
    """
    """
    return regex.sub(lambda mo, d=emoticons: d[mo.string[mo.start():mo.end()]], text)