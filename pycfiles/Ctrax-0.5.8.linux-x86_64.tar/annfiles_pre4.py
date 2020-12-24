# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/annfiles_pre4.py
# Compiled at: 2013-09-26 00:29:39
import multiprocessing, os, pickle, shutil, tempfile, time
from types import IntType, SliceType
import numpy as num
from scipy.io import savemat
import wx
from version import __version__, DEBUG
from movies import known_extensions
from params import params, diagnostics
import ellipsesk as ell, sys
DEBUG_LEVEL = 0
if not DEBUG:
    DEBUG_LEVEL = 0
dataformatstring = 'identity x y major minor angle'

class InvalidFileFormatException(Exception):
    pass


class AnnotationFile():

    def __init__(self, filename=None, bg_imgs=None, doreadheader=True, justreadheader=False, doreadbgmodel=True, doreadtrx=False, readonly=False):
        """This function should be called inside an exception handler
        in case the annotation header versions are different from expected
        or the file doesn't exist."""
        self.filename = filename
        if self.filename is not None:
            self.outdir = os.path.dirname(filename)
        self.version = __version__
        self.file = None
        self.file_lock = multiprocessing.RLock()
        self.bg_imgs = bg_imgs
        self.orientations_chosen = False
        if justreadheader:
            if DEBUG_LEVEL > 0:
                print 'Just reading header'
            self.file = open(filename, 'rb')
            if doreadbgmodel:
                if DEBUG_LEVEL > 0:
                    print 'Reading header ...'
                self.ReadAnnHeader(doreadstartframe=doreadtrx)
                if DEBUG_LEVEL > 0:
                    print 'Done reading header.'
            else:
                if DEBUG_LEVEL > 0:
                    print 'Reading settings ...'
                self.ReadSettings()
                if DEBUG_LEVEL > 0:
                    print 'Done reading settings.'
            self.file.close()
            return
        else:
            self.isdatawritten = False
            self.firstframetracked = 0
            self.lastframetracked = -1
            self.firstframewritten = 0
            self.lastframewritten = -1
            self.firstframebuffered = 0
            self.lastframebuffered = -1
            self.idtable = dict()
            self.n_fields = len(dataformatstring.split())
            self.recycledids = []
            if DEBUG_LEVEL > 0:
                print 'Initialized data structures'
            if filename is None:
                if DEBUG_LEVEL > 0:
                    print 'Creating a temporary file'
                self.file = tempfile.NamedTemporaryFile(mode='wb+', suffix='.ann')
                self.filename = self.file.name
                if DEBUG_LEVEL > 0:
                    print 'temporary filename = ' + self.filename
                params.nids = 0
                return
            if os.path.isfile(filename) and not readonly:
                dirname, shortname = os.path.split(filename)
                mod_time = os.path.getmtime(filename)
                time_str = time.strftime('bak_%y%m%d-%H%M%S_', time.localtime(mod_time))
                new_name = os.path.join(dirname, time_str + shortname)
                try:
                    shutil.copy2(filename, new_name)
                except:
                    try:
                        shutil.copyfile(filename, new_name)
                    except:
                        print 'Could not create back-up of ann file ' + filename

            newfile = False
            if readonly:
                self.file = open(filename, 'rb')
            else:
                try:
                    self.file = open(filename, 'rb+')
                except IOError:
                    self.file = open(filename, 'wb+')
                    newfile = True

                if not newfile:
                    try:
                        self.CheckAnnHeader()
                    except:
                        s = 'Could not read annotation header, not reading in %s.' % filename
                        if params.feedback_enabled:
                            wx.MessageBox(s, 'Warning', wx.ICON_WARNING)
                        else:
                            print s
                        raise
                        self.file.close()
                        self.file = open(filename, 'wb+')
                        newfile = True

                self.common_initialization()
                if DEBUG_LEVEL > 0:
                    print 'nbuffer = %d, lookupinterval = %d' % (self.nbuffer, self.lookupinterval)
                if doreadheader and not newfile:
                    self.ReadAnnHeader()
                if not doreadtrx and (not params.feedback_enabled or newfile):
                    return
                if DEBUG_LEVEL > 0:
                    print 'Reading trajectories...'
                self.firstframetracked = params.start_frame
                self.firstframebuffered = self.firstframetracked
                self.lastframetracked = self.firstframetracked - 1
                self.lastframebuffered = self.firstframebuffered - 1
                if DEBUG_LEVEL > 0:
                    print 'initialized firstframetracked = %d, firstframebuffered = %d' % (self.firstframetracked, self.firstframebuffered)
                i = 0
                while True:
                    p = self.file.tell()
                    line = self.file.readline()
                    if line == '':
                        break
                    if i % self.lookupinterval == 0:
                        if DEBUG_LEVEL > 0:
                            print 'i = %d, adding %x to the lookup table for frame = %d' % (i, p, self.lastframetracked + 1)
                        if DEBUG_LEVEL > 0:
                            print 'line = ' + str(line.split())
                        self.lookup.append(p)
                    try:
                        ells = self.ParseData(line)
                    except:
                        print 'Error parsing line %d. Aborting.' % len(self.buffer)
                        break

                    self.CountIds(ells)
                    if len(self.buffer) < self.nbuffer:
                        self.buffer.append(ells)
                        self.lastframebuffered += 1
                    i += 1
                    self.lastframetracked += 1

            self.nframestracked = self.lastframetracked - self.firstframetracked + 1
            if DEBUG_LEVEL > 0:
                print 'Finished reading in trajectories'
            if DEBUG_LEVEL > 0:
                print 'firstframetracked = %d, lastframetracked = %d' % (self.firstframetracked, self.lastframetracked)
            if DEBUG_LEVEL > 0:
                print 'firstframebuffered = %d, lastframebuffered = %d, n = %d' % (self.firstframebuffered, self.lastframebuffered, len(self.buffer))
            self.firstframewritten = self.firstframetracked
            self.lastframewritten = self.lastframetracked
            self.isdatawritten = True
            if DEBUG_LEVEL > 0:
                print 'Finished reading trajectories'
            if DEBUG_LEVEL > 0:
                print 'framestracked = [%d,%d], framesbuffered = [%d,%d], frameswritten = [%d,%d]' % (self.firstframetracked, self.lastframetracked, self.firstframebuffered, self.lastframebuffered, self.firstframewritten, self.lastframewritten)
            return

    def common_initialization(self):
        """Some initializtion code that doesn't need 3 instances."""
        self.nframestracked = 0
        self.maxlookback = max(params.lostdetection_length, params.spuriousdetection_length, params.mergeddetection_length, params.splitdetection_length) + 1
        self.buffer = []
        self.nbuffer = max(1000, self.maxlookback) + 1
        self.lookup = []
        self.lookupinterval = 1000
        params.nids = 0

    def InitializeData(self, firstframe=0, lastframe=None):
        """Initialize data structures, annotation file to store 
        firstframe through lastframe.
        Data structures:
        buffer: a queue that will store up to maxnbuffer frames worth of 
        annotation. It is a list of lists of ellipses. the first frame
        stored is "firstframebuffered" and the last frame stored is 
        "lastframebuffered". the number of frames stored so far is "n" and
        at most "nbuffer" will be stored. 
        file: the annotation file contains the header followed by the 
        ellipses for each frame from "firstframewritten" through
        "lastframewritten". 
        lookup: list of the locations in the file of tracks for
        certain frames. we store the locations of frames f such that
        (f - firstframetracked) % lookupinterval == 0
        """
        if lastframe is None:
            lastframe = firstframe - 1
        if lastframe >= firstframe and not self.isdatawritten:
            raise Exception, 'This should never happen: we are trying to store frames, but we have not written the annotation file yet'
        if lastframe < firstframe:
            self.InitializeEmptyData(firstframe, lastframe)
        else:
            if DEBUG_LEVEL > 0:
                print 'cropping data to %d:%d' % (firstframe, lastframe)
            self.CropData(firstframe, lastframe)
        self.orientations_chosen = False
        if DEBUG_LEVEL > 0:
            print 'Finished Initializing Data'
        return

    def InitializeEmptyData(self, firstframe, lastframe):
        self.firstframetracked = firstframe
        self.lastframetracked = lastframe
        self.firstframewritten = firstframe
        self.lastframewritten = lastframe
        self.firstframebuffered = firstframe
        self.lastframebuffered = lastframe
        self.idtable = dict()
        self.recycledids = []
        self.common_initialization()
        if not self.file.closed:
            self.file.close()
        self.file = open(self.filename, mode='wb+')
        if DEBUG_LEVEL > 0:
            print 'Writing annotation header'
        self.WriteAnnHeader(params.start_frame)

    def InitializeBufferForTracking(self, f):
        if not self.IsAnnData() or f <= self.firstframetracked:
            return
        with self.file_lock:
            g = max(f - self.nbuffer, self.firstframetracked)
            if DEBUG_LEVEL > 0:
                print 'Filling buffer with frames %d through %d' % (g, f - 1)
            self.seek(g)
            self.buffer = []
            self.firstframebuffered = g
            self.lastframebuffered = f - 1
            for h in range(g, f):
                self.buffer.append(self.read_ellipses())

            g = max(self.firstframetracked, f - self.maxlookback - 1)
            self.truncate(g)

    def truncate(self, g):
        with self.file_lock:
            self.seek(g)
            if DEBUG_LEVEL > 0:
                print 'Cropping written trajectories before frame %d = %x' % (g, self.file.tell())
            self.file.truncate()
            i, j = self.lookupfloor(g - 1)
            for j in range(i + 1, len(self.lookup)):
                if DEBUG_LEVEL > 0:
                    print 'Removing lookup[%d] = %x from lookup' % (j, self.lookup[j])
                tmp = self.lookup.pop(j)
                self.lastframewritten = g - 1

    def CropData(self, firstframe, lastframe):
        if firstframe < self.firstframewritten or lastframe > self.lastframewritten:
            raise Exception, 'This should never happen: we need to store frames that we do not have in the annotation file (wrote %d-%d, cropping to %d-%d)' % (self.firstframewritten, self.lastframewritten, firstframe, lastframe)
        self.file_lock.acquire()
        if self.file.closed:
            self.file = open(self.filename, mode='rb+')
        else:
            self.file.flush()
        self.file.seek(0, 0)
        cpfile = tempfile.TemporaryFile()
        shutil.copyfileobj(self.file, cpfile)
        cpfile.flush()
        if DEBUG_LEVEL > 0:
            print 'Copied ann file to temporary file'
        self.file.close()
        self.file = open(self.filename, mode='wb+')
        if DEBUG_LEVEL > 0:
            print 'Reopened %s for writing' % self.filename
        self.WriteAnnHeader(params.start_frame)
        if DEBUG_LEVEL > 0:
            print 'Wrote header'
        oldlookup = self.lookup
        oldlookupinterval = self.lookupinterval
        oldfirstframetracked = self.firstframetracked
        oldnframestracked = self.nframestracked
        self.common_initialization()
        self.firstframetracked = firstframe
        self.firstframewritten = firstframe
        self.lastframetracked = lastframe
        self.lastframewritten = lastframe
        self.firstframebuffered = firstframe
        self.lastframebuffered = min(lastframe, firstframe + self.nbuffer - 1)
        self.nframestracked = oldnframestracked
        if DEBUG_LEVEL > 0:
            print 'CropData: firstframe = %d, lastframe = %d, framestracked = [%d,%d], framesbuffered = [%d,%d], frameswritten = [%d,%d]' % (firstframe, lastframe, self.firstframetracked, self.lastframetracked, self.firstframebuffered, self.lastframebuffered, self.firstframewritten, self.lastframewritten)
        self.seek(firstframe, filep=cpfile, lookup=oldlookup, lookupinterval=oldlookupinterval, firstframetracked=oldfirstframetracked)
        self.idtable = {}
        for f in range(firstframe, lastframe + 1):
            if self.islookupframe(f):
                self.file.flush()
                self.lookup.append(self.file.tell())
                if DEBUG_LEVEL > 0:
                    print 'Adding frame %d (%x) to new lookup' % (f, self.lookup[(-1)])
            ells = self.read_ellipses(filein=cpfile)
            ells = self.ReplaceIds(ells)
            if DEBUG_LEVEL > 0 and self.islookupframe(f):
                print 'writing frame %d at %x: ' % (f, self.file.tell()) + str(ells)
            if f >= self.firstframebuffered and f <= self.lastframebuffered:
                self.buffer.append(ells)
            self.write_ellipses(ells)

        cpfile.close()
        self.nframestracked = self.lastframetracked - self.firstframetracked + 1
        self.isdatawritten = True
        if DEBUG_LEVEL > 0:
            print 'Finished cropping'
        self.file_lock.release()

    def seek(self, f, filep=None, lookup=None, lookupinterval=None, firstframetracked=None):
        release_lock = False
        if filep is None:
            filep = self.file
            self.file_lock.acquire()
            release_lock = True
        if lookup is None:
            lookup = self.lookup
        if lookupinterval is None:
            lookupinterval = self.lookupinterval
        if firstframetracked is None:
            firstframetracked = self.firstframetracked
        i, g = self.lookupfloor(f, lookupinterval, firstframetracked)
        if DEBUG_LEVEL > 0:
            print 'seek: lookup[%d] = %x + %d lines' % (i, lookup[i], f - g)
        filep.seek(lookup[i], 0)
        for h in range(g, f):
            tmp = filep.readline()

        if DEBUG_LEVEL > 0:
            print 'Frame %d at %x' % (f, filep.tell())
        if release_lock:
            self.file_lock.release()
        return

    def islookupframe(self, f, lookupinterval=None, firstframetracked=None):
        if lookupinterval is None:
            lookupinterval = self.lookupinterval
        if firstframetracked is None:
            firstframetracked = self.firstframetracked
        return 0 == (f - firstframetracked) % lookupinterval

    def get_frame(self, f):
        if f < self.firstframebuffered or f > self.lastframebuffered:
            self.file_lock.acquire()
            if DEBUG_LEVEL > 0:
                print 'get_frame: Need to read frame ' + str(f) + ' from file. buffered frames = [%d,%d], tracked frames = [%d,%d]' % (self.firstframebuffered, self.lastframebuffered, self.firstframetracked, self.lastframetracked)
            try:
                i = int(num.floor((f - self.firstframetracked) / self.lookupinterval))
            except OverflowError:
                print 'OverflowError diagnostics:', f, self.firstframetracked, self.lookupinterval
                raise

            if DEBUG_LEVEL > 0:
                print 'lookup element %d = %x' % (i, self.lookup[i])
            g = self.firstframetracked + self.lookupinterval * i
            self.firstframebuffered = max(g, f - self.nbuffer + 1)
            self.lastframebuffered = min(max(f, g + self.nbuffer - 1), self.lastframetracked)
            self.file.seek(self.lookup[i])
            for h in range(g, self.firstframebuffered):
                s = self.file.readline()

            self.buffer = []
            for h in range(self.firstframebuffered, self.lastframebuffered + 1):
                self.buffer.append(self.read_ellipses())

            self.file_lock.release()
        return self.buffer[(f - self.firstframebuffered)]

    def get_frames(self, f1, f2):
        with self.file_lock:
            ells = []
            for f in range(int(f1), int(f2) + 1):
                ells.append(self.get_frame(f))

            return ells

    def replace_frame(self, ellipses, t):
        with self.file_lock:
            if DEBUG_LEVEL > 0:
                print 'Replacing frame %d, frames tracked = [%d,%d], frames buffered = [%d,%d], frames written = [%d,%d]' % (t, self.firstframetracked, self.lastframetracked, self.firstframebuffered, self.lastframebuffered, self.firstframewritten, self.lastframewritten)
            bufferoff = t - self.firstframebuffered
            if DEBUG_LEVEL > 0:
                print 'bufferoff = ' + str(bufferoff)
            if t <= self.lastframewritten:
                print 'Replacing frame %d, frames written = [%d,%d]' % (t, self.firstframewritten, self.lastframewritten)
                print 'bufferoff %d, n %d' % (bufferoff, len(self.buffer))
                raise NotImplementedError('Cannot change a frame that is already written to disk')
            if bufferoff < 0 or bufferoff > len(self.buffer):
                print 'Replacing frame %d, frames tracked = [%d,%d], frames buffered = [%d,%d], frames written = [%d,%d]' % (t, self.firstframetracked, self.lastframetracked, self.firstframebuffered, self.lastframebuffered, self.firstframewritten, self.lastframewritten)
                print 'bufferoff %d, n %d' % (bufferoff, len(self.buffer))
                raise NotImplementedError('Buffer must contain frame to be changed')
            self.buffer[bufferoff] = ellipses

    def append(self, ellipses):
        self.add_frame(ellipses)

    def add_frame(self, ellipses):
        self.file_lock.acquire()
        if DEBUG_LEVEL > 1:
            print 'add_frame: %d, initially framestracked = [%d,%d], framesbuffered = [%d,%d], frameswritten = [%d,%d]' % (self.lastframetracked + 1, self.firstframetracked, self.lastframetracked, self.firstframebuffered, self.lastframebuffered, self.firstframewritten, self.lastframewritten)
        if len(self.buffer) > self.maxlookback:
            self.lastframewritten += 1
            if DEBUG_LEVEL > 1:
                print 'Writing to file. lastframewritten is now %d' % self.lastframewritten
            if self.islookupframe(self.lastframewritten):
                self.lookup.append(self.file.tell())
                if DEBUG_LEVEL > 0:
                    print 'Adding to lookup frame %d (%x)' % (self.lastframewritten, self.lookup[(-1)])
            if DEBUG_LEVEL > 1:
                print 'Writing frame %d at %x: ' % (self.lastframebuffered - self.maxlookback, self.file.tell()) + str(self.buffer[(len(self.buffer) - self.maxlookback)])
            self.write_ellipses(self.buffer[(len(self.buffer) - self.maxlookback - 1)])
        if len(self.buffer) >= self.nbuffer:
            tmp = self.buffer.pop(0)
            if DEBUG_LEVEL > 0:
                print 'popping frame %d from buffer: ' % self.firstframebuffered + str(tmp)
            self.firstframebuffered += 1
        self.buffer.append(ellipses)
        if DEBUG_LEVEL > 1:
            print 'after adding buffer length = %d' % len(self.buffer)
        self.lastframebuffered += 1
        self.lastframetracked += 1
        self.nframestracked += 1
        if DEBUG_LEVEL > 1:
            print 'Added to end of buffer[%d] (frame = %d), nflies = %d: ' % (len(self.buffer) - 1, self.lastframebuffered, len(ellipses)) + str(ellipses)
        if DEBUG_LEVEL > 1:
            print 'framestracked: [%d,%d], frameswritten: [%d,%d], framesbuffered: [%d,%d], nframestracked: %d, n: %d' % (self.firstframetracked, self.lastframetracked, self.firstframewritten, self.lastframewritten, self.firstframebuffered, self.lastframebuffered, self.nframestracked, len(self.buffer))
        self.isdatawritten = True
        self.file_lock.release()

    def __getitem__(self, i):
        if type(i) == IntType:
            if i < 0:
                j = self.lastframetracked + 1 + i
            else:
                j = self.firstframetracked + i
            return self.get_frame(j)
        if type(i) == SliceType:
            ind = i.indices(self.lastframetracked - self.firstframetracked)
            assert ind[2] == 1
            return self.get_frames(ind[0], ind[1])

    def __setitem__(self, i, val):
        if i < 0:
            j = self.lastframetracked + 1 + i
        else:
            j = self.firstframetracked + i
        if j == self.lastframetracked + 1:
            self.add_frame(val)
        elif j > self.lastframetracked:
            raise NotImplementedError('Trying to set frame %d, lastframetracked = %d') % (j, self.lastframetracked)
        else:
            self.replace_frame(val, j)

    def __len__(self):
        return self.nframestracked

    def finish_writing(self):
        if self.file.closed:
            return
        self.file_lock.acquire()
        if DEBUG_LEVEL > 0:
            print 'Finishing writing'
        self.file.flush()
        self.file.seek(0, 2)
        for f in range(self.lastframewritten + 1, self.lastframetracked + 1):
            if self.islookupframe(f):
                self.file.flush()
                self.lookup.append(self.file.tell())
            if DEBUG_LEVEL > 0:
                print 'Writing frame %d at %x: ' % (f, self.file.tell()) + str(self.buffer[(f - self.firstframebuffered)])
            if not self.file.closed:
                self.write_ellipses(self.buffer[(f - self.firstframebuffered)])

        self.lastframewritten = self.lastframetracked
        self.file.flush()
        self.file.truncate()
        self.isdatawritten = True
        self.file_lock.release()

    def copy_to_sbfmf(self):
        """Make a .sbfmf.ann copy of self.ann."""
        front, ext = os.path.splitext(self.filename)
        if ext != '.ann':
            print "not copying to .sbfmf.ann -- filename doesn't end with .ann."
            return
        moviename, ext = os.path.splitext(front)
        if ext not in known_extensions():
            print 'not copying to .sbfmf.ann -- movie filename extension %s is unknown.' % ext
            return
        sbfmf_moviename = moviename + '.sbfmf'
        if not os.path.isfile(sbfmf_moviename):
            print 'not copying to .sbfmf.ann -- SBFMF file %s does not exist.' % sbfmf_moviename
            return
        sbfmf_annname = sbfmf_moviename + '.ann'
        try:
            shutil.copy2(self.filename, sbfmf_annname)
        except:
            shutil.copyfile(self.filename, sbfmf_annname)

    def lookupfloor(self, f, lookupinterval=None, firstframetracked=None):
        if lookupinterval is None:
            lookupinterval = self.lookupinterval
        if firstframetracked is None:
            firstframetracked = self.firstframetracked
        i = int(num.floor((f - firstframetracked) / lookupinterval))
        g = firstframetracked + lookupinterval * i
        return (i, g)

    def IsAnnData(self):
        return self.lastframetracked >= self.firstframetracked

    def __del__(self):
        if hasattr(self, 'file') and self.file is not None and not self.file.closed:
            self.file.close()
        return

    def write_ellipses(self, ellipse_list, fileout=None):
        """Write one frame of data to already-open file."""
        release_lock = False
        if fileout is None:
            fileout = self.file
            release_lock = True
        string = self.write_ellipses_string(ellipse_list)
        if release_lock:
            self.file_lock.acquire()
        try:
            try:
                fileout.write('%s' % string)
            except IOError:
                print 'got an I/O error writing ellipses, trying again'
                try:
                    fileout.write('%s' % string)
                except IOError:
                    if params.interactive:
                        wx.MessageBox('I/O error writing annotation', 'Error', wx.ICON_ERROR)
                    raise

        finally:
            if release_lock:
                self.file_lock.release()

        return

    def write_ellipses_string(self, ellipse_list):
        """Write one frame of data to string."""
        s = ''
        for ellipse in ellipse_list.itervalues():
            s += '%f\t%f\t%f\t%f\t%f\t%d\t' % (ellipse.center.x,
             ellipse.center.y,
             ellipse.size.width,
             ellipse.size.height,
             ellipse.angle,
             ellipse.identity)

        s += '\n'
        return s

    def WriteAnnHeader(self, start_frame):
        """Write the header for an annotation file."""
        self.file_lock.acquire()
        SIZEOFDOUBLE = 8
        self.file.write('Ctrax header\n')
        self.file.write('version:%s\n' % self.version)
        if hasattr(self.bg_imgs, 'bg_type'):
            self.file.write('bg_type:%s\n' % self.bg_imgs.bg_type)
        self.file.write('n_bg_std_thresh:%.3f\n' % params.n_bg_std_thresh)
        self.file.write('n_bg_std_thresh_low:%.3f\n' % params.n_bg_std_thresh_low)
        self.file.write('bg_std_min:%.2f\n' % params.bg_std_min)
        self.file.write('bg_std_max:%.2f\n' % params.bg_std_max)
        if hasattr(self.bg_imgs, 'n_bg_frames'):
            self.file.write('n_bg_frames:%d\n' % self.bg_imgs.n_bg_frames)
        self.file.write('min_nonarena:%.1f\n' % params.min_nonarena)
        self.file.write('max_nonarena:%.1f\n' % params.max_nonarena)
        if params.arena_center_x is not None:
            self.file.write('arena_center_x:%.2f\n' % params.arena_center_x)
            self.file.write('arena_center_y:%.2f\n' % params.arena_center_y)
            self.file.write('arena_radius:%.2f\n' % params.arena_radius)
        self.file.write('min_arena_center_x:%.3f\n' % params.min_arena_center_x)
        self.file.write('max_arena_center_x:%.3f\n' % params.max_arena_center_x)
        self.file.write('min_arena_center_y:%.3f\n' % params.min_arena_center_y)
        self.file.write('max_arena_center_y:%.3f\n' % params.max_arena_center_y)
        self.file.write('min_arena_radius:%.3f\n' % params.min_arena_radius)
        self.file.write('max_arena_radius:%.3f\n' % params.max_arena_radius)
        self.file.write('do_set_circular_arena:%d\n' % params.do_set_circular_arena)
        self.file.write('do_use_morphology:%d\n' % params.do_use_morphology)
        self.file.write('opening_radius:%d\n' % params.opening_radius)
        self.file.write('closing_radius:%d\n' % params.closing_radius)
        if hasattr(self.bg_imgs, 'use_median'):
            self.file.write('bg_algorithm:')
            if self.bg_imgs.use_median:
                self.file.write('median\n')
            else:
                self.file.write('mean\n')
        if hasattr(self.bg_imgs, 'med'):
            sz = self.bg_imgs.med.size * SIZEOFDOUBLE
            self.file.write('background median:%d\n' % sz)
            self.file.write(self.bg_imgs.med.astype(num.float64))
        if hasattr(self.bg_imgs, 'mean'):
            sz = self.bg_imgs.mean.size * SIZEOFDOUBLE
            self.file.write('background mean:%d\n' % sz)
            self.file.write(self.bg_imgs.mean.astype(num.float64))
        if hasattr(self.bg_imgs, 'center'):
            sz = num.prod(self.bg_imgs.center.size) * SIZEOFDOUBLE
            self.file.write('background center:%d\n' % sz)
            self.file.write(self.bg_imgs.center.astype(num.float64))
        if hasattr(self.bg_imgs, 'mad'):
            sz = self.bg_imgs.mad.size * SIZEOFDOUBLE
            self.file.write('background mad:%d\n' % sz)
            self.file.write(self.bg_imgs.mad.astype(num.float64))
        if hasattr(self.bg_imgs, 'std'):
            sz = self.bg_imgs.std.size * SIZEOFDOUBLE
            self.file.write('background std:%d\n' % sz)
            self.file.write(self.bg_imgs.std.astype(num.float64))
        if hasattr(self.bg_imgs, 'dev'):
            sz = num.prod(self.bg_imgs.dev.size) * SIZEOFDOUBLE
            self.file.write('background dev:%d\n' % sz)
            self.file.write(self.bg_imgs.dev.astype(num.float64))
        if hasattr(self.bg_imgs, 'fracframesisback'):
            sz = num.prod(self.bg_imgs.fracframesisback.size) * SIZEOFDOUBLE
            self.file.write('fracframesisback:%d\n' % sz)
            self.file.write(self.bg_imgs.fracframesisback.astype(num.float64))
        if hasattr(self.bg_imgs, 'isarena'):
            sz = num.prod(self.bg_imgs.isarena.size) * SIZEOFDOUBLE
            self.file.write('isarena:%d\n' % sz)
            self.file.write(self.bg_imgs.isarena.astype(num.float64))
        if hasattr(self.bg_imgs, 'hfnorm'):
            sz = self.bg_imgs.hfnorm.size * SIZEOFDOUBLE
            self.file.write('hfnorm:%d\n' % sz)
            self.file.write(self.bg_imgs.hfnorm.astype(num.float64))
        if hasattr(params, 'movie_size'):
            self.file.write('movie_height:%d\n' % params.movie_size[0])
            self.file.write('movie_width:%d\n' % params.movie_size[1])
        if hasattr(params, 'roipolygons'):
            s = pickle.dumps(params.roipolygons)
            self.file.write('roipolygons:%d\n' % len(s))
            self.file.write(s)
        if hasattr(self.bg_imgs, 'norm_type'):
            self.file.write('bg_norm_type:%s\n' % self.bg_imgs.norm_type)
        self.file.write('hm_cutoff:%.2f\n' % params.hm_cutoff)
        self.file.write('hm_boost:%d\n' % params.hm_boost)
        self.file.write('hm_order:%d\n' % params.hm_order)
        self.file.write('maxarea:%.2f\n' % params.maxshape.area)
        self.file.write('maxmajor:%.2f\n' % params.maxshape.major)
        self.file.write('maxminor:%.2f\n' % params.maxshape.minor)
        self.file.write('maxecc:%.2f\n' % params.maxshape.ecc)
        self.file.write('minarea:%.2f\n' % params.minshape.area)
        self.file.write('minmajor:%.2f\n' % params.minshape.major)
        self.file.write('minminor:%.2f\n' % params.minshape.minor)
        self.file.write('minecc:%.2f\n' % params.minshape.ecc)
        self.file.write('meanarea:%.2f\n' % params.meanshape.area)
        self.file.write('meanmajor:%.2f\n' % params.meanshape.major)
        self.file.write('meanminor:%.2f\n' % params.meanshape.minor)
        self.file.write('meanecc:%.2f\n' % params.meanshape.ecc)
        self.file.write('nframes_size:%d\n' % params.n_frames_size)
        self.file.write('nstd_shape:%d\n' % params.n_std_thresh)
        self.file.write('max_jump:%.2f\n' % params.max_jump)
        self.file.write('max_jump_split:%.2f\n' % params.max_jump_split)
        self.file.write('min_jump:%.2f\n' % params.min_jump)
        self.file.write('ang_dist_wt:%.2f\n' % params.ang_dist_wt)
        self.file.write('center_dampen:%.2f\n' % params.dampen)
        self.file.write('angle_dampen:%.2f\n' % params.angle_dampen)
        if params.velocity_angle_weight is not None:
            self.file.write('velocity_angle_weight:%.2f\n' % params.velocity_angle_weight)
        if params.max_velocity_angle_weight is not None:
            self.file.write('max_velocity_angle_weight:%.2f\n' % params.max_velocity_angle_weight)
        self.file.write('minbackthresh:%.2f\n' % params.minbackthresh)
        self.file.write('maxclustersperblob:%d\n' % params.maxclustersperblob)
        self.file.write('maxpenaltymerge:%.2f\n' % params.maxpenaltymerge)
        self.file.write('maxareadelete:%.2f\n' % params.maxareadelete)
        self.file.write('minareaignore:%.2f\n' % params.minareaignore)
        self.file.write('max_n_clusters:%d\n' % params.max_n_clusters)
        self.file.write('do_fix_split:%d\n' % params.do_fix_split)
        self.file.write('splitdetection_length:%d\n' % params.splitdetection_length)
        self.file.write('splitdetection_cost:%.2f\n' % params.splitdetection_cost)
        self.file.write('do_fix_merged:%d\n' % params.do_fix_merged)
        self.file.write('mergeddetection_length:%d\n' % params.mergeddetection_length)
        self.file.write('mergeddetection_distance:%.2f\n' % params.mergeddetection_distance)
        self.file.write('do_fix_spurious:%d\n' % params.do_fix_spurious)
        self.file.write('spuriousdetection_length:%d\n' % params.spuriousdetection_length)
        self.file.write('do_fix_lost:%d\n' % params.do_fix_lost)
        self.file.write('lostdetection_length:%d\n' % params.lostdetection_length)
        self.file.write('lostdetection_distance:%d\n' % params.lostdetection_distance)
        if params.expbgfgmodel_filename is None:
            expbgfgmodel_filename = ''
        else:
            expbgfgmodel_filename = params.expbgfgmodel_filename
        self.file.write('expbgfgmodel_filename:%s\n' % expbgfgmodel_filename)
        self.file.write('use_expbgfgmodel:%d\n' % params.use_expbgfgmodel)
        self.file.write('expbgfgmodel_llr_thresh:%f\n' % params.expbgfgmodel_llr_thresh)
        self.file.write('expbgfgmodel_llr_thresh_low:%f\n' % params.expbgfgmodel_llr_thresh_low)
        self.file.write('min_frac_frames_isback:%f\n' % params.min_frac_frames_isback)
        if hasattr(params, 'expbgfgmodel_fill'):
            self.file.write('expbgfgmodel_fill:%s\n' % params.expbgfgmodel_fill)
        self.file.write('movie_name:' + params.movie_name + '\n')
        self.max_jump = params.max_jump
        if params.max_jump_split < 0:
            self.max_jump_split = self.max_jump
        else:
            self.max_jump_split = params.max_jump_split
        self.min_jump = params.min_jump
        self.file.write('start_frame:%d\n' % start_frame)
        self.file.write('orientations_chosen:%d\n' % self.orientations_chosen)
        self.file.write('data format:%s\n' % dataformatstring)
        self.file.write('end header\n')
        self.file.flush()
        self.endofheader = self.file.tell()
        self.file_lock.release()
        return

    def CheckAnnHeader(self):
        """Read header from an annotation file."""
        with self.file_lock:
            self.file.seek(0, 0)
            line = self.file.readline()
            if line == 'mtrax header\n':
                pass
            else:
                if line == 'Ctrax header\n':
                    pass
                else:
                    if line != '':
                        print 'line = >' + line + '<'
                    raise InvalidFileFormatException("Annotation file does not start with 'Ctrax header' or 'mtrax header'")
                i = 0
                while True:
                    line = self.file.readline()
                    if line == '':
                        raise InvalidFileFormatException("End of Annotation File reached; did not find 'end header'")
                    if line == 'end header\n':
                        self.start_data = self.file.tell()
                        break
                    words = line.split(':', 1)
                    if len(words) is not 2:
                        if len(line) > 1000:
                            print '(line shortened for printing)'
                            nline = line[:500] + line[-500:]
                        else:
                            nline = line
                        raise InvalidFileFormatException("More than one ':' in line >> " + nline)
                    parameter = words[0]
                    value = words[1]
                    if value[(-1)] == '\n':
                        value = value[:-1]
                    else:
                        if len(line) > 1000:
                            print '(line shortened for printing)'
                            nline = line[:500] + line[-500:]
                        else:
                            nline = line
                        raise InvalidFileFormatException('Line does not end in newline character. line >> ' + nline)
                    if len(value) == 0:
                        continue
                    if parameter == 'background median' or parameter == 'background mean' or parameter == 'background mad' or parameter == 'background std' or parameter == 'hfnorm' or parameter == 'roipolygons' or parameter == 'background center' or parameter == 'background dev' or parameter == 'fracframesisback' or parameter == 'isarena':
                        sz = int(value)
                        self.file.seek(sz, 1)
                    elif parameter == 'data format':
                        self.n_fields = len(value.split())
                    i += 1

    def get_bg_img(self, byte_size):
        """Read and reshape an image. Return None if error."""
        with self.file_lock:
            if self.bg_imgs is None:
                self.file.seek(byte_size, os.SEEK_CUR)
            else:
                try:
                    img = num.fromstring(self.file.read(byte_size), dtype=num.float64)
                    img.shape = params.movie_size
                except Exception as details:
                    print 'error getting image from ann-file:', details
                else:
                    return img

        return

    def ReadAnnHeader(self, doreadbgmodel=True, doreadstartframe=True):
        """Read header from an annotation file."""
        with self.file_lock:
            self.file.seek(0, 0)
            line = self.file.readline()
            if line == 'mtrax header\n' or line == 'Ctrax header\n':
                pass
            else:
                if line == '':
                    raise InvalidFileFormatException('Empty file (first line of header empty)')
                else:
                    print 'line = >' + line + '<'
                    raise InvalidFileFormatException("Annotation file does not start with 'Ctrax header' or 'mtrax header'")
                while True:
                    line = self.file.readline()
                    if line == '':
                        raise InvalidFileFormatException("End of Annotation File reached; did not find 'end header'")
                    if line == 'end header\n':
                        self.start_data = self.file.tell()
                        if DEBUG_LEVEL > 0:
                            print 'Found end of annotation header at %x' % self.start_data
                        break
                    words = line.split(':', 1)
                    if len(words) is not 2:
                        raise InvalidFileFormatException("More than one ':' in line >> " + line)
                    parameter = words[0]
                    value = words[1]
                    if value[(-1)] == '\n':
                        value = value[:-1]
                    else:
                        raise InvalidFileFormatException('Line does not end in newline character. line >> ' + line)
                    if len(value) == 0:
                        continue
                    if parameter == 'bg_type' and self.bg_imgs is not None:
                        try:
                            bgt = int(value)
                            if bgt == 0:
                                self.bg_imgs.bg_type = 'light_on_dark'
                            elif bgt == 1:
                                self.bg_imgs.bg_type = 'dark_on_light'
                            else:
                                self.bg_imgs.bg_type = 'other'
                            print "converted background type setting '%s' to Ctrax 0.2+ compatibility" % self.bg_imgs.bg_type
                        except ValueError:
                            if value != 'light_on_dark' and value != 'dark_on_light':
                                value = 'other'
                            self.bg_imgs.bg_type = value

                    elif parameter == 'n_bg_std_thresh':
                        params.n_bg_std_thresh = float(value)
                    elif parameter == 'n_bg_std_thresh_low':
                        params.n_bg_std_thresh_low = float(value)
                    elif parameter == 'bg_std_min':
                        params.bg_std_min = float(value)
                    elif parameter == 'bg_std_max':
                        params.bg_std_max = float(value)
                    elif parameter == 'n_bg_frames' and self.bg_imgs is not None:
                        self.bg_imgs.n_bg_frames = int(value)
                    elif parameter == 'min_nonarena':
                        params.min_nonarena = float(value)
                    elif parameter == 'max_nonarena':
                        params.max_nonarena = float(value)
                    elif parameter == 'arena_center_x':
                        params.arena_center_x = float(value)
                    elif parameter == 'arena_center_y':
                        params.arena_center_y = float(value)
                    elif parameter == 'arena_radius':
                        params.arena_radius = float(value)
                    elif parameter == 'min_arena_center_x':
                        params.min_arena_center_x = float(value)
                    elif parameter == 'min_arena_center_y':
                        params.min_arena_center_y = float(value)
                    elif parameter == 'min_arena_radius':
                        params.min_arena_radius = float(value)
                    elif parameter == 'max_arena_center_x':
                        params.max_arena_center_x = float(value)
                    elif parameter == 'max_arena_center_y':
                        params.max_arena_center_y = float(value)
                    elif parameter == 'max_arena_radius':
                        params.max_arena_radius = float(value)
                    elif parameter == 'do_set_circular_arena':
                        params.do_set_circular_arena = bool(int(value))
                    elif parameter == 'do_use_morphology':
                        params.do_use_morphology = bool(int(value))
                    elif parameter == 'opening_radius':
                        params.opening_radius = int(value)
                        if self.bg_imgs is not None:
                            self.bg_imgs.opening_struct = self.bg_imgs.create_morph_struct(params.opening_radius)
                    elif parameter == 'closing_radius':
                        params.closing_radius = int(value)
                        if self.bg_imgs is not None:
                            self.bg_imgs.closing_struct = self.bg_imgs.create_morph_struct(params.closing_radius)
                    elif parameter == 'bg_algorithm' and self.bg_imgs is not None:
                        if value == 'median':
                            self.bg_imgs.use_median = True
                        else:
                            self.bg_imgs.use_median = False
                    elif parameter == 'background median':
                        img = self.get_bg_img(int(value))
                        if doreadbgmodel and img is not None:
                            self.bg_imgs.med = img
                    elif parameter == 'background mean':
                        img = self.get_bg_img(int(value))
                        if doreadbgmodel and img is not None:
                            self.bg_imgs.mean = img
                    elif parameter == 'background center':
                        img = self.get_bg_img(int(value))
                        if doreadbgmodel and img is not None:
                            self.bg_imgs.center = img
                    elif parameter == 'bg_norm_type' and self.bg_imgs is not None:
                        try:
                            bgnt = int(value)
                            if bgnt == 2:
                                self.bg_imgs.norm_type = 'homomorphic'
                            elif bgnt == 1:
                                self.bg_imgs.norm_type = 'intensity'
                            else:
                                self.bg_imgs.norm_type = 'std'
                            print 'converted background normalization setting to Ctrax 0.2+ compatibility'
                        except ValueError:
                            if value != 'homomorphic' and value != 'intensity':
                                value = 'std'
                            self.bg_imgs.norm_type = value

                    elif parameter == 'background mad':
                        img = self.get_bg_img(int(value))
                        if doreadbgmodel and img is not None:
                            self.bg_imgs.mad = img
                    elif parameter == 'background std':
                        img = self.get_bg_img(int(value))
                        if doreadbgmodel and img is not None:
                            self.bg_imgs.std = img
                    elif parameter == 'background dev':
                        img = self.get_bg_img(int(value))
                        if doreadbgmodel and img is not None:
                            self.bg_imgs.dev = img
                    elif parameter == 'fracframesisback':
                        img = self.get_bg_img(int(value))
                        if doreadbgmodel and img is not None:
                            self.bg_imgs.fracframesisback = img
                    elif parameter == 'isarena':
                        img = self.get_bg_img(int(value))
                        if doreadbgmodel and img is not None:
                            self.bg_imgs.isarena = img.astype(bool)
                    elif parameter == 'hfnorm':
                        img = self.get_bg_img(int(value))
                        if doreadbgmodel and img is not None:
                            self.bg_imgs.hfnorm = img
                    elif parameter == 'roipolygons':
                        sz = int(value)
                        if doreadbgmodel:
                            params.roipolygons = pickle.loads(self.file.read(sz))
                        else:
                            self.file.seek(sz, 1)
                    elif parameter == 'hm_cutoff':
                        params.hm_cutoff = float(value)
                    elif parameter == 'hm_boost':
                        params.hm_boost = int(value)
                    elif parameter == 'hm_order':
                        params.hm_order = int(value)
                    elif parameter == 'maxarea':
                        params.maxshape.area = float(value)
                    elif parameter == 'maxmajor':
                        params.maxshape.major = float(value)
                    elif parameter == 'maxminor':
                        params.maxshape.minor = float(value)
                    elif parameter == 'maxecc':
                        params.maxshape.ecc = float(value)
                    elif parameter == 'minarea':
                        params.minshape.area = float(value)
                    elif parameter == 'minmajor':
                        params.minshape.major = float(value)
                    elif parameter == 'minminor':
                        params.minshape.minor = float(value)
                    elif parameter == 'minecc':
                        params.minshape.ecc = float(value)
                    elif parameter == 'meanarea':
                        params.meanshape.area = float(value)
                    elif parameter == 'meanmajor':
                        params.meanshape.major = float(value)
                    elif parameter == 'meanminor':
                        params.meanshape.minor = float(value)
                    elif parameter == 'meanecc':
                        params.meanshape.ecc = float(value)
                    elif parameter == 'nframes_size':
                        params.n_frames_size = int(value)
                    elif parameter == 'nstd_shape':
                        params.n_std_thresh = float(value)
                    elif parameter == 'max_jump':
                        params.max_jump = float(value)
                        self.max_jump = params.max_jump
                    elif parameter == 'max_jump_split':
                        params.max_jump_split = float(value)
                        self.max_jump_split = params.max_jump_split
                    elif parameter == 'min_jump':
                        params.min_jump = float(value)
                        self.min_jump = params.min_jump
                    elif parameter == 'orientations_chosen':
                        self.orientations_chosen = bool(int(value))
                    elif parameter == 'ang_dist_wt':
                        params.ang_dist_wt = float(value)
                    elif parameter == 'center_dampen':
                        params.dampen = float(value)
                    elif parameter == 'angle_dampen':
                        params.angle_dampen = float(value)
                    elif parameter == 'velocity_angle_weight':
                        params.velocity_angle_weight = float(value)
                    elif parameter == 'max_velocity_angle_weight':
                        params.max_velocity_angle_weight = float(value)
                    elif parameter == 'minbackthresh':
                        params.minbackthresh = float(value)
                    elif parameter == 'maxclustersperblob':
                        params.maxclustersperblob = int(value)
                    elif parameter == 'maxpenaltymerge':
                        params.maxpenaltymerge = float(value)
                    elif parameter == 'maxareadelete':
                        params.maxareadelete = float(value)
                    elif parameter == 'minareaignore':
                        params.minareaignore = float(value)
                    elif parameter == 'max_n_clusters':
                        params.max_n_clusters = int(value)
                    elif parameter == 'do_fix_split':
                        params.do_fix_split = bool(int(value))
                    elif parameter == 'splitdetection_length':
                        params.splitdetection_length = int(value)
                    elif parameter == 'splitdetection_cost':
                        params.splitdetection_cost = float(value)
                    elif parameter == 'do_fix_merged':
                        params.do_fix_merged = bool(int(value))
                    elif parameter == 'mergeddetection_length':
                        params.mergeddetection_length = int(value)
                    elif parameter == 'mergeddetection_distance':
                        params.mergeddetection_distance = float(value)
                    elif parameter == 'do_fix_spurious':
                        params.do_fix_spurious = bool(int(value))
                    elif parameter == 'spuriousdetection_length':
                        params.spuriousdetection_length = int(value)
                    elif parameter == 'do_fix_lost':
                        params.do_fix_lost = bool(int(value))
                    elif parameter == 'lostdetection_length':
                        params.lostdetection_length = int(value)
                    elif parameter == 'lostdetection_distance':
                        params.lostdetection_distance = int(value)
                    elif parameter == 'expbgfgmodel_filename':
                        if value == '':
                            params.expbgfgmodel_filename = None
                        else:
                            params.expbgfgmodel_filename = value
                            if self.bg_imgs is not None:
                                self.bg_imgs.setExpBGFGModel(params.expbgfgmodel_filename)
                    elif parameter == 'use_expbgfgmodel':
                        params.use_expbgfgmodel = bool(int(value))
                    elif parameter == 'expbgfgmodel_llr_thresh':
                        params.expbgfgmodel_llr_thresh = float(value)
                    elif parameter == 'expbgfgmodel_llr_thresh_low':
                        params.expbgfgmodel_llr_thresh_low = float(value)
                    elif parameter == 'expbgfgmodel_fill':
                        params.expbgfgmodel_fill = value
                    elif parameter == 'min_frac_frames_isback':
                        params.min_frac_frames_isback = float(value)
                    elif parameter == 'start_frame':
                        if doreadstartframe:
                            params.start_frame = int(value)
                    elif parameter == 'data format':
                        self.n_fields = len(value.split())

            if doreadbgmodel and self.bg_imgs is not None:
                self.bg_imgs.updateParameters()
            if params.max_jump_split < 0 and params.max_jump > 0:
                params.max_jump_split = params.max_jump
                self.max_jump_split = self.max_jump
        return

    def ReadSettings(self):
        """Read header from an annotation file."""
        self.ReadAnnHeader(doreadbgmodel=False, doreadstartframe=False)

    def ReplaceIds(self, ells):
        new_ells = ell.TargetList()
        for i, e in ells.iteritems():
            if i not in self.idtable:
                if DEBUG_LEVEL > 0:
                    print 'identity %d is not in idtable: ' % i + str(self.idtable)
                self.idtable[i] = params.nids
                params.nids += 1
                if DEBUG_LEVEL > 0:
                    print 'incrementing params.nids to %d' % params.nids
            e.identity = self.idtable[i]
            new_ells.append(e)

        return new_ells

    def CountIds(self, ells):
        for i, e in ells.iteritems():
            if i not in self.idtable:
                if DEBUG_LEVEL > 0:
                    print 'identity %d is not in idtable: ' % i + str(self.idtable)
                self.idtable[i] = params.nids
                params.nids += 1
                if DEBUG_LEVEL > 0:
                    print 'incrementing params.nids to %d' % params.nids

    def ParseData(self, line, doreplaceids=False):
        """Split a line of annotation data into per-fly information.
        Returns an EllipseList. Allows passing in an EllipseList, which is
        overwritten and returned, to avoid memory reallocation."""
        fly_sep = line.split()
        if len(fly_sep) % self.n_fields > 0:
            print 'Error reading trajectories from annotation file. '
            print 'line = %s' % line
            print 'parsed as ' + str(fly_sep)
            raise Exception, 'Error reading trajectories from annotation file'
        ellipses = ell.TargetList()
        for ff in range(len(fly_sep) / self.n_fields):
            try:
                new_ellipse = ell.Ellipse(centerX=float(fly_sep[(self.n_fields * ff)]), centerY=float(fly_sep[(self.n_fields * ff + 1)]), sizeW=float(fly_sep[(self.n_fields * ff + 2)]), sizeH=float(fly_sep[(self.n_fields * ff + 3)]), angle=float(fly_sep[(self.n_fields * ff + 4)]), identity=int(fly_sep[(self.n_fields * ff + 5)]))
            except ValueError:
                msgtxt = 'Could not read ellipse %d, skipping' % ff
                print msgtxt
                new_ellipse = ell.Ellipse(centerX=0, centerY=0, sizeW=1, sizeH=1, angle=0, identity=int(fly_sep[(self.n_fields * ff + 5)]))

            ellipses.append(new_ellipse)

        return ellipses

    def read_ellipses_string(self, s):
        return self.ParseData(s)

    def read_ellipses(self, filein=None):
        if filein is None:
            filein = self.file
        return self.ParseData(filein.readline())

    def WriteMAT(self, filename):
        """Writes data to a MATLAB .mat file."""
        nframes = self.lastframetracked - self.firstframetracked + 1
        startframe = self.firstframetracked
        ntargets = num.ones(nframes)
        if self.nbuffer < nframes:
            msgtxt = 'Saving numeric output require loading all %d frames of tracked data into memory, which may require a prohibitive amount of RAM.' % nframes
            if params.feedback_enabled:
                a = wx.MessageBox(msgtxt + 'Proceed?', 'Store to file?', wx.YES | wx.NO)
                if a == wx.NO:
                    return
                wx.Yield()
            else:
                print msgtxt
        off = self.firstframetracked
        for i in range(nframes):
            ntargets[i] = len(self.get_frame(off + i))

        z = num.sum(ntargets)
        x_pos = num.ones(z) * num.nan
        y_pos = num.ones(z) * num.nan
        maj_ax = num.ones(z) * num.nan
        min_ax = num.ones(z) * num.nan
        angle = num.ones(z) * num.nan
        identity = num.ones(z) * num.nan
        i = 0
        for j in range(nframes):
            ells = self.get_frame(off + j)
            for ee in ells.itervalues():
                if num.isnan(ee.center.x):
                    x_pos[i] = num.inf
                else:
                    x_pos[i] = ee.center.x
                if num.isnan(ee.center.y):
                    y_pos[i] = num.inf
                else:
                    y_pos[i] = ee.center.y
                maj_ax[i] = ee.height
                min_ax[i] = ee.width
                angle[i] = ee.angle
                identity[i] = ee.identity
                i += 1

        save_dict = {'x_pos': x_pos, 'y_pos': y_pos, 
           'maj_ax': maj_ax, 
           'min_ax': min_ax, 
           'angle': angle, 
           'identity': identity, 
           'ntargets': ntargets, 
           'startframe': startframe}
        if DEBUG_LEVEL > 0:
            print 'reading in movie to save stamps'
        stamps = params.movie.get_some_timestamps(t1=startframe, t2=startframe + nframes)
        save_dict['timestamps'] = stamps
        savemat(filename, save_dict, oned_as='column')

    def WriteCSV(self, filename):
        """Write comma-separated values to a .csv file."""
        nframes = self.lastframetracked - self.firstframetracked + 1
        off = self.firstframetracked
        max_id = 0
        for fr in range(nframes):
            ells = self.get_frame(off + fr)
            for ee in ells.itervalues():
                max_id = max(max_id, ee.identity)

        print 'max ID', max_id
        arr = num.zeros((nframes, (max_id + 1) * 6)) - 1.0
        for fr in range(nframes):
            ells = self.get_frame(off + fr)
            for ee in ells.itervalues():
                i = ee.identity
                arr[(fr, i * 6)] = ee.identity
                arr[(fr, i * 6 + 1)] = ee.center.x
                arr[(fr, i * 6 + 2)] = ee.center.y
                arr[(fr, i * 6 + 3)] = ee.height
                arr[(fr, i * 6 + 4)] = ee.width
                arr[(fr, i * 6 + 5)] = ee.angle

        num.savetxt(filename, arr, delimiter=',')

    def tell(self):
        return self.file.tell()

    def get_frame_prev(self):
        with self.file_lock:
            return self.get_frame(self.lastframetracked - 1)

    def get_frame_prevprev(self):
        with self.file_lock:
            return self.get_frame(self.lastframetracked - 2)

    def GetNewId(self):
        """Get next available ID, or the top recycled ID if available."""
        if len(self.recycledids) > 0:
            newid = self.recycledids.pop()
        else:
            newid = params.nids
            params.nids += 1
        return newid

    def RecycleId(self, id):
        """Allow an ID to be recycled."""
        self.recycledids.append(id)

    def rename_file(self, newfilename=None):
        self.file_lock.acquire()
        oldfile = self.file
        oldfilename = self.filename
        if newfilename is None:
            self.file = tempfile.NamedTemporaryFile(suffix='.ann')
            self.filename = self.file.name
        else:
            self.filename = newfilename
            self.file = open(self.filename, 'wb+')
        if DEBUG_LEVEL > 0:
            print 'rename_file: created new file %s' % self.filename
        oldfile.seek(0, 0)
        shutil.copyfileobj(oldfile, self.file)
        oldfile.close()
        self.file_lock.release()
        return

    def close(self):
        if hasattr(self, 'file'):
            try:
                self.file.close()
            except:
                print 'could not close annotation file'


def LoadSettings(filename, bg_imgs, doreadbgmodel=False):
    tmpannfile = AnnotationFile(filename, bg_imgs, justreadheader=True, doreadbgmodel=doreadbgmodel)


def WriteDiagnostics(filename):
    file = open(filename, 'w')
    for name, value in diagnostics.iteritems():
        file.write('%s,%s\n' % (name, value))

    file.close()