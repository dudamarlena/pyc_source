# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/__init__.py
# Compiled at: 2010-10-14 14:04:23
"""
unidist

Unified Distributed Computing

by Geoff Howland <geoff AT ge01f DOT com>

unidist resources consists of:

- Shared Locks: to ensure resource control can be limited, and confirm resources
    are being used.  State is never saved for process restarts.  Locks are lost.

- Shared Counters: to track values of interest to different threads, updated
    in an atomic fashion.  Usable as unique ID incrementors and thread safe.
    State can be saved for process restart, snapshotting only.

- Shared State: to track data in buckets in a thread-safe manner.  Shared
    state allows disperate threads to use each other's information, safely.
    State can be saved for process restart, archival method and snapshotting
    is available.

- Message Queues: inter-thread communication or delayed processing.  Thread
    safe and can be stored to disk for restart survival.  Storage methods
    include archive and snapshotting, and can be tuned.

- Thread Safe Dictionary: used as a core part of all thread-safe operations,
    the ThreadSafeDict is a core tool for ensuring multiple threads can access
    common information in a thread-safe manner.

- Thread Safe List: used as a core part of all thread-safe operations,
    the ThreadSafeList is a core tool for ensuring multiple threads can access
    common information in a thread-safe manner.

- Logging: A best-of-breed logging solution for single hosts or a large
    distributed system.  Made for ease of use, and maximum information control,
    will store locally, rotate, send to syslog, keep collection information to
    be scraped for central storage, keep track of the scripts and line numbers
    being logged from, and many other useful and configurable parameters.
    Defaults should "just work".  Can target to different logging tracks, going
    into different files, or whatever.
    
    Logging has less to do with shared resources than these other items, but
    I have found all programs need robust logging, and the standard Python
    logging library is great in lots of ways, but takes a lot of effort to set
    up, and more effort to do distributed things correctly, and much more effort
    to do scalable distributed things, so I'm just doing a version that will
    be universably available and work easily and scale massively, and including
    it with the rest of the shared resources to make it a more useful library.
    
    Feel free to ignore any parts of this library you wish.  :)

The purpose of this shared set of libraries is to wrap the most common functions
needed for a small piece of code to operate on an enterprise level.

Small code using this library can take advantage of the benefits that
distributed systems technologies provide to keep logic small, and pass the
responsibility of labor to other small code blocks, so testing can be better,
and complexity can be reduced.  More of the complexity can be handed to the
well-tested shared resource code, which provides the framework for smaller
code to operate robustly and provide a breadth of features.

This is not sales-speak, several tiny scripts should be able to pull off very
large and complex seeming jobs if they use the shared resources properly, and
should be able to scale to thousands of nodes communicating and sharing data, if
required, while still keeping custom code small and easy to change and verify.

These libraries are built with the intend of being used in operating-system
level scripts.  If you are trying to do high transactions with minimal memory
footprints, you will want to use a specific storage solution for that purpose,
like a stand-alone Message Queue service (ex. ActiveMQ), or a State Server
(ex. reddis).

These libraries are intendend to make development easier and
faster, but are not meant to take the place of specialized fine-tuned services
if scale and performance is required.

unidist is specifically aimed at automating System Administration tasks, and
having internal distributed computing mechanisms that do not require services
that need their own computing and network resources, which would further
complicate and add failure conditions to the system being managed.
"""
import sharedlock, sharedcounter, sharedstate, messagequeue, threadsafedict, threadsafelist, log, stack, error_info, dotinspect, html, node