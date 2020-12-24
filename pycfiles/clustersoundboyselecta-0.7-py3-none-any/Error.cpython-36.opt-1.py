# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/CLI/Error.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 4839 bytes
__doc__ = '\nCLI error handling helper functions\n'
from __future__ import print_function
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import errno, logging, os.path
from resource import getrlimit, RLIMIT_NOFILE
import signal, sys
from ClusterShell.Engine.Engine import EngineNotSupportedError
from ClusterShell.NodeUtils import GroupResolverConfigError
from ClusterShell.NodeUtils import GroupResolverIllegalCharError
from ClusterShell.NodeUtils import GroupResolverSourceError
from ClusterShell.NodeUtils import GroupSourceError
from ClusterShell.NodeUtils import GroupSourceNoUpcall
from ClusterShell.NodeSet import NodeSetExternalError, NodeSetParseError
from ClusterShell.NodeSet import RangeSetParseError
from ClusterShell.Propagation import RouteResolvingError
from ClusterShell.Topology import TopologyError
from ClusterShell.Worker.EngineClient import EngineClientError
from ClusterShell.Worker.Worker import WorkerError
GENERIC_ERRORS = (
 configparser.Error,
 EngineNotSupportedError,
 EngineClientError,
 NodeSetExternalError,
 NodeSetParseError,
 RangeSetParseError,
 GroupResolverConfigError,
 GroupResolverIllegalCharError,
 GroupResolverSourceError,
 GroupSourceError,
 GroupSourceNoUpcall,
 RouteResolvingError,
 TopologyError,
 TypeError,
 IOError,
 OSError,
 KeyboardInterrupt,
 WorkerError)
LOGGER = logging.getLogger(__name__)

def handle_generic_error(excobj, prog=os.path.basename(sys.argv[0])):
    """handle error given `excobj' generic script exception"""
    try:
        raise excobj
    except EngineNotSupportedError as exc:
        msgfmt = "%s: I/O events engine '%s' not supported on this host"
        print((msgfmt % (prog, exc.engineid)), file=(sys.stderr))
    except EngineClientError as exc:
        print(('%s: EngineClientError: %s' % (prog, exc)), file=(sys.stderr))
    except NodeSetExternalError as exc:
        print(('%s: External error: %s' % (prog, exc)), file=(sys.stderr))
    except (NodeSetParseError, RangeSetParseError) as exc:
        print(('%s: Parse error: %s' % (prog, exc)), file=(sys.stderr))
    except GroupResolverIllegalCharError as exc:
        print(('%s: Illegal group character: "%s"' % (prog, exc)), file=(sys.stderr))
    except GroupResolverConfigError as exc:
        print(('%s: Group resolver error: %s' % (prog, exc)), file=(sys.stderr))
    except GroupResolverSourceError as exc:
        print(('%s: Unknown group source: "%s"' % (prog, exc)), file=(sys.stderr))
    except GroupSourceNoUpcall as exc:
        msgfmt = '%s: No %s upcall defined for group source "%s"'
        print((msgfmt % (prog, exc, exc.group_source.name)), file=(sys.stderr))
    except GroupSourceError as exc:
        print(('%s: Group error: %s' % (prog, exc)), file=(sys.stderr))
    except (RouteResolvingError, TopologyError) as exc:
        print(('%s: TREE MODE: %s' % (prog, exc)), file=(sys.stderr))
    except configparser.Error as exc:
        print(('%s: %s' % (prog, exc)), file=(sys.stderr))
    except (TypeError, WorkerError) as exc:
        print(('%s: %s' % (prog, exc)), file=(sys.stderr))
    except (IOError, OSError) as exc:
        if exc.errno == errno.EPIPE:
            LOGGER.debug(exc)
        else:
            print(('ERROR: %s' % exc), file=(sys.stderr))
            if exc.errno == errno.EMFILE:
                print(('ERROR: maximum number of open file descriptors: soft=%d hard=%d' % getrlimit(RLIMIT_NOFILE)),
                  file=(sys.stderr))
    except KeyboardInterrupt as exc:
        return 128 + signal.SIGINT
    except:
        if not False:
            raise AssertionError('wrong GENERIC_ERRORS')

    return 1