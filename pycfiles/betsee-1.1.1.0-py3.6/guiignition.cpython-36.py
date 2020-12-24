# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/guiignition.py
# Compiled at: 2019-01-12 02:14:13
# Size of source mod 2**32: 3531 bytes
"""
High-level application initialization common to both the CLI and GUI.
"""

def reinit() -> None:
    """
    (Re-)initialize this application -- but *not* mandatory third-party
    dependencies of this application, which requires external resources (e.g.,
    command-line options, configuration files) to be parsed.

    Specifically, this function (in order):

    #. Initializes all lower-level BETSE logic by calling the
       :func:`betse.ignition.init` function.
    #. Validates but does *not* initialize mandatory third-party dependencies of
       this application, which must be initialized independently by the
       :func:`betsee.lib.guilib.init` function.
    #. Validates the active Python interpreter to support multithreading.

    Design
    ----------
    To support caller-specific error handling, this function is intended to be
    called immediately *after* this application begins catching otherwise
    uncaught exceptions.

    Whereas BETSE is intended to be both run non-interactively from the
    command-line and imported interactively from Python REPLs (e.g., Jupyter),
    BETSEE is intended to only be run non-interactively from desktop application
    launchers. In the former case, BETSE detects and ignores attempts to
    re-initialize itself in the same application process. In the latter case, no
    re-initialization is expected, detected, or ignored.

    See Also
    ----------
    :func:`betsee.lib.libs.reinit`
        Function (re)-initializing all mandatory third-party dependencies.
    """
    from betse import ignition as betse_ignition
    from betsee.guimetaapp import BetseeMetaApp
    from betsee.lib import guilib
    app_meta = BetseeMetaApp()
    betse_ignition.reinit(app_meta)
    guilib.die_unless_runtime_mandatory_all()