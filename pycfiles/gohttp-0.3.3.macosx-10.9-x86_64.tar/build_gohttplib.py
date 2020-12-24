# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/gohttp/build_gohttplib.py
# Compiled at: 2016-05-20 22:32:02
from cffi import FFI
ffi = FFI()
ffi.set_source('gohttp._gohttplib', None)
ffi.cdef('\ntypedef struct Request_\n{\n    const char *Method;\n    const char *Host;\n    const char *URL;\n} Request;\n\ntypedef unsigned int ResponseWriterPtr;\n\ntypedef void FuncPtr(ResponseWriterPtr w, Request *r);\n\nvoid Call_HandleFunc(ResponseWriterPtr w, Request *r, FuncPtr *fn);\n\nvoid ListenAndServe(char* p0);\n\nvoid HandleFunc(char* p0, FuncPtr* p1);\n\nint ResponseWriter_Write(unsigned int p0, char* p1, int p2);\n\nvoid ResponseWriter_WriteHeader(unsigned int p0, int p1);\n')
if __name__ == '__main__':
    ffi.compile()