# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/vorbisDecodeComponent.py
# Compiled at: 2008-10-19 12:19:52
"""This is a deprecation stub, due for later removal.
"""
import Kamaelia.Support.Deprecate as Deprecate
from Kamaelia.Codec.Vorbis import VorbisDecode as __VorbisDecode
from Kamaelia.Codec.Vorbis import AOAudioPlaybackAdaptor as __AOAudioPlaybackAdaptor
Deprecate.deprecationWarning('Use Kamaelia.Codec.Vorbis instead of Kamaelia.vorbisDecodeComponent')
VorbisDecode = Deprecate.makeClassStub(__VorbisDecode, 'Use Kamaelia.Codec.Vorbis:VorbisDecode instead of Kamaelia.vorbisDecodeComponent:VorbisDecode', 'WARN')
AOAudioPlaybackAdaptor = Deprecate.makeClassStub(__AOAudioPlaybackAdaptor, 'Use Kamaelia.Codec.Vorbis:AOAudioPlaybackAdaptor instead of Kamaelia.vorbisDecodeComponent:AOAudioPlaybackAdaptor', 'WARN')