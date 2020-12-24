# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tome\tomeTempl.py
# Compiled at: 2013-01-25 20:05:41
"""
Adds some additional "built-in" functions to templ, for use with tome.
"""
import templ.texec, templ.ttypes, templ.texceptions

@templ.texec.function
class xRomanUpper(templ.texec.MathExec, templ.texec.TFunction):
    """
    {roman-up NUMBER}

    Returns a string giving the value of the given NUMBER in upper-case Roman numerals.
    """
    __mnemonics__ = ('roman-up', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        number = self.parseNumericArg(name, 0, args)
        if number <= 0:
            raise templ.texceptions.TemplateValueError('Invalid argument for "%s": expected a value greater than 0.' % name, self.filepos, 0)
        else:
            if number >= 4000:
                raise templ.texceptions.TemplateValueError('Invalid argument for "%s": cannot represent values greater than 3999 in Roman numerals.' % name, self.filepos, 0)
            symbols = (
             ('I', 'V'), ('X', 'L'), ('C', 'D'), ('M', None), (None, None))
            xstr = ''
            idx = 0
            while number > 0:
                number, digit = divmod(number, 10)
                one, five = symbols[idx]
                ten, fifty = symbols[(idx + 1)]
                idx += 1
                if digit == 0:
                    pass
                elif digit in (1, 2, 3):
                    xstr = one * digit + xstr
                elif digit == 4:
                    xstr = one + five + xstr
                elif digit == 5:
                    xstr = five + xstr
                elif digit in (6, 7, 8):
                    xstr = five + one * (digit - 5) + xstr
                else:
                    xstr = one + ten + xstr

        return templ.ttypes.String(xstr)


@templ.texec.function
class xRomanLower(xRomanUpper):
    """
    {roman-low NUMBER}

    Returns a string giving the value of the given NUMBER in upper-case Roman numerals.
    """
    __mnemonics__ = ('roman-low', )

    def execute(self, name, args, ostream, stack):
        tstr = super(xRomanLower, self).execute(name, args, ostream, stack)
        xstr = tstr.str
        return templ.ttypes.String(xstr.lower())