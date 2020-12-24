# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/validity/dissertation.py
# Compiled at: 2015-04-13 16:10:50
"""A dissertation DTD that uses all basic constraints

<!ELEMENT dissertation (dedication?, chapter+, appendix*)>
<!ELEMENT dedication (#PCDATA)>
<!ELEMENT chapter (title, paragraph+)>
<!ELEMENT title (#PCDATA)>
<!ELEMENT paragraph (#PCDATA | figure | table)+>
<!ELEMENT figure EMPTY>
<!ELEMENT table EMPTY>
<!ELEMENT appendix (#PCDATA)>
"""
from gnosis.xml.validity import *

class appendix(PCDATA):
    pass


class table(EMPTY):
    pass


class figure(EMPTY):
    pass


class _mixedpara(Or):
    _disjoins = (PCDATA, figure, table)


class paragraph(Some):
    _type = _mixedpara


class title(PCDATA):
    pass


class _paras(Some):
    _type = paragraph


class chapter(Seq):
    _order = (title, _paras)


class dedication(PCDATA):
    pass


class _apps(Any):
    _type = appendix


class _chaps(Some):
    _type = chapter


class _dedi(Maybe):
    _type = dedication


class dissertation(Seq):
    _order = (_dedi, _chaps, _apps)


explicit_section = "section(( dedication(PCDATA('To Mom')),\n              chapter(( title(PCDATA('It starts')),\n                        _paras([paragraph(\n                                [_mixedpara(\n                                  PCDATA('When it began'))])])\n                      ))\n           ))"
lifting_section = "LiftSeq(section, ('To Mom',('It starts','When it began...')))"

def mk_dissertation():
    """Miscellaneous other typical uses"""
    p = paragraph(['spam and eggs', figure(), 'toast'])
    ps_ch1 = _paras([p, paragraph('this and that'), 'something else',
     paragraph(_mixedpara(figure())),
     paragraph(['stuff', table(), PCDATA('still more')])])
    chap1 = chapter((title('My chapter'), ps_ch1))
    dedict = _dedi(dedication('To Mom'))
    diss = LiftSeq(dissertation, ([], _chaps(chap1), _apps()))
    ps_ch1 += ['friend, romans, countrymen',
     paragraph([figure(), table(), figure()])]
    ps_ch1.append('whatever')
    ps_ch1 += 'Just words'
    del ps_ch1[-2]
    return diss


if __name__ == '__main__':
    from sys import exit

    class section(Seq):
        _order = (dedication, chapter)


    print '____________ Fully spelled out section initialization _________________'
    print explicit_section
    print '--'
    print eval(explicit_section)
    print "________ Aggressive use of 'lifting' in initialization ________________"
    print lifting_section
    print '--'
    print eval(lifting_section)
    print '________ Various other OK initializations and operations ______________'
    print '            (See code for comments and constructs)'
    print
    print mk_dissertation()