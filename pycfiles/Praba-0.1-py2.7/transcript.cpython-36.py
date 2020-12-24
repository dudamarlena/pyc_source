# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/textgrids/transcript.py
# Compiled at: 2020-01-21 09:57:13
# Size of source mod 2**32: 10552 bytes
__doc__ = 'transcript.py -- Praat-to-Unicode transcription conversions\n\n  A str-derived class for handling Praat-to-Unicode and Unicode-to-Praat\n  transcription conversions.\n\n  2019-07-11    Separated from textgrids module.\n  2019-08-04    Corrected "unrounded open back" symbol.\n\n'
symbols = {'\\i-':'ɨ', 
 '\\u-':'ʉ', 
 '\\mt':'ɯ', 
 '\\ic':'ɪ', 
 '\\yc':'ʏ', 
 '\\hs':'ʊ', 
 '\\o/':'ø', 
 '\\e-':'ɘ', 
 '\\o-':'ɵ', 
 '\\rh':'ɤ', 
 '\\sw':'ə', 
 '\\ef':'ɛ', 
 '\\oe':'œ', 
 '\\er':'ɜ', 
 '\\kb':'ɞ', 
 '\\vt':'ʌ', 
 '\\ct':'ɔ', 
 '\\ae':'æ', 
 '\\at':'ɐ', 
 '\\Oe':'ɶ', 
 '\\as':'ɑ', 
 '\\ab':'ɒ'}
vowels = list('aeiouyæø') + list(symbols.keys()) + list(symbols.values())
symbols.update({'\\t.':'ʈ',  '\\?-':'ʡ', 
 '\\?g':'ʔ', 
 '\\d.':'ɖ', 
 '\\j-':'ɟ', 
 '\\gs':'ɡ', 
 '\\gc':'ɢ', 
 '\\mj':'ɱ', 
 '\\n.':'ɳ', 
 '\\ng':'ŋ', 
 '\\nc':'ɴ', 
 '\\ff':'ɸ', 
 '\\tf':'Ɵ', 
 '\\l-':'ɬ', 
 '\\sh':'ʃ', 
 '\\s.':'ʂ', 
 '\\cc':'ɕ', 
 '\\c,':'ç', 
 '\\wt':'ʍ', 
 '\\cf':'χ', 
 '\\h-':'ħ', 
 '\\hc':'ʜ', 
 '\\bf':'β', 
 '\\dh':'ð', 
 '\\lz':'ɮ', 
 '\\zh':'ʒ', 
 '\\z.':'ʐ', 
 '\\zc':'ʑ', 
 '\\jc':'ʝ', 
 '\\gf':'ɣ', 
 '\\ri':'ʁ', 
 '\\9e':'ʕ', 
 '\\9-':'ʢ', 
 '\\h^':'ɦ', 
 '\\vs':'ʋ', 
 '\\rt':'ɹ', 
 '\\r.':'ɻ', 
 '\\ht':'ɥ', 
 '\\ml':'ɰ', 
 '\\bc':'ʙ', 
 '\\rc':'ʀ', 
 '\\fh':'ɾ', 
 '\\rl':'ɺ', 
 '\\f.':'ɽ', 
 '\\l.':'ɭ', 
 '\\yt':'ʎ', 
 '\\lc':'ʟ', 
 '\\b^':'ɓ', 
 '\\d^':'ɗ', 
 '\\j^':'ʄ', 
 '\\g^':'ɠ', 
 '\\G^':'ʛ', 
 '\\O.':'ʘ', 
 '\\|1':'ǀ', 
 '\\|2':'ǁ', 
 '\\|-':'ǂ', 
 '\\l~':'ɫ', 
 '\\hj':'ɧ'})
inline_diacritics = {'\\:f':'ː', 
 '\\.f':'ˑ', 
 "\\'1":'ˈ', 
 "\\'2":'ˌ', 
 '\\|f':'|', 
 '\\cn':'̚', 
 '\\er':'˞'}
index_diacritics = {'\\|v':'̩', 
 '\\0v':'̥', 
 '\\Tv':'̞', 
 '\\T^':'̝', 
 '\\T(':'̘', 
 '\\T)':'̙', 
 '\\-v':'̠', 
 '\\+v':'̟', 
 '\\:v':'̤', 
 '\\~v':'̰', 
 '\\Nv':'̪', 
 '\\Uv':'̺', 
 '\\Dv':'̻', 
 '\\nv':'̯', 
 '\\3v':'̹', 
 '\\cv':'̜', 
 '\\0^':'̊', 
 "\\'^":'́', 
 '\\`^':'̀', 
 '\\-^':'̄', 
 '\\~^':'̃', 
 '\\v^':'̌', 
 '\\^^':'̂', 
 '\\:^':'̈', 
 '\\N^':'̆', 
 '\\li':'͡'}
diacritics = inline_diacritics.copy()
diacritics.update(index_diacritics)

class Transcript(str):
    """Transcript"""

    def transcode(self, to_unicode=True, retain_diacritics=False):
        """Provide Praat-to-Unicode and Unicode-to-Praat transcoding.

        Unless to_unicode is False, Praat-to-Unicode is assumed, otherwise
        Unicode-to-Praat.

        If retain_diacritics is False (the default), removes over/understrike
        (i.e., “index”) diacritics (usually best practice for graphs).
        """
        global index_diacritics
        global inline_diacritics
        global symbols
        out = str(self)
        if not to_unicode:
            if retain_diacritics:
                for uni in index_diacritics.values():
                    p = out.find(uni)
                    while p >= 0:
                        out = out[:p] + out[(p + 1)] + out[p] + out[p + 2:]
                        p = out.find(uni, p + 2)

            else:
                for uni in index_diacritics.values():
                    out = out.replace(uni, '')

        inline_symbols = symbols.copy()
        inline_symbols.update(inline_diacritics)
        for praat, uni in inline_symbols.items():
            if to_unicode:
                out = out.replace(praat, uni)
            else:
                out = out.replace(uni, praat)

        if to_unicode and retain_diacritics:
            for praat in index_diacritics:
                p = 0
                while out.find(praat, p) > 0:
                    p = out.index('\\')
                    out = out[:p - 1] + index_diacritics[out[p:p + 3]] + out[(p - 1)] + out[p + 3:]
                    p += 2

        for praat, uni in index_diacritics.items():
            if to_unicode:
                out = out.replace(praat, uni if retain_diacritics else '')
            elif retain_diacritics:
                out = out.replace(uni, praat)

        return out