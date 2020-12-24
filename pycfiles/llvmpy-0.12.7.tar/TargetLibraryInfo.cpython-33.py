# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/Target/TargetLibraryInfo.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 3006 bytes
from binding import *
from ..namespace import llvm
from src.Pass import ImmutablePass
TargetLibraryInfo = llvm.Class(ImmutablePass)
LibFunc = llvm.Namespace('LibFunc')
LibFunc.Enum('Func', '\n                ZdaPv, ZdlPv, Znaj, ZnajRKSt9nothrow_t,\n                Znam, ZnamRKSt9nothrow_t, Znwj, ZnwjRKSt9nothrow_t,\n                Znwm, ZnwmRKSt9nothrow_t, cxa_atexit, cxa_guard_abort,\n                cxa_guard_acquire, cxa_guard_release, memcpy_chk,\n                acos, acosf, acosh, acoshf,\n                acoshl, acosl, asin, asinf,\n                asinh, asinhf, asinhl, asinl,\n                atan, atan2, atan2f, atan2l,\n                atanf, atanh, atanhf, atanhl,\n                atanl, calloc, cbrt, cbrtf,\n                cbrtl, ceil, ceilf, ceill,\n                copysign, copysignf, copysignl, cos,\n                cosf, cosh, coshf, coshl,\n                cosl, exp, exp10, exp10f,\n                exp10l, exp2, exp2f, exp2l,\n                expf, expl, expm1, expm1f,\n                expm1l, fabs, fabsf, fabsl,\n                fiprintf,\n                floor, floorf, floorl, fmod,\n                fmodf, fmodl, fputc,\n                fputs, free, fwrite, iprintf,\n                log, log10, log10f, log10l,\n                log1p, log1pf, log1pl, log2,\n                log2f, log2l, logb, logbf,\n                logbl, logf, logl, malloc,\n                memchr, memcmp, memcpy, memmove,\n                memset, memset_pattern16, nearbyint, nearbyintf,\n                nearbyintl, posix_memalign, pow, powf,\n                powl, putchar, puts,\n                realloc, reallocf, rint, rintf,\n                rintl, round, roundf, roundl,\n                sin, sinf, sinh, sinhf,\n                sinhl, sinl, siprintf,\n                sqrt, sqrtf, sqrtl, stpcpy,\n                strcat, strchr, strcmp, strcpy,\n                strcspn, strdup, strlen, strncat,\n                strncmp, strncpy, strndup, strnlen,\n                strpbrk, strrchr, strspn, strstr,\n                strtod, strtof, strtol, strtold,\n                strtoll, strtoul, strtoull, tan,\n                tanf, tanh, tanhf, tanhl,\n                tanl, trunc, truncf,\n                truncl, valloc, NumLibFuncs')
from src.ADT.Triple import Triple
from src.ADT.StringRef import StringRef

@TargetLibraryInfo
class TargetLibraryInfo:
    _include_ = 'llvm/Target/TargetLibraryInfo.h'
    new = Constructor()
    new |= Constructor(ref(Triple))
    delete = Destructor()
    has = Method(cast(bool, Bool), LibFunc.Func)
    hasOptimizedCodeGen = Method(cast(bool, Bool), LibFunc.Func)
    getName = Method(cast(str, StringRef), LibFunc.Func)
    setUnavailable = Method(Void, LibFunc.Func)
    setAvailable = Method(Void, LibFunc.Func)
    setAvailableWithName = Method(Void, LibFunc.Func, cast(str, StringRef))
    disableAllFunctions = Method()