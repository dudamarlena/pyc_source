# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\Subrata Sarkar\Text\Class XI\kaka\bangla key1.4\banglakey1.4\BanglaKey 3.0\pybengengphonetic\conparse.py
# Compiled at: 2016-09-25 01:36:37
__doc__ = "This tool converts unicode data to speakable pyttsx data\n   using convert_to_pyttsx_speakable() and converts unicode data to speakable\n   phonetic using convert_to_speakable_phonetic() and speak bengali\n   using speak()\nExample:convert_to_pyttsx_speakable(u'\\u09A2\\u09A0')\n        speak(u'\\u09A2\\u09A0')"

def convert_to_pyttsx_speakable(gitre=''):
    text2 = ''
    count = 0
    import string
    for letter in gitre:
        if count != 0:
            try:
                str(letter)
                text2 += letter
            except UnicodeEncodeError:
                matra = 'অআইঈউঊঋঌএঐওঔািীুূৃেৈোৌ'
                try:
                    if letter in matra:
                        text2 += letter
                    elif letter in unicode(string.printable):
                        text2 = text2 + letter
                    else:
                        text2 = text2 + letter + 'a'
                except:
                    text2 += letter

        else:
            count += 1

    gitre = text2
    import hinavro
    gitre = hinavro.parse(gitre)
    return gitre


def convert_to_speakable_phonetic(gitre=''):
    text2 = ''
    count = 0
    import string
    for letter in gitre:
        if count != 0:
            try:
                str(letter)
                text2 += letter
            except UnicodeEncodeError:
                matra = 'অআইঈউঊঋঌএঐওঔািীুূৃেৈোৌ'
                try:
                    if letter in matra:
                        text2 += letter
                    elif letter in unicode(string.printable):
                        text2 = text2 + letter
                    else:
                        text2 = text2 + letter + 'o'
                except:
                    text2 += letter

        else:
            count += 1


def speak(text=''):
    import pyttsx
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 60)
    speakman1 = convert_to_pyttsx_speakable(gitre=text)
    engine.say(speakman1)
    engine.runAndWait()
    return 'Speak Over'


if __name__ == '__main__':
    speak('ঢঠ')