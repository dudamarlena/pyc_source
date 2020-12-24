# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dev\pylib\visvis\vvmovie\images2avi.py
# Compiled at: 2016-03-22 04:56:47
# Size of source mod 2**32: 5685 bytes
""" Module images2avi

Uses ffmpeg to read and write AVI files. Requires PIL

I found these sites usefull:
http://www.catswhocode.com/blog/19-ffmpeg-commands-for-all-needs
http://linux.die.net/man/1/ffmpeg

"""
import os, time, subprocess, shutil
from visvis.vvmovie import images2ims

def _cleanDir(tempDir):
    for i in range(3):
        try:
            shutil.rmtree(tempDir)
        except Exception:
            time.sleep(0.2)
        else:
            break
    else:
        print('Oops, could not fully clean up temporary files.')


def writeAvi(filename, images, duration=0.1, encoding='mpeg4', inputOptions='', outputOptions=''):
    """ writeAvi(filename, duration=0.1, encoding='mpeg4',
                    inputOptions='', outputOptions='')
    
    Export movie to a AVI file, which is encoded with the given 
    encoding. Hint for Windows users: the 'msmpeg4v2' codec is 
    natively supported on Windows.
    
    Images should be a list consisting of PIL images or numpy arrays. 
    The latter should be between 0 and 255 for integer types, and 
    between 0 and 1 for float types.
    
    Requires the "ffmpeg" application:
      * Most linux users can install using their package manager
      * There is a windows installer on the visvis website
    
    """
    try:
        fps = float(1.0 / duration)
    except Exception:
        raise ValueError('Invalid duration parameter for writeAvi.')

    tempDir = os.path.join(os.path.expanduser('~'), '.tempIms')
    images2ims.writeIms(os.path.join(tempDir, 'im*.jpg'), images)
    N = len(images)
    formatter = '%04d'
    if N < 10:
        formatter = '%d'
    else:
        if N < 100:
            formatter = '%02d'
        else:
            if N < 1000:
                formatter = '%03d'
        command = 'ffmpeg -r %i %s ' % (int(fps), inputOptions)
        command += '-i im%s.jpg ' % (formatter,)
        command += '-g 1 -vcodec %s %s ' % (encoding, outputOptions)
        command += 'output.avi'
        S = subprocess.Popen(command, shell=True, cwd=tempDir, stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        outPut = S.stdout.read()
        if S.wait():
            print(outPut)
            print(S.stderr.read())
            _cleanDir(tempDir)
            raise RuntimeError('Could not write avi.')
        else:
            shutil.copy(os.path.join(tempDir, 'output.avi'), filename)
            _cleanDir(tempDir)


def readAvi(filename, asNumpy=True):
    """ readAvi(filename, asNumpy=True)
    
    Read images from an AVI (or MPG) movie.
    
    Requires the "ffmpeg" application:
      * Most linux users can install using their package manager
      * There is a windows installer on the visvis website
    
    """
    if not os.path.isfile(filename):
        raise IOError('File not found: ' + str(filename))
    else:
        tempDir = os.path.join(os.path.expanduser('~'), '.tempIms')
        if not os.path.isdir(tempDir):
            os.makedirs(tempDir)
        shutil.copy(filename, os.path.join(tempDir, 'input.avi'))
        command = 'ffmpeg -i input.avi im%d.jpg'
        S = subprocess.Popen(command, shell=True, cwd=tempDir, stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        outPut = S.stdout.read()
        if S.wait():
            print(outPut)
            print(S.stderr.read())
            _cleanDir(tempDir)
            raise RuntimeError('Could not read avi.')
        else:
            images = images2ims.readIms(os.path.join(tempDir, 'im*.jpg'), asNumpy)
            _cleanDir(tempDir)
    return images