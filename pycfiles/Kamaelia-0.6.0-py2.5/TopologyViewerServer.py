# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Visualisation/PhysicsGraph/TopologyViewerServer.py
# Compiled at: 2008-10-19 12:19:52
"""==============================
Generic Topology Viewer Server
==============================

A generic topology viewer that one client can connect to at a time over a
TCP socket and send topology change data for visualisation.

Example Usage
-------------
Visualiser that listens on port 1500 for a TCP connection through which
it receives topology change data to render::
    
    TopologyViewerServer( serverPort = 1500 ).run()
    
A simple client to drive the visualiser::
    
    Pipeline( ConsoleReader(),
              TCPClient( server=<address>, port=1500 ),
            ).run()
    
Run the server, then run the client::
    
    >>> DEL ALL
    >>> ADD NODE 1 "1st node" randompos -
    >>> ADD NODE 2 "2nd node" randompos -
    >>> ADD NODE 3 "3rd node" randompos -
    >>> ADD LINK 1 2
    >>> ADD LINK 3 2
    >>> DEL LINK 1 2
    >>> DEL NODE 1

See also Kamaelia.Visualisation.Axon.AxonVisualiserServer - which is a
specialisation of this component.

How does it work?
-----------------

TopologyViewerServer is a Pipeline of the following components:
    
- Kamaelia.Internet.SingleServer
- chunks_to_lines
- lines_to_tokenlists
- TopologyViewer
- ConsoleEchoer

This Pipeline serves to listen on the specified port (defaults to 1500) for
clients. One client is allowed to connect at a time.

That client can then send topology change commands formatted as lines of text.
The lines are parsed and tokenised for the TopologyViewer.

Any output from the TopologyViewer is sent to the console.

If the noServer option is used at initialisation, then the Pipeline is built
without the SingleServer component. It then becomes a TopologyViewer
capable of processing non-tokenised input and with diagnostic console output.

See TopologyViewer for more detail on topology change data and
its behaviour.
"""
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer
from Kamaelia.Internet.SingleServer import SingleServer
from Kamaelia.Util.Console import ConsoleEchoer

def TopologyViewerServer(serverPort=1500, **dictArgs):
    """    TopologyViewerServer([noServer][,serverPort],**args) -> new TopologyViewerServer component.

    One-client-at-a-time TCP socket Topology viewer server. Connect on the
    specified port and send topology change data for display by a
    TopologyViewer.

    Keyword arguments:
    
    - serverPort  -- None, or port number to listen on (default=1500)
    - args        -- all remaining keyword arguments passed onto TopologyViewer
    """
    return Pipeline(SingleServer(port=serverPort), chunks_to_lines(), lines_to_tokenlists(), TopologyViewer(**dictArgs), ConsoleEchoer())


def TextControlledTopologyViewer(**dictArgs):
    return Pipeline(chunks_to_lines(), lines_to_tokenlists(), TopologyViewer(**dictArgs), ConsoleEchoer())


__kamaelia_prefabs__ = (
 TopologyViewerServer, TextControlledTopologyViewer)