# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\libs\video.py
# Compiled at: 2012-05-17 11:54:26
"""
"Define all types necessary for interfacing with avisynth.dll
 Moved from internal.h *"

   Copia del avisynth .h
   mas que nada por compatibilidad con los parámetros que se le pasen a la inicialización
         y tiene algunas funciones extras para trabajar con video
   """
import math

class cVideoInfo:
    """
        #Contiene la información del video propiamente dicho
        width=640 # width=0 means no video; ancho
        height=480 #alto
        num_frames=0 #cantidad total de cuadros (corresponde a avisynth)
        fps_numerator=1 #numerador del FPS
        fps_denominator=1 #denominador del FPS
        fps=1 #Fps en float
        fpscof1 = 1 #fpscof1 = fps /1000.0 #coeficientes precalculados para el calculo de milisegundos y frames
        fpscof2 = 1 #fpscof2 = 1000.0 / fps
        fake_stride = 0 #un stride precalculado para cuando se necesite hacer width*4
        """
    width = 640
    height = 480
    num_frames = 0
    fps = 30.0
    fpscof1 = 30.0 / 1000.0
    fpscof2 = 1000.0 / 30.0
    fake_stride = 0

    def MSToFrame(self, ms):
        """Convierte de milisegundos a pnumero de cuadro"""
        return int(math.ceil(ms * self.fpscof1))

    def FrameToMS(self, frame):
        """Convierte de numero de cuadro a milisegundos"""
        return frame * self.vi.fpscof2

    def ClampFrameNum(self, frame):
        u"""Recorta un número (entero) al rango entre 0 y el máximo numero de frames (+ o - 1)"""
        if frame < 0:
            return 0
        if frame > self.num_frames:
            return self.num_frames
        return frame

    def HasVideo(self):
        return self.width != 0


class cCurrentFrame:
    """
        Contiene información del cuadro actual
        ctx = contexto de cairo global
        sfc = surface de cairo global
        framen = numero de cuadro actual
        """
    ctx = None
    framen = -1


cf = cCurrentFrame()
vi = cVideoInfo()
SAMPLE_INT8 = 1
SAMPLE_INT16 = 2
SAMPLE_INT24 = 4
SAMPLE_INT32 = 8
SAMPLE_FLOAT = 16
PLANAR_Y = 1
PLANAR_U = 2
PLANAR_V = 4
PLANAR_ALIGNED = 8
PLANAR_Y_ALIGNED = 9
PLANAR_U_ALIGNED = 10
PLANAR_V_ALIGNED = 12
CS_BGR = 268435456
CS_YUV = 536870912
CS_INTERLEAVED = 1073741824
CS_PLANAR = 2147483648
CS_UNKNOWN = 0
CS_BGR24 = 1 | CS_BGR | CS_INTERLEAVED
CS_BGR32 = 2 | CS_BGR | CS_INTERLEAVED
CS_YUY2 = 4 | CS_YUV | CS_INTERLEAVED
CS_YV12 = 8 | CS_YUV | CS_PLANAR
CS_I420 = 16 | CS_YUV | CS_PLANAR
CS_IYUV = 16 | CS_YUV | CS_PLANAR
pixel_type = 0
audio_samples_per_second = 0
sample_type = 0
num_audio_samples = 0
nchannels = 0
image_type = 0
IT_BFF = 1
IT_TFF = 2
IT_FIELDBASED = 4

def Check(var, type):
    return var & type == type


def GetMode(ptype):
    """Dado un modo de avisynth, devuelve el modo para cairo.
        actualmente implementado RGB24 y ARGB32
        """
    import cairo
    if Check(ptype, CS_BGR24):
        return cairo.FORMAT_RGB24
    if Check(ptype, CS_BGR32):
        return cairo.FORMAT_ARGB32
    return cairo.FORMAT_ARGB32


def BytesFromPixels(pixels, ptype):
    return pixels * BytesPerPixel(ptype)


def BytesPerPixel(ptype):
    if ptype == CS_BGR24:
        return 3
    if ptype == CS_BGR32:
        return 4
    if ptype == CS_YUY2:
        return 2
    if ptype == CS_YV12 or ptype == CS_I420:
        return 1.5
    return 0