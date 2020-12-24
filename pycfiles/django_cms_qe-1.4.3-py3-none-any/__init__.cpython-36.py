# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_video/__init__.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1070 bytes
"""
Video plugin
############

Plugin for Django CMS QE providing video players for hosting services like
YouTube or also custom local file. For local files is used HTML5 player.

Usage
*****

Add plugin from section **Video player** called **Video player - source file**
or **Video player - hosting services**.

Video player - source file
==========================

Choose or upload a source file at configuration screen and setup player
parameters if needed.

Track
-----

You can also add subtitles, captions, descriptions or chapters to your video.
Add sub-plugin **Track** and choose which kind of track to add.

Video player - hosting services
===============================

Choose which video hosting service you want to use at configuration screen
and setup player parameters if needed.

API
***

Django CMS
==========

.. autoclass:: cms_qe_video.cms_plugins.SourceFileVideoPlayerPlugin
    :members:

.. autoclass:: cms_qe_video.cms_plugins.HostingVideoPlayerPlugin
    :members:

.. autoclass:: cms_qe_video.cms_plugins.VideoTrackPlugin
    :members:

"""