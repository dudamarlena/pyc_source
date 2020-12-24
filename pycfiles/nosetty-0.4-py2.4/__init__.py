# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/nosetty/__init__.py
# Compiled at: 2007-05-24 09:48:31
"""A plugin to run nosetests more interactively

nosetty is a plugin for [http://somethingaboutorange.com/mrl/projects/nose/ nose], a test runner for python.  It accepts various commands at the terminal, giving you some one-on-one quality time with your tracebacks.  Most importantly, editing a failure point is as easy as typing a number.  How about a screenshot?

http://farmdev.com/projects/nosetty/nosetty-screenshot.png

== Install ==

{{{
easy_install nosetty
}}}

get the [http://peak.telecommunity.com/DevCenter/EasyInstall easy_install command here].

Development versions are available as:

{{{
easy_install nosetty==dev
}}}

...or via subversion at [http://nosetty.googlecode.com/svn/trunk/#egg=nosetty-dev http://nosetty.googlecode.com/svn/trunk/]

== Usage ==

Activate the plugin like so:

{{{
nosetests --tty
}}}

But to get some useful results, you'll have to tell it how to hook into your editor and other things.  All this is described in detail on the [Recipes] page.

To give the plugin a whirl, you can [http://code.google.com/p/nosetty/source checkout the source] and type...

{{{
cd src/nosetty
easy_install .
nosetests -w examples --tty
}}}

...to get what's shown in the above screenshot.

== Project Page ==

If you're not already there, the nosetty project lives on [http://code.google.com/p/nosetty/ google code].  Please submit any bugs, patches, failing tests, et cetera using the [http://code.google.com/p/nosetty/issues/list Issue Tracker].

"""
__version__ = '0.4'
try:
    import nose
except ImportError:
    pass
else:
    del nose
    from nosetty import *