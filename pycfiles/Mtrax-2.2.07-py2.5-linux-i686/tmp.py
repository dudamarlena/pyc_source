# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/tmp.py
# Compiled at: 2008-08-08 16:19:40
(RIFF, riff_size, AVI) = struct.unpack('4sI4s', file.read(12))
(LIST, hdrl_size, hdrl) = struct.unpack('4sI4s', file.read(12))
(avih, avih_size) = struct.unpack('4sI', file.read(8))
avihchunkstart = file.tell()
(microsecperframe,) = struct.unpack('I', file.read(4))
framespersec = 1000000.0 / float(microsecperframe)
file.seek(12, 1)
(nframes,) = struct.unpack('I', file.read(4))
file.seek(12, 1)
(width, height) = struct.unpack('2I', file.read(8))
file.seek(avihchunkstart + avih_size, 0)
(LIST, stream_listsize, strl) = struct.unpack('4sI4s', file.read(12))
(strh, strh_size) = struct.unpack('4sI', file.read(8))
strhstart = file.tell()
(vids, fcc) = struct.unpack('4s4s', file.read(8))
file.seek(strhstart + strh_size, 0)