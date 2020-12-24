# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pychangelog\version.py
# Compiled at: 2014-05-20 20:14:10
__doc__ = '\nThe ``version`` module provides version numbering for the entire package.\n\n.. contents:: **Page Contents**\n    :local:\n    :depth: 3\n    :backlinks: top\n\n\nVersioning\n-------------\n\nThis packages uses a five part version number, plus an incremental release number.\nEither the version number or the release number can be used to identify\na released version of the code.\n\n\nVersion Number\n~~~~~~~~~~~~~~~\n\nThe version number is a four part dotted number, with an optional suffix on the end.\nFormally, a version number looks like:\n\n.. productionlist::\n    version number: <Major>.<minor>[.<patch>[.<semantic>]][-[x-]<suffix>]\n\nWith each new released version of the code, exactly one of the four numbers will\nincrease, and any numbers to its right will reset to 0.\n\nThe easiest way to understand version numbers is from the perspective of someone who has\nwritten *client code*: i.e., code that makes use of a particular version of the\nlibrary. From this perspective, the version number indicates whether or\nnot your client code can be expected to work with different versions of this package.\n\n.. _major-version:\n\nMajor Version\n***************\n\nThe ``<Major>`` component is the **major version number**, and it describes *backward\ncompatibility*. Going to a *newer* version of the package, your code should continue to work\nas long as the major version doesn\'t change.\n\nThe major version is changed only when something is removed from the public\ninterface. For instance, if a function is no longer supported, the major version number\nwould have to increase, because client code which relied on that function would no longer\nwork.\n\nThe major version number can be accessed through the `MAJOR` member of this module.\n\n.. _minor-version:\n\nMinor Version\n***************\n\nThe ``<minor>`` component is the **minor version number**, and it describes *forward\ncompatibility*: Going to an *older* version of the package, your code will continue to work\nas long as the minor version doesn\'t change. (As before, your code will also work\nfor *newer* versions, as long as the major version number hasn\'t changed).\n\nThe minor version number is changed only when something is added to the public\ninterface, for instance a new function is added. Such a change maintains *backward*\ncompatibility (as described above), but *loses forward compatibility*, because any client\ncode written again this new version may not work with an older version.\n\nThe minor version number can be accessed through the `MINOR` member of this module.\n\n.. _patch-version:\n\nPatch Version\n***************\n\nThe ``<patch>`` component is the **patch number**, and it describes changes that\n*do not affect compatibility*, either forwards or backwards. Your client code will\ncontinue to work with an older or newer version of the package as long as the major and minor\nversion numbers are the same, regardless of the patch number.\n\nPatch changes are code changes that do not effect the interface, for instance bug-fixes\nor performance enhancements. (although some bugs effect the interface and may therefore\ncause a higher version number to change).\n\nThe patch number can be accessed through the `PATCH` member of this module.\n\n\n.. _semantic-version:\n\nSemantic Version\n*******************\n\nThe ``<semantic>`` component is the **semantic version number**, and it describes changes\nthat do not affect how the code runs at all. Ths generally means that documentation or\nother auxilliary files included in the package have changed.\n\nThe semantic version number can be accessed through the `SEMANTIC` member of this module.\n\n\nCompatibility Summary\n**********************\n\nThe following table summarizes compatibility for a hypothetical client application\nbuilt against released version ``M.n.p.s``:\n\n===========     =================== ======================\nComponent       Compatibile (all)   Incompatible (any)\n===========     =================== ======================\nMajor           M                   != M\nminor           >= n                < n\npatch           any                 \nsemantic        any                 \n===========     =================== ======================\n\n\n\nVersion Suffix\n********************\n\nThe ``<suffic>`` component is the **version suffix**, which is used only for non-released\ncode. The suffix has one of the following forms:\n\n.. productionlist::\n    version suffix  :   << empty >>\n                    :   dev[-<rev>]\n                    :   blood-<branch>[-<rev>]\n\nThe first form is an empty suffix, and is reserved for released (tagged) code only.\n\nThe second form, `"dev"`, is for non-released code in the *trunk*. This is the\nmain line of development. Dev code may not be completely functional, and may even\nbreak the existing interface.\n\nThe third form, `"blood-..."`, if for non-released code on a *branch*. The `<branch>`\ncomponent of this form should be the name of the branch. This is considered\n*bleeding-edge* code and may be highly unstable.\n\nThe optional ``<rev>`` component on both the second and third forms can be used to\nspecify a specific revision for comitted development code. This must be an globally\nunambiguous identifier for the revision, for instance the change set id.\n\nDevelopment code\n*********************\n\nA non-empty version suffix indicates a *development version* of the code. In this case, \nthe four version numbers remain *unchanged* until the code is released (in which case\nit is no longer development code, and the suffix is changed to empty).\n\nIn other words, anytime you see a non-empty version suffix, the version numbers shown\nrefer to version from which the development code is derived. This is done because it\nis not generally known until release what the next released version number will\nbe, since it is not known what types of changes will be included in it.\n\n\nSpecifying a version number\n******************************\n\nWhen specifying a version number, the major and minor version numbers should always\nbe included. Additionally, all non-zero version numbers should be included, and\nany version number to the left of a non-zero version number should be included.\n\nThe suffix should always be included in the version number, with the indicated hyphen\nseparating the semantic version number and the suffix. The only exception is for\nreleased code, in which case the suffix is empty and should be omitted, along with the\njoining hyphen.\n\nThe optional ``"x-"`` shown preceding the suffix in the version number is for compatibility\nwith setup-tools so that versions compare correctly.\n\nThe above rules will unambiguously describe any released version of the package.\n\nInterface Version\n******************************\n\nBecause any change to the public interface requires a change to either the major or minor\nversion numbers, the interface can be specified by a shortened two part version:\n\n.. productionlist::\n    interface version   :   <Major>.<minor>\n\nNote that this only applies for released versions: development versions may modify the\npublic interface prior to changing the version numbers.\n    \n\nRelease Number\n~~~~~~~~~~~~~~~~~~~~~\n\nThe release number is a simple integer which increments by one for every public release\nof the code. It does not convey any information about compatibility with other versions,\nbut it does provide a simple alternative to identifying released versions.\n\nThe release number should be written with a leading ``"r"`` or ``"rel"``. For\ninstance, the first release was ``"r1"``.\n\nFor release code, the release number may be used in place of the suffix in the version\nnumber. This is optional because the version number and the release number are\nsynonymous. However, including them both in the version string is a useful way to\nprovide both pieces of information.\n\nThis alternative form of the version number is:\n    \n.. productionlist::\n    alt. version number :   <Major>.<minor>[.<patch>[.<semantic>]]-r<release>\n\n\nModule Contents\n--------------------\n\n'
RELEASE = 2
MAJOR = 1
MINOR = 1
PATCH = 0
SEMANTIC = 0
SUFFIX = None
COPYRIGHT = 2014
YEAR = 2014
MONTH = 5
DAY = 19
MONTH_NAMES = [
 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
assert MONTH > 0 and MONTH <= len(MONTH_NAMES)

def setuptools_string():
    """
    Returns the version string used by `setuptools`. This takes one of two forms:

    .. productionlist::
        setuptools_string   :   <Major>.<minor>.<patch>.<semantic>-x-<suffix>
                            :   <Major>.<minor>.<patch>.<semantic>-r<release>

    The first form is used for development code (i.e., when `SUFFIX` is not `None`),
    and the second it used for released code.

    This is similar to `string`, except for the additional ``x-`` for development
    versions, which is used to ensure that `setuptools` sorts versions correctly.
    (specifically, so that released versions are earler than development versions
    which are derived from them).
    """
    vstr = '%d.%d.%d.%d' % (MAJOR, MINOR, PATCH, SEMANTIC)
    if SUFFIX is not None:
        vstr += '-x-%s' % SUFFIX
    else:
        vstr += '-r%d' % RELEASE
    return vstr


def tag_name():
    """
    Returns the tag name for the most recent release.
    """
    return 'r%d-v%d.%d.%d.%d' % (RELEASE, MAJOR, MINOR, PATCH, SEMANTIC)


def short_string():
    """
    Returns a string describing the `Interface Version`_ (i.e., ``<Major>.<minor>``).
    """
    return '%d.%d' % (MAJOR, MINOR)


def string():
    """
    Like `setuptools_string`, except leaves out the ``x-`` for development
    versions.
    """
    vstr = '%d.%d.%d.%d' % (MAJOR, MINOR, PATCH, SEMANTIC)
    if SUFFIX is not None:
        vstr += '-%s' % SUFFIX
    else:
        vstr += '-r%d' % RELEASE
    return vstr


def datestr():
    """
    Returns a simple string giving the date of release. Format
    of this string is unspecified, it intended to be human readable,
    not machine parsed. For machine processing, use the individual
    variables, as listed below.

    .. seealso ::
        * `YEAR`
        * `MONTH`
        * `DAY`
        * `MONTH_NAMES`

    """
    assert MONTH > 0 and MONTH <= len(MONTH_NAMES)
    return '%d %s %02d' % (YEAR, MONTH_NAMES[(MONTH - 1)], DAY)