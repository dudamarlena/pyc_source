# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\templ\tbuiltin.py
# Compiled at: 2013-07-26 13:05:06
"""
Copyright 2013 Brian Mearns

This file is part of templ.

templ is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

templ is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with templ.  If not, see <http://www.gnu.org/licenses/>.

*****************************************************************************

Builtin executables.
"""
import ttypes, texec, filepos as tFilepos, teval, texceptions, os, sys, tstreams, math, version, time, calendar, random, subprocess, templ, StringIO

@texec.function
class xList(texec.TFunction):
    """
    {list [VAL1 [VAL2 [...]]] }

    Returns a List of the given elements.
    """
    __mnemonics__ = ('list', "'", 'list.new')

    def execute(self, name, args, ostream, stack):
        return ttypes.List(args)


@texec.function
class xEscList(texec.TFunction):
    """
    {esc-list LIST}

    Returns a new List equivalent to the given list, but with a ' inserted as the first element.
    Useful for escaping lists in macros.
    """
    __mnemonics__ = ('esc-list', 'list.esc')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        xlist = list(self.checkArgType(name, 0, args, ttypes.List).list)
        return ttypes.List(["'"] + xlist)


@texec.function
class xSort(texec.TFunction):
    """
    {sort LIST}

    Returns a new list containing all of the elements in LIST, but sorted in lexicographical order. Sorting
    only works for lists that contain only string, otherwise it is an error.
    """
    __mnemonics__ = ('sort', 'list.sort')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        self.checkArgType(name, 0, args, ttypes.List)

        def key(string):
            self.checkType('element of List.', string, ttypes.String)
            return string.str

        return ttypes.List(sorted(args[0].list, key=key))


@texec.function
class xEcho(texec.TFunction):
    """
    {echo [VAL0 [VAL1 [...]]]}
    """
    __mnemonics__ = ('echo', 'exp.echo')

    def execute(self, name, args, ostream, stack):
        count = len(args)
        string = ''
        for i in xrange(count):
            self.checkArgType(name, i, args, ttypes.String)
            string += args[i].str

        ostream.write(string)
        return


@texec.function
class xImplode(texec.TFunction):
    """
    {implode [GLUE] LIST}
    """
    __mnemonics__ = ('implode', 'imp', 'pck.join')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2])
        if count == 1:
            glue = ''
            self.checkArgType(name, 0, args, ttypes.List)
            tlist = args[0]
        else:
            self.checkArgType(name, 0, args, ttypes.String)
            glue = args[0].str
            self.checkArgType(name, 1, args, ttypes.List)
            tlist = args[1]
        strings = []
        for i in xrange(len(tlist)):
            self.checkType('element %d in LIST argument of "%s" function' % (i, name), tlist[i], ttypes.String)
            strings.append(tlist[i].str)

        return ttypes.String(glue.join(strings))


@texec.function
class xJoin(texec.TFunction):
    """
    {join GLUE [VAL0 [VAL1 [...]]])
        Possible Alias: ">*<"
        Aliases: "exp.join" as in "expanded" because the args are not packed into a list.
        : Like implode, but the values are unpacked instead of in a list.
    """
    __mnemonics__ = ('join', 'exp.join', '>*<')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, min=1)
        self.checkArgType(name, 0, args, ttypes.String)
        glue = args[0].str
        strings = []
        for i in xrange(1, count):
            self.checkArgType(name, i, args, ttypes.String)
            strings.append(args[i].str)

        return ttypes.String(glue.join(strings))


@texec.macro
class xGlue(texec.TMacro):
    """
    {glue [VAL0 [VAL1 [...]]])
        Possible Alias: "><"
        Qualified name: str.cat
        : macro alias for {join "" ... }
    """
    __mnemonics__ = ('glue', 'str.cat', '><')

    def execute(self, name, args, ostream, stack):
        return ttypes.List(['join', ''] + list(args))


@texec.macro
class xSpit(texec.TMacro):
    """
    {spit LIST}
    """
    __mnemonics__ = ('spit', 'pck.echo')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        self.checkArgType(name, 0, args, ttypes.List)
        return ttypes.List(['echo', ['implode', '', args[0]]])


@texec.function
class xStr(texec.TFunction):
    """
    {str VAL}
        Qualified name: str.new
        : Converts VAL to a String form, regardless of it's Type.
    """
    __mnemonics__ = ('str', 'str.new')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        if isinstance(args[0], ttypes.String):
            return args[0]
        else:
            return ttypes.String(str(args[0]))


@texec.function
class xGetset(texec.TFunction):
    """
    {getset NAME [VALUE]}
        Aliases: "$"
        :If two arguments are given, sets the value of the lowest occurence of
        :NAME in the stack to VALUE, and results in VALUE. If the value
        :doesn't exist, it's created in the current (lowest) scope.
        :
        :If one argument is given, just looks up NAME in the stack and returns
        :the value. Error if no such symbol exists.
    """
    __mnemonics__ = ('getset', '$')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2])
        self.checkArgType(name, 0, args, ttypes.String)
        if count == 1:
            val = stack.lookup(args[0])
            if val is None:
                raise texceptions.NoSuchSymbolException(args[0].str, args[0].filepos)
            return val
        stack.set(args[0], args[1])
        return args[1]
        return


@texec.function
class xSubstr(texec.TFunction, texec.IndexExec):
    """
    {substr FIRST [END] STRING}
        Qualified name: str.slice

    Returns a substring of `STRING` starting with index `FIRST` and
    ending immediately before index `END`, or the end of the string
    whichever comes first. Not an error if `END` runs past the end of the
    string. If it does not run past, then the length of the string is
    END - FIRST. If FIRST is not less than END, then it is an empty string.

    Negative indices are valid, they specify distances from the end of the
    string, so -1 is the last character. I.e., if FIRST is -1 and END is
    unspecified, it will return the last character of the string.

    END can also be the special string "END" (case sensitive), as an
    alternative to not specifying it. In otherwords, that means it will
    go all the way to the end.
    """
    __mnemonics__ = ('substr', 'str.slice')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[2, 3])
        first = self.parseIndexArg(name, 0, args)
        last = None
        if count == 3:
            last = self.parseEndIndexArg(name, 1, args)
            stringIdx = 2
        else:
            stringIdx = 1
        string = self.checkArgType(name, stringIdx, args, ttypes.String)
        if last is None:
            last = len(string)
        return ttypes.String(string.str[first:last])


@texec.macro
class xCharAt(texec.TMacro):
    """
    {char-at INDEX STRING}
        Qualified name: str.at
        : Macro alias for {substr INDEX INDEX+1 STRING}
    """
    __mnemonics__ = ('char-at', 'str.at')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        return ttypes.List(['substr', args[0], ['add', args[0], '1'], args[1]])


@texec.function
class xStrpos(texec.FindExec, texec.TFunction):
    """
    {strpos NEEDLE [START [END]] HAYSTACK}
    Searches for the index of the first occurrence of NEEDLE in
    HAYSTACK, starting no SOONER than START and ending *before* END. If
    three args given, END is defualt. Default START is 0, Default END is
    to search the length of the string (search all the way to the end).
    Returns ttypes.Null if not found, otherwise a *positive* index into
    HAYSTACK.

    The special value "END" (case sensitive) is acceptable for the `END` argument.
    See `substr` for details.
    """
    __mnemonics__ = ('strpos', 'str.find')

    def find(self, name, needle, start, end, haystack, args, needleIdx, startIdx, endIdx, haystackIdx):
        self.checkArgType(name, needleIdx, args, ttypes.String)
        self.checkArgType(name, haystackIdx, args, ttypes.String)
        length = len(haystack)
        if end is None:
            end = length
        return haystack.str.find(needle.str, start, end)


@texec.function
class xType(texec.TFunction):
    """
    {type VALUE}

    Returns a string describing the type of VALUE.
    """
    __mnemonics__ = ('type', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.String(str(type(args[0])))


@texec.function
class xIsNull(texec.IsTypeExec, texec.TFunction):
    """
        {is-null X}
                Qualified name: null.is

    Returns "1" is X is ttypes.Null, "0" otherwise.
    """
    __mnemonics__ = ('is-null', 'null.is')

    @property
    def expectedType(self):
        return ttypes.Null


@texec.function
class xIsStr(texec.IsTypeExec, texec.TFunction):
    """
        {is-str X}
    Returns "1" is X is a String, "0" otherwise.
    """
    __mnemonics__ = ('is-str', 'str.is')

    @property
    def expectedType(self):
        return ttypes.String


@texec.function
class xIsList(texec.IsTypeExec, texec.TFunction):
    """
        {is-list X}
    Returns "1" is X is a List, "0" otherwise.
    """
    __mnemonics__ = ('is-list', 'list.is')

    @property
    def expectedType(self):
        return ttypes.List


@texec.function
class xIsExe(texec.IsTypeExec, texec.TFunction):
    """
        {is-exe X}
    Returns "1" is X is an Executable, "0" otherwise.
    """
    __mnemonics__ = ('is-exe', 'exe.is')

    @property
    def expectedType(self):
        return texec.Executable


@texec.function
class xIsFunc(texec.IsTypeExec, texec.TFunction):
    """
        {is-func X}
    Returns "1" is X is a Function Executable, "0" otherwise.
    """
    __mnemonics__ = ('is-func', 'func.is')

    @property
    def expectedType(self):
        return texec.TFunction


@texec.function
class xIsOper(texec.IsTypeExec, texec.TFunction):
    """
        {is-oper X}
    Returns "1" is X is an Operator Executable, "0" otherwise.
    """
    __mnemonics__ = ('is-oper', 'oper.is')

    @property
    def expectedType(self):
        return texec.TOperator


@texec.function
class xIsMacro(texec.IsTypeExec, texec.TFunction):
    """
        {is-macro X}
    Returns "1" is X is a Macro Executable, "0" otherwise.
    """
    __mnemonics__ = ('is-macro', 'macro.is')

    @property
    def expectedType(self):
        return texec.TMacro


@texec.macro
class xInStr(texec.TMacro):
    """
        {in-str NEEDLE [START] [END] HAYSTACK}
                Qualified name: str.in
                :Macro alias for {not {is-null {strpos NEEDLE START END HAYSTACK}}}.
    """
    __mnemonics__ = ('in-str', 'str.in')

    def execute(self, name, args, ostream, stack):
        return ttypes.List(['not', ['is-null', ['strpos'] + list(args)]])


@texec.function
class xStrReverse(texec.TFunction):
    """
        {str.reverse STRING}
    Returns a new String with is the reverse of the given `STRING`.
    """
    __mnemonics__ = ('str.reverse', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        string = self.checkArgType(name, 0, args, ttypes.String)
        return ttypes.String(('').join(reversed(string.str)))


@texec.function
class xToLower(texec.TFunction):
    """
        {to-lower STRING}
                : Returns a copy of STRING with all character replaced by lower-case
                : versions.
    """
    __mnemonics__ = ('to-lower', 'str.lower')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        string = self.checkArgType(name, 0, args, ttypes.String)
        return ttypes.String(string.str.lower())


@texec.function
class xToUpper(texec.TFunction):
    """
        {to-upper STRING}
                : Returns a copy of STRING with all character replaced by upper-case
                : versions.
    """
    __mnemonics__ = ('to-upper', 'str.upper')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        string = self.checkArgType(name, 0, args, ttypes.String)
        return ttypes.String(string.str.upper())


@texec.function
class xStrlen(texec.TFunction):
    """
        {strlen STRING}
                Qualified name: str.len
                :Returns the number of characters in STRING.
    """
    __mnemonics__ = ('strlen', 'str.len')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        string = self.checkArgType(name, 0, args, ttypes.String)
        return ttypes.String(len(string))


@texec.function
class xFlatten(texec.TFunction):
    """
        {flatten LIST}
                Qualified name: list.flatten

                Returns flattened version of the list: when a nested list is found,
                it is flattened and the flattened version is expanded to take it's
                place.
    """
    __mnemonics__ = ('flatten', 'list.flatten')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        tlist = self.checkArgType(name, 0, args, ttypes.List)
        return ttypes.List(self.flatten(tlist))

    def flatten(self, tlist):
        res = []
        for element in tlist:
            if isinstance(element, ttypes.List):
                res += self.flatten(element)
            else:
                res.append(element)

        return res


@texec.function
class xFind(texec.FindExec, texec.TFunction):
    """
        {find NEEDLE [START] [END] HAYSTACK}
                Qualified name: list.find
                : Finds the index into HAYSTACK of the first occurence of something
                : equal to the value NEEDLE, which can be any type. START and END are
                : as with strpos. Returns ttypes.Null if not found.
    """
    __mnemonics__ = ('find', 'list.find')

    def find(self, name, needle, start, end, haystack, args, needleIdx, startIdx, endIdx, haystackIdx):
        self.checkArgType(name, haystackIdx, args, ttypes.List)
        length = len(haystack)
        if end is None:
            end = length
        try:
            return haystack.list.index(needle, start, end)
        except ValueError:
            return

        return


@texec.macro
class xIn(texec.TMacro):
    """
        {in NEEDLE [START] [END] HAYSTACK}
                Qualified name: list.in
                : Macro alias for {not {is-null {find NEEDLE START END HAYSTACK}}}.
    """
    __mnemonics__ = ('in', 'list.in')

    def execute(self, name, args, ostream, stack):
        return ttypes.List(['not', ['is-null', ['find'] + list(args)]])


@texec.function
class xReverse(texec.TFunction):
    """
        {reverse LIST}
                Qualified name: list.reverse
                : Returns a copy of LIST in the opposite order.
    """
    __mnemonics__ = ('reverse', 'list.reverse')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        tlist = self.checkArgType(name, 0, args, ttypes.List)
        return ttypes.List(reversed(tlist))


@texec.function
class xChars(texec.TFunction):
    """
        {chars STRING}
                Qualified name: str.list
                : Returns a new list whose elements are individual characters of
                : STRING.
    """
    __mnemonics__ = ('chars', 'str.list')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        string = self.checkArgType(name, 0, args, ttypes.String)
        return ttypes.List(c for c in string)


@texec.function
class xChr(texec.TFunction, texec.IndexExec):
    """
        {chr VAL}
                Returns a String of one character, the character has a numerical
                value given by `VAL`. Note this this supports unicode characters
        natively as strings are stored internally as a sequence of code points.
        When it comes time to output the string, you'll need to either encode it
        to bytes using the `unicode` function, or else ensure that `templ`
        has been invoked with the proper output encoding.
    """
    __mnemonics__ = ('chr', 'unichr')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        idx = self.parseIndexArg(name, 0, args)
        try:
            return ttypes.String(unichr(idx))
        except ValueError:
            raise texceptions.TemplateValueError('Index value out of range for function "%s".' % name, args[0].filepos, args[0])


@texec.function
class xDecode(texec.TFunction):
    """
        {decode STRING [ENC]}
                Decodes a byte string into a unicode string using the given encoding.
        Internally, all strings are stored as a sequence of numerical code points
        and "byte strings" and "unicode strings" are not differentiated. The
        input parameter `STRING` is assumed to consist entirely of codepoints
        less than 256 and further that the codepoints, treated as octets,
        are valid under the specified encoding. In this case, the result of
        this function is a new string whose codepoints are the decoded values.

        In otherwords, this takes codepoints which have been encoded into one or
        more bytes, and decodes them back into the original codepoint. Note that
        this may change the length of the string.
    """
    __mnemonics__ = ('decode', 'unicode.decode')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1, 2])
        string = self.checkArgType(name, 0, args, ttypes.String).str
        if len(args) > 1:
            enc = self.checkArgType(name, 1, args, ttypes.String).str
        else:
            enc = 'utf-8'
        try:
            return ttypes.String(string.decode(enc))
        except ValueError:
            raise texceptions.TemplateValueError('Index value out of range for function "%s".' % name, args[0].filepos, args[0])


@texec.function
class xEncode(texec.TFunction):
    """
        {encode STRING [ENC]}
                Encodes the value `STRING` using the specified `ENC`, or UTF-8 if `ENC`
        is not given. Strings are stored internally as a sequence of numerical
        codepoints (one codepoint per character): encoding represents each
        codepoint as one or more octets and results in a string where each
        of the resulting octets is stored as an individual character (whose
        code point is equal to the byte value).
    """
    __mnemonics__ = ('encode', 'unicode.encode')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1, 2])
        string = self.checkArgType(name, 0, args, ttypes.String).str
        if len(args) > 1:
            enc = self.checkArgType(name, 1, args, ttypes.String).str
        else:
            enc = 'utf-8'
        try:
            return ttypes.String(string.encode(enc))
        except ValueError:
            raise texceptions.TemplateValueError('Index value out of range for function "%s".' % name, args[0].filepos, args[0])


@texec.function
class xOrd1(texec.TFunction):
    """
        {ord-1 CHAR}
                Same as ord, but doesn't care if CHAR has more than one character
                or not, it just gives the ORD of the first character.
    """
    __mnemonics__ = ('ord-1', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        string = self.checkArgType(name, 0, args, ttypes.String)
        if len(string) < 1:
            raise texceptions.TemplateValueError('Argument to function "%s" must have at least one character.' % name, args[0].filepos, string)
        return ttypes.String(ord(string.str[0]))


@texec.function
class xOrd(texec.TFunction):
    """
        {ord CHAR}
                : Returns a ttypes.String representing the integer value of the single
                : character CHAR. CHAR must be a String, and must have exactly one
                : character, otherwise you get an exception. You can use `ord1`
                : instead.
    """
    __mnemonics__ = ('ord', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        string = self.checkArgType(name, 0, args, ttypes.String)
        if len(string) != 1:
            raise texceptions.TemplateValueError('Argument to function "%s" must have exactly one character.' % name, args[0].filepos, string)
        return ttypes.String(ord(string.str))


@texec.function
class xCat(texec.TFunction):
    """
        {cat [LIST0 [LIST1 [...]]]}
                Qualified name: list.cat
                : REturns a new list consisting of all the given lists strung
                : together. With no args, results in an empty list.
    """
    __mnemonics__ = ('cat', 'list.cat')

    def execute(self, name, args, ostream, stack):
        count = len(args)
        res = []
        for i in xrange(count):
            res += self.checkArgType(name, i, args, ttypes.List).list

        return ttypes.List(res)


@texec.function
class xAt(texec.IndexExec, texec.TFunction):
    """
        {at IDX LIST}
                Qualified name: list.at
                Aliases: "@"
                :Returns the element at index IDX in LIST. Error if IDX is out of
                :bounds. negative indices are acceptable, but not END.
    """
    __mnemonics__ = ('at', '@', 'list.at')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        idx = self.parseIndexArg(name, 0, args)
        tlist = self.checkArgType(name, 1, args, ttypes.List)
        if idx >= len(tlist) or idx < 0 and -idx > len(tlist):
            raise texceptions.TemplateSequenceIndexOutOfBoundsError('Out of bounds index specified for first argument of "%s".' % name, args[0].filepos, len(tlist), idx)
        return tlist[idx]


@texec.function
class xSlice(texec.IndexExec, texec.TFunction):
    """
        {slice FIRST [END] LIST}
                Qualified name: list.slice
                :Returns a new List with the specified elements of List. Starts at
                :FIRST, ends right before END. If END isn't given, it's the length of
                :the list. Not an error for END to go past the end of the list, it
                :just truncates.
    """
    __mnemonics__ = ('slice', 'list.slice')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[2, 3])
        first = self.parseIndexArg(name, 0, args)
        last = None
        if count == 3:
            last = self.parseEndIndexArg(name, 1, args)
            listIdx = 2
        else:
            listIdx = 1
        tlist = self.checkArgType(name, listIdx, args, ttypes.List)
        if last is None:
            last = len(tlist)
        return ttypes.List(tlist.list[first:last])


@texec.function
class xLen(texec.TFunction):
    """
        {len LIST}
                Qualified name: "list.len"
                :Returns the number of elements in List LIST.
    """
    __mnemonics__ = ('len', 'list.len')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        tlist = self.checkArgType(name, 0, args, ttypes.List)
        return ttypes.String(len(tlist))


@texec.function
class xEmpty(texec.TFunction):
    """
        {empty LIST}
                Aliases: "mt", "is-empty", "list.empty"
                :True if LIST has 0 elements in it. This is a question, not a
                :constructor. You might be looking for `nil`.
    """
    __mnemonics__ = ('empty', 'mt', 'is-empty', 'list.empty')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        tlist = self.checkArgType(name, 0, args, ttypes.List)
        return ttypes.String(bool(len(tlist) == 0))


@texec.macro
class xNil(texec.TMacro):
    """
        {nil}
                Qualified name: "list.nil"
                :Creates a new empty array. This is a macro expansion of {' }.
    """
    __mnemonics__ = ('nil', 'list.nil')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.List(['list'])


@texec.function
class xLet(texec.TFunction):
    """
        {let [NAME0 [NAME1 [...]]]}
                Qualified name: exp.let
                :Adds new symbols to the lowest scope in the stack.
        Returns null.
    """
    __mnemonics__ = ('let', 'exp.let')

    def execute(self, name, args, ostream, stack):
        count = len(args)
        for i in xrange(count):
            arg = self.checkArgType(name, i, args, ttypes.String)
            if stack.localExists(arg):
                raise texceptions.TemplateKeyError('Local variable "%s" already exists: cannot allocate with "%s".' % (arg.str, name), arg.filepos)
            else:
                stack.new(arg, ttypes.Null(filepos=arg.filepos))

        return ttypes.Null()


@texec.function
class xPckLet(texec.TFunction):
    """
        {pck.let LIST}
                :For each element in LIST, a new symbol with that name is created in
                :the lowest scope on the stack.
                :Elements of LIST must all be Strings.
    """
    __mnemonics__ = ('pck.let', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        tlist = self.checkArgType(name, 0, args, ttypes.List)
        for i in xrange(len(tlist)):
            arg = self.checkType('%s element of argument to "%s".' % (self.ordinal(i), name), tlist[i], ttypes.String)
            if stack.localExists(arg):
                raise texceptions.TemplateKeyError('Local variable "%s" already exists: cannot allocate with "%s".' % (arg.str, name), arg.filepos)
            else:
                stack.new(arg, ttypes.Null(filepos=arg.filepos))

        return ttypes.Null()


@texec.macro
class xIn(texec.TMacro):
    """
        {get NAME}
                :Macro alias for {getset NAME}, returns the value of symbol NAME.
    """
    __mnemonics__ = ('get', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['getset', args[0]])


@texec.function
class xExists(texec.TFunction):
    """
        {exists NAME}
                Aliases: "?"
                :Determines if a symbol exists with name NAME.
    """
    __mnemonics__ = ('exists', '?')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        name = self.checkArgType(name, 0, args, ttypes.String)
        return ttypes.String(stack.exists(name))


@texec.macro
class xSet(texec.TMacro):
    """
        {set NAME VALUE}
                Aliases: "$="
                :Macro alias for {getset NAME VALUE}.
    """
    __mnemonics__ = ('set', '$=')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        return ttypes.List(['getset', args[0], args[1]])


@texec.operator
class xVoid(texec.TOperator):
    """
        {void [EXPR]}
                Aliases: "v"
                :Evaluates EXPR unconditionally but results in a ttypes.Null value
                :regardless.
    """
    __mnemonics__ = ('void', 'v')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, max=1)
        if count == 1:
            teval.evalExpression(args[0], ostream, stack)
        return ttypes.Null()


@texec.operator
class xVota(texec.TOperator):
    """
        {vota ARG}
                Aliases: "value-of-the-argument", "$$"
                Very useful operator for defining macros: simply returns the parsed by
        Unprocessed value of the first (and only) arguments. 
    """
    __mnemonics__ = ('vota', 'value-of-the-argument', '$$')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return args[0]


@texec.operator
class xPoe(texec.TOperator):
    """
        {poe ARG}
                Aliases: NO ALIASES: We have to look for the specific value "poe". This
         is basically syntax, not a normal executable.

                More powerful than vota, this actually searches recursively through
        ARG and when it finds a list that starts with ete, it evaluates it in place.

        On the other hand, when it finds a nested "poe", it doesn't evaluate it or
        recurse into it.
    """
    __mnemonics__ = ('poe', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return self.poe(name, args[0], ostream, stack)

    def poe(self, name, tlist, ostream, stack):
        if not isinstance(tlist, ttypes.List):
            return tlist
        else:
            length = len(tlist)
            if length > 0 and tlist[0] == 'ete':
                return teval.evalExpression(tlist, ostream, stack)
            if length > 0 and tlist[0] == 'poe':
                return tlist
            return ttypes.List([ self.poe(name, item, ostream, stack) for item in tlist ])


@texec.operator
class xEte(texec.TOperator):
    """
        {ete ARG}
                Aliases: "eval-this-expression"
                See poe.
    """
    __mnemonics__ = ('ete', 'eval-this-expression')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return teval.evalExpression(args[0], ostream, stack)


@texec.operator
class xDont(texec.TOperator):
    """
                {dont [...]}
                        Aliases: "#", "syn", "syntax", "rem"
                        : Doesn't do anything, but must be wellformed.
                        : The syn and syntax aliasesare meant for use with syntax
                        : highlighting engines, like VIM.
    """
    __mnemonics__ = ('dont', '#', 'syn', 'syntax', 'end-syntax', 'end-syn', 'rem')

    def execute(self, name, args, ostream, stack):
        pass


@texec.operator
class xLambda(texec.TOperator):
    """
    {lambda [[DOC] ARGNAMES] EXPR}
    """
    __mnemonics__ = ('lambda', )

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2, 3])
        if count == 1:
            expr = args[0]
            argnames = doc = None
        elif count == 2:
            argnames, expr = args
            doc = None
        else:
            doc, argnames, expr = args
        if argnames is not None:
            argnames = teval.evalExpression(argnames, ostream, stack)
            self.checkType('ARGNAMES argument to "%s" operator' % name, argnames, ttypes.List)
            for i in xrange(len(argnames)):
                self.checkType('element at index %d of ARGNAMES argument to "%s" operator' % (i, name), argnames[i], ttypes.String)

        if doc is not None:
            self.checkArgType(name, 0, args, ttypes.String)
        func = texec.UserFunc(self.filepos, expr, argnames, doc)
        return func


@texec.operator
class xMacro(texec.TOperator):
    """
    {macro [[DOC] ARGNAMES] EXPR}
    """
    __mnemonics__ = ('macro', )

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2, 3])
        if count == 1:
            expr = args[0]
            argnames = doc = None
        elif count == 2:
            argnames, expr = args
            doc = None
        else:
            doc, argnames, expr = args
        if argnames is not None:
            argnames = teval.evalExpression(argnames, ostream, stack)
            self.checkType('ARGNAMES argument to "%s" operator' % name, argnames, ttypes.List)
            for i in xrange(len(argnames)):
                self.checkType('element at index %d of ARGNAMES argument to "%s" operator' % (i, name), argnames[i], ttypes.String)

        if doc is not None:
            self.checkArgType(name, 0, args, ttypes.String)
        expr.filepos = self.filepos
        macro = texec.UserMacro(self.filepos, expr, argnames, doc)
        return macro


@texec.operator
class xMacroSubst(texec.TOperator):
    """
    {macro-subst MACRO [ARG0 [ARG1 [...]]]}
    Executes the given MACRO with the given args, but does not evaluate the resuting
    subst as would usually happen when a macro is executed, just returns the subst
    directly.
    """
    __mnemonics__ = ('macro-subst', 'macro.subst')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, min=1)
        macro = teval.evalExpression(args[0], ostream, stack)
        self.checkType('first argument to macro "%s"' % name, macro, texec.TMacro)
        if isinstance(args[0], ttypes.String):
            mname = args[0]
        else:
            mname = macro.name
        subst = macro(str(mname), ttypes.List(args[1:]), ostream, stack)
        return subst


@texec.operator
class xIf(texec.TOperator):
    """
    {if IF0 THEN0 [IF1 THEN1 [IF 2 THEN2 [...]]] [ELSE] }
    : Operator for conditional execution. Evalutes each of the IF
    : expressions one at a time. The first that evaluates to anything
    : other than "0" has it's corresponding (subsequent) THEN
    : expression evaluated, and the result of that eval is the result
    : of the `if` expression. If all of the IFs evaluate to "0", then
    : the ELSE is evaluated and the result is the result of this.
    :
    : If nothing is evaluated, result is ttypes.Null.
    """
    __mnemonics__ = ('if', )

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, min=2)
        i = 0
        done = False
        res = None
        while i + 1 < count:
            test = args[i]
            block = args[(i + 1)]
            i += 2
            test = teval.evalExpression(test, ostream, stack)
            if test != '0':
                res = teval.evalExpression(block, ostream, stack)
                done = True
                break

        if not done and i < count:
            assert i == count - 1
            res = teval.evalExpression(args[i], ostream, stack)
        return res


@texec.operator
class xBlock(texec.TOperator):
    """
    {block [EXPR0 [EXPR1 [...]]]}
        Like scope except that a new scope is NOT created.
    """
    __mnemonics__ = ('block', ':', 'exp.block')

    def execute(self, name, args, ostream, stack):
        res = None
        for arg in args:
            res = teval.evalExpression(arg, ostream, stack)
            if isinstance(res, ttypes.Return):
                break

        return res


@texec.operator
class xExecBlock(texec.TOperator):
    """
    {exec-block LIST}
    Qualified name: "pck.block"
    :Same as block, but the expressions are packed into a list.
    """
    __mnemonics__ = ('exec-block', 'pck.block')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        tlist = self.checkArgType(name, 0, args, ttypes.List)
        res = None
        for expr in tlist:
            res = teval.evalExpression(expr, ostream, stack)
            if isinstance(res, ttypes.Return):
                break

        return res


@texec.function
class xExec(texec.TFunction):
    """
    {exec LIST}
    Qualified name: "pck.scope"
    :Same as scope, but the expressesion are packed into a list, which
    :means this is *not* an operator, this is a function.
    """
    __mnemonics__ = ('exec', 'pck.scope')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        tlist = self.checkArgType(name, 0, args, ttypes.List)
        scope = stack.push()
        res = None
        try:
            for expr in tlist:
                res = teval.evalExpression(expr, ostream, stack)
                if isinstance(res, ttypes.Return):
                    break

        finally:
            stack.pop()

        return res


@texec.operator
class xScope(texec.TOperator):
    """
    {scope [EXPR0 [EXPR1 [...]]]}
    Aliases: "::"
    Qualified name: "exp.scope"
    : Executes each EXPRn one at a time, resulting value is the resulting
    : value of the last expression executed. If any value results in a
    : Retrun object, no further statements are executed. The return object
    : itself is still the resulting value, it is not unwrapped.
    :
    : Execution occurs in a new scope which is popped before the
    : expressino concludes.
    """
    __mnemonics__ = ('scope', '::', 'exp.scope')

    def execute(self, name, args, ostream, stack):
        scope = stack.push()
        res = None
        try:
            for arg in args:
                assert arg.filepos is not None
                res = teval.evalExpression(arg, ostream, stack)
                if isinstance(res, ttypes.Return):
                    break

        finally:
            stack.pop()

        return res


@texec.function
class xReturn(texec.TFunction):
    """
    {return [VAL]}
    Returns a new Return object, wrapping VAL if given.
    """
    __mnemonics__ = ('return', )

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, max=1)
        if count == 0:
            return ttypes.Return()
        else:
            return ttypes.Return(args[0])


@texec.function
class xUnret(texec.TFunction):
    """
    {unret RET}
    : Unwraps a Return value, resulting in the value that the Return
    : value wraps.
    """
    __mnemonics__ = ('unret', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        ret = self.checkArgType(name, 0, args, ttypes.Return)
        return ret.raw()


@texec.function
class xEq(texec.TFunction):
    """
        {eq VAL1 VAL}
                Aliases: "equal", "==="
                :checks equality of two objects.
    """
    __mnemonics__ = ('eq', 'equal', '===')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        return ttypes.String(args[0] == args[1])


@texec.function
class xNeq(texec.TFunction):
    """
        {neq VAL1 VAL}
                Aliases: "not-equal", "!=="
                :checks equality of two objects.
    """
    __mnemonics__ = ('neq', 'not-equal', '!==')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        return ttypes.String(args[0] != args[1])


@texec.function
class LtFunc(texec.BinaryCompareExec):
    __mnemonics__ = ('lt', '<')

    def compare(self, a, b):
        return a < b


@texec.function
class LteFunc(texec.BinaryCompareExec):
    __mnemonics__ = ('lte', '<=')

    def compare(self, a, b):
        return a <= b


@texec.function
class GtFunc(texec.BinaryCompareExec):
    __mnemonics__ = ('gt', '>')

    def compare(self, a, b):
        return a > b


@texec.function
class GteFunc(texec.BinaryCompareExec):
    __mnemonics__ = ('gte', '>=')

    def compare(self, a, b):
        return a >= b


@texec.operator
class xFor(texec.ForLoopExec, texec.TOperator):
    """
    {for NAME INTHIS [WHILE] DO}
    : Loops over the values in list `INTHIS`. Before iterating, a new
    : scope is pushed to the stack. For each iteration, the symbol
    : named by `NAME` is assigned the next value from `INTHIS`, and
    : then the expression `IF` is evaluated: if the result is the
    : String "0", then this iteration is skipped, but the loop is
    : *not* aborted. Otherwise, this iteration is performed by
    : evaluating the expression `DO`.
    : 
    : The resulting value is the result of the last evaluation of
    : `DO`. If any evaluations of `DO` is a Return value, the loop is
    : aborted (no further iterations are performed) and the Return
    : value is stripped to give the result.
    """
    __mnemonics__ = ('for', 'for.loop')

    def execute(self, name, args, ostream, stack):
        res = None
        for res in self.loop(name, args, ostream, stack):
            pass

        return res


@texec.operator
class xWhile(texec.WhileLoopExec, texec.TOperator):
    """
    {while TEST DO}
        : A simple loop. For each iteration, evaluates the expression
        : `TEST`: if it's equal to "1" then we perform the iteration by
        : evaluating `DO`, otherwise we abort the loop.
        :
        : A new scope is pushed before any iterations, and opped before
        : returning.
        :
        : The resulting value is the result of the last evaluation of
        : `DO`. If any evaluations of `DO` is a Return value, the loop is
        : aborted (no further iterations are performed) and the Return
        : value is stripped to give the result.
    """
    __mnemonics__ = ('while', 'while.loop')

    def execute(self, name, args, ostream, stack):
        res = None
        for res in self.loop(name, args, ostream, stack):
            pass

        return res


@texec.operator
class xLoop(texec.LoopLoopExec, texec.TOperator):
    """
    :{loop [INIT] [TEST] [POST] DO}
    :{loop [INIT] TEST [POST] DO}
    :{loop [INIT] TEST POST DO}
    :
    :Works like a C-style for loop: it pushes a new scope to the stack, then evaluates INIT.
    :Then it begins to loop: at the start of the loop, it evaluates TEST: if that evaluates to "0",
    :it's done, otherwise it evaluates DO, then evaluates POST, then does the next iteration of the
    :loop, starting with evaluation of TEST again.
    :
    :With three argument, INIT is not used. With two arguments, neither INIT nor POST are used.
    :With only one argument, only DO is used, so it just keeps going until DO evaluates to a RETURN.
    :
    :The resulting value is the result of the last evaluation of
    :`DO`. If any evaluations of `DO` is a Return value, the loop is
    :aborted (no further iterations are performed) and the Return
    :value is stripped to give the result.
    """
    __mnemonics__ = ('loop', 'loop.loop')

    def execute(self, name, args, ostream, stack):
        res = None
        for res in self.loop(name, args, ostream, stack):
            pass

        return res


@texec.operator
class xGen(texec.ForLoopExec, texec.TOperator):
    """
    {gen NAME INTHIS [WHILE] DO}
    : Runs like a `for` loop but a list is built from the results of
    : each evaluation of `DO`. It's a list comprehension.
    """
    __mnemonics__ = ('gen', 'for.gen')

    def execute(self, name, args, ostream, stack):
        res = None
        return ttypes.List(res for res in self.loop(name, args, ostream, stack))


@texec.operator
class xGenWhile(texec.WhileLoopExec, texec.TOperator):
    """
    {gen-while TEST DO}
    :Like `gen`, but uses the WHILE loop setup instead of FOR loop.
    """
    __mnemonics__ = ('gen-while', 'while.gen')

    def execute(self, name, args, ostream, stack):
        res = None
        return ttypes.List(res for res in self.loop(name, args, ostream, stack))


@texec.operator
class xGenLoop(texec.LoopLoopExec, texec.TOperator):
    """
    {gen-loop [[INIT] [TEST] [POST]] DO}
    Aliases: "loop.gen"
    :Like `gen`, but uses the LOOP loop setup instead of FOR loop.
    """
    __mnemonics__ = ('gen-loop', 'loop.gen')

    def execute(self, name, args, ostream, stack):
        res = None
        return ttypes.List(res for res in self.loop(name, args, ostream, stack))


@texec.function
class xRange(texec.MathExec, texec.TFunction):
    """
    {range [START] STOP [STEP]}
    :Produces a ttypes.List consisting of numeric values starting with START, incrementing by STEP,
    :and ending before getting to STOP. Default START is 0, default STEP is 1. If any values
    :are floats, the resulting elements are floats.
    :One argument works as  {range 0 STOP 1}.
    :Two arguments works as {range START STOP 1}.
    """
    __mnemonics__ = ('range', )

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2, 3])
        values = self.parseNumericArgs(name, args)
        start = 0
        step = 1
        if count == 1:
            stop = values[0]
        else:
            if count == 2:
                start, stop = values
            else:
                start, stop, step = values
                if step == 0:
                    raise texceptions.TemplateValueError('Invalid third argument for "%s": STEP cannot be 0.' % name, args[2].filepos, step)
            res = []
            val = start
            if step > 0:
                cond = lambda x: x < stop
            else:
                cond = lambda x: x > stop
            while cond(val):
                res.append(val)
                val = val + step

        return ttypes.List(ttypes.String(v) for v in res)


@texec.operator
class xTry(texec.TOperator):
    """
    {try EXPR [[NAME] CATCH]}
    : Evaluates EXPR, but if any errors occur, they are trapped. If
    : CATCH is given, it is evaluated as an EXPR if and only if an
    : error occurs. A new scope is pushed before execution and popped
    : afterwards. If NAME is given, the error value is assigned to
    : a symbol name NAME in this new scope, before evaluating CATCH.
    :
    : If an error occurred, the result is the result of CATCH, otherwise
    : it's just the result of EXPR.
    """
    __mnemonics__ = ('try', )

    def execute--- This code section failed: ---

 L.1400         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'checkArgCount'
                6  LOAD_FAST             1  'name'
                9  LOAD_FAST             2  'args'
               12  LOAD_CONST               'exact'
               15  LOAD_CONST               1
               18  LOAD_CONST               2
               21  LOAD_CONST               3
               24  BUILD_LIST_3          3 
               27  CALL_FUNCTION_258   258  None
               30  STORE_FAST            5  'count'

 L.1402        33  LOAD_CONST               None
               36  STORE_FAST            6  'catch'

 L.1403        39  LOAD_CONST               None
               42  STORE_FAST            7  'exname'

 L.1404        45  LOAD_FAST             2  'args'
               48  LOAD_CONST               0
               51  BINARY_SUBSCR    
               52  STORE_FAST            8  'expr'

 L.1405        55  LOAD_FAST             5  'count'
               58  LOAD_CONST               2
               61  COMPARE_OP            4  >
               64  POP_JUMP_IF_FALSE    90  'to 90'

 L.1406        67  LOAD_FAST             2  'args'
               70  LOAD_CONST               1
               73  BINARY_SUBSCR    
               74  STORE_FAST            7  'exname'

 L.1407        77  LOAD_FAST             2  'args'
               80  LOAD_CONST               2
               83  BINARY_SUBSCR    
               84  STORE_FAST            6  'catch'
               87  JUMP_FORWARD         25  'to 115'

 L.1408        90  LOAD_FAST             5  'count'
               93  LOAD_CONST               1
               96  COMPARE_OP            4  >
               99  POP_JUMP_IF_FALSE   115  'to 115'

 L.1409       102  LOAD_FAST             2  'args'
              105  LOAD_CONST               1
              108  BINARY_SUBSCR    
              109  STORE_FAST            6  'catch'
              112  JUMP_FORWARD          0  'to 115'
            115_0  COME_FROM           112  '112'
            115_1  COME_FROM            87  '87'

 L.1411       115  LOAD_FAST             7  'exname'
              118  LOAD_CONST               None
              121  COMPARE_OP            9  is-not
              124  POP_JUMP_IF_FALSE   177  'to 177'

 L.1412       127  LOAD_GLOBAL           2  'teval'
              130  LOAD_ATTR             3  'evalExpression'
              133  LOAD_FAST             7  'exname'
              136  LOAD_FAST             3  'ostream'
              139  LOAD_FAST             4  'stack'
              142  CALL_FUNCTION_3       3  None
              145  STORE_FAST            7  'exname'

 L.1413       148  LOAD_FAST             0  'self'
              151  LOAD_ATTR             4  'checkType'
              154  LOAD_CONST               'Second argument (NAME) to "%s"'
              157  LOAD_FAST             1  'name'
              160  BINARY_MODULO    
              161  LOAD_FAST             7  'exname'
              164  LOAD_GLOBAL           5  'ttypes'
              167  LOAD_ATTR             6  'String'
              170  CALL_FUNCTION_3       3  None
              173  POP_TOP          
              174  JUMP_FORWARD          0  'to 177'
            177_0  COME_FROM           174  '174'

 L.1415       177  LOAD_FAST             4  'stack'
              180  LOAD_ATTR             7  'push'
              183  CALL_FUNCTION_0       0  None
              186  POP_TOP          

 L.1416       187  SETUP_EXCEPT         29  'to 219'

 L.1417       190  LOAD_GLOBAL           2  'teval'
              193  LOAD_ATTR             3  'evalExpression'
              196  LOAD_FAST             2  'args'
              199  LOAD_CONST               0
              202  BINARY_SUBSCR    
              203  LOAD_FAST             3  'ostream'
              206  LOAD_FAST             4  'stack'
              209  CALL_FUNCTION_3       3  None
              212  STORE_FAST            9  'res'
              215  POP_BLOCK        
              216  JUMP_FORWARD        156  'to 375'
            219_0  COME_FROM           187  '187'

 L.1418       219  DUP_TOP          
              220  LOAD_GLOBAL           8  'texceptions'
              223  LOAD_ATTR             9  'TemplateException'
              226  COMPARE_OP           10  exception-match
              229  POP_JUMP_IF_FALSE   374  'to 374'
              232  POP_TOP          
              233  STORE_FAST           10  'e'
              236  POP_TOP          

 L.1419       237  SETUP_FINALLY       119  'to 359'

 L.1420       240  LOAD_FAST             7  'exname'
              243  LOAD_CONST               None
              246  COMPARE_OP            9  is-not
              249  POP_JUMP_IF_FALSE   313  'to 313'

 L.1421       252  LOAD_FAST            10  'e'
              255  LOAD_ATTR            10  'templValue'
              258  STORE_FAST           11  'ex'

 L.1422       261  LOAD_GLOBAL          11  'isinstance'
              264  LOAD_FAST            11  'ex'
              267  LOAD_GLOBAL           5  'ttypes'
              270  LOAD_ATTR            12  'TType'
              273  CALL_FUNCTION_2       2  None
              276  POP_JUMP_IF_TRUE    294  'to 294'
              279  LOAD_ASSERT              AssertionError
              282  LOAD_GLOBAL          14  'type'
              285  LOAD_FAST            11  'ex'
              288  CALL_FUNCTION_1       1  None
              291  RAISE_VARARGS_2       2  None

 L.1423       294  LOAD_FAST             4  'stack'
              297  LOAD_ATTR            15  'new'
              300  LOAD_FAST             7  'exname'
              303  LOAD_FAST            11  'ex'
              306  CALL_FUNCTION_2       2  None
              309  POP_TOP          
              310  JUMP_FORWARD          0  'to 313'
            313_0  COME_FROM           310  '310'

 L.1424       313  LOAD_FAST             6  'catch'
              316  LOAD_CONST               None
              319  COMPARE_OP            9  is-not
              322  POP_JUMP_IF_FALSE   349  'to 349'

 L.1425       325  LOAD_GLOBAL           2  'teval'
              328  LOAD_ATTR             3  'evalExpression'
              331  LOAD_FAST             6  'catch'
              334  LOAD_FAST             3  'ostream'
              337  LOAD_FAST             4  'stack'
              340  CALL_FUNCTION_3       3  None
              343  STORE_FAST            9  'res'
              346  JUMP_FORWARD          6  'to 355'

 L.1427       349  LOAD_CONST               None
              352  STORE_FAST            9  'res'
            355_0  COME_FROM           346  '346'
              355  POP_BLOCK        
              356  LOAD_CONST               None
            359_0  COME_FROM_FINALLY   237  '237'

 L.1429       359  LOAD_FAST             4  'stack'
              362  LOAD_ATTR            16  'pop'
              365  CALL_FUNCTION_0       0  None
              368  POP_TOP          
              369  END_FINALLY      

 L.1430       370  LOAD_FAST             9  'res'
              373  RETURN_VALUE     
              374  END_FINALLY      
            375_0  COME_FROM           374  '374'
            375_1  COME_FROM           216  '216'

 L.1431       375  LOAD_FAST             4  'stack'
              378  LOAD_ATTR            16  'pop'
              381  CALL_FUNCTION_0       0  None
              384  POP_TOP          

 L.1432       385  LOAD_FAST             9  'res'
              388  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 355


@texec.function
class xError(texec.TFunction):
    """
    {error [VAL]}
    : Raises an error with error value VAL. If nothing catches it, it
    : results in an error and execution is terminated. If VAL isn't
    : given, default is NULL.
    """
    __mnemonics__ = ('error', )

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[0, 1])
        if count == 1:
            raise texceptions.TemplateUserException(args[0], self.filepos)
        else:
            raise texceptions.TemplateUserException(ttypes.Null(filepos=self.filepos), self.filepos)


@texec.function
class xCall(texec.TFunction):
    """
    {call EXE [ARGS]}
    Qualified name: pck.call
    :Resolves executable EXE then invokes it passing the List ARGS as
    :arguments. Default ARGS is empty list.
    """
    __mnemonics__ = ('call', 'pck.call')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2])
        name, exe = teval.resolveExecutable(args[0], stack)
        exe.filepos = self.filepos
        if count == 1:
            xargs = ttypes.List([], self.filepos)
        else:
            self.checkArgType(name, 1, args, ttypes.List)
            xargs = ttypes.List(args[1].list, args[1].filepos)
        return exe(name, xargs, ostream, stack)


@texec.function
class xInvoke(texec.TFunction):
    """
    {invoke EXE [ARG0 [ARG1 [...]]]}
    Qualified name: exp.call
    :Same as call, but arguments are unpacked.
    """
    __mnemonics__ = ('invoke', 'exp.call')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, min=1)
        name, exe = teval.resolveExecutable(args[0], stack)
        exe.filepos = self.filepos
        xargs = ttypes.List(args[1:])
        return exe(name, xargs, ostream, stack)


@texec.function
class xFilepos(texec.TFunction):
    """
    {filepos VAL}
    """
    __mnemonics__ = ('filepos', 'str.filepos')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.String(args[0].filepos.toString(preposition=''))


@texec.function
class xFileposTuple(texec.TFunction):
    """
    {filepos-tuple VAL}
    """
    __mnemonics__ = ('filepos-tuple', 'list.filepos')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        fp = args[0].filepos
        return ttypes.List((fp.filename, fp.line, fp.offset))


@texec.function
class xFileposPlist(texec.TFunction):
    """
    {filepos-plist VAL}
    """
    __mnemonics__ = ('filepos-plist', 'plist.filepos')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        fp = args[0].filepos
        return ttypes.List((':file', fp.filename, ':line', fp.line, ':column', fp.offset))


@texec.function
class xInsert(texec.IndexExec, texec.TFunction):
    """
        {insert VAL [IDX] LIST}
    Qualified name: "list.insert"
    :returns a new list which is the same as LIST except that it has a new
    :value VAL inserted so that it is at index IDX. The value that used to
    :be at index IDX, and all values are higher indicies, are moved up by
    :one index. If IDX isn't given, default is 0 (front of the list).
    :
    :Special value END is allowed for IDX, then it works like append.
    """
    __mnemonics__ = ('insert', 'list.insert')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[2, 3])
        val = args[0]
        if count == 2:
            idx = 0
            listIdx = 1
        else:
            idx = self.parseEndIndexArg(name, 1, args)
            listIdx = 2
        tlist = self.checkArgType(name, listIdx, args, ttypes.List)
        xlist = list(tlist.list)
        length = len(xlist)
        if idx is None:
            idx = length
        elif idx > length:
            raise texceptions.TemplateSequenceIndexOutOfBoundsError('Out of bounds index specified for second argument of "%s".' % name, args[1].filepos, length, idx)
        elif idx < 0 and -idx > length:
            raise texceptions.TemplateSequenceIndexOutOfBoundsError('Out of bounds index specified for second argument of "%s".' % name, args[1].filepos, length, idx)
        xlist.insert(idx, val)
        return ttypes.List(xlist)


@texec.function
class xSplice(texec.IndexExec, texec.TFunction):
    """
        {splice THIS [IDX] INTO}
    Qualified name: "list.splice"
    :Like insert, except in this case THIS is a ttypes.List of items which are
    :all inserted into the target list `INTO`.
    :
    :Special value END is allowed for IDX, then it works like cat but with
    :arguments in reverse order.
    """
    __mnemonics__ = ('splice', 'list.splice')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[2, 3])
        val = self.checkArgType(name, 0, args, ttypes.List)
        if count == 2:
            idx = 0
            listIdx = 1
        else:
            idx = self.parseEndIndexArg(name, 1, args)
            listIdx = 2
        tlist = self.checkArgType(name, listIdx, args, ttypes.List)
        xlist = list(tlist.list)
        length = len(xlist)
        if idx is None:
            idx = length
        elif idx > length:
            raise texceptions.TemplateSequenceIndexOutOfBoundsError('Out of bounds index specified for second argument of "%s".' % name, args[1].filepos, length, idx)
        elif idx < 0 and -idx > length:
            raise texceptions.TemplateSequenceIndexOutOfBoundsError('Out of bounds index specified for second argument of "%s".' % name, args[1].filepos, length, idx)
        return ttypes.List(xlist[:idx] + list(val.list) + xlist[idx:])


@texec.function
class xAppend(texec.TFunction):
    """
        {append VAL LIST}
    Qualified name: "list.append"
    : Returns a new list that is the same as LIST but with VAL attached as
    : a new element to the end.
    : Note that the splice equivalent of append is cat, except the args
    : are in a different order.
    """
    __mnemonics__ = ('append', 'list.append')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        val = args[0]
        tlist = self.checkArgType(name, 1, args, ttypes.List)
        xlist = list(tlist.list)
        xlist.append(val)
        return ttypes.List(xlist)


@texec.function
class xGetf(texec.TFunction):
    """
        {getf LABEL LIST}
    Qualified name: plist.get
    :Returns the element in LIST immediately following the element which
    :is equal to LABEL. Error if no LABEL is not found in LIST, or if
    :there is no element following it.
    """
    __mnemonics__ = ('getf', 'plist.get')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        label = self.checkArgType(name, 0, args, ttypes.String)
        plist = self.checkArgType(name, 1, args, ttypes.List)
        i = 0
        length = len(plist)
        while i + 1 < length:
            if plist[i] == label:
                return plist[(i + 1)]
            i += 2

        raise texceptions.NoSuchFieldException(label, label.filepos)


@texec.function
class xFields(texec.TFunction):
    """
    {fields PLIST}
    Returns a list of all the field names in the given PLIST.
    """
    __mnemonics__ = ('fields', 'plist.fields')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        plist = self.checkArgType(name, 0, args, ttypes.List)
        fields = []
        i = 0
        length = len(plist)
        while i + 1 < length:
            fields.append(plist[i])
            i += 2

        return ttypes.List(fields)


@texec.function
class xIdxf(texec.TFunction):
    """
        {idxf LABEL PLIST}
    Qualified name: plist.idx
    : Returns the numerical index into the given plist of the field with
    : the given label. This is the index of the *value*, not the label.
    : The label is always at the previous index.
    :
    : If not found, returns None.
    """
    __mnemonics__ = ('idxf', 'plist.idx')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        label = self.checkArgType(name, 0, args, ttypes.String)
        plist = self.checkArgType(name, 1, args, ttypes.List)
        i = 0
        length = len(plist)
        while i + 1 < length:
            if plist[i] == label:
                return ttypes.String(i + 1)
            i += 2

        return ttypes.Null()


@texec.function
class xHasf(texec.TFunction):
    """
        {hasf LABEL LIST}
    Qualified name: plist.has
    :Determines if LABEL exists in the given LIST and is NOT the last
    :element of the list. I.e., whether or not LABEL will work in a call
    :to getf.
    """
    __mnemonics__ = ('hasf', 'plist.has')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        label = self.checkArgType(name, 0, args, ttypes.String)
        plist = self.checkArgType(name, 1, args, ttypes.List)
        i = 0
        length = len(plist)
        while i + 1 < length:
            if plist[i] == label:
                return ttypes.String(True)
            i += 2

        return ttypes.String(False)


@texec.function
class xPlistFind(texec.TFunction):
    """
        {plist.find VALUE PLIST}
    : Finds the index into PLIST of the first occurence of something
    : equal to VALUE , which can be any type. Note this is only checking
    : values, not fields (i.e., only the even indices), and returns the
    : index of that value. The label for the field is always at the
    : previous index.
    """
    __mnemonics__ = ('plist.find', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        value = args[0]
        plist = self.checkArgType(name, 1, args, ttypes.List)
        i = 0
        length = len(plist)
        while i + 1 < length:
            if plist[(i + 1)] == value:
                return ttypes.String(i + 1)
            i += 2

        return ttypes.Null()


@texec.macro
class xPlistIn(texec.TMacro):
    """
    Qualified name: plist.in
    : Macro alias for {not {is-null {plist.find VALUE PLIST}}}.
    """
    __mnemonics__ = ('plist.in', )

    def execute(self, name, args, ostream, stack):
        return ttypes.List(['not', ['is-null', ['plist.find'] + list(args)]])


@texec.function
class xPlistLen(texec.TFunction):
    """
        x {plist.len PLIST}
    :Returns the number of *fields* in the given PLIST. A field is a pair
    :of subsequent elements in a List: LABEL VALUE. So a List with 4
    :elements has 2 fields as a plist. Note that a final odd-indexed
    :element is not considered part of a plist, so is not included in the
    :length.
    """
    __mnemonics__ = ('plist.len', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        plist = self.checkArgType(name, 0, args, ttypes.List)
        length = len(plist)
        return ttypes.String(int(length / 2))


@texec.function
class xCons(texec.TFunction):
    """
        {cons X [Y]}
                Qualified name: cons.new
                :Creates a new List [X, Y]. Default value for Y is an empty list
                :(which typically is used to terminate linked lists and trees).
    """
    __mnemonics__ = ('cons', 'cons.new')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2])
        if count == 1:
            return ttypes.List([args[0], []])
        else:
            return ttypes.List(args)


@texec.function
class xCar(texec.TFunction):
    """
        {car CONS}
                :Returns the first item from the List CONS.
        :An error if CONS is an empty list.
    """
    __mnemonics__ = ('car', 'first')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        tlist = self.checkArgType(name, 0, args, ttypes.List)
        if len(tlist) != 2:
            raise texceptions.NotAConsException('Attempting to car a non-cons.', tlist.filepos, tlist)
        return tlist[0]


@texec.function
class xCdr(texec.TFunction):
    """
        {cdr CONS}
    :Returns the second item from the List CONS. Error if there are fewer
    :than 2 elements in CONS.
    :Pronounces "could-er"
    """
    __mnemonics__ = ('cdr', 'rest')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        tlist = self.checkArgType(name, 0, args, ttypes.List)
        if len(tlist) != 2:
            raise texceptions.NotAConsException('Attempting to cdr a non-cons.', tlist.filepos, tlist)
        return tlist[1]


@texec.macro
class xCaar(texec.TMacro):
    """
        {caar CONS}
                :Returns the first item of the first item of the CONS tree.
        :macro expansion of {car {car CONS}}
        :Pronounced with both a's distinctly: "cuh-ar", or sometimes "care".
    """
    __mnemonics__ = ('caar', 'first-of-first')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['car', ['car', args[0]]])


@texec.macro
class xCadr(texec.TMacro):
    """
        {cadr CONS}
                :Returns the first item of the rest of the CONS linked list.
        :macro expansion of {car {cdr CONS}}
        :Pronoucnes "ka-der"
    """
    __mnemonics__ = ('cadr', 'first-of-rest')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['car', ['cdr', args[0]]])


@texec.macro
class xCddr(texec.TMacro):
    """
        {cddr CONS}
                :Returns the rest of the rest of the CONS linked list.
        :macro expansion of {cdr {cdr CONS}}.
        :Pronounced like you have a stutter: "could-eder" ("ku duh der")
    """
    __mnemonics__ = ('cddr', 'rest-of-rest')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['cdr', ['cdr', args[0]]])


@texec.macro
class xCaaar(texec.TMacro):
    """
        {caaar CONS}
        :Pronounces "zang"
    """
    __mnemonics__ = ('caaar', 'first-of-first-of-first')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['car', ['car', ['car', args[0]]]])


@texec.macro
class xCaadr(texec.TMacro):
    """
        {caadr CONS}
        :Pronounce "ka'adder"
    """
    __mnemonics__ = ('caadr', 'first-of-first-of-rest')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['car', ['car', ['cdr', args[0]]]])


@texec.macro
class xCadar(texec.TMacro):
    """
        {cadar CONS}
        :Pronounce "ka-dar"
    """
    __mnemonics__ = ('cadar', 'first-of-rest-of-first')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['car', ['cdr', ['car', args[0]]]])


@texec.macro
class xCaddr(texec.TMacro):
    """
        {caddr CONS}
        :Pronounce "ka-duh-der"
    """
    __mnemonics__ = ('caddr', 'first-of-rest-of-rest')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['car', ['cdr', ['cdr', args[0]]]])


@texec.macro
class xCdaar(texec.TMacro):
    """
        {cdaar CONS}
        :Pronounce "kud-uh-ar"
    """
    __mnemonics__ = ('cdaar', 'rest-of-first-of-first')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['cdr', ['car', ['car', args[0]]]])


@texec.macro
class xCdadr(texec.TMacro):
    """
        {cdadr CONS}
        :Pronounce "kuh-dad-er"
    """
    __mnemonics__ = ('cdadr', 'rest-of-first-of-rest')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['cdr', ['car', ['cdr', args[0]]]])


@texec.macro
class xCddar(texec.TMacro):
    """
        {cddar CONS}
        :Pronounce "kud-uh-dare"
    """
    __mnemonics__ = ('cddar', 'rest-of-rest-of-first')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['cdr', ['cdr', ['car', args[0]]]])


@texec.macro
class xCdddr(texec.TMacro):
    """
        {cdddr CONS}
        :Pronounce "kuh-duh-duh-der"
    """
    __mnemonics__ = ('cdddr', 'rest-of-rest-of-rest')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['cdr', ['cdr', ['cdr', args[0]]]])


@texec.function
class xConsLen(texec.TFunction):
    """
        {cons.len CONS}
                :Determines the number of elements in the CONS linked list. 
                : Error if any of the elements in the linked list are not CONS
                : cells.
    """
    __mnemonics__ = ('cons.len', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        cons = args[0]
        depth = 0
        while True:
            if isinstance(cons, ttypes.List) and len(cons) == 0:
                return ttypes.String(depth)
            if not isinstance(cons, ttypes.List) or len(cons) != 2:
                raise texceptions.NotAConsException('Attempting to get cons-length of non-cons item at depth %d in "%s".' % (depth + 1, name), cons.filepos, cons)
            depth += 1
            cons = cons[1]


@texec.macro
class xEocb(texec.TMacro):
    r"""
    {eocb}

    "Escaped Opening Curly Brace"
    Expands to ttypes.String "\{".
    """
    __mnemonics__ = ('eocb', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('\\{')


@texec.macro
class xOcb(texec.TMacro):
    """
    {ocb}

    "Opening Curly Brace"
    Expands to String literal "{".
    """
    __mnemonics__ = ('ocb', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('{')


@texec.macro
class xEccb(texec.TMacro):
    r"""
    {eccb}

    "Escaped Closing Curly Brace"
    Expands to String "\}".
    """
    __mnemonics__ = ('eccb', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('\\}')


@texec.macro
class xCcb(texec.TMacro):
    """
    {ccb}

    "Closed Curly Brace"
    Expands to String literal "}".
    """
    __mnemonics__ = ('ccb', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('}')


@texec.macro
class xEol(texec.TMacro):
    """
    {eol}
                : End-of-line macro. Macro expands directly to a String object giving
                : an appropriate end of line string for the current system. Usually
                : "
", or just "
". This is probably only necessary when writing
                : to a binary stream, otherwise just use `lnbrk` and your os will
                : probably translate it.
    """
    __mnemonics__ = ('eol', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String(os.linesep)


@texec.macro
class xLnbrk(texec.TMacro):
    r"""
    {lnbrk}
                Aliases: "\n"
                : Line-break macro. Macro expands directly to the single-character
                : String with ASCII value 0x0A (decimal 10). This is the traditional
                : "linebreak" character, often escaped in other programming languages 
                : as "
". Note that templ has no escapes in strings or string
                : literals.
    """
    __mnemonics__ = ('lnbrk', '\\n')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('\n')


@texec.macro
class xTab(texec.TMacro):
    r"""
        {tab}
                Aliases: "\t"
                : Tab macro. Macro expands directly to the single-character
                : String with ASCII value 9. This is the traditional
                : "horizontal tab" character, often escaped in other programming languages 
                : as "  ". Note that templ has no escapes in strings or string
                : literals.
    """
    __mnemonics__ = ('tab', '\\t')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('\t')


@texec.macro
class xBackslash(texec.TMacro):
    """
        {backslash}
                : Backslash macro. Macro expands directly to the single-character
                : backslash String.
    """
    __mnemonics__ = ('bslash', '\\')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('\\')


@texec.macro
class xQuestion(texec.TMacro):
    """
        {question}
                : Question macro. Macro expands directly to the single-character
                : question-mark String.
    """
    __mnemonics__ = ('q-mark', '\\?')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('?')


@texec.macro
class xDquote(texec.TMacro):
    """
        {dquote}
                : Double-quote macro. Macro expands directly to the single-character
                : String containing a double-quote character.
    """
    __mnemonics__ = ('double-quote', 'dq')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('"')


@texec.macro
class xSquote(texec.TMacro):
    """
        {squote}
                : Single-quote macro. Macro expands directly to the single-character
                : String containing a single-quote character.
    """
    __mnemonics__ = ('single-quote', 'sq', "\\'")

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String("'")


@texec.macro
class xAlert(texec.TMacro):
    """
        {alert}
                : Alert/Bell character macro. Macro expands directly to the single-character
                : String containing an alert (aka BEL) character, ASCII value 7.
    """
    __mnemonics__ = ('alert', 'bel', 'bell', '\\a')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('\x07')


@texec.macro
class xBackspace(texec.TMacro):
    """
        {backspace}
                : Backspace character macro. Macro expands directly to the single-character
                : String containing a backspace character, ASCII value 8.
    """
    __mnemonics__ = ('bs', '\\b')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('\x08')


@texec.macro
class xFormfeed(texec.TMacro):
    """
        {formfeed}
                : Formfeed character macro. Macro expands directly to the single-character
                : String containing a formfeed character, ASCII value 12 (0x0C).
    """
    __mnemonics__ = ('ff', '\\f')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('\x0c')


@texec.macro
class xCarriageReturn(texec.TMacro):
    """
        {carriage-return}
                : CR character macro. Macro expands directly to the single-character
                : String containing a carriage-return character, ASCII value 13 (0x0D).
    """
    __mnemonics__ = ('cr', '\\r')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('\r')


@texec.macro
class xVerticalTab(texec.TMacro):
    """
        {vertical-tab}
                : Vertical tab character macro. Macro expands directly to the single-character
                : String containing a vertical-tab character, ASCII value 11 (0x0B).
    """
    __mnemonics__ = ('vt', '\\v')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('\x0b')


@texec.function
class xSub(texec.TFunction, texec.MathExec):
    """
    {sub [VAL1] VAL2}
    With two arguments, returns VAL1 - VAL2. With one argument, returns
    -(VAL2).
    """
    __mnemonics__ = ('sub', '-', 'math.sub')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2])
        a = self.parseNumericArg(name, 0, args)
        if count == 1:
            return ttypes.String(-a)
        else:
            b = self.parseNumericArg(name, 1, args)
            return ttypes.String(a - b)


@texec.function
class xAdd(texec.TFunction, texec.MathExec):
    """
    {add [VAL1 [VAL2 [...]]]}
    Returns the sum of all the values.
    """
    __mnemonics__ = ('add', '+', 'math.add')

    def execute(self, name, args, ostream, stack):
        return ttypes.String(sum(self.parseNumericArgs(name, args)))


@texec.function
class xMult(texec.MathExec, texec.TFunction):
    """
    {mult [VAL1 [VAL2 [...]]]}
    Returns the product of all the values.
    """
    __mnemonics__ = ('mult', '*', 'math.mult')

    def execute(self, name, args, ostream, stack):
        p = 1
        for val in self.parseNumericArgs(name, args):
            p = p * val

        return ttypes.String(p)


@texec.macro
class xNeg(texec.TMacro):
    """
    {neg VAL}
    Returns the negative of VAL, expands to {sub VAL}
    """
    __mnemonics__ = ('neg', 'math.neg')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['sub', args[0]])


@texec.function
class xDiv(texec.MathExec, texec.TFunction):
    """
    {div VAL1 VAL2}

    Returns the quotient VAL1 / VAL2. If either VAL1 or VAL2 is floating point, does floating point division, otherwise integer
    division without remainder.
    """
    __mnemonics__ = ('div', 'math.div')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        vals = self.parseNumericArgs(name, args)
        return ttypes.String(vals[0] / vals[1])


@texec.function
class xMod(texec.MathExec, texec.TFunction):
    """
    {mod VAL MOD}

    Returns VAL reduced modulo MOD. To get both the quotient and the remainder, use `divmod`.
    """
    __mnemonics__ = ('mod', 'div.mode')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        vals = self.parseNumericArgs(name, args)
        return ttypes.String(vals[0] % vals[1])


@texec.function
class xDivmod(texec.MathExec, texec.TFunction):
    """
    {divmod NUM DENOM}

    Returns a List of two elements, the first is the integer quotient of NUM divided by DENOM, and the second element
    is the remainder of the same.
    """
    __mnemonics__ = ('divmod', 'math.divmod')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        vals = self.parseNumericArgs(name, args)
        return ttypes.List(ttypes.String(x, self.filepos) for x in divmod(vals[0], vals[1]))


@texec.function
class xPow(texec.MathExec, texec.TFunction):
    """
    {pow BASE EXP}

    Returns the value of BASE raised to power EXP.
    """
    __mnemonics__ = ('pow', '**', 'math.pow')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        vals = self.parseNumericArgs(name, args)
        return ttypes.String(pow(vals[0], vals[1]))


@texec.function
class xExp(texec.MathExec, texec.TFunction):
    """
    {exp [EXP]}
    Return e raised to the power of EXP. Default EXP is 1.
    """
    __mnemonics__ = ('exp', 'math.exp', 'math.e')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[0, 1])
        if count == 0:
            exp = 1.0
        else:
            exp = self.parseNumericArg(name, 0, args)
        return ttypes.String(pow(math.e, exp))


@texec.function
class xSqrt(texec.MathExec, texec.TFunction):
    """
    {sqrt VAL}
    Returns the square root of VAL.
    """
    __mnemonics__ = ('sqrt', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        val = self.parseNumericArg(name, 0, args)
        return ttypes.String(math.sqrt(val))


@texec.function
class xSin(texec.MathExec, texec.TFunction):
    """
    {sin THETA}
    Returns the sine of angle THETA, THETA in radians.
    """
    __mnemonics__ = ('sin', 'sine')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.String(math.sin(self.parseNumericArg(name, 0, args)))


@texec.function
class xCos(texec.MathExec, texec.TFunction):
    """
    {cos THETA}
    Returns the cosine of angle THETA, THETA in radians.
    """
    __mnemonics__ = ('cos', 'cosine')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.String(math.cos(self.parseNumericArg(name, 0, args)))


@texec.function
class xTan(texec.MathExec, texec.TFunction):
    """
    {tan THETA}
    Returns the tangent of angle THETA, THETA in radians.
    """
    __mnemonics__ = ('tan', 'tangent')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.String(math.tan(self.parseNumericArg(name, 0, args)))


@texec.function
class xAsin(texec.MathExec, texec.TFunction):
    """
    {asin X}
    Returns the arc-sine of X, in radians.
    """
    __mnemonics__ = ('asin', 'arc-sine')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.String(math.asin(self.parseNumericArg(name, 0, args)))


@texec.function
class xAcos(texec.MathExec, texec.TFunction):
    """
    {acos X}
    Returns the arc-cosine of X, in radians.
    """
    __mnemonics__ = ('acos', 'arc-cosine')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.String(math.acos(self.parseNumericArg(name, 0, args)))


@texec.function
class xAtan(texec.MathExec, texec.TFunction):
    """
    {atan X}
    Returns the arc-tangent of X, in radians.
    """
    __mnemonics__ = ('atan', 'arc-tangent')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.String(math.atan(self.parseNumericArg(name, 0, args)))


@texec.function
class xAtanq(texec.MathExec, texec.TFunction):
    """
    {atanq Y X}
    Returns the 4-quadrant arc-tangent of Y/X, in radians, taking into account the signs
    of Y and X. Resulting value is between negative pi and pi.
    """
    __mnemonics__ = ('atanq', 'atan-quad', 'arc-tangent-quad')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        y = self.parseNumericArg(name, 0, args)
        x = self.parseNumericArg(name, 1, args)
        return ttypes.String(math.atan2(y, x))


@texec.function
class xDeg(texec.MathExec, texec.TFunction):
    """
    {deg RADS}
    Converts RADS in radians to degrees.
    """
    __mnemonics__ = ('deg', )
    __convert = 180.0 / math.pi

    def execute(self, name, args, ostrem, stack):
        self.checkArgCount(name, args, exact=[1])
        val = self.parseNumericArg(name, 0, args)
        return ttypes.String(val * self.__convert)


@texec.function
class xRad(texec.MathExec, texec.TFunction):
    """
    {rad DEG}
    Converts DEG in degrees to radian.
    """
    __mnemonics__ = ('rad', )
    __convert = math.pi / 180.0

    def execute(self, name, args, ostrem, stack):
        self.checkArgCount(name, args, exact=[1])
        val = self.parseNumericArg(name, 0, args)
        return ttypes.String(val * self.__convert)


@texec.macro
class xPi(texec.TMacro):
    """
    {pi}
    Macro expands to the value of pi.
    """
    __mnemonics__ = ('pi', '\\u03C0')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String(math.pi)


@texec.macro
class xTau(texec.TMacro):
    """
    {tau}
    Returns twice the transcendtal number pi.
    """
    __mnemonics__ = ('tau', '\\u03C4')
    __tau = 2.0 * math.pi

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String(self.__tau)


@texec.function
class xLog(texec.MathExec, texec.TFunction):
    """
    {log VAL [BASE]}
    Returns the logarithm of VAL in base BASE. If BASE is not given, it's a natural log (BASE is 'e').
    """
    __mnemonics__ = ('log', 'ln')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2])
        vals = self.parseNumericArgs(name, args)
        if count == 1:
            base = math.e
        else:
            base = vals[1]
        return ttypes.String(math.log(vals[0], base))


@texec.function
class xFloor(texec.PrecisionExec, texec.TFunction):
    """
    {floor VAL [PREC]}

    Returns the floor of VAL, to the given PREC. PREC specifies the number of decimal digits after the decimal point to consider.
    The default precision is 0, meaning he result will be an integer.

    Negative values for PREC are also acceptable, in which case the specified number of digits to the left of the decimal point
    are zeroed out as well. If PREC is less than 1, the result is an integer, otherwise it is a float.
    """
    __mnemonics__ = ('floor', '\\u230A')

    def makeInt(self, val):
        return math.floor(val)


@texec.function
class xCeil(texec.PrecisionExec, texec.TFunction):
    """
    {ceil VAL [PREC]}

    Returns the ceiling of VAL, to the given PREC. PREC specifies the number of decimal digits after the decimal point to consider.
    The default precision is 0, meaning he result will be an integer.

    Negative values for PREC are also acceptable, in which case the specified number of digits to the left of the decimal point
    are zeroed out as well. If PREC is less than 1, the result is an integer, otherwise it is a float.
    """
    __mnemonics__ = ('ceil', '\\u2308')

    def makeInt(self, val):
        return math.ceil(val)


@texec.function
class xRound(texec.PrecisionExec, texec.TFunction):
    """
    {round VAL [PREC]}

    Returns the VAL, rounded to the given PREC. PREC specifies the number of decimal digits after the decimal point to consider.
    The default precision is 0, meaning he result will be an integer.

    Negative values for PREC are also acceptable, in which case the specified number of digits to the left of the decimal point
    are zeroed out as well. If PREC is less than 1, the result is an integer, otherwise it is a float.
    """
    __mnemonics__ = ('round', )

    def makeInt(self, val):
        return round(val)


@texec.function
class xEquiv(texec.BinaryCompareExec):
    """
        {equiv VAL1 VAL2}
                : Test equality of two numerical values, regardless of type. Which is
                : to that for instance 2.0 == 2. But values must be numeric strings.
    """
    __mnemonics__ = ('equiv', '==')

    def compare(self, a, b):
        return a == b


@texec.function
class xNequiv(texec.BinaryCompareExec):
    __mnemonics__ = ('nequiv', '!=')

    def compare(self, a, b):
        return a != b


@texec.macro
class xTrue(texec.TMacro):
    """
        {true}
    :Macro alias for String value "1", a Boolean true.
    """
    __mnemonics__ = ('true', 'bool.t')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('1')


@texec.macro
class xFalse(texec.TMacro):
    """
        {false}
    :Macro alias for String value "0", a Boolean false.
    """
    __mnemonics__ = ('false', 'bool.f')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String('0')


@texec.function
class xBool(texec.TFunction):
    """
        {bool VAL}
                :If VAL is equal to "0", result value is "0", otherwise result is "1".
    """
    __mnemonics__ = ('bool', 'bool.new')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        if args[0] == '0':
            return ttypes.String('0')
        else:
            return ttypes.String('1')


@texec.function
class xIsTrue(texec.TFunction):
    """
        {is-true VAL}
                :If VAL is equal to "1", result value is "1", otherwise result is "0".
    """
    __mnemonics__ = ('is-true', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        if isinstance(args[0], ttypes.String) and args[0] == '1':
            string = '1'
        else:
            string = '0'
        return ttypes.String(string)


@texec.function
class xIsFalse(texec.TFunction):
    """
        {is-false VAL}
                Aliases: "not"
                :If VAL is equal to "0", result value is "1", otherwise result is "0".
    """
    __mnemonics__ = ('is-false', 'not')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        if isinstance(args[0], ttypes.String) and args[0] == '0':
            string = '1'
        else:
            string = '0'
        return ttypes.String(string)


@texec.function
class xAnd(texec.TFunction):
    """
        {and [VAL0 [VAL1 [...]]]}
    Aliases: "&&", "all"
    Qualified name: "exp.and"
    :If no args given, results in True. If one or more args given, results
    :in True if an only if none of the arguments are equal to False.
    """
    __mnemonics__ = ('and', '&&', 'all', 'exp.and')

    def execute(self, name, args, ostream, stack):
        return ttypes.String(bool(all(s != '0' for s in args)))


@texec.function
class xOr(texec.TFunction):
    """
    Aliases: "||", "any"
    Qualified name: "exp.or"
    :If no args given, results in False. If one or more args given,
    :results in True if any of the arguments are not equal to True.
    """
    __mnemonics__ = ('or', '||', 'any', 'exp.or')

    def execute(self, name, args, ostream, stack):
        return ttypes.String(bool(any(s != '0' for s in args)))


@texec.function
class XorFunc(texec.TFunction):
    __mnemonics__ = ('xor', )

    def execute(self, name, args, ostream, stack):
        res = False
        for arg in args:
            if arg != '0':
                res = not res

        if res:
            return ttypes.String(1)
        else:
            return ttypes.String(0)


@texec.function
class xFileGetContents(texec.TFunction):
    """
    {file-get-contents FILENAME [MODE]}

    Reads the contents of specified file at the specified path in the filsystem,
    and results in the contents as a string. This is a convenience function to avoid
    creating a file descriptor for the file. If MODE is not specified, it is opened for
    reading in text mode.
    """
    __mnemonics__ = ('file-get-contents', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1, 2])
        fname = self.checkArgType(name, 0, args, ttypes.String).str
        if len(args) == 1:
            mode = 'r'
        else:
            mode = self.checkArgType(name, 1, args, ttypes.String).str
        try:
            fp = open(fname, mode)
            contents = fp.read()
            fp.close()
        except Exception as e:
            raise texceptions.TemplateIOException(e, self.filepos)

        return ttypes.String(contents)


@texec.function
class xFilePutContents(texec.TFunction):
    """
    {file-put-contents FILENAME [MODE] CONTENTS}

    Writes the specified String CONTENTS to the indicated file on the filesystem.
    FILENAME should be a file system path, not a file descriptor. This is a convenience
    function for not having to create a file descriptor for the file.

    Reuslt is Null

    If MODE is not specified, it is opened for writing in text mode.
    """
    __mnemonics__ = ('file-put-contents', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2, 3])
        fname = self.checkArgType(name, 0, args, ttypes.String).str
        if len(args) == 2:
            mode = 'w'
            cidx = 1
        else:
            mode = self.checkArgType(name, 1, args, ttypes.String).str
            cidx = 2
        contents = self.checkArgType(name, cidx, args, ttypes.String).str
        try:
            fp = open(fname, mode)
            contents = fp.write(contents)
            fp.close()
        except Exception as e:
            raise texceptions.TemplateIOException(e, self.filepos)

        return ttypes.Null()


@texec.function
class xOpen(texec.TFunction):
    """
        {open NAME MODE}
                :Results in a string giving the file descriptor (FD) of an opened
        file.
    """
    __mnemonics__ = ('open', 'file.open')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        fname = self.checkArgType(name, 0, args, ttypes.String).str
        mode = self.checkArgType(name, 1, args, ttypes.String).str
        if mode in ('r', 'rb'):
            flag = os.O_RDONLY
        else:
            if mode in ('w', 'wb'):
                flag = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
            elif mode in ('a', 'ab'):
                flag = os.O_APPEND | os.O_CREAT
            elif mode in ('rw', 'rwb'):
                flag = os.O_RDWR | os.O_CREAT
            else:
                raise texceptions.TemplateValueError('Unexpected file mode for "%s". Allowed modes are r(b), w(b), a(b), and rw(b).' % name, args[1].filepos, args[1])
            if mode.endswith('b'):
                if hasattr(os, 'O_BINARY'):
                    flag = flag | os.O_BINARY
            try:
                fd = os.open(fname, flag)
                return ttypes.String(fd)
            except OSError as e:
                raise texceptions.TemplateIOException(e, self.filepos)


@texec.function
class xClose(texec.IndexExec, texec.TFunction):
    """
        {close FD}
                :Close the file. Results in ttypes.Null.
    """
    __mnemonics__ = ('close', 'file.close')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        fd = self.parseIndexArg(name, 0, args)
        try:
            os.close(fd)
            return ttypes.Null()
        except IOError as e:
            raise texceptions.TemplateIOException(e, self.filepos)


@texec.function
class xWrite(texec.IndexExec, texec.TFunction):
    """
    {write FD STR}
    Writes the String STR to an open file identified by FD.
    Results in the number of bytes written.
    """
    __mnemonics__ = ('write', 'file.write')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        fd = self.parseIndexArg(name, 0, args)
        string = self.checkArgType(name, 1, args, ttypes.String).str
        try:
            written = os.write(fd, string)
            return ttypes.String(written)
        except OSError as e:
            raise texceptions.TemplateIOException(e, self.filepos)


@texec.function
class xRead(texec.IndexExec, texec.TFunction):
    """
    {read FD [COUNT]}
    Reads data from the file designate by FD, up to the specified COUNT number of characters.
    If COUNT is not given, reads until the EOF. Results in a String of the read data.
    """
    __mnemonics__ = ('read', 'file.read')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2])
        fd = self.parseIndexArg(name, 0, args)
        rcount = None
        if count == 2:
            rcount = self.parseIndexArg(name, 1, args)
        try:
            if rcount is None:
                ccount = 4096
                read = ''
                while True:
                    chunk = os.read(fd, ccount)
                    read += chunk
                    if len(chunk) < ccount:
                        break

            else:
                read = os.read(fd, rcount)
            return ttypes.String(read)
        except OSError as e:
            raise texceptions.TemplateIOException(e, self.filepos)

        return


@texec.function
class xStdout(texec.TFunction):
    """
        {stdout}
                :Results in the STDOUT FD.
    """
    __mnemonics__ = ('stdout', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String(sys.stdout.fileno())


@texec.function
class xStderr(texec.TFunction):
    """
        {stdout}
                :Results in the STDERR FD.
    """
    __mnemonics__ = ('stderr', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String(sys.stderr.fileno())


@texec.function
class xStdin(texec.TFunction):
    """
        {stdin}
                :Results in the STDin FD.
    """
    __mnemonics__ = ('stdin', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String(sys.stdin.fileno())


@texec.operator
class xRedirect(texec.TOperator):
    """
        {redirect FD EXPR}
                : First evaluates FD, then evaluates EXPR but redirecting all of the
                : expressions output to the specified FD file. Result is the result of
        : EXPR.
    """
    __mnemonics__ = ('redirect', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        fd = teval.evalExpression(args[0], ostream, stack)
        try:
            fd = int(fd)
        except Exception:
            raise texceptions.TemplateValueError('Invalid first argument for "%s": expected an integer value.' % name, fd.filepos, fd)

        try:
            s = tstreams.TemplateFDOutputStream(fd)
            res = teval.evalExpression(args[1], s, stack)
        except texceptions.TemplateIOException as e:
            if e.filepos is None:
                e.filepos = args[1].filepos
                raise e

        return res


@texec.operator
class xBuffer(texec.TOperator):
    """
        {buffer EXPR}
                : Evaluates EXPR but buffers all of its output, and results in the String
        : that it buffered. That means the result of EXPR is lost. You can use
        : `buffer-to` if you need the result of EXPR.
    """
    __mnemonics__ = ('buffer', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        s = tstreams.BufferedTemplateOutputStream()
        teval.evalExpression(args[0], s, stack)
        return ttypes.String(s.str())


@texec.operator
class xBufferTo(texec.TOperator):
    """
        {buffer-to NAME EXPR}
                Evaluates EXPR but buffers all of its output, and saves the string to
        the symbol named NAME (using a mechanism just like `set`).
        The result of this expression is the result of EXPR. If you don't need
        the result of EXPR, you can use `buffer` instead.
    """
    __mnemonics__ = ('buffer-to', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[2])
        sname = teval.evalExpression(args[0], ostream, stack)
        sname = self.checkType('first argument to "%s".' % name, sname, ttypes.String).str
        s = tstreams.BufferedTemplateOutputStream()
        res = teval.evalExpression(args[1], s, stack)
        stack.set(sname, ttypes.String(s.str(), filepos=self.filepos))
        return res


@texec.function
class xVersion(texec.TFunction):
    """
    {version}
    Returns the version string of templ.
    """
    __mnemonics__ = ('version', 'str.version')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String(version.string())


@texec.function
class xVersionDate(texec.TFunction):
    """
    {ver-date}
    Returns the version-date-string of templ.
    """
    __mnemonics__ = ('ver-date', 'str.ver-date')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String(version.datestr())


@texec.function
class xVersionTuple(texec.TFunction):
    """
    {version-tuple}
    Returns the version of templ as a tuple: (MAJOR, MINOR, PATCH, SEMANTIC, TAG, YEAR, MONTH, DAY)
    """
    __mnemonics__ = ('version-tuple', 'list.version')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.List([version.MAJOR, version.MINOR, version.PATCH, version.SEMANTIC, version.TAG,
         version.YEAR, version.MONTH, version.DAY])


@texec.function
class xVersionPlist(texec.TFunction):
    """
    {version-plist}
    Returns the version of templ as a Plist with fields ":major", ":minor", ":patch", ":semantic",
    ":tag", ":year", ":month", ":day"
    """
    __mnemonics__ = ('version-plist', 'plist.version')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.List([':major', version.MAJOR, ':minor', version.MINOR, ':patch', version.PATCH,
         ':semantic', version.SEMANTIC, ':tag', version.TAG,
         ':year', version.YEAR, ':month', version.MONTH, ':day', version.DAY])


@texec.function
class xDoc(texec.TFunction):
    """
    {doc EXE}
    Returns documentation string for the executable object EXE.
    """
    __mnemonics__ = ('doc', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        self.checkArgType(name, 0, args, texec.Executable)
        return ttypes.String(type(args[0]).__doc__, self.filepos)


@texec.function
class xExeName(texec.TFunction):
    """
    {exename EXE}

    Returns the canonical name of the given executable object (like a function, macro, or operator).
    """
    __mnemonics__ = ('exename', 'exe-name')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        self.checkArgType(name, 0, args, texec.Executable)
        name = args[0].name
        if name is None:
            return ttypes.Null()
        else:
            return ttypes.String(args[0].name)
            return


@texec.function
class xAliases(texec.TFunction):
    """
    {aliases EXE}

    Returns a ttypes.List of the known aliases for the given executable object. This does not include the canonical
    name (e.g., as returned by `exename`). This is only the built in aliases, if you've assigned the object
    to another symbol, it won't show up here.
    """
    __mnemonics__ = ('aliases', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        self.checkArgType(name, 0, args, texec.Executable)
        return ttypes.List(args[0].aliases)


@texec.function
class xStamp(texec.TFunction):
    """
    {stamp [LIST]}
    Returns the current UNIX timestamp, the number of seconds elapsed since Midnight on Jan 1 1970 UTC.
    Or, if LIST is given, it should be as the output of `localtime` or `gmtime`, and the corresponding
    timestamp for the time it represents is returned.
    """
    __mnemonics__ = ('stamp', 'time.stamp')
    __acceptable = (
     ('month', 0, 11),
     ('day of the month', 1, 31),
     ('hour', 0, 23),
     ('minute', 0, 59),
     ('second', 0, 61))

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[0, 1])
        if count == 0:
            return ttypes.String(int(time.time()))
        else:
            tlist = self.checkArgType(name, 0, args, ttypes.List)
            length = len(tlist)
            if length > 9:
                raise texceptions.TemplateValueError('Invalid time struct for argument to "%s": expected list with no more than 9 items.', args[0].filepos, tlist)
            xlist = [1970, 0, 1] + [0] * 6
            for i in xrange(length):
                val = self.checkType('%s element of LIST argument to "%s".' % (self.ordinal(i), name), tlist[i], ttypes.String).str
                try:
                    xlist[i] = int(val)
                except Exception:
                    fp = tlist[i].filepos
                    if fp is None:
                        fp = tlist.filepos
                    raise texceptions.TemplateValueError('Invalid value for %s element of LIST argument to "%s": expected an integer.' % (
                     self.ordinal(i), name), fp, val)

            for i in xrange(1, 6):
                label, min, max = self.__acceptable[(i - 1)]
                if xlist[i] < min or xlist[i] > max:
                    if i >= length:
                        fp = tlist.filepos
                    else:
                        fp = tlist[i].filepos
                        if fp is None:
                            fp = tlist.filepos
                    raise texceptions.TemplateValueError('Invalid %s value for "%s". Value should be in [%d, %d].' % (
                     label, name, min, max), fp, xlist[i])

            xlist[1] += 1
            del xlist[6:]
            return ttypes.String(calendar.timegm(xlist))
            return


@texec.function
class xLocalTime(texec.MathExec, texec.TFunction):
    """
    {localtime [STAMP]}
    Returns a List representing the date/time components of the specified time, or the current time
    if STAMP is not given. STAMP, if given, should be like the output of `stamp`.

    Returned value represents local time. Use `gmtime` for UTC time.

    The returned list has 9 elements: year, month, day (of the month), hour, min, sec, weekday, 
    year day, is-DST. This matches the standard C struct tm, or the python time.struct_time object.
    """
    __mnemonics__ = ('localtime', 'time', 'time.time')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[0, 1])
        stamp = None
        if count == 1:
            stamp = self.parseNumericArg(name, 0, args)
        tm = list(time.localtime(stamp))
        tm[1] -= 1
        tm[7] -= 1
        return ttypes.List(iter(tm))


@texec.function
class xGmtime(texec.MathExec, texec.TFunction):
    """
    {gmtime [STAMP]}
    Returns a List representing the data/time components of the specified time, or the current time
    if STAMP is not given. STAMP, if given, should be like the output of `stamp`.

    Returned value represents greenwhich mean time. Use `time`  (aka `localtime`) for local time.

    The returned list has 9 elements: year, month, day (of the month), hour, min, sec, weekday, 
    year day, is-DST. This matches the standard C struct tm, or the python time.struct_time object.

    Note that the different between GMT (aka UT1) and UTC is irrelevant as 1 second resolution: they
    are not allowed to differ by more than 0.9 seconds, so they are the same at this level.
    """
    __mnemonics__ = ('gmtime', 'utctime', 'time.utctime')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[0, 1])
        stamp = None
        if count == 1:
            stamp = self.parseNumericArg(name, 0, args)
        tm = list(time.gmtime(stamp))
        tm[1] -= 1
        tm[7] -= 1
        return ttypes.List(iter(tm))


@texec.function
class xTimePlist(texec.TFunction):
    """
    {time-plist TM-LIST}

    Given a TM struct as a list, like returned by `localtime` or `gmtime`, converts it to a plist
    with field names corresponding to the C standard fields of the tm struct, but without the leading
    "tm_". So we have ":year", ":mon", ":mday", ":hour", ":min", ":sec", ":wday", ":yday", and ":isdst".
    """
    __mnemonics__ = ('time-plist', 'time.toPlist')
    __fields = (':year', ':mon', ':mday', ':hour', ':min', ':sec', ':wday', ':yday',
                ':isdst')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1])
        tlist = self.checkArgType(name, 0, args, ttypes.List)
        length = len(tlist)
        if length > 9:
            raise texceptions.TemplateValueError('Invalid time struct for argument to "%s": expected list with no more than 9 items.', args[0].filepos, tlist)
        assert len(self.__fields) >= length
        res = []
        for i in xrange(length):
            res.append(self.__fields[i])
            res.append(tlist[i])

        return ttypes.List(res)


@texec.function
class xRand(texec.IndexExec, texec.TFunction):
    """
    {rand [MAX]}
    Returns a pseudo-random integer in the closed range [0, MAX]. If MAX is not given, 
    2^32 is used.

    All of these random functions use an unspecified RNG which is up to the implementation.
    That is also why there is no seed function because a seed function implies that if
    you start with the same seed, you'll always get the same values, which isn't necessarily
    true if the implementation uses a HW RNG, or if you move to a different implementation.
    """
    __mnemonics__ = ('rand', 'randint', 'random.int')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[0, 1])
        if count == 0:
            max = 4294967296
        else:
            max = self.parseIndexArg(name, 0, args)
        return ttypes.String(random.randint(0, max))


@texec.function
class xRandFloat(texec.TFunction):
    """
    {rand-float}
    Returns a pseudo-random floating-point value in the semi-open range [0.0, 1.0).
     See `rand` for details.
    """
    __mnemonics__ = ('rand-float', 'random.float')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        return ttypes.String(random.random())


@texec.function
class xSystem(texec.TFunction):
    """
    {system COMMAND}
    Invoke the system's command processor to execute the given COMMAND String, piping STDOUT from the
    command to the output stream, and returning the exit code. STDERR from the stream is written to
    STDERR of this process.
    """
    __mnemonics__ = ('system', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        command = self.checkArgType(name, 0, args, ttypes.String).str
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        ostream.write(out)
        ret = proc.wait()
        return ttypes.String(ret)


@texec.function
class xPipe(texec.TFunction):
    """
    {pipe COMMAND [[EC-NAME] STDIN]}
    Uses the system's command processor to execute the given COMMAND String, like `system`, but
    the given String STDIN is piped into the process, and instead of piping the output to this processes
    output stream, it buffers it into a string and returns it as the resulting value. If EC-NAME is given,
    the commands error-code is stored at the symbol (as with `getset`).
    """
    __mnemonics__ = ('pipe', )

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2, 3])
        command = self.checkArgType(name, 0, args, ttypes.String).str
        ecName = None
        stdin = None
        if count == 2:
            stdin = self.checkArgType(name, 1, args, ttypes.String).str
        elif count == 3:
            ecName = self.checkArgType(name, 1, args, ttypes.String)
            stdin = self.checkArgType(name, 2, args, ttypes.String).str
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        out, err = proc.communicate(stdin)
        ret = proc.wait()
        if ecName is not None:
            stack.set(ecName, ttypes.String(ret))
        return ttypes.String(out)


@texec.function
class xPipeBoth(texec.TFunction):
    """
    {pipe-both COMMAND [[EC-NAME] STDIN]}
    Like `pipe`, but returns a two-tuple List: (out, err), where out is what was written to the 
    process's STDOUT, and err is what was written to it's STDERR.
    """
    __mnemonics__ = ('pipe-both', )

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[1, 2, 3])
        command = self.checkArgType(name, 0, args, ttypes.String).str
        ecName = None
        stdin = None
        if count == 2:
            stdin = self.checkArgType(name, 1, args, ttypes.String).str
        elif count == 3:
            ecName = self.checkArgType(name, 1, args, ttypes.String)
            stdin = self.checkArgType(name, 2, args, ttypes.String).str
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        out, err = proc.communicate(stdin)
        ret = proc.wait()
        if ecName is not None:
            stack.set(ecName, ttypes.String(ret))
        return ttypes.List([ttypes.String(out, self.filepos), ttypes.String(err, self.filepos)])


@texec.function
class xVars(texec.TFunction):
    """
    {vars}
    Returns a ttypes.List of all the variable (names) in the stack.
    """
    __mnemonics__ = ('vars', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[0])
        names = []
        for scope in stack:
            names += scope.keys()

        return ttypes.List(names)


@texec.function
class xUnpack(texec.TFunction):
    """
    {unpack NAMES [REST] VALUES}

    For lists NAMES and VALUES, assigns values from VALUES into variables named by the corresponding element of NAMES.

    Acceptable for VALUES to have more elements than NAMES. In this case, if REST is given, then it is the name of a
    variable which will be assigned the remaining elements of VALUES (as a list). If REST isn't given, unassigned
    values from VALUES are just not assigned.

    If there are more NAMES than VALUES, it's an error. If REST is given and there are no values from VALUES that
    are left unassigned, then REST will be assigned an empty list.

    Resulting value is NULL.
    """
    __mnemonics__ = ('unpack', ',=')

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[2, 3])
        names = self.checkArgType(name, 0, args, ttypes.List)
        if count == 2:
            rest = None
            values = self.checkArgType(name, 1, args, ttypes.List)
        else:
            rest = self.checkArgType(name, 1, args, ttypes.String)
            values = self.checkArgType(name, 2, args, ttypes.List)
        if len(names) > len(values):
            raise texceptions.TemplateValueError('Invalid arguments for "%s": more names specified than values to unpack' % name, self.filepos)
        for i in range(len(names)):
            key = names[i]
            self.checkType('%s element of NAME for "%s"' % (self.ordinal(i), name), key, ttypes.String)
            val = values[i]
            stack.set(key, val)

        if rest is not None:
            stack.set(rest, ttypes.List(values.list[i + 1:]))
        return ttypes.Null()


@texec.function
class xEval(texec.TFunction):
    """
    {eval STRING}

    Evaluates a string as though it's templ code. This is equivalent to writing STRING to a file
    and then including that file with `include`.
    """
    __mnemonics__ = ('eval', 'str.eval')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        string = self.checkArgType(name, 0, args, ttypes.String).str
        stream = StringIO.StringIO(string)
        ipath = '<eval-string>'
        try:
            istream = tstreams.TemplateInputStream(stream, ipath)
            templ.processWithStack(istream, ostream, stack, iname=ipath)
            stream.close()
        except texceptions.TemplateException as e:
            e.filepos = tFilepos.IncludedFilepos.new(e.filepos, self.filepos)
            raise e

        return


@texec.function
class xEvalList(texec.TFunction):
    """
    {eval-list LIST}

    Evaluates a list as though it's a templ expression, and returns the result.
    This is actually not very much like eval.
    """
    __mnemonics__ = ('eval-list', 'list.eval')

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        tlist = self.checkArgType(name, 0, args, ttypes.List)
        try:
            return teval.evalExpression(tlist, ostream, stack)
        except texceptions.TemplateException as e:
            e.filepos = tFilepos.IncludedFilepos.new(e.filepos, self.filepos)
            raise e


@texec.function
class xInclude(texec.TFunction):
    """
    {include FILE}
    """
    __mnemonics__ = ('include', )

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        ipath = self.checkArgType(name, 0, args, ttypes.String).str
        try:
            stream = open(ipath, 'rb')
            istream = tstreams.TemplateInputStream(stream, ipath)
            templ.processWithStack(istream, ostream, stack, iname=ipath)
            stream.close()
        except IOError as e:
            raise texceptions.TemplateIOException(e, self.filepos)
        except texceptions.TemplateException as e:
            e.filepos = tFilepos.IncludedFilepos.new(e.filepos, self.filepos)
            raise

        return


@texec.function
class xIncludeAsList(texec.TFunction):
    """
    {include-as-list FILE}

    Parses the contents of the specified FILE as a templ template, returns a List
    describing the contents of template. Similar to `embed`, but this doesn't eval
    anything in the include file.
    """
    __mnemonics__ = ('include-as-list', )

    def execute--- This code section failed: ---

 L.3443         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'checkArgCount'
                6  LOAD_FAST             1  'name'
                9  LOAD_FAST             2  'args'
               12  LOAD_CONST               'exact'
               15  LOAD_CONST               1
               18  BUILD_LIST_1          1 
               21  CALL_FUNCTION_258   258  None
               24  POP_TOP          

 L.3444        25  LOAD_FAST             0  'self'
               28  LOAD_ATTR             1  'checkArgType'
               31  LOAD_FAST             1  'name'
               34  LOAD_CONST               0
               37  LOAD_FAST             2  'args'
               40  LOAD_GLOBAL           2  'ttypes'
               43  LOAD_ATTR             3  'String'
               46  CALL_FUNCTION_4       4  None
               49  LOAD_ATTR             4  'str'
               52  STORE_FAST            5  'ipath'

 L.3446        55  SETUP_EXCEPT        265  'to 323'

 L.3447        58  LOAD_GLOBAL           5  'open'
               61  LOAD_FAST             5  'ipath'
               64  LOAD_CONST               'rb'
               67  CALL_FUNCTION_2       2  None
               70  STORE_FAST            6  'stream'

 L.3448        73  LOAD_GLOBAL           6  'tstreams'
               76  LOAD_ATTR             7  'TemplateInputStream'
               79  LOAD_FAST             6  'stream'
               82  LOAD_FAST             5  'ipath'
               85  CALL_FUNCTION_2       2  None
               88  STORE_FAST            7  'istream'

 L.3449        91  BUILD_LIST_0          0 
               94  STORE_FAST            8  'elements'

 L.3450        97  SETUP_LOOP          196  'to 296'
              100  LOAD_GLOBAL           8  'True'
              103  POP_JUMP_IF_FALSE   295  'to 295'

 L.3451       106  LOAD_GLOBAL           9  'templ'
              109  LOAD_ATTR            10  'parse'
              112  LOAD_FAST             7  'istream'
              115  CALL_FUNCTION_1       1  None
              118  UNPACK_SEQUENCE_3     3 
              121  STORE_FAST            9  'stmt'
              124  STORE_FAST           10  'value'
              127  STORE_FAST           11  'filepos'

 L.3453       130  LOAD_FAST             9  'stmt'
              133  LOAD_GLOBAL           9  'templ'
              136  LOAD_ATTR            11  'STMT_EOI'
              139  COMPARE_OP            2  ==
              142  POP_JUMP_IF_FALSE   149  'to 149'

 L.3454       145  BREAK_LOOP       
              146  JUMP_BACK           100  'to 100'

 L.3456       149  LOAD_FAST             9  'stmt'
              152  LOAD_GLOBAL           9  'templ'
              155  LOAD_ATTR            12  'STMT_TEXT'
              158  LOAD_GLOBAL           9  'templ'
              161  LOAD_ATTR            13  'STMT_CEMBED'
              164  BUILD_TUPLE_2         2 
              167  COMPARE_OP            6  in
              170  POP_JUMP_IF_FALSE   237  'to 237'

 L.3457       173  LOAD_GLOBAL          14  'isinstance'
              176  LOAD_FAST            10  'value'
              179  LOAD_GLOBAL           4  'str'
              182  LOAD_GLOBAL          15  'unicode'
              185  BUILD_TUPLE_2         2 
              188  CALL_FUNCTION_2       2  None
              191  POP_JUMP_IF_TRUE    209  'to 209'
              194  LOAD_ASSERT              AssertionError
              197  LOAD_GLOBAL          17  'type'
              200  LOAD_FAST            10  'value'
              203  CALL_FUNCTION_1       1  None
              206  RAISE_VARARGS_2       2  None

 L.3458       209  LOAD_FAST             8  'elements'
              212  LOAD_ATTR            18  'append'
              215  LOAD_GLOBAL           2  'ttypes'
              218  LOAD_ATTR             3  'String'
              221  LOAD_FAST            10  'value'
              224  LOAD_FAST            11  'filepos'
              227  CALL_FUNCTION_2       2  None
              230  CALL_FUNCTION_1       1  None
              233  POP_TOP          
              234  JUMP_BACK           100  'to 100'

 L.3460       237  LOAD_FAST             9  'stmt'
              240  LOAD_GLOBAL           9  'templ'
              243  LOAD_ATTR            19  'STMT_LIST'
              246  COMPARE_OP            2  ==
              249  POP_JUMP_IF_FALSE   100  'to 100'

 L.3461       252  LOAD_GLOBAL          14  'isinstance'
              255  LOAD_FAST            10  'value'
              258  LOAD_GLOBAL           2  'ttypes'
              261  LOAD_ATTR            20  'List'
              264  CALL_FUNCTION_2       2  None
              267  POP_JUMP_IF_TRUE    276  'to 276'
              270  LOAD_ASSERT              AssertionError
              273  RAISE_VARARGS_1       1  None

 L.3462       276  LOAD_FAST             8  'elements'
              279  LOAD_ATTR            18  'append'
              282  LOAD_FAST            10  'value'
              285  CALL_FUNCTION_1       1  None
              288  POP_TOP          
              289  JUMP_BACK           100  'to 100'
              292  JUMP_BACK           100  'to 100'
              295  POP_BLOCK        
            296_0  COME_FROM            97  '97'

 L.3463       296  LOAD_FAST             6  'stream'
              299  LOAD_ATTR            21  'close'
              302  CALL_FUNCTION_0       0  None
              305  POP_TOP          

 L.3464       306  LOAD_GLOBAL           2  'ttypes'
              309  LOAD_ATTR            20  'List'
              312  LOAD_FAST             8  'elements'
              315  CALL_FUNCTION_1       1  None
              318  RETURN_VALUE     
              319  POP_BLOCK        
              320  JUMP_FORWARD         97  'to 420'
            323_0  COME_FROM            55  '55'

 L.3466       323  DUP_TOP          
              324  LOAD_GLOBAL          22  'IOError'
              327  COMPARE_OP           10  exception-match
              330  POP_JUMP_IF_FALSE   362  'to 362'
              333  POP_TOP          
              334  STORE_FAST           12  'e'
              337  POP_TOP          

 L.3467       338  LOAD_GLOBAL          23  'texceptions'
              341  LOAD_ATTR            24  'TemplateIOException'
              344  LOAD_FAST            12  'e'
              347  LOAD_FAST             0  'self'
              350  LOAD_ATTR            25  'filepos'
              353  CALL_FUNCTION_2       2  None
              356  RAISE_VARARGS_1       1  None
              359  JUMP_FORWARD         58  'to 420'

 L.3468       362  DUP_TOP          
              363  LOAD_GLOBAL          23  'texceptions'
              366  LOAD_ATTR            26  'TemplateException'
              369  COMPARE_OP           10  exception-match
              372  POP_JUMP_IF_FALSE   419  'to 419'
              375  POP_TOP          
              376  STORE_FAST           12  'e'
              379  POP_TOP          

 L.3469       380  LOAD_GLOBAL          27  'tFilepos'
              383  LOAD_ATTR            28  'IncludedFilepos'
              386  LOAD_ATTR            29  'new'
              389  LOAD_FAST            12  'e'
              392  LOAD_ATTR            25  'filepos'
              395  LOAD_FAST             0  'self'
              398  LOAD_ATTR            25  'filepos'
              401  CALL_FUNCTION_2       2  None
              404  LOAD_FAST            12  'e'
              407  STORE_ATTR           25  'filepos'

 L.3470       410  LOAD_FAST            12  'e'
              413  RAISE_VARARGS_1       1  None
              416  JUMP_FORWARD          1  'to 420'
              419  END_FINALLY      
            420_0  COME_FROM           419  '419'
            420_1  COME_FROM           320  '320'

Parse error at or near `POP_BLOCK' instruction at offset 295


@texec.function
class xEmbed(texec.TFunction):
    """
    {embed FILE}
    Reads and parses FILE as a template, processing it as though its
    an embedded template (except it's not terminated by >>>), and returns
    the List, just like an embedded template.

    This is similar to `include-as-list`, but it evaluates to-level Lists
    in the template.
    """
    __mnemonics__ = ('embed', )

    def execute--- This code section failed: ---

 L.3486         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'checkArgCount'
                6  LOAD_FAST             1  'name'
                9  LOAD_FAST             2  'args'
               12  LOAD_CONST               'exact'
               15  LOAD_CONST               1
               18  BUILD_LIST_1          1 
               21  CALL_FUNCTION_258   258  None
               24  POP_TOP          

 L.3487        25  LOAD_FAST             0  'self'
               28  LOAD_ATTR             1  'checkArgType'
               31  LOAD_FAST             1  'name'
               34  LOAD_CONST               0
               37  LOAD_FAST             2  'args'
               40  LOAD_GLOBAL           2  'ttypes'
               43  LOAD_ATTR             3  'String'
               46  CALL_FUNCTION_4       4  None
               49  LOAD_ATTR             4  'str'
               52  STORE_FAST            5  'ipath'

 L.3489        55  SETUP_EXCEPT        310  'to 368'

 L.3490        58  LOAD_GLOBAL           5  'open'
               61  LOAD_FAST             5  'ipath'
               64  LOAD_CONST               'rb'
               67  CALL_FUNCTION_2       2  None
               70  STORE_FAST            6  'stream'

 L.3491        73  LOAD_GLOBAL           6  'tstreams'
               76  LOAD_ATTR             7  'TemplateInputStream'
               79  LOAD_FAST             6  'stream'
               82  LOAD_FAST             5  'ipath'
               85  CALL_FUNCTION_2       2  None
               88  STORE_FAST            7  'istream'

 L.3492        91  BUILD_LIST_0          0 
               94  STORE_FAST            8  'elements'

 L.3493        97  SETUP_LOOP          241  'to 341'
              100  LOAD_GLOBAL           8  'True'
              103  POP_JUMP_IF_FALSE   340  'to 340'

 L.3494       106  LOAD_GLOBAL           9  'templ'
              109  LOAD_ATTR            10  'parse'
              112  LOAD_FAST             7  'istream'
              115  CALL_FUNCTION_1       1  None
              118  UNPACK_SEQUENCE_3     3 
              121  STORE_FAST            9  'stmt'
              124  STORE_FAST           10  'value'
              127  STORE_FAST           11  'filepos'

 L.3496       130  LOAD_FAST             9  'stmt'
              133  LOAD_GLOBAL           9  'templ'
              136  LOAD_ATTR            11  'STMT_EOI'
              139  COMPARE_OP            2  ==
              142  POP_JUMP_IF_FALSE   149  'to 149'

 L.3497       145  BREAK_LOOP       
              146  JUMP_BACK           100  'to 100'

 L.3499       149  LOAD_FAST             9  'stmt'
              152  LOAD_GLOBAL           9  'templ'
              155  LOAD_ATTR            12  'STMT_TEXT'
              158  LOAD_GLOBAL           9  'templ'
              161  LOAD_ATTR            13  'STMT_CEMBED'
              164  BUILD_TUPLE_2         2 
              167  COMPARE_OP            6  in
              170  POP_JUMP_IF_FALSE   237  'to 237'

 L.3500       173  LOAD_GLOBAL          14  'isinstance'
              176  LOAD_FAST            10  'value'
              179  LOAD_GLOBAL           4  'str'
              182  LOAD_GLOBAL          15  'unicode'
              185  BUILD_TUPLE_2         2 
              188  CALL_FUNCTION_2       2  None
              191  POP_JUMP_IF_TRUE    209  'to 209'
              194  LOAD_ASSERT              AssertionError
              197  LOAD_GLOBAL          17  'type'
              200  LOAD_FAST            10  'value'
              203  CALL_FUNCTION_1       1  None
              206  RAISE_VARARGS_2       2  None

 L.3501       209  LOAD_FAST             8  'elements'
              212  LOAD_ATTR            18  'append'
              215  LOAD_GLOBAL           2  'ttypes'
              218  LOAD_ATTR             3  'String'
              221  LOAD_FAST            10  'value'
              224  LOAD_FAST            11  'filepos'
              227  CALL_FUNCTION_2       2  None
              230  CALL_FUNCTION_1       1  None
              233  POP_TOP          
              234  JUMP_BACK           100  'to 100'

 L.3503       237  LOAD_FAST             9  'stmt'
              240  LOAD_GLOBAL           9  'templ'
              243  LOAD_ATTR            19  'STMT_LIST'
              246  COMPARE_OP            2  ==
              249  POP_JUMP_IF_FALSE   100  'to 100'

 L.3504       252  LOAD_GLOBAL          14  'isinstance'
              255  LOAD_FAST            10  'value'
              258  LOAD_GLOBAL           2  'ttypes'
              261  LOAD_ATTR            20  'List'
              264  CALL_FUNCTION_2       2  None
              267  POP_JUMP_IF_TRUE    276  'to 276'
              270  LOAD_ASSERT              AssertionError
              273  RAISE_VARARGS_1       1  None

 L.3507       276  LOAD_GLOBAL          21  'teval'
              279  LOAD_ATTR            22  'evalExpression'
              282  LOAD_FAST            10  'value'
              285  LOAD_FAST             3  'ostream'
              288  LOAD_FAST             4  'stack'
              291  CALL_FUNCTION_3       3  None
              294  STORE_FAST           12  'res'

 L.3508       297  LOAD_GLOBAL          14  'isinstance'
              300  LOAD_FAST            12  'res'
              303  LOAD_GLOBAL           2  'ttypes'
              306  LOAD_ATTR            23  'TType'
              309  CALL_FUNCTION_2       2  None
              312  POP_JUMP_IF_TRUE    321  'to 321'
              315  LOAD_ASSERT              AssertionError
              318  RAISE_VARARGS_1       1  None

 L.3509       321  LOAD_FAST             8  'elements'
              324  LOAD_ATTR            18  'append'
              327  LOAD_FAST            12  'res'
              330  CALL_FUNCTION_1       1  None
              333  POP_TOP          
              334  JUMP_BACK           100  'to 100'
              337  JUMP_BACK           100  'to 100'
              340  POP_BLOCK        
            341_0  COME_FROM            97  '97'

 L.3511       341  LOAD_FAST             6  'stream'
              344  LOAD_ATTR            24  'close'
              347  CALL_FUNCTION_0       0  None
              350  POP_TOP          

 L.3512       351  LOAD_GLOBAL           2  'ttypes'
              354  LOAD_ATTR            20  'List'
              357  LOAD_FAST             8  'elements'
              360  CALL_FUNCTION_1       1  None
              363  RETURN_VALUE     
              364  POP_BLOCK        
              365  JUMP_FORWARD         97  'to 465'
            368_0  COME_FROM            55  '55'

 L.3514       368  DUP_TOP          
              369  LOAD_GLOBAL          25  'IOError'
              372  COMPARE_OP           10  exception-match
              375  POP_JUMP_IF_FALSE   407  'to 407'
              378  POP_TOP          
              379  STORE_FAST           13  'e'
              382  POP_TOP          

 L.3515       383  LOAD_GLOBAL          26  'texceptions'
              386  LOAD_ATTR            27  'TemplateIOException'
              389  LOAD_FAST            13  'e'
              392  LOAD_FAST             0  'self'
              395  LOAD_ATTR            28  'filepos'
              398  CALL_FUNCTION_2       2  None
              401  RAISE_VARARGS_1       1  None
              404  JUMP_FORWARD         58  'to 465'

 L.3516       407  DUP_TOP          
              408  LOAD_GLOBAL          26  'texceptions'
              411  LOAD_ATTR            29  'TemplateException'
              414  COMPARE_OP           10  exception-match
              417  POP_JUMP_IF_FALSE   464  'to 464'
              420  POP_TOP          
              421  STORE_FAST           13  'e'
              424  POP_TOP          

 L.3517       425  LOAD_GLOBAL          30  'tFilepos'
              428  LOAD_ATTR            31  'IncludedFilepos'
              431  LOAD_ATTR            32  'new'
              434  LOAD_FAST            13  'e'
              437  LOAD_ATTR            28  'filepos'
              440  LOAD_FAST             0  'self'
              443  LOAD_ATTR            28  'filepos'
              446  CALL_FUNCTION_2       2  None
              449  LOAD_FAST            13  'e'
              452  STORE_ATTR           28  'filepos'

 L.3518       455  LOAD_FAST            13  'e'
              458  RAISE_VARARGS_1       1  None
              461  JUMP_FORWARD          1  'to 465'
              464  END_FINALLY      
            465_0  COME_FROM           464  '464'
            465_1  COME_FROM           365  '365'

Parse error at or near `POP_BLOCK' instruction at offset 340


@texec.function
class xStrrep(texec.MathExec, texec.TFunction):
    """
    {strrep THIS WITHTHIS INHERE [COUNT]}

    Replaces occurences of String THIS in String INHERE with the String WITHTHIS. If COUNT is given, it performs at most
    that many replacements, leaving the rest. If not given, perform all replacements in the string.
    """
    __mnemonics__ = ('strrep', )

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[3, 4])
        self.checkArgType(name, 0, args, ttypes.String)
        self.checkArgType(name, 1, args, ttypes.String)
        self.checkArgType(name, 2, args, ttypes.String)
        oldstr = args[0].str
        newstr = args[1].str
        instr = args[2].str
        if count == 3:
            ret = instr.replace(oldstr, newstr)
        else:
            count = self.parseArg(name, 3, args[3])
            ret = instr.replace(oldstr, newstr, count)
        return ttypes.String(ret, self.filepos)


@texec.macro
class xWrap(texec.TMacro):
    """
    {wrap WITH [ANDTHIS] STRING}
    
    Expands to {join "" WITH STRING ANDTHIS}. If ANDTHIS is not given, it's WITH.
    """
    __mnemonics__ = ('wrap', )

    def execute(self, name, args, ostream, stack):
        count = self.checkArgCount(name, args, exact=[2, 3])
        if count == 2:
            w = a = args[0]
            s = args[1]
        else:
            w, a, s = args
        return ttypes.List(['join', '', w, s, a])


@texec.macro
class xQuote(texec.TMacro):
    r"""
   {quote STR}
   Puts double-quotes around the given string, expands as a macro to {wrap "\"" STR}.
   This does NOT escape quote characters that may already be inside STR.
   """
    __mnemonics__ = ('quote', "''")

    def execute(self, name, args, ostream, stack):
        self.checkArgCount(name, args, exact=[1])
        return ttypes.List(['wrap', '"', args[0]])