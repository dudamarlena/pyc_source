# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/usfm2osis/convert.py
# Compiled at: 2015-05-07 21:33:17
"""usfm2osis.convert

Copyright 2012-2015 by Christopher C. Little

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

The full text of the GNU General Public License is available at:
<http://www.gnu.org/licenses/gpl-3.0.txt>.
"""
from __future__ import unicode_literals
import re, codecs
from encodings.aliases import aliases
from .bookdata import specialBooks, peripherals, introPeripherals, bookDict
from .util import verbosePrint
from ._compat import _unichr

def convertToOsis(sFile, relaxedConformance=False, encoding=b'', debug=False, verbose=False):
    """Open a USFM file and return a string consisting of its OSIS equivalent.

    Keyword arguments:
    sFile -- Path to the USFM file to be converted

    """
    verbosePrint(b'Processing: ' + sFile, verbose)

    def cvtPreprocess(osis, relaxedConformance):
        """Perform preprocessing on a USFM document, returning the processed
        text as a string.
        Removes excess spaces & CRs and escapes XML entities.

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\n\\s*([^\\\\s])', b' \\1', osis)
        osis = osis.replace(b'\r', b'\n')
        osis = re.sub(b'\\s+\n', b'\n', osis)
        osis = osis.replace(b'&', b'&amp;')
        osis = osis.replace(b'<', b'&lt;')
        osis = osis.replace(b'>', b'&gt;')
        return osis

    def cvtRelaxedConformanceRemaps(osis, relaxedConformance):
        """Perform preprocessing on a USFM document, returning the processed
        text as a string.
        Remaps certain deprecated USFM tags to recommended alternatives.

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        if not relaxedConformance:
            return osis
        osis = re.sub(b'\\\\tr\\d\\b', b'\\\\tr', osis)
        osis = re.sub(b'\\\\pub\\b\\s', b'\\periph Publication Data\n', osis)
        osis = re.sub(b'\\\\toc\\b\\s', b'\\periph Table of Contents\n', osis)
        osis = re.sub(b'\\\\pref\\b\\s', b'\\periph Preface\n', osis)
        osis = re.sub(b'\\\\maps\\b\\s', b'\\periph Map Index\n', osis)
        osis = re.sub(b'\\\\cov\\b\\s', b'\\periph Cover\n', osis)
        osis = re.sub(b'\\\\spine\\b\\s', b'\\periph Spine\n', osis)
        osis = re.sub(b'\\\\pubinfo\\b\\s', b'\\periph Publication Information\n', osis)
        osis = re.sub(b'\\\\intro\\b\\s', b'\\id INT\n', osis)
        osis = re.sub(b'\\\\conc\\b\\s', b'\\id CNC\n', osis)
        osis = re.sub(b'\\\\glo\\b\\s', b'\\id GLO\n', osis)
        osis = re.sub(b'\\\\idx\\b\\s', b'\\id TDX\n', osis)
        return osis

    def cvtIdentification(osis, relaxedConformance):
        r"""Converts USFM **Identification** tags to OSIS, returning the
        processed text as a string.

        Supported tags: \id, \ide, \sts, 
em, \h,         oc1,    oc2,    oc3

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\\\id\\s+([A-Z0-9]{3})\\b\\s*([^\\\\' + b'\n]*?)\n' + b'(.*)(?=\\\\id|$)', lambda m: b'\ufdd0<div type="book" osisID="' + bookDict[m.group(1)] + b'">\n' + (b'<!-- id comment - ' + m.group(2) + b' -->\n' if m.group(2) else b'') + m.group(3) + b'</div type="book">\ufdd0\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ide\\b.*\n', b'', osis)
        osis = re.sub(b'\\\\sts\\b\\s+(.+)\\s*\n', b'<milestone type="x-usfm-sts" n="\\1"/>' + b'\n', osis)
        osis = re.sub(b'\\\\rem\\b\\s+(.+)', b'<!-- rem - \\1 -->', osis)
        if relaxedConformance:
            osis = re.sub(b'\\\\restore\\b\\s+(.+)', b'<!-- restore - \\1 -->', osis)
        osis = re.sub(b'\\\\h\\b\\s+(.+)\\s*\n', b'<title type="runningHead">\\1</title>' + b'\n', osis)
        osis = re.sub(b'\\\\h(\\d)\\b\\s+(.+)\\s*\n', b'<title type="runningHead" n="\\1">\\2</title>' + b'\n', osis)
        osis = re.sub(b'\\\\toc1\\b\\s+(.+)\\s*\n', b'<milestone type="x-usfm-toc1" n="\\1"/>' + b'\n', osis)
        osis = re.sub(b'\\\\toc2\\b\\s+(.+)\\s*\n', b'<milestone type="x-usfm-toc2" n="\\1"/>' + b'\n', osis)
        osis = re.sub(b'\\\\toc3\\b\\s+(.+)\\s*\n', b'<milestone type="x-usfm-toc3" n="\\1"/>' + b'\n', osis)
        return osis

    def cvtIntroductions(osis, relaxedConformance):
        r"""Converts USFM **Introduction** tags to OSIS, returning the processed
        text as a string.

        Supported tags: \imt#, \is#, \ip, \ipi, \im, \imi, \ipq, \imq, \ipr,
                        \iq#, \ib, \ili#, \iot, \io#, \ior...\ior*, \iex,
                        \iqt...\iqt*, \imte, \ie

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\\\imt(\\d?)\\s+(.+)', lambda m: b'<title ' + (b'level="' + m.group(1) + b'" ' if m.group(1) else b'') + b'type="main" subType="x-introduction">' + m.group(2) + b'</title>', osis)
        osis = re.sub(b'\\\\imte(\\d?)\\b\\s+(.+)', lambda m: b'<title ' + (b'level="' + m.group(1) + b'" ' if m.group(1) else b'') + b'type="main" subType="x-introduction-end">' + m.group(2) + b'</title>', osis)
        osis = re.sub(b'\\\\is1?\\s+(.+)', lambda m: b'\ufde2<div type="section" subType="x-introduction"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufde2<div type="section" subType="x-introduction">[^\ufde2]+)(?!\\c\x08)', b'\\1</div>\ufde2\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\is2\\s+(.+)', lambda m: b'\ufde3<div type="subSection" subType="x-introduction"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufde3<div type="subSection" subType="x-introduction">[^\ufde2\ufde3]+)(?!\\c\x08)', b'\\1</div>\ufde3\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\is3\\s+(.+)', lambda m: b'\ufde4<div type="x-subSubSection" subType="x-introduction"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufde4<div type="subSubSection" subType="x-introduction">[^\ufde2\ufde3\ufde4]+)(?!\\c\x08)', b'\\1</div>\ufde4\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\is4\\s+(.+)', lambda m: b'\ufde5<div type="x-subSubSubSection" subType="x-introduction"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufde5<div type="subSubSubSection" subType="x-introduction">[^\ufde2\ufde3\ufde4\ufde5]+)(?!\\c\x08)', b'\\1</div>\ufde5\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\is5\\s+(.+)', lambda m: b'\ufde6<div type="x-subSubSubSubSection" subType="x-introduction"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufde6<div type="subSubSubSubSection" subType="x-introduction">[^\ufde2\ufde3\ufde4\ufde5\ufde6]+?)(?!\\c\x08)', b'\\1</div>\ufde6\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ip\\s+(.*?)(?=(\\\\(i?m|i?p|lit|cls|tr|io|iq|i?li|iex?|s|c)\\b|<(/?div|p|closer)\\b))', lambda m: b'\ufdd3<p subType="x-introduction">\n' + m.group(1) + b'\ufdd3</p>\n', osis, flags=re.DOTALL)
        pType = {b'ipi': b'x-indented', b'im': b'x-noindent', b'imi': b'x-noindent-indented', b'ipq': b'x-quote', b'imq': b'x-noindent-quote', b'ipr': b'x-right'}
        osis = re.sub(b'\\\\(ipi|im|ipq|imq|ipr)\\s+(.*?)(?=(\\\\(i?m|i?p|lit|cls|tr|io|iq|i?li|iex?|s|c)\\b|<(/?div|p|closer)\\b))', lambda m: b'\ufdd3<p type="' + pType[m.group(1)] + b'" subType="x-introduction">\n' + m.group(2) + b'\ufdd3</p>\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\iq\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4' + b']|\\\\(iq\\d?|fig|q\\d?|b)\\b|<title\\b))', b'<l level="1" subType="x-introduction">\\1</l>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\iq(\\d)\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4' + b']|\\\\(iq\\d?|fig|q\\d?|b)\\b|<title\\b))', b'<l level="\\1" subType="x-introduction">\\2</l>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ib\\b\\s?', b'<lb type="x-p"/>', osis)
        osis = osis.replace(b'\n</l>', b'</l>\n')
        osis = re.sub(b'\\\\ili\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4' + b']|\\\\(ili\\d?|c|p|iot|io\\d?|iex?)\\b|<(lb|title|item|\\?div)\\b))', b'<item type="x-indent-1" subType="x-introduction">\ufde0' + b'\\1' + b'\ufde0</item>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ili(\\d)\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4' + b']|\\\\(ili\\d?|c|p|iot|io\\d?|iex?)\\b|<(lb|title|item|\\?div)\\b))', b'<item type="x-indent-\\1" subType="x-introduction">\ufde0' + b'\\2' + b'\ufde0</item>', osis, flags=re.DOTALL)
        osis = osis.replace(b'\n</item>', b'</item>\n')
        osis = re.sub(b'(<item [^\ufdd0\ufdd1\ufdd3\ufdd4]+</item>)', b'\ufdd3<list>\\1</list>\ufdd3', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\io\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4' + b']|\\\\(iot|io\\d?|iex?|c|p)\\b|<(lb|title|item|\\?div)\\b))', b'<item type="x-indent-1" subType="x-introduction">\ufde1' + b'\\1' + b'\ufde1</item>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\io(\\d)\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4' + b']|\\\\(iot|io\\d?|iex?|c|p)\\b|<(lb|title|item|\\?div)\\b))', b'<item type="x-indent-\\1" subType="x-introduction">\ufde1' + b'\\2' + b'\ufde1</item>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\iot\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4' + b']|\\\\(iot|io\\d?|iex?|c|p)\\b|<(lb|title|item|\\?div)\\b))', b'<item type="head">\ufde1' + b'\\1' + b'\ufde1</item type="head">', osis, flags=re.DOTALL)
        osis = osis.replace(b'\n</item>', b'</item>\n')
        osis = re.sub(b'(<item [^\ufdd0\ufdd1\ufdd3\ufdd4\ufde0]+</item>)', b'\ufdd3<div type="outline"><list>' + b'\\1' + b'</list></div>\ufdd3', osis, flags=re.DOTALL)
        osis = re.sub(b'item type="head"', b'head', osis)
        osis = re.sub(b'\\\\ior\\b\\s+(.+?)\\\\ior\\*', b'<reference>\\1</reference>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\iex\\b\\s*(.+?)' + b'?=(\\s*(\\c|</div type="book">\ufdd0))', b'<div type="bridge">\\1</div>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\iqt\\s+(.+?)\\\\iqt\\*', b'<q subType="x-introduction">\\1</q>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ie\\b\\s*', b'<milestone type="x-usfm-ie"/>', osis)
        return osis

    def cvtTitles(osis, relaxedConformance):
        r"""Converts USFM **Title, Heading, and Label** tags to OSIS, returning
        the processed text as a string.

        Supported tags: \mt#, \mte#, \ms#, \mr, \s#, \sr, 
, 
q...
q*, \d,
                        \sp 

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\\\ms1?\\s+(.+)', lambda m: b'\ufdd5<div type="majorSection"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufdd5[^\ufdd5\ufdd0]+)', b'\\1</div>\ufdd5\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ms2\\s+(.+)', lambda m: b'\ufdd6<div type="majorSection" n="2"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufdd6[^\ufdd5\ufdd0\ufdd6]+)', b'\\1</div>\ufdd6\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ms3\\s+(.+)', lambda m: b'\ufdd7<div type="majorSection" n="3"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufdd7[^\ufdd5\ufdd0\ufdd6\ufdd7]+)', b'\\1</div>\ufdd7\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ms4\\s+(.+)', lambda m: b'\ufdd8<div type="majorSection" n="4"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufdd8[^\ufdd5\ufdd0\ufdd6\ufdd7\ufdd8]+)', b'\\1</div>\ufdd8\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ms5\\s+(.+)', lambda m: b'\ufdd9<div type="majorSection" n="5"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufdd9[^\ufdd5\ufdd0\ufdd6\ufdd7\ufdd8\ufdd9]+)', b'\\1</div>\ufdd9\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\mr\\s+(.+)', b'\ufdd4<title type="scope"><reference>' + b'\\1</reference></title>', osis)
        osis = re.sub(b'\\\\s1?\\s+(.+)', lambda m: b'\ufdda<div type="section"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufdda<div type="section">[^\ufdd5\ufdd0\ufdd6\ufdd7\ufdd8\ufdd9\ufdda]+)', b'\\1</div>\ufdda\n', osis, flags=re.DOTALL)
        if relaxedConformance:
            osis = re.sub(b'\\\\ss\\s+', b'\\\\s2 ', osis)
            osis = re.sub(b'\\\\sss\\s+', b'\\\\s3 ', osis)
        osis = re.sub(b'\\\\s2\\s+(.+)', lambda m: b'\ufddb<div type="subSection"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufddb<div type="subSection">[^\ufdd5\ufdd0\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb]+)', b'\\1</div>\ufddb\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\s3\\s+(.+)', lambda m: b'\ufddc<div type="x-subSubSection"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufddc<div type="x-subSubSection">[^\ufdd5\ufdd0\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb\ufddc]+)', b'\\1</div>\ufddc\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\s4\\s+(.+)', lambda m: b'\ufddd<div type="x-subSubSubSection"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufddd<div type="x-subSubSubSection">[^\ufdd5\ufdd0\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb\ufddc\ufddd]+)', b'\\1</div>\ufddd\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\s5\\s+(.+)', lambda m: b'\ufdde<div type="x-subSubSubSubSection"><title>' + m.group(1) + b'</title>', osis)
        osis = re.sub(b'(\ufdde<div type="x-subSubSubSubSection">[^\ufdd5\ufdd0\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb\ufddc\ufddd\ufdde]+)', b'\\1</div>\ufdde\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\sr\\s+(.+)', b'\ufdd4<title type="scope"><reference>' + b'\\1</reference></title>', osis)
        osis = re.sub(b'\\\\r\\s+(.+)', b'\ufdd4<title type="parallel"><reference type="parallel">' + b'\\1</reference></title>', osis)
        osis = re.sub(b'\\\\rq\\s+(.+?)\\\\rq\\*', b'<reference type="source">\\1</reference>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\d\\s+(.+)', b'\ufdd4<title canonical="true" type="psalm">' + b'\\1</title>', osis)
        osis = re.sub(b'\\\\sp\\s+(.+)', b'<speaker>\\1</speaker>', osis)
        osis = re.sub(b'\\\\mt(\\d?)\\s+(.+)', lambda m: b'<title ' + (b'level="' + m.group(1) + b'" ' if m.group(1) else b'') + b'type="main">' + m.group(2) + b'</title>', osis)
        osis = re.sub(b'\\\\mte(\\d?)\\s+(.+)', lambda m: b'<title ' + (b'level="' + m.group(1) + b'" ' if m.group(1) else b'') + b'type="main" subType="x-end">' + m.group(2) + b'</title>', osis)
        return osis

    def cvtChaptersAndVerses(osis, relaxedConformance):
        """Converts USFM **Chapter and Verse** tags to OSIS, returning the
        processed text as a string.

        Supported tags: \\c, \\ca...\\ca*, \\cl, \\cp, \\cd, \x0b, \x0ba...\x0ba*,
        \x0bp...\x0bp*

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\\\c\\s+([^\\s]+)\\b(.+?)(?=(\\\\c\\s+|</div type="book"))', lambda m: b'\ufdd1<chapter osisID="$BOOK$.' + m.group(1) + b'" sID="$BOOK$.' + m.group(1) + b'"/>' + m.group(2) + b'<chapter eID="$BOOK$.' + m.group(1) + b'"/>\ufdd3\n', osis, flags=re.DOTALL)

        def replaceChapterNumber(matchObject):
            r"""Regex helper function to replace chapter numbers from \c_# with
            values that appeared in \cp_# and \ca_#\ca*, returing the chapter
            text as a string.

            Keyword arguments:
            matchObject -- a regex match object in which the first element is
            the chapter text

            """
            ctext = matchObject.group(1)
            cp = re.search(b'\\\\cp\\s+(.+?)(?=(\\\\|\\s))', ctext)
            if cp:
                ctext = re.sub(b'\\\\cp\\s+(.+?)(?=(\\\\|\\s))', b'', ctext, flags=re.DOTALL)
                cp = cp.group(1)
                ctext = re.sub(b'"\\$BOOK\\$\\.([^"\\.]+)"', b'"$BOOK$.' + cp + b'"', ctext)
            ca = re.search(b'\\\\ca\\s+(.+?)\\\\ca\\*', ctext)
            if ca:
                ctext = re.sub(b'\\\\ca\\s+(.+?)\\\\ca\\*', b'', ctext, flags=re.DOTALL)
                ca = ca.group(1)
                ctext = re.sub(b'(osisID="\\$BOOK\\$\\.[^"\\.]+)"', b'\\1 $BOOK$.' + ca + b'"', ctext)
            return ctext

        osis = re.sub(b'(<chapter [^<]+sID[^<]+/>.+?<chapter eID[^>]+/>)', replaceChapterNumber, osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\cl\\s+(.+)', b'\ufdd4<title>\\1</title>', osis)
        osis = re.sub(b'\\\\cd\\b\\s+(.+)', b'\ufdd4<title type="x-description">' + b'\\1</title>', osis)
        osis = re.sub(b'\\\\v\\s+([^\\s]+)\\b\\s*(.+?)(?=(\\\\v\\s+|</div type="book"|<chapter eID))', lambda m: b'\ufdd2<verse osisID="$BOOK$.$CHAP$.' + m.group(1) + b'" sID="$BOOK$.$CHAP$.' + m.group(1) + b'"/>' + m.group(2) + b'<verse eID="$BOOK$.$CHAP$.' + m.group(1) + b'"/>\ufdd2\n', osis, flags=re.DOTALL)

        def replaceVerseNumber(matchObject):
            """Regex helper function to replace verse numbers from \x0b_# with
            values that appeared in \x0bp_#\x0bp* and \x0ba_#\x0ba*, returing the verse
            text as a string.

            Keyword arguments:
            matchObject -- a regex match object in which the first element is
            the verse text

            """
            vtext = matchObject.group(1)
            vp = re.search(b'\\\\vp\\s+(.+?)\\\\vp\\*', vtext)
            if vp:
                vtext = re.sub(b'\\\\vp\\s+(.+?)\\\\vp\\*', b'', vtext, flags=re.DOTALL)
                vp = vp.group(1)
                vtext = re.sub(b'"\\$BOOK\\$\\.\\$CHAP\\$\\.([^"\\.]+)"', b'"$BOOK$.$CHAP$.' + vp + b'"', vtext)
            va = re.search(b'\\\\va\\s+(.+?)\\\\va\\*', vtext)
            if va:
                vtext = re.sub(b'\\\\va\\s+(.+?)\\\\va\\*', b'', vtext, flags=re.DOTALL)
                va = va.group(1)
                vtext = re.sub(b'(osisID="\\$BOOK\\$\\.\\$CHAP\\$\\.[^"\\.]+)"', b'\\1 $BOOK$.$CHAP$.' + va + b'"', vtext)
            return vtext

        osis = re.sub(b'(<verse [^<]+sID[^<]+/>.+?<verse eID[^>]+/>)', replaceVerseNumber, osis, flags=re.DOTALL)
        return osis

    def cvtParagraphs(osis, relaxedConformance):
        """Converts USFM **Paragraph** tags to OSIS, returning the processed
        text as a string.

        Supported tags: \\p, \\m, \\pmo, \\pm, \\pmc, \\pmr, \\pi#, \\mi, 
b, \\cls,
                        \\li#, \\pc, \\pr, \\ph#, \x08

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        paragraphregex = b'pc|pr|m|pmo|pm|pmc|pmr|pi|pi1|pi2|pi3|pi4|pi5|mi|nb'
        if relaxedConformance:
            paragraphregex += b'|phi|ps|psi|p1|p2|p3|p4|p5'
        osis = re.sub(b'\\\\p\\s+(.*?)(?=(\\\\(i?m|i?p|lit|cls|tr|p|' + paragraphregex + b')\\b|<chapter eID|<(/?div|p|closer)\\b))', lambda m: b'\ufdd3<p>\n' + m.group(1) + b'\ufdd3</p>\n', osis, flags=re.DOTALL)
        pType = {b'pc': b'x-center', b'pr': b'x-right', b'm': b'x-noindent', b'pmo': b'x-embedded-opening', b'pm': b'x-embedded', b'pmc': b'x-embedded-closing', b'pmr': b'x-right', b'pi': b'x-indented-1', b'pi1': b'x-indented-1', b'pi2': b'x-indented-2', b'pi3': b'x-indented-3', b'pi4': b'x-indented-4', b'pi5': b'x-indented-5', b'mi': b'x-noindent-indented', b'nb': b'x-nobreak', b'phi': b'x-indented-hanging', b'ps': b'x-nobreakNext', b'psi': b'x-nobreakNext-indented', b'p1': b'x-level-1', b'p2': b'x-level-2', b'p3': b'x-level-3', b'p4': b'x-level-4', b'p5': b'x-level-5'}
        osis = re.sub(b'\\\\(' + paragraphregex + b')\\s+(.*?)(?=(\\\\(i?m|i?p|lit|cls|tr|' + paragraphregex + b')\\b|<chapter eID|<(/?div|p|closer)\\b))', lambda m: b'\ufdd3<p type="' + pType[m.group(1)] + b'">\n' + m.group(2) + b'\ufdd3</p>\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\m\\s+(.+?)(?=(\\\\(i?m|i?p|lit|cls|tr)\\b|<chapter eID|<(/?div|p|closer)\\b))', lambda m: b'\ufdd3<closer>' + m.group(1) + b'\ufdd3</closer>\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ph\\b\\s*', b'\\\\li ', osis)
        osis = re.sub(b'\\\\ph(\\d)\\b\\s*', b'\\\\li\\1 ', osis)
        osis = re.sub(b'\\\\li\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4\ufde0\ufde1\ufdd5\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb\ufddc\ufddd\ufdde' + b']|\\\\li\\d?\\b|<(lb|title|item|/?div|/?chapter)\\b))', b'<item type="x-indent-1">\\1</item>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\li(\\d)\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4\ufde0\ufde1\ufdd5\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb\ufddc\ufddd\ufdde' + b']|\\\\li\\d?\\b|<(lb|title|item|/?div|/?chapter)\\b))', b'<item type="x-indent-\\1">\\2</item>', osis, flags=re.DOTALL)
        osis = osis.replace(b'\n</item>', b'</item>\n')
        osis = re.sub(b'(<item [^\ufdd0\ufdd1\ufdd3\ufdd4\ufde0\ufde1\ufdd5\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb\ufddc\ufddd\ufdde]+</item>)', b'\ufdd3<list>\\1</list>\ufdd3', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\b\\b\\s?', b'<lb type="x-p"/>', osis)
        return osis

    def cvtPoetry(osis, relaxedConformance):
        """Converts USFM **Poetry** tags to OSIS, returning the processed text
        as a string.

        Supported tags: \\q#, \\qr, \\qc, \\qs...\\qs*, \\qa, \\qac...\\qac*, \\qm#, \x08

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\\\qa\\s+(.+)', b'\ufdd4<title type="acrostic">' + b'\\1</title>', osis)
        osis = re.sub(b'\\\\qac\\s+(.+?)\\\\qac\\*', b'<hi type="acrostic">\\1</hi>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\qs\\b\\s(.+?)\\\\qs\\*', b'<l type="selah">\\1</l>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\q\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4\ufdd5\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb\ufddc\ufddd\ufdde' + b']|\\\\(q\\d?|fig)\\b|<(l|lb|title|list|/?div)\\b))', b'<l level="1">\\1</l>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\q(\\d)\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4\ufdd5\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb\ufddc\ufddd\ufdde' + b']|\\\\(q\\d?|fig)\\b|<(l|lb|title|list|/?div)\\b))', b'<l level="\\1">\\2</l>', osis, flags=re.DOTALL)
        qType = {b'qr': b'x-right', b'qc': b'x-center', b'qm': b'x-embedded" level="1', b'qm1': b'x-embedded" level="1', b'qm2': b'x-embedded" level="2', b'qm3': b'x-embedded" level="3', b'qm4': b'x-embedded" level="4', b'qm5': b'x-embedded" level="5'}
        osis = re.sub(b'\\\\(qr|qc|qm\\d)\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4\ufdd5\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb\ufddc\ufddd\ufdde' + b']|\\\\(q\\d?|fig)\\b|<(l|lb|title|list|/?div)\\b))', lambda m: b'<l type="' + qType[m.group(1)] + b'">' + m.group(2) + b'</l>', osis, flags=re.DOTALL)
        osis = osis.replace(b'\n</l>', b'</l>\n')
        osis = re.sub(b'(<l [^\ufdd0\ufdd1\ufdd3\ufdd4\ufdd5\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb\ufddc\ufddd\ufdde]+</l>)', b'<lg>\\1</lg>', osis, flags=re.DOTALL)
        osis = re.sub(b'(<lg>.+?</lg>)', lambda m: m.group(1).replace(b'<lb type="x-p"/>', b'</lg><lg>'), osis, flags=re.DOTALL)
        return osis

    def cvtTables(osis, relaxedConformance):
        """Converts USFM **Table** tags to OSIS, returning the processed text as
        a string.

        Supported tags:         r,      h#,     hr#,    c#,     cr#

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\\\tr\\b\\s*(.*?)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4' + b']|\\\\tr\\s|<(lb|title)\\b))', b'<row>\\1</row>', osis, flags=re.DOTALL)
        tType = {b'th': b' role="label"', b'thr': b' role="label" type="x-right"', b'tc': b'', b'tcr': b' type="x-right"'}
        osis = re.sub(b'\\\\(thr?|tcr?)\\d*\\b\\s*(.*?)(?=(\\\\t[hc]|</row))', lambda m: b'<cell' + tType[m.group(1)] + b'>' + m.group(2) + b'</cell>', osis, flags=re.DOTALL)
        osis = re.sub(b'(<row>.*?</row>)(?=([' + b'\ufdd0\ufdd1\ufdd3\ufdd4' + b']|\\\\tr\\s|<(lb|title)\\b))', b'<table>\\1</table>', osis, flags=re.DOTALL)
        return osis

    def processNote(note):
        """Convert note-internal USFM tags to OSIS, returning the note as a
        string.

        Keyword arguments:
        note -- The note as a string.

        """
        note = note.replace(b'\n', b' ')
        note = re.sub(b'\\\\fdc\\b\\s(.+?)\\\\fdc\\b\\*', b'<seg editions="dc">\\1</seg>', note)
        note = re.sub(b'\\\\fq\\b\\s(.+?)(?=(\\\\f|' + b'\ufddf))', b'\ufddf' + b'<catchWord>\\1</catchWord>', note)
        note = re.sub(b'\\\\fqa\\b\\s(.+?)(?=(\\\\f|' + b'\ufddf))', b'\ufddf' + b'<rdg type="alternate">\\1</rdg>', note)
        note = re.sub(b'\\\\ft\\s', b'', note)
        note = re.sub(b'\\\\fr\\b\\s(.+?)(?=(\\\\f|' + b'\ufddf))', b'\ufddf' + b'<reference type="annotateRef">\\1</reference>', note)
        note = re.sub(b'\\\\fk\\b\\s(.+?)(?=(\\\\f|' + b'\ufddf))', b'\ufddf' + b'<catchWord>\\1</catchWord>', note)
        note = re.sub(b'\\\\fl\\b\\s(.+?)(?=(\\\\f|' + b'\ufddf))', b'\ufddf<label>\\1</label>', note)
        note = re.sub(b'\\\\fp\\b\\s(.+?)(?=(\\\\fp|$))', b'<p>\\1</p>', note)
        note = re.sub(b'(<note\\b[^>]*?>)(.*?)<p>', b'\\1<p>\\2</p><p>', note)
        note = re.sub(b'\\\\fv\\b\\s(.+?)(?=(\\\\f|' + b'\ufddf))', b'\ufddf' + b'<hi type="super">\\1</hi>', note)
        note = re.sub(b'\\\\f(q|qa|t|r|k|l|p|v)\\*', b'', note)
        note = note.replace(b'\ufddf', b'')
        return note

    def cvtFootnotes(osis, relaxedConformance):
        """Converts USFM **Footnote** tags to OSIS, returning the processed text
        as a string.

        Supported tags: \x0c...\x0c*, \x0ce...\x0ce*, \x0cr, \x0ck, \x0cq, \x0cqa, \x0cl, \x0cp,
                        \x0cv, \x0ct, \x0cdc...\x0cdc*, \x0cm...\x0cm*

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\\\f\\s+([^\\s\\\\]+)?\\s*(.+?)\\s*\\\\f\\*', lambda m: b'<note' + (b' n=""' if m.group(1) == b'-' else b'' if m.group(1) == b'+' else b' n="' + m.group(1) + b'"') + b' placement="foot">' + m.group(2) + b'\ufddf</note>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\fe\\s+([^\\s\\\\]+?)\\s*(.+?)\\s*\\\\fe\\*', lambda m: b'<note' + (b' n=""' if m.group(1) == b'-' else b'' if m.group(1) == b'+' else b' n="' + m.group(1) + b'"') + b' placement="end">' + m.group(2) + b'\ufddf</note>', osis, flags=re.DOTALL)
        osis = re.sub(b'(<note\\b[^>]*?>.*?</note>)', lambda m: processNote(m.group(1)), osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\fm\\b\\s(.+?)\\\\fm\\*', b'<hi type="super">\\1</hi>', osis)
        return osis

    def processXref(note):
        """Convert cross-reference note-internal USFM tags to OSIS, returning
        the cross-reference note as a string.

        Keyword arguments:
        note -- The cross-reference note as a string.

        """
        note = note.replace(b'\n', b' ')
        note = re.sub(b'\\\\xot\\b\\s(.+?)\\\\xot\\b\\*', b'\ufddf' + b'<seg editions="ot">\\1</seg>', note)
        note = re.sub(b'\\\\xnt\\b\\s(.+?)\\\\xnt\\b\\*', b'\ufddf' + b'<seg editions="nt">\\1</seg>', note)
        note = re.sub(b'\\\\xdc\\b\\s(.+?)\\\\xdc\\b\\*', b'\ufddf' + b'<seg editions="dc">\\1</seg>', note)
        note = re.sub(b'\\\\xq\\b\\s(.+?)(?=(\\\\x|' + b'\ufddf))', b'\ufddf' + b'<catchWord>\\1</catchWord>', note)
        note = re.sub(b'\\\\xo\\b\\s(.+?)(?=(\\\\x|' + b'\ufddf))', b'\ufddf' + b'<reference type="annotateRef">\\1</reference>', note)
        note = re.sub(b'\\\\xk\\b\\s(.+?)(?=(\\\\x|' + b'\ufddf))', b'\ufddf' + b'<catchWord>\\1</catchWord>', note)
        note = re.sub(b'\\\\xt\\b\\s(.+?)(?=(\\\\x|' + b'\ufddf))', b'\ufddf' + b'<reference>\\1</reference>', note)
        if relaxedConformance:
            note = re.sub(b'\\\\xtSee\\b\\s(.+?)\\\\xtSee\\b\\*', b'\ufddf' + b'<reference osisRef="\\1">See: \\1</reference>', note)
            note = re.sub(b'\\\\xtSeeAlso\\b\\s(.+?)\\\\xtSeeAlso\\b\\*', b'\ufddf' + b'<reference osisRef="\\1">See also: \\1</reference>', note)
        note = re.sub(b'\\\\x(q|t|o|k)\\*', b'', note)
        note = note.replace(b'\ufddf', b'')
        return note

    def cvtCrossReferences(osis, relaxedConformance):
        r"""Converts USFM **Cross Reference** tags to OSIS, returning the
        processed text as a string.

        Supported tags: \x...\x*, \xo, \xk, \xq, \xt, \xot...\xot*,
                        \xnt...\xnt*, \xdc...\xdc*

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\\\x\\s+([^\\s]+?)\\s+(.+?)\\s*\\\\x\\*', lambda m: b'<note' + (b' n=""' if m.group(1) == b'-' else b'' if m.group(1) == b'+' else b' n="' + m.group(1) + b'"') + b' type="crossReference">' + m.group(2) + b'\ufddf</note>', osis, flags=re.DOTALL)
        osis = re.sub(b'(<note [^>]*?type="crossReference"[^>]*>.*?</note>)', lambda m: processXref(m.group(1)), osis, flags=re.DOTALL)
        return osis

    def cvtSpecialText(osis, relaxedConformance):
        """Converts USFM **Special Text** tags to OSIS, returning the processed
        text as a string.

        Supported tags: \x07dd...\x07dd*, \x08k...\x08k*, \\dc...\\dc*, \\k...\\k*, \\lit,
                        
d...
d*, \\ord...\\ord*, \\pn...\\pn*, \\qt...\\qt*,
                        \\sig...\\sig*, \\sls...\\sls*,     l...    l*, \\wj...\\wj*

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\\\add\\s+(.+?)\\\\add\\*', b'<transChange type="added">\\1</transChange>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\wj\\s+(.+?)\\\\wj\\*', b'<q who="Jesus" marker="">\\1</q>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\nd\\s+(.+?)\\\\nd\\*', b'<divineName>\\1</divineName>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\pn\\s+(.+?)\\\\pn\\*', b'<name>\\1</name>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\qt\\s+(.+?)\\\\qt\\*', b'<seg type="otPassage">\\1</seg>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\sig\\s+(.+?)\\\\sig\\*', b'<signed>\\1</signed>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ord\\s+(.+?)\\\\ord\\*', b'<hi type="super">\\1</hi>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\tl\\s+(.+?)\\\\tl\\*', b'<foreign>\\1</foreign>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\bk\\s+(.+?)\\\\bk\\*', b'<name type="x-workTitle">\\1</name>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\k\\s+(.+?)\\\\k\\*', b'<seg type="keyword">\\1</seg>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\lit\\s+(.*?)(?=(\\\\(i?m|i?p|nb|lit|cls|tr)\\b|<(chapter eID|/?div|p|closer)\\b))', lambda m: b'\ufdd3<p type="x-liturgical">\n' + m.group(1) + b'\ufdd3</p>\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\dc\\b\\s*(.+?)\\\\dc\\*', b'<transChange type="added" editions="dc">\\1</transChange>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\sls\\b\\s*(.+?)\\\\sls\\*', b'<foreign>/1</foreign>', osis, flags=re.DOTALL)
        if relaxedConformance:
            osis = re.sub(b'\\\\addpn\\s+(.+?)\\\\addpn\\*', b'<hi type="x-dotUnderline">\\1</hi>', osis, flags=re.DOTALL)
            osis = re.sub(b'\\\\k1\\s+(.+?)\\\\k1\\*', b'<seg type="keyword" n="1">\\1</seg>', osis, flags=re.DOTALL)
            osis = re.sub(b'\\\\k2\\s+(.+?)\\\\k2\\*', b'<seg type="keyword" n="2">\\1</seg>', osis, flags=re.DOTALL)
            osis = re.sub(b'\\\\k3\\s+(.+?)\\\\k3\\*', b'<seg type="keyword" n="3">\\1</seg>', osis, flags=re.DOTALL)
            osis = re.sub(b'\\\\k4\\s+(.+?)\\\\k4\\*', b'<seg type="keyword" n="4">\\1</seg>', osis, flags=re.DOTALL)
            osis = re.sub(b'\\\\k5\\s+(.+?)\\\\k5\\*', b'<seg type="keyword" n="5">\\1</seg>', osis, flags=re.DOTALL)
        return osis

    def cvtCharacterStyling(osis, relaxedConformance):
        """Converts USFM **Character Styling** tags to OSIS, returning the
        processed text as a string.

        Supported tags: \\em...\\em*, \x08d...\x08d*, \\it...\\it*, \x08dit...\x08dit*,
                        
o...
o*, \\sc...\\sc*

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\\\em\\s+(.+?)\\\\em\\*', b'<hi type="emphasis">\\1</hi>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\bd\\s+(.+?)\\\\bd\\*', b'<hi type="bold">\\1</hi>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\it\\s+(.+?)\\\\it\\*', b'<hi type="italic">\\1</hi>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\bdit\\s+(.+?)\\\\bdit\\*', b'<hi type="bold"><hi type="italic">\\1</hi></hi>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\no\\s+(.+?)\\\\no\\*', b'<hi type="normal">\\1</hi>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\sc\\s+(.+?)\\\\sc\\*', b'<hi type="small-caps">\\1</hi>', osis, flags=re.DOTALL)
        return osis

    def cvtSpacingAndBreaks(osis, relaxedConformance):
        r"""Converts USFM **Spacing and Breaks** tags to OSIS, returning the
        processed text as a string.

        Supported tags: ~, //, \pb

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = osis.replace(b'~', b'\xa0')
        osis = osis.replace(b'//', b'<lb type="x-optional"/>')
        osis = re.sub(b'\\\\pb\\s*', b'<milestone type="pb"/>\n', osis, flags=re.DOTALL)
        return osis

    def cvtSpecialFeatures(osis, relaxedConformance):
        """Converts USFM **Special Feature** tags to OSIS, returning the
        processed text as a string.

        Supported tags: \x0cig...\x0cig*, 
dx...
dx*, \\pro...\\pro*, \\w...\\w*,
                        \\wg...\\wg*, \\wh...\\wh*

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """

        def makeFigure(matchObject):
            """Regex helper function to convert USFM \x0cig to OSIS <figure/>,
            returning the OSIS element as a string.

            Keyword arguments:
            matchObject -- a regex match object containing the elements of a
            USFM \x0cig tag

            """
            fig_desc, fig_file, fig_size, fig_loc, fig_copy, fig_cap, fig_ref = matchObject.groups()
            figure = b'<figure'
            if fig_file:
                figure += b' src="' + fig_file + b'"'
            if fig_size:
                figure += b' size="' + fig_size + b'"'
            if fig_copy:
                figure += b' rights="' + fig_copy + b'"'
            figure += b'>\n'
            if fig_cap:
                figure += b'<caption>' + fig_cap + b'</caption>\n'
            if fig_ref:
                figure += b'<reference type="annotateRef">' + fig_ref + b'</reference>\n'
            if fig_desc:
                figure += b'<!-- fig DESC - ' + fig_desc + b' -->\n'
            if fig_loc:
                figure += b'<!-- fig LOC - ' + fig_loc + b' -->\n'
            figure += b'</figure>'
            return figure

        osis = re.sub(b'\\\\fig\\b\\s+([^\\|]*)\\s*\\|([^\\|]*)\\s*\\|([^\\|]*)\\s*\\|([^\\|]*)\\s*\\|([^\\|]*)\\s*\\|([^\\|]*)\\s*\\|([^\\\\]*)\\s*\\\\fig\\*', makeFigure, osis)
        osis = re.sub(b'\\\\ndx\\s+(.+?)(\\s*)\\\\ndx\\*', b'\\1<index index="Index" level1="\\1"/>\\2', osis, flags=re.DOTALL)
        osis = re.sub(b'([^\\s]+)(\\s*)\\\\pro\\s+(.+?)(\\s*)\\\\pro\\*', b'<w xlit="\\3">\\1</w>\\2\\4', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\w\\s+(.+?)(\\s*)\\\\w\\*', b'\\1<index index="Glossary" level1="\\1"/>\\2', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\wg\\s+(.+?)(\\s*)\\\\wg\\*', b'\\1<index index="Greek" level1="\\1"/>\\2', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\wh\\s+(.+?)(\\s*)\\\\wh\\*', b'\\1<index index="Hebrew" level1="\\1"/>\\2', osis, flags=re.DOTALL)
        if relaxedConformance:
            osis = re.sub(b'\\\\wr\\s+(.+?)(\\s*)\\\\wr\\*', b'\\1<index index="Reference" level1="\\1"/>\\2', osis, flags=re.DOTALL)
        return osis

    def cvtPeripherals(osis, relaxedConformance):
        r"""Converts USFM **Peripheral** tags to OSIS, returning the processed
        text as a string.

        Supported tag: \periph

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """

        def tagPeriph(matchObject):
            """Regex helper function to tag peripherals, returning a
            <div>-encapsulated string.

            Keyword arguments:
            matchObject -- a regex match object containing the peripheral type
            and contents

            """
            periphType, contents = matchObject.groups()[0:2]
            periph = b'<div type="'
            if periphType in peripherals:
                periph += peripherals[periphType]
            elif periphType in introPeripherals:
                periph += b'introduction" subType="x-' + introPeripherals[periphType]
            else:
                periph += b'x-unknown'
            periph += b'">\n' + contents + b'</div>\n'
            return periph

        osis = re.sub(b'\\\\periph\\s+([^\n' + b']+)\\s*' + b'\n' + b'(.+?)(?=(</div type="book">|\\\\periph\\s+))', tagPeriph, osis, flags=re.DOTALL)
        return osis

    def cvtStudyBibleContent(osis, relaxedConformance):
        r"""Converts USFM **Study Bible Content** tags to OSIS, returning the
        processed text as a string.

        Supported tags: \ef...\ef*, \ex...\ex*, \esb...\esbe, \cat

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\\\ef\\s+([^\\s\\\\]+?)\\s*(.+?)\\s*\\\\ef\\*', lambda m: b'<note' + (b' n=""' if m.group(1) == b'-' else b'' if m.group(1) == b'+' else b' n="' + m.group(1) + b'"') + b' type="study">' + m.group(2) + b'\ufddf</note>', osis, flags=re.DOTALL)
        osis = re.sub(b'(<note\\b[^>]*?>.*?</note>)', lambda m: processNote(m.group(1)), osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\ex\\s+([^\\s]+?)\\s+(.+?)\\s*\\\\ex\\*', lambda m: b'<note' + (b' n=""' if m.group(1) == b'-' else b'' if m.group(1) == b'+' else b' n="' + m.group(1) + b'"') + b' type="crossReference" subType="x-study"><reference>' + m.group(2) + b'</reference>\ufddf</note>', osis, flags=re.DOTALL)
        osis = re.sub(b'(<note [^>]*?type="crossReference"[^>]*>.*?</note>)', lambda m: processXref(m.group(1)), osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\esb\\b\\s*(.+?)\\\\esbe\\b\\s*', b'\ufdd5<div type="x-sidebar">' + b'\\1' + b'</div>\ufdd5\n', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\cat\\b\\s+(.+?)\\\\cat\\*', b'<index index="category" level1="\\1"/>', osis)
        return osis

    def cvtPrivateUseExtensions(osis, relaxedConformance):
        r"""Converts USFM **\z namespace** tags to OSIS, returning the processed
        text as a string.

        Supported tags: \z<Extension>

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'\\z([^\\s]+)\\s(.+?)(\\z\\1\\*)', b'<seg type="x-\\1">\\2</seg>', osis, flags=re.DOTALL)
        osis = re.sub(b'\\\\z([^\\s]+)', b'<milestone type="x-usfm-z-\\1"/>', osis)
        return osis

    def processOsisIDs(osis):
        """Perform postprocessing on an OSIS document, returning the processed
        text as a string.
        Recurses through chapter & verses, substituting acutal book IDs &
        chapter numbers for placeholders.

        Keyword arguments:
        osis -- The document as a string.

        """

        def expandRange(vRange):
            """Expands a verse range into its constituent verses as a string.

            Keyword arguments:
            vRange -- A string of the lower & upper bounds of the range, with a
            hypen in between.
            
            """
            vRange = re.findall(b'\\d+', vRange)
            osisID = list()
            for n in range(int(vRange[0]), int(vRange[1]) + 1):
                osisID.append(b'$BOOK$.$CHAP$.' + str(n))

            return (b' ').join(osisID)

        osis = re.sub(b'\\$BOOK\\$\\.\\$CHAP\\$\\.(\\d+-\\d+)"', lambda m: expandRange(m.group(1)) + b'"', osis)

        def expandSeries(vSeries):
            """Expands a verse series (list) into its constituent verses as a
            string.

            Keyword arguments:
            vSeries -- A comma-separated list of verses.
            
            """
            vSeries = re.findall(b'\\d+', vSeries)
            osisID = list()
            for n in vSeries:
                osisID.append(b'$BOOK$.$CHAP$.' + str(n))

            return (b' ').join(osisID)

        osis = re.sub(b'\\$BOOK\\$\\.\\$CHAP\\$\\.(\\d+(,\\d+)+)"', lambda m: expandSeries(m.group(1)) + b'"', osis)
        bookChunks = osis.split(b'\ufdd0')
        osis = b''
        for bc in bookChunks:
            bookValue = re.search(b'<div type="book" osisID="([^"]+?)"', bc)
            if bookValue:
                bookValue = bookValue.group(1)
                bc = bc.replace(b'$BOOK$', bookValue)
                chapChunks = bc.split(b'\ufdd1')
                newbc = b''
                for cc in chapChunks:
                    chapValue = re.search(b'<chapter osisID="[^\\."]+\\.([^"]+)', cc)
                    if chapValue:
                        chapValue = chapValue.group(1)
                        cc = cc.replace(b'$CHAP$', chapValue)
                    newbc += cc

                bc = newbc
            osis += bc

        return osis

    def osisReorderAndCleanup(osis):
        """Perform postprocessing on an OSIS document, returning the processed
        text as a string.
        Reorders elements, strips non-characters, and cleans up excess spaces
        & newlines

        Keyword arguments:
        osis -- The document as a string.
        relaxedConformance -- Boolean value indicating whether to process
        non-standard & deprecated USFM tags.

        """
        osis = re.sub(b'(\ufdd3<chapter eID=.+?\n)(<verse eID=.+?>\ufdd2)\n?', b'\\2\n\\1', osis)
        osis = re.sub(b'([\ufdd5\ufdd6\ufdd7\ufdd8\ufdd9]</div>)([^\ufdd5\ufdd6\ufdd7\ufdd8\ufdd9]*<chapter eID.+?>)', b'\\2\\1', osis)
        osis = re.sub(b'(\ufdd3</p>\n?\ufdd3<p>)\n?(<verse eID=.+?>\ufdd2)\n?', b'\\2\n\\1\n', osis)
        osis = re.sub(b'\n(<verse eID=.+?>\ufdd2)', b'\\1\n', osis)
        osis = re.sub(b'\n*(<l.+?>)(<verse eID=.+?>[\ufdd2\n]*<verse osisID=.+?>)', b'\\2\\1', osis)
        osis = re.sub(b'(</l>)(<note .+?</note>)', b'\\2\\1', osis)
        osis = re.sub(b'(</[^\\s>]+) [^>]*>', b'\\1>', osis)
        osis = osis.replace(b'<lb type="x-p"/>', b'<lb/>')
        for c in b'\ufdd0\ufdd1\ufdd2\ufdd3\ufdd4\ufdd5\ufdd6\ufdd7\ufdd8\ufdd9\ufdda\ufddb\ufddc\ufddd\ufdde\ufddf\ufde0\ufde1\ufde2\ufde3\ufde4\ufde5\ufde6\ufde7\ufde8\ufde9\ufdea\ufdeb\ufdec\ufded\ufdee\ufdef':
            osis = osis.replace(c, b'')

        for endBlock in [b'p', b'div', b'note', b'l', b'lg', b'chapter', b'verse', b'head', b'title', b'item', b'list']:
            osis = re.sub(b'\\s+</' + endBlock + b'>', b'</' + endBlock + b'>\\n', osis)
            osis = re.sub(b'\\s+<' + endBlock + b'( eID=[^/>]+/>)', b'<' + endBlock + b'\\1' + b'\n', osis)

        osis = re.sub(b' +((</[^>]+>)+) *', b'\\1 ', osis)
        osis = re.sub(b'  +', b' ', osis)
        osis = re.sub(b' ?\n\n+', b'\n', osis)
        return osis

    if encoding:
        osis = codecs.open(sFile, b'r', encoding).read().strip() + b'\n'
    else:
        encoding = b'utf-8'
        osis = codecs.open(sFile, b'r', encoding).read().strip() + b'\n'
        encoding = re.search(b'\\\\ide\\s+(.+)\n', osis)
        if encoding:
            encoding = encoding.group(1).lower().strip()
            if encoding != b'utf-8':
                if encoding in aliases:
                    osis = codecs.open(sFile, b'r', encoding).read().strip() + b'\n'
                else:
                    print b'WARNING: Encoding "' + encoding + b'" unknown, processing ' + sFile + b' as UTF-8'
                    encoding = b'utf-8'
        osis = osis.lstrip(_unichr(65279))
        osis = cvtPreprocess(osis, relaxedConformance)
        osis = cvtRelaxedConformanceRemaps(osis, relaxedConformance)
        osis = cvtIdentification(osis, relaxedConformance)
        osis = cvtIntroductions(osis, relaxedConformance)
        osis = cvtTitles(osis, relaxedConformance)
        osis = cvtChaptersAndVerses(osis, relaxedConformance)
        osis = cvtParagraphs(osis, relaxedConformance)
        osis = cvtPoetry(osis, relaxedConformance)
        osis = cvtTables(osis, relaxedConformance)
        osis = cvtFootnotes(osis, relaxedConformance)
        osis = cvtCrossReferences(osis, relaxedConformance)
        osis = cvtSpecialText(osis, relaxedConformance)
        osis = cvtCharacterStyling(osis, relaxedConformance)
        osis = cvtSpacingAndBreaks(osis, relaxedConformance)
        osis = cvtSpecialFeatures(osis, relaxedConformance)
        osis = cvtPeripherals(osis, relaxedConformance)
        osis = cvtStudyBibleContent(osis, relaxedConformance)
        osis = cvtPrivateUseExtensions(osis, relaxedConformance)
        osis = processOsisIDs(osis)
        osis = osisReorderAndCleanup(osis)
        for sb in specialBooks:
            osis = osis.replace(b'<div type="book" osisID="' + sb + b'">', b'<div type="' + sb.lower() + b'">')

    if debug:
        localUnhandledTags = set(re.findall(b'(\\\\[^\\s]*)', osis))
        if localUnhandledTags:
            print b'Unhandled USFM tags in ' + sFile + b': ' + (b', ').join(localUnhandledTags) + b' (' + str(len(localUnhandledTags)) + b' total)'
    return osis


osisSchema = b'<xs:schema targetNamespace="http://www.bibletechnologies.net/2003/OSIS/namespace" xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace" xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified" attributeFormDefault="unqualified" xml:lang="en"><xs:import namespace="http://www.w3.org/XML/1998/namespace" schemaLocation="http://www.w3.org/2001/xml.xsd"/><xs:element name="osis" type="osisCT"/><xs:complexType name="osisCT"><xs:choice><xs:element name="osisCorpus" type="osisCorpusCT" minOccurs="0"/><xs:element name="osisText" type="osisTextCT" minOccurs="0"/></xs:choice><xs:attribute name="TEIform" fixed="TEI.2"/></xs:complexType><xs:complexType name="osisCorpusCT"><xs:sequence><xs:element name="header" type="corpusHeaderCT" minOccurs="0"/><xs:element name="titlePage" type="titlePageCT" minOccurs="0" maxOccurs="1"/><xs:element name="osisText" type="osisTextCT" minOccurs="1" maxOccurs="unbounded"/></xs:sequence><xs:attribute name="TEIform" fixed="teiCorpus.2"/></xs:complexType><xs:complexType name="corpusHeaderCT"><xs:sequence><xs:element name="revisionDesc" type="revisionDescCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="work" type="workCT" maxOccurs="unbounded"/></xs:sequence><xs:attribute name="TEIform" fixed="teiHeader"/><xs:attribute name="canonical" type="xs:boolean" use="optional" default="false"/></xs:complexType><xs:complexType name="osisTextCT"><xs:sequence><xs:element name="header" type="headerCT"/><xs:element name="titlePage" type="titlePageCT" minOccurs="0" maxOccurs="1"/><xs:element name="div" type="divCT" minOccurs="0" maxOccurs="unbounded"/></xs:sequence><xs:attribute name="annotateRef" type="annotateRefType" use="optional"/><xs:attribute name="canonical" type="xs:boolean" use="optional" default="true"/><xs:attribute name="ID" type="xs:ID" use="optional"/><xs:attribute name="osisID" type="osisIDType" use="optional"/><xs:attribute name="osisIDWork" type="osisWorkType" use="required"/><xs:attribute name="osisRefWork" type="osisWorkType" use="optional" default="Bible"/><xs:attribute name="type" type="attributeExtension" use="optional"/><xs:attribute name="subType" type="attributeExtension" use="optional"/><xs:attribute ref="xml:lang" use="required"/><xs:attribute ref="xml:space" default="default"/><xs:attribute name="TEIform" fixed="text"/></xs:complexType><xs:complexType name="headerCT"><xs:sequence><xs:element name="revisionDesc" type="revisionDescCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="work" type="workCT" maxOccurs="unbounded"/><xs:element name="workPrefix" type="workPrefixCT" minOccurs="0" maxOccurs="unbounded"/></xs:sequence><xs:attribute name="TEIform" fixed="teiHeader"/><xs:attribute name="canonical" type="xs:boolean" use="optional" default="false"/></xs:complexType><xs:complexType name="actorCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="index" type="indexCT"/><xs:element name="note" type="noteCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="who" type="xs:string" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="actor"/></xs:complexType><xs:complexType name="castGroupCT"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="head" type="headCT"/><xs:element name="castItem" type="castItemCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="castGroup"/></xs:complexType><xs:complexType name="castItemCT"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="actor" type="actorCT"/><xs:element name="role" type="roleCT"/><xs:element name="roleDesc" type="roleDescCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="castItem"/></xs:complexType><xs:complexType name="castListCT"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="castGroup" type="castGroupCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="castList"/></xs:complexType><xs:complexType name="contributorCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="file-as" type="xs:string" use="optional"/><xs:attribute name="role" type="roleType" use="optional"/><xs:attributeGroup ref="globalWithType"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="coverageCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attributeGroup ref="globalWithType"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="creatorCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attribute name="role" type="roleType" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="descriptionCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="type" type="descriptionType" use="optional"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="formatCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attributeGroup ref="globalWithType"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="identifierCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="type" type="identifierType"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="languageCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attribute name="type" type="languageType"/><xs:attribute name="use" type="languageUsage"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="publisherCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attributeGroup ref="globalWithType"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="refSystemCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attributeGroup ref="globalWithType"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="relationCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attributeGroup ref="globalWithType"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="revisionDescCT"><xs:sequence><xs:element name="date" type="dateCT"/><xs:element name="p" type="pCT" maxOccurs="unbounded"/></xs:sequence><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="revisionDesc"/></xs:complexType><xs:complexType name="rightsCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attributeGroup ref="globalWithType"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="roleCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="index" type="indexCT"/><xs:element name="note" type="noteCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="role"/></xs:complexType><xs:complexType name="roleDescCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="index" type="indexCT"/><xs:element name="note" type="noteCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="roleDesc"/></xs:complexType><xs:complexType name="subjectCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="type" type="subjectType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="sourceCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="scopeCT"><xs:simpleContent><xs:extension base="osisRefType"><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="teiHeaderCT" mixed="true"><xs:sequence><xs:any processContents="skip" maxOccurs="unbounded"/></xs:sequence><xs:attribute name="TEIform" fixed="teiHeader"/></xs:complexType><xs:complexType name="typeCT"><xs:simpleContent><xs:extension base="xs:string"><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="type" type="typeType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/></xs:extension></xs:simpleContent></xs:complexType><xs:complexType name="workCT"><xs:sequence><xs:element name="title" type="titleCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="contributor" type="contributorCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="creator" type="creatorCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="subject" type="subjectCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="date" type="dateCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="description" type="descriptionCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="publisher" type="publisherCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="type" type="typeCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="format" type="formatCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="identifier" type="identifierCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="source" type="sourceCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="language" type="languageCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="relation" type="relationCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="coverage" type="coverageCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="rights" type="rightsCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="scope" type="scopeCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="castList" type="castListCT" minOccurs="0" maxOccurs="unbounded"/><xs:element name="teiHeader" type="teiHeaderCT" minOccurs="0"/><xs:element name="refSystem" type="refSystemCT" minOccurs="0" maxOccurs="unbounded"/></xs:sequence><xs:attribute name="osisWork" type="osisWorkType" use="required"/><xs:attributeGroup ref="globalWithType"/></xs:complexType><xs:complexType name="workPrefixCT"><xs:attribute name="path" type="osisWorkPrefix" use="required"/><xs:attribute name="osisWork" type="osisWorkType" use="required"/><xs:attributeGroup ref="globalWithoutType"/></xs:complexType><xs:complexType name="aCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="index" type="indexCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="href" type="xs:string" use="required"/><xs:attributeGroup ref="globalWithType"/></xs:complexType><xs:complexType name="abbrCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="index" type="indexCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="expansion" type="xs:string" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="abbr"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="captionCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attributeGroup ref="globalWithType"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="TEIform" fixed="figDesc"/></xs:complexType><xs:complexType name="catchWordCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="inscription" type="inscriptionCT"/><xs:element name="lb" type="lbCT"/><xs:element name="list" type="listCT"/><xs:element name="mentioned" type="mentionedCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="title" type="titleCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="osisRef" type="osisRefType" use="optional"/><xs:attributeGroup ref="globalWithType"/></xs:complexType><xs:complexType name="cellCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="closer" type="closerCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="figure" type="figureCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="inscription" type="inscriptionCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="list" type="listCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="p" type="pCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="salute" type="saluteCT"/><xs:element name="seq" type="segCT"/><xs:element name="signed" type="signedCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="speech" type="speechCT"/><xs:element name="table" type="tableCT"/><xs:element name="title" type="titleCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="role" type="tableRole" use="optional" default="data"/><xs:attribute name="align" type="osisCellAlign" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="cell"/></xs:complexType><xs:complexType name="chapterCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="closer" type="closerCT"/><xs:element name="date" type="dateCT"/><xs:element name="div" type="divCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="figure" type="figureCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="inscription" type="inscriptionCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="list" type="listCT"/><xs:element name="mentioned" type="mentionedCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="p" type="pCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="salute" type="saluteCT"/><xs:element name="seg" type="segCT"/><xs:element name="signed" type="signedCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="speech" type="speechCT"/><xs:element name="table" type="tableCT"/><xs:element name="title" type="titleCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="chapterTitle" type="xs:string" use="optional"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="osisRef" type="osisRefType" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="div"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="closerCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="list" type="listCT"/><xs:element name="mentioned" type="mentionedCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="p" type="pCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="signed" type="signedCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="closer"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="dateCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="index" type="indexCT"/><xs:element name="note" type="noteCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="event" type="eventType" use="optional"/><xs:attribute name="type" type="calendar" use="optional" default="ISO"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="date"/></xs:complexType><xs:complexType name="divCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:sequence><xs:element name="titlePage" type="titlePageCT" minOccurs="0" maxOccurs="1"/><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="chapter" type="chapterCT"/><xs:element name="closer" type="closerCT"/><xs:element name="date" type="dateCT"/><xs:element name="div" type="divCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="figure" type="figureCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="inscription" type="inscriptionCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="list" type="listCT"/><xs:element name="mentioned" type="mentionedCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="p" type="pCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="salute" type="saluteCT"/><xs:element name="seg" type="segCT"/><xs:element name="signed" type="signedCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="speech" type="speechCT"/><xs:element name="table" type="tableCT"/><xs:element name="title" type="titleCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice></xs:sequence><xs:attribute name="canonical" type="xs:boolean" default="false" use="optional"/><xs:attribute name="osisRef" type="osisRefType" use="optional"/><xs:attribute name="scope" type="osisRefType" use="optional"/><xs:attribute name="type" type="divType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="div"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="divineNameCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="index" type="indexCT"/><xs:element name="note" type="noteCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/></xs:complexType><xs:complexType name="figureCT"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="caption" type="captionCT"/><xs:element name="index" type="indexCT"/><xs:element name="note" type="noteCT"/><xs:element name="reference" type="referenceCT"/></xs:choice><xs:attribute name="alt" type="xs:string" use="optional"/><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="catalog" type="xs:string" use="optional"/><xs:attribute name="location" type="xs:string" use="optional"/><xs:attribute name="osisRef" type="osisRefType" use="optional"/><xs:attribute name="rights" type="xs:string" use="optional"/><xs:attribute name="size" type="xs:string" use="optional"/><xs:attribute name="src" type="xs:string"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="figure"/></xs:complexType><xs:complexType name="foreignCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="title" type="titleCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="foreign"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="headCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="head" type="headCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="head"/></xs:complexType><xs:complexType name="hiCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="type" type="hiType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="hi"/></xs:complexType><xs:complexType name="indexCT"><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="index" type="xs:string" use="required"/><xs:attribute name="level1" type="xs:string" use="required"/><xs:attribute name="level2" type="xs:string" use="optional"/><xs:attribute name="level3" type="xs:string" use="optional"/><xs:attribute name="level4" type="xs:string" use="optional"/><xs:attribute name="see" type="xs:string" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="index"/></xs:complexType><xs:complexType name="inscriptionCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="speech" type="speechCT"/><xs:element name="title" type="titleCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/></xs:complexType><xs:complexType name="itemCT" mixed="true"><xs:sequence minOccurs="0" maxOccurs="unbounded"><xs:element name="label" type="labelCT" minOccurs="0"/><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lg" type="lgCT"/><xs:element name="list" type="listCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="p" type="pCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="title" type="titleCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice></xs:sequence><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="role" type="xs:string" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="item"/></xs:complexType><xs:complexType name="labelCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="role" type="xs:string" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="label"/></xs:complexType><xs:complexType name="lCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="chapter" type="chapterCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="mentioned" type="mentionedCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="level" type="xs:positiveInteger" use="optional"/><xs:attribute name="type" type="lineType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="l"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="lbCT"><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="milestone"/></xs:complexType><xs:complexType name="lgCT" mixed="false"><xs:complexContent><xs:extension base="milestoneable"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="chapter" type="chapterCT"/><xs:element name="index" type="indexCT"/><xs:element name="l" type="lCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="q" type="qCT"/><xs:element name="verse" type="verseCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="type" type="lineGroupType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="lg"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="listCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="chapter" type="chapterCT"/><xs:element name="head" type="headCT"/><xs:element name="index" type="indexCT"/><xs:element name="item" type="itemCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="q" type="qCT"/><xs:element name="verse" type="verseCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="list"/></xs:complexType><xs:complexType name="mentionedCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="mentioned"/></xs:complexType><xs:complexType name="milestoneCT"><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="type" type="milestonePt"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="marker" type="xs:string" default="DEFAULT" use="optional"/><xs:attribute name="TEIform" fixed="milestone"/></xs:complexType><xs:complexType name="milestoneEndCT"><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="type" type="milestoneSe"/><xs:attribute name="start" type="xs:string" use="required"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="milestone"/></xs:complexType><xs:complexType name="milestoneStartCT"><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="end" type="xs:string" use="required"/><xs:attribute name="type" type="milestoneSe"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="milestone"/></xs:complexType><xs:complexType name="nameCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="index" type="indexCT"/><xs:element name="note" type="noteCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="regular" type="xs:string" use="optional"/><xs:attribute name="type" type="nameType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="name"/></xs:complexType><xs:complexType name="noteCT" mixed="true"><xs:sequence><xs:element name="note" type="noteCT" minOccurs="0" maxOccurs="unbounded"/><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="catchWord" type="catchWordCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="figure" type="figureCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="inscription" type="inscriptionCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="list" type="listCT"/><xs:element name="mentioned" type="mentionedCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="p" type="pCT"/><xs:element name="q" type="qCT"/><xs:element name="rdg" type="rdgCT"/><xs:element name="rdgGrp" type="rdgGrpCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="table" type="tableCT"/><xs:element name="title" type="titleCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice></xs:sequence><xs:attribute name="canonical" type="xs:boolean" use="optional" default="false"/><xs:attribute name="osisRef" type="osisRefType" use="optional"/><xs:attribute name="placement" type="notePlacement" use="optional"/><xs:attribute name="type" type="noteType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="note"/></xs:complexType><xs:complexType name="pCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="catchWord" type="catchWordCT"/><xs:element name="chapter" type="chapterCT"/><xs:element name="closer" type="closerCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="figure" type="figureCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="inscription" type="inscriptionCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="list" type="listCT"/><xs:element name="mentioned" type="mentionedCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="rdg" type="rdgCT"/><xs:element name="rdgGrp" type="rdgGrpCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="salute" type="saluteCT"/><xs:element name="seg" type="segCT"/><xs:element name="signed" type="signedCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="speech" type="speechCT"/><xs:element name="table" type="tableCT"/><xs:element name="title" type="titleCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="p"/></xs:complexType><xs:complexType name="qCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="closer" type="closerCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="inscription" type="inscriptionCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="list" type="listCT"/><xs:element name="mentioned" type="mentionedCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="p" type="pCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="salute" type="saluteCT"/><xs:element name="seg" type="segCT"/><xs:element name="signed" type="signedCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="level" type="xs:string" use="optional"/><xs:attribute name="marker" type="xs:string" default="DEFAULT" use="optional"/><xs:attribute name="osisRef" type="osisRefType" use="optional"/><xs:attribute name="type" type="quoteType" use="optional"/><xs:attribute name="who" type="xs:string" use="optional"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="q"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="rdgCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="list" type="listCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="p" type="pCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="witness" type="osisRefType" use="optional"/><xs:attribute name="type" type="rdgType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="rdg"/></xs:complexType><xs:complexType name="rdgGrpCT" mixed="false"><xs:sequence><xs:element name="rdg" type="rdgCT" minOccurs="1" maxOccurs="unbounded"/></xs:sequence><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="rdgGrp"/></xs:complexType><xs:complexType name="referenceCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="seg" type="segCT"/><xs:element name="title" type="titleCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional" default="false"/><xs:attribute name="osisRef" type="osisRefType" use="optional"/><xs:attribute name="type" type="referenceType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/></xs:complexType><xs:complexType name="rowCT"><xs:sequence><xs:element name="cell" type="cellCT" maxOccurs="unbounded"/></xs:sequence><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="role" type="tableRole" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="row"/></xs:complexType><xs:complexType name="saluteCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="list" type="listCT"/><xs:element name="mentioned" type="mentionedCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="p" type="pCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="salute"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="segCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="type" type="segType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="seg"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="signedCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="signed"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="speakerCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="index" type="indexCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="who" type="xs:string" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="sp"/></xs:complexType><xs:complexType name="speechCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:sequence><xs:element name="speech" type="speechCT" minOccurs="0" maxOccurs="unbounded"/><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="chapter" type="chapterCT"/><xs:element name="closer" type="closerCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="inscription" type="inscriptionCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="list" type="listCT"/><xs:element name="mentioned" type="mentionedCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="p" type="pCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="salute" type="saluteCT"/><xs:element name="seg" type="segCT"/><xs:element name="signed" type="signedCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="table" type="tableCT"/><xs:element name="title" type="titleCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice></xs:sequence><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="marker" type="xs:string" default="DEFAULT" use="optional"/><xs:attribute name="TEIform" fixed="speech"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="tableCT"><xs:sequence><xs:element name="head" type="headCT" minOccurs="0"/><xs:element name="row" type="rowCT" minOccurs="0" maxOccurs="unbounded"/></xs:sequence><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="cols" type="xs:positiveInteger" use="optional"/><xs:attribute name="rows" type="xs:positiveInteger" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="table"/></xs:complexType><xs:complexType name="titleCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="figure" type="figureCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="inscription" type="inscriptionCT"/><xs:element name="lb" type="lbCT"/><xs:element name="lg" type="lgCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="title" type="titleCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="verse" type="verseCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional" default="false"/><xs:attribute name="level" type="xs:integer" use="optional"/><xs:attribute name="placement" type="titlePlacement" use="optional"/><xs:attribute name="short" type="xs:string" use="optional"/><xs:attribute name="type" type="osisTitleType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/><xs:attribute name="TEIform" fixed="title"/></xs:complexType><xs:complexType name="titlePageCT"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="title" type="titleCT"/><xs:element name="contributor" type="contributorCT"/><xs:element name="creator" type="creatorCT"/><xs:element name="subject" type="subjectCT"/><xs:element name="date" type="dateCT"/><xs:element name="description" type="descriptionCT"/><xs:element name="publisher" type="publisherCT"/><xs:element name="type" type="typeCT"/><xs:element name="format" type="formatCT"/><xs:element name="identifier" type="identifierCT"/><xs:element name="source" type="sourceCT"/><xs:element name="language" type="languageCT"/><xs:element name="relation" type="relationCT"/><xs:element name="coverage" type="coverageCT"/><xs:element name="p" type="pCT"/><xs:element name="figure" type="figureCT"/><xs:element name="milestone" type="milestoneCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional" default="false"/><xs:attributeGroup ref="globalWithType"/></xs:complexType><xs:complexType name="transChangeCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="lb" type="lbCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="type" type="changeType" use="optional"/><xs:attributeGroup ref="globalWithoutType"/></xs:complexType><xs:complexType name="verseCT" mixed="true"><xs:complexContent mixed="true"><xs:extension base="milestoneable"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="abbr" type="abbrCT"/><xs:element name="date" type="dateCT"/><xs:element name="divineName" type="divineNameCT"/><xs:element name="foreign" type="foreignCT"/><xs:element name="hi" type="hiCT"/><xs:element name="index" type="indexCT"/><xs:element name="inscription" type="inscriptionCT"/><xs:element name="lb" type="lbCT"/><xs:element name="list" type="listCT"/><xs:element name="mentioned" type="mentionedCT"/><xs:element name="milestone" type="milestoneCT"/><xs:element name="milestoneEnd" type="milestoneEndCT"/><xs:element name="milestoneStart" type="milestoneStartCT"/><xs:element name="name" type="nameCT"/><xs:element name="note" type="noteCT"/><xs:element name="q" type="qCT"/><xs:element name="reference" type="referenceCT"/><xs:element name="seg" type="segCT"/><xs:element name="speaker" type="speakerCT"/><xs:element name="title" type="titleCT"/><xs:element name="transChange" type="transChangeCT"/><xs:element name="w" type="wCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional" default="true"/><xs:attributeGroup ref="globalWithType"/></xs:extension></xs:complexContent></xs:complexType><xs:complexType name="wCT" mixed="true"><xs:choice minOccurs="0" maxOccurs="unbounded"><xs:element name="a" type="aCT"/><xs:element name="index" type="indexCT"/><xs:element name="note" type="noteCT"/><xs:element name="seg" type="segCT"/></xs:choice><xs:attribute name="canonical" type="xs:boolean" use="optional"/><xs:attribute name="gloss" type="xs:string" use="optional"/><xs:attribute name="lemma" type="osisGenType" use="optional"/><xs:attribute name="morph" type="osisGenType" use="optional"/><xs:attribute name="POS" type="osisGenType" use="optional"/><xs:attribute name="src" type="xs:string" use="optional"/><xs:attribute name="xlit" type="xs:string" use="optional"/><xs:attributeGroup ref="globalWithType"/><xs:attribute name="TEIform" fixed="w"/></xs:complexType><xs:attributeGroup name="globalWithType"><xs:attribute name="annotateRef" type="annotateRefType" use="optional"/><xs:attribute name="annotateWork" type="xs:string" use="optional"/><xs:attribute name="annotateType" type="annotationType" use="optional"/><xs:attribute name="editions" type="xs:NMTOKENS" use="optional"/><xs:attribute name="ID" type="xs:ID" use="optional"/><xs:attribute name="osisID" type="osisIDType" use="optional"/><xs:attribute name="resp" type="xs:string" use="optional"/><xs:attribute name="type" type="attributeExtension" use="optional"/><xs:attribute name="subType" type="attributeExtension" use="optional"/><xs:attribute name="n" type="xs:string" use="optional"/><xs:attribute ref="xml:lang" use="optional"/><xs:attribute ref="xml:space" use="optional"/><xs:attribute name="script" type="osisScripts" use="optional"/></xs:attributeGroup><xs:attributeGroup name="globalWithoutType"><xs:attribute name="annotateRef" type="annotateRefType" use="optional"/><xs:attribute name="annotateWork" type="xs:string" use="optional"/><xs:attribute name="annotateType" type="annotationType" use="optional"/><xs:attribute name="editions" type="xs:NMTOKENS" use="optional"/><xs:attribute name="ID" type="xs:ID" use="optional"/><xs:attribute name="osisID" type="osisIDType" use="optional"/><xs:attribute name="resp" type="xs:string" use="optional"/><xs:attribute name="subType" type="attributeExtension" use="optional"/><xs:attribute name="n" type="xs:string" use="optional"/><xs:attribute ref="xml:lang" use="optional"/><xs:attribute ref="xml:space" use="optional"/><xs:attribute name="script" type="osisScripts" use="optional"/></xs:attributeGroup><xs:complexType name="milestoneable"><xs:attribute name="sID" type="xs:string" use="optional"/><xs:attribute name="eID" type="xs:string" use="optional"/></xs:complexType><xs:simpleType name="osisGenRegex"><xs:restriction base="xs:string"><xs:pattern value="((((\\p{L}|\\p{N}|_)+)(\\.(\\p{L}|\\p{N}|_))*:)?([^:\\s])+)"/></xs:restriction></xs:simpleType><xs:simpleType name="osisIDRegex"><xs:restriction base="xs:string"><xs:pattern value="(((\\p{L}|\\p{N}|_)+)((\\.(\\p{L}|\\p{N}|_)+)*)?:)?((\\p{L}|\\p{N}|_|(\\\\[^\\s]))+)((\\.(\\p{L}|\\p{N}|_|(\\\\[^\\s]))+)*)?(!((\\p{L}|\\p{N}|_|(\\\\[^\\s]))+)((\\.(\\p{L}|\\p{N}|_|(\\\\[^\\s]))+)*)?)?"/></xs:restriction></xs:simpleType><xs:simpleType name="osisRefRegex"><xs:restriction base="xs:string"><xs:pattern value="(((\\p{L}|\\p{N}|_)+)((\\.(\\p{L}|\\p{N}|_)+)*)?:)?((\\p{L}|\\p{N}|_|(\\\\[^\\s]))+)(\\.(\\p{L}|\\p{N}|_|(\\\\[^\\s]))*)*(!((\\p{L}|\\p{N}|_|(\\\\[^\\s]))+)((\\.(\\p{L}|\\p{N}|_|(\\\\[^\\s]))+)*)?)?(@(cp\\[(\\p{Nd})*\\]|s\\[(\\p{L}|\\p{N})+\\](\\[(\\p{N})+\\])?))?(\\-((((\\p{L}|\\p{N}|_|(\\\\[^\\s]))+)(\\.(\\p{L}|\\p{N}|_|(\\\\[^\\s]))*)*)+)(!((\\p{L}|\\p{N}|_|(\\\\[^\\s]))+)((\\.(\\p{L}|\\p{N}|_|(\\\\[^\\s]))+)*)?)?(@(cp\\[(\\p{Nd})*\\]|s\\[(\\p{L}|\\p{N})+\\](\\[(\\p{N})+\\])?))?)?"/></xs:restriction></xs:simpleType><xs:simpleType name="osisScripts"><xs:restriction base="xs:string"><xs:pattern value="([A-Z][a-z]{3}|x-[A-Za-z0-9]+)"/></xs:restriction></xs:simpleType><xs:simpleType name="osisWorkPrefix"><xs:restriction base="xs:string"><xs:pattern value="((//((\\p{L}|\\p{N}|_|-|\\.|:)+))(/(\\p{L}|\\p{N}|_|-|\\.|:)+)?(/@(\\p{L}|\\p{N}|_|-|\\.|:)+))"/></xs:restriction></xs:simpleType><xs:simpleType name="osisWorkType"><xs:restriction base="xs:string"><xs:pattern value="((\\p{L}|\\p{N}|_)+)((\\.(\\p{L}|\\p{N}|_)+)*)?"/></xs:restriction></xs:simpleType><xs:simpleType name="annotateRefType"><xs:list itemType="osisAnnotateRefType"/></xs:simpleType><xs:simpleType name="annotationType"><xs:union memberTypes="osisAnnotation attributeExtension"/></xs:simpleType><xs:simpleType name="attributeExtension"><xs:restriction base="xs:string"><xs:pattern value="x-([^\\s])+"/></xs:restriction></xs:simpleType><xs:simpleType name="calendar"><xs:restriction base="xs:string"><xs:enumeration value="Chinese"/><xs:enumeration value="Gregorian"/><xs:enumeration value="Islamic"/><xs:enumeration value="ISO"/><xs:enumeration value="Jewish"/><xs:enumeration value="Julian"/></xs:restriction></xs:simpleType><xs:simpleType name="changeType"><xs:union memberTypes="osisChanges attributeExtension"/></xs:simpleType><xs:simpleType name="descriptionType"><xs:union memberTypes="osisDescription attributeExtension"/></xs:simpleType><xs:simpleType name="divType"><xs:union memberTypes="osisDivs attributeExtension"/></xs:simpleType><xs:simpleType name="eventType"><xs:union memberTypes="osisEvents attributeExtension"/></xs:simpleType><xs:simpleType name="hiType"><xs:union memberTypes="osisHi attributeExtension"/></xs:simpleType><xs:simpleType name="identifierType"><xs:union memberTypes="osisIdentifier attributeExtension"/></xs:simpleType><xs:simpleType name="languageType"><xs:union memberTypes="osisLanguage attributeExtension"/></xs:simpleType><xs:simpleType name="languageUsage"><xs:union memberTypes="osisLanguageUsage attributeExtension"/></xs:simpleType><xs:simpleType name="lineType"><xs:union memberTypes="osisLine attributeExtension xs:string"/></xs:simpleType><xs:simpleType name="lineGroupType"><xs:union memberTypes="osisLineGroup attributeExtension xs:string"/></xs:simpleType><xs:simpleType name="milestonePt"><xs:union memberTypes="osisMilestonePt attributeExtension"/></xs:simpleType><xs:simpleType name="milestoneSe"><xs:restriction base="xs:string"><xs:enumeration value="abbr"/><xs:enumeration value="chapter"/><xs:enumeration value="closer"/><xs:enumeration value="div"/><xs:enumeration value="foreign"/><xs:enumeration value="l"/><xs:enumeration value="lg"/><xs:enumeration value="q"/><xs:enumeration value="salute"/><xs:enumeration value="seg"/><xs:enumeration value="signed"/><xs:enumeration value="speech"/><xs:enumeration value="verse"/></xs:restriction></xs:simpleType><xs:simpleType name="nameType"><xs:union memberTypes="osisNames attributeExtension"/></xs:simpleType><xs:simpleType name="notePlacement"><xs:union memberTypes="osisPlacementNote attributeExtension"/></xs:simpleType><xs:simpleType name="noteType"><xs:union memberTypes="osisNotes attributeExtension"/></xs:simpleType><xs:simpleType name="quoteType"><xs:union memberTypes="osisQuotes attributeExtension"/></xs:simpleType><xs:simpleType name="referenceType"><xs:union memberTypes="osisReferences attributeExtension"/></xs:simpleType><xs:simpleType name="rdgType"><xs:union memberTypes="osisRdg attributeExtension xs:string"/></xs:simpleType><xs:simpleType name="segType"><xs:union memberTypes="osisSegs attributeExtension"/></xs:simpleType><xs:simpleType name="subjectType"><xs:union memberTypes="osisSubjects attributeExtension"/></xs:simpleType><xs:simpleType name="titlePlacement"><xs:union memberTypes="osisPlacementTitle attributeExtension"/></xs:simpleType><xs:simpleType name="typeType"><xs:union memberTypes="osisType attributeExtension"/></xs:simpleType><xs:simpleType name="osisAnnotateRefType"><xs:union memberTypes="osisRefRegex osisGenRegex"/></xs:simpleType><xs:simpleType name="osisAnnotation"><xs:restriction base="xs:string"><xs:enumeration value="commentary"/><xs:enumeration value="exposition"/><xs:enumeration value="meditation"/><xs:enumeration value="outline"/><xs:enumeration value="rebuttal"/><xs:enumeration value="sermon"/><xs:enumeration value="studyGuide"/><xs:enumeration value="translation"/></xs:restriction></xs:simpleType><xs:simpleType name="osisCellAlign"><xs:restriction base="xs:string"><xs:enumeration value="left"/><xs:enumeration value="right"/><xs:enumeration value="center"/><xs:enumeration value="justify"/><xs:enumeration value="start"/><xs:enumeration value="end"/></xs:restriction></xs:simpleType><xs:simpleType name="osisChanges"><xs:restriction base="xs:string"><xs:enumeration value="added"/><xs:enumeration value="amplified"/><xs:enumeration value="changed"/><xs:enumeration value="deleted"/><xs:enumeration value="implied"/><xs:enumeration value="moved"/><xs:enumeration value="tenseChange"/></xs:restriction></xs:simpleType><xs:simpleType name="osisDescription"><xs:restriction base="xs:string"><xs:enumeration value="usfm"/></xs:restriction></xs:simpleType><xs:simpleType name="osisDivs"><xs:restriction base="xs:string"><xs:enumeration value="acknowledgement"/><xs:enumeration value="afterword"/><xs:enumeration value="annotant"/><xs:enumeration value="appendix"/><xs:enumeration value="article"/><xs:enumeration value="back"/><xs:enumeration value="bibliography"/><xs:enumeration value="body"/><xs:enumeration value="book"/><xs:enumeration value="bookGroup"/><xs:enumeration value="bridge"/><xs:enumeration value="chapter"/><xs:enumeration value="colophon"/><xs:enumeration value="commentary"/><xs:enumeration value="concordance"/><xs:enumeration value="coverPage"/><xs:enumeration value="dedication"/><xs:enumeration value="devotional"/><xs:enumeration value="entry"/><xs:enumeration value="front"/><xs:enumeration value="gazetteer"/><xs:enumeration value="glossary"/><xs:enumeration value="imprimatur"/><xs:enumeration value="index"/><xs:enumeration value="introduction"/><xs:enumeration value="majorSection"/><xs:enumeration value="map"/><xs:enumeration value="outline"/><xs:enumeration value="paragraph"/><xs:enumeration value="part"/><xs:enumeration value="preface"/><xs:enumeration value="publicationData"/><xs:enumeration value="section"/><xs:enumeration value="subSection"/><xs:enumeration value="summary"/><xs:enumeration value="tableofContents"/><xs:enumeration value="titlePage"/></xs:restriction></xs:simpleType><xs:simpleType name="osisEvents"><xs:restriction base="xs:string"><xs:enumeration value="edition"/><xs:enumeration value="eversion"/><xs:enumeration value="imprint"/><xs:enumeration value="original"/></xs:restriction></xs:simpleType><xs:simpleType name="osisGenType"><xs:list itemType="osisGenRegex"/></xs:simpleType><xs:simpleType name="osisHi"><xs:restriction base="xs:string"><xs:enumeration value="acrostic"/><xs:enumeration value="bold"/><xs:enumeration value="emphasis"/><xs:enumeration value="illuminated"/><xs:enumeration value="italic"/><xs:enumeration value="line-through"/><xs:enumeration value="normal"/><xs:enumeration value="small-caps"/><xs:enumeration value="sub"/><xs:enumeration value="super"/><xs:enumeration value="underline"/></xs:restriction></xs:simpleType><xs:simpleType name="osisIdentifier"><xs:restriction base="xs:string"><xs:enumeration value="Dewey"/><xs:enumeration value="DOI"/><xs:enumeration value="ISBN"/><xs:enumeration value="ISSN"/><xs:enumeration value="LCCN"/><xs:enumeration value="OSIS"/><xs:enumeration value="SICI"/><xs:enumeration value="URI"/><xs:enumeration value="URL"/><xs:enumeration value="URN"/></xs:restriction></xs:simpleType><xs:simpleType name="osisIDType"><xs:list itemType="osisIDRegex"/></xs:simpleType><xs:simpleType name="osisLanguage"><xs:restriction base="xs:string"><xs:enumeration value="IANA"/><xs:enumeration value="IETF"/><xs:enumeration value="ISO-639-1"/><xs:enumeration value="ISO-639-2"/><xs:enumeration value="ISO-639-2-B"/><xs:enumeration value="ISO-639-2-T"/><xs:enumeration value="LINGUIST"/><xs:enumeration value="other"/><xs:enumeration value="SIL"/></xs:restriction></xs:simpleType><xs:simpleType name="osisLanguageUsage"><xs:restriction base="xs:string"><xs:enumeration value="base"/><xs:enumeration value="didactic"/><xs:enumeration value="interlinear"/><xs:enumeration value="original"/><xs:enumeration value="quotation"/><xs:enumeration value="source"/><xs:enumeration value="target"/><xs:enumeration value="translation"/></xs:restriction></xs:simpleType><xs:simpleType name="osisLine"><xs:restriction base="xs:string"><xs:enumeration value="refrain"/><xs:enumeration value="doxology"/><xs:enumeration value="selah"/><xs:enumeration value="attribution"/></xs:restriction></xs:simpleType><xs:simpleType name="osisLineGroup"><xs:restriction base="xs:string"></xs:restriction></xs:simpleType><xs:simpleType name="osisMilestonePt"><xs:restriction base="xs:string"><xs:enumeration value="column"/><xs:enumeration value="cQuote"/><xs:enumeration value="footer"/><xs:enumeration value="halfLine"/><xs:enumeration value="header"/><xs:enumeration value="line"/><xs:enumeration value="pb"/><xs:enumeration value="screen"/></xs:restriction></xs:simpleType><xs:simpleType name="osisNames"><xs:restriction base="xs:string"><xs:enumeration value="geographic"/><xs:enumeration value="holiday"/><xs:enumeration value="nonhuman"/><xs:enumeration value="person"/><xs:enumeration value="ritual"/></xs:restriction></xs:simpleType><xs:simpleType name="osisNotes"><xs:restriction base="xs:string"><xs:enumeration value="allusion"/><xs:enumeration value="alternative"/><xs:enumeration value="background"/><xs:enumeration value="citation"/><xs:enumeration value="crossReference"/><xs:enumeration value="devotional"/><xs:enumeration value="encoder"/><xs:enumeration value="exegesis"/><xs:enumeration value="explanation"/><xs:enumeration value="liturgical"/><xs:enumeration value="speaker"/><xs:enumeration value="study"/><xs:enumeration value="translation"/><xs:enumeration value="variant"/></xs:restriction></xs:simpleType><xs:simpleType name="osisPlacementNote"><xs:restriction base="xs:string"><xs:enumeration value="foot"/><xs:enumeration value="end"/><xs:enumeration value="inline"/><xs:enumeration value="left"/><xs:enumeration value="right"/><xs:enumeration value="interlinear"/><xs:enumeration value="apparatus"/></xs:restriction></xs:simpleType><xs:simpleType name="osisPlacementTitle"><xs:restriction base="xs:string"><xs:enumeration value="leftHead"/><xs:enumeration value="centerHead"/><xs:enumeration value="rightHead"/><xs:enumeration value="insideHead"/><xs:enumeration value="outsideHead"/><xs:enumeration value="leftFoot"/><xs:enumeration value="centerFoot"/><xs:enumeration value="rightFoot"/><xs:enumeration value="insideFoot"/><xs:enumeration value="outsideFoot"/></xs:restriction></xs:simpleType><xs:simpleType name="osisQuotes"><xs:restriction base="xs:string"><xs:enumeration value="block"/><xs:enumeration value="citation"/><xs:enumeration value="embedded"/></xs:restriction></xs:simpleType><xs:simpleType name="osisReferences"><xs:restriction base="xs:string"><xs:enumeration value="annotateRef"/><xs:enumeration value="parallel"/><xs:enumeration value="source"/></xs:restriction></xs:simpleType><xs:simpleType name="osisRdg"><xs:restriction base="xs:string"><xs:enumeration value="alternate"/><xs:enumeration value="variant"/></xs:restriction></xs:simpleType><xs:simpleType name="osisRefType"><xs:list itemType="osisRefRegex"/></xs:simpleType><xs:simpleType name="osisRoles"><xs:restriction base="xs:string"><xs:enumeration value="adp"/><xs:enumeration value="ann"/><xs:enumeration value="art"/><xs:enumeration value="aut"/><xs:enumeration value="aqt"/><xs:enumeration value="aft"/><xs:enumeration value="aui"/><xs:enumeration value="bnd"/><xs:enumeration value="bdd"/><xs:enumeration value="bkd"/><xs:enumeration value="bkp"/><xs:enumeration value="bjd"/><xs:enumeration value="bpd"/><xs:enumeration value="ctg"/><xs:enumeration value="clb"/><xs:enumeration value="cmm"/><xs:enumeration value="cwt"/><xs:enumeration value="com"/><xs:enumeration value="ctb"/><xs:enumeration value="cre"/><xs:enumeration value="edt"/><xs:enumeration value="encoder"/><xs:enumeration value="ilu"/><xs:enumeration value="ill"/><xs:enumeration value="pbl"/><xs:enumeration value="trl"/></xs:restriction></xs:simpleType><xs:simpleType name="osisSegs"><xs:restriction base="xs:string"><xs:enumeration value="alluded"/><xs:enumeration value="keyword"/><xs:enumeration value="otPassage"/><xs:enumeration value="verseNumber"/></xs:restriction></xs:simpleType><xs:simpleType name="osisSubjects"><xs:restriction base="xs:string"><xs:enumeration value="ATLA"/><xs:enumeration value="BILDI"/><xs:enumeration value="DBC"/><xs:enumeration value="DDC"/><xs:enumeration value="EUT"/><xs:enumeration value="FGT"/><xs:enumeration value="LCC"/><xs:enumeration value="LCSH"/><xs:enumeration value="MeSH"/><xs:enumeration value="NLSH"/><xs:enumeration value="RSWK"/><xs:enumeration value="SEARS"/><xs:enumeration value="SOG"/><xs:enumeration value="SWD_RSWK"/><xs:enumeration value="UDC"/><xs:enumeration value="VAT"/></xs:restriction></xs:simpleType><xs:simpleType name="roleType"><xs:union memberTypes="osisRoles attributeExtension"/></xs:simpleType><xs:simpleType name="osisTitles"><xs:restriction base="xs:string"><xs:enumeration value="acrostic"/><xs:enumeration value="chapter"/><xs:enumeration value="continued"/><xs:enumeration value="main"/><xs:enumeration value="parallel"/><xs:enumeration value="psalm"/><xs:enumeration value="runningHead"/><xs:enumeration value="scope"/><xs:enumeration value="sub"/></xs:restriction></xs:simpleType><xs:simpleType name="osisTitleType"><xs:union memberTypes="osisTitles attributeExtension"/></xs:simpleType><xs:simpleType name="osisType"><xs:restriction base="xs:string"><xs:enumeration value="OSIS"/></xs:restriction></xs:simpleType><xs:simpleType name="tableRole"><xs:restriction base="xs:string"><xs:enumeration value="label"/><xs:enumeration value="data"/></xs:restriction></xs:simpleType></xs:schema>'