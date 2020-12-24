# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\additional_api.py
# Compiled at: 2020-04-18 05:35:37
# Size of source mod 2**32: 16652 bytes
import ctypes as ct
from reapy import reascript_api as RPR
from reapy.reascript_api import _RPR

def packs_l(v: str, encoding='latin-1') -> ct.c_char_p:
    MAX_STRBUF = 4194304
    return ct.create_string_buffer(str(v).encode(encoding), MAX_STRBUF)


def unpacks_l(v):
    return str(v.value.decode('latin-1'))


def MIDI_GetEvt(take, evtidx, selectedOut, mutedOut, ppqposOut, msg, msg_sz):
    a = _RPR._ft['MIDI_GetEvt']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_char_p, ct.c_void_p)(a)
    t = (
     _RPR.rpr_packp('MediaItem_Take*', take), ct.c_int(evtidx),
     ct.c_byte(selectedOut), ct.c_byte(mutedOut), ct.c_double(ppqposOut),
     packs_l(msg), ct.c_int(msg_sz))
    r = f(t[0], t[1], ct.byref(t[2]), ct.byref(t[3]), ct.byref(t[4]), t[5], ct.byref(t[6]))
    return (
     r, take, evtidx, int(t[2].value), int(t[3].value), float(t[4].value),
     unpacks_l(t[5]), int(t[6].value))


def MIDI_GetHash(p0, p1, p2, p3):
    a = _RPR._ft['MIDI_GetHash']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_byte, ct.c_char_p, ct.c_int)(a)
    t = (
     _RPR.rpr_packp('MediaItem_Take*', p0), ct.c_byte(p1), packs_l(p2), ct.c_int(p3))
    r = f(t[0], t[1], t[2], t[3])
    return (r, p0, p1, unpacks_l(t[2]), p3)


def MIDI_GetTrackHash(p0, p1, p2, p3):
    a = _RPR._ft['MIDI_GetTrackHash']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_byte, ct.c_char_p, ct.c_int)(a)
    t = (_RPR.rpr_packp('MediaTrack*', p0),
     ct.c_byte(p1), packs_l(p2), ct.c_int(p3))
    r = f(t[0], t[1], t[2], t[3])
    return (r, p0, p1, unpacks_l(t[2]), p3)


def MIDI_InsertEvt(take, selected, muted, ppqpos, bytestr, bytestr_sz):
    a = _RPR._ft['MIDI_InsertEvt']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_byte, ct.c_byte, ct.c_double, ct.c_char_p, ct.c_int)(a)
    t = (
     _RPR.rpr_packp('MediaItem_Take*', take),
     ct.c_byte(selected),
     ct.c_byte(muted),
     ct.c_double(ppqpos),
     packs_l(bytestr),
     ct.c_int(bytestr_sz))
    r = f(t[0], t[1], t[2], t[3], t[4], t[5])
    return r


def MIDI_InsertTextSysexEvt(take, selected, muted, ppqpos, type_, bytestr, bytestr_sz):
    a = _RPR._ft['MIDI_InsertTextSysexEvt']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_byte, ct.c_byte, ct.c_double, ct.c_int, ct.c_char_p, ct.c_int)(a)
    t = (
     _RPR.rpr_packp('MediaItem_Take*', take),
     ct.c_byte(selected),
     ct.c_byte(muted),
     ct.c_double(ppqpos),
     ct.c_int(type_),
     packs_l(bytestr),
     ct.c_int(bytestr_sz))
    r = f(t[0], t[1], t[2], t[3], t[4], t[5], t[6])
    return r


def MIDI_SetEvt(p0, p1, p2, p3, p4, p5, p6, p7):
    a = _RPR._ft['MIDI_SetEvt']
    f = ct.CFUNCTYPE(ct.c_byte, ct.c_uint64, ct.c_int, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_char_p, ct.c_int, ct.c_void_p)(a)
    t = (
     _RPR.rpr_packp('MediaItem_Take*', p0), ct.c_int(p1), ct.c_byte(p2), ct.c_byte(p3),
     ct.c_double(p4), packs_l(p5), ct.c_int(p6), ct.c_byte(p7))
    r = f(t[0], t[1], ct.byref(t[2]), ct.byref(t[3]), ct.byref(t[4]), t[5], t[6], ct.byref(t[7]))
    return (
     r, p0, p1, int(t[2].value), int(t[3].value), float(t[4].value), p5, p6,
     int(t[7].value))