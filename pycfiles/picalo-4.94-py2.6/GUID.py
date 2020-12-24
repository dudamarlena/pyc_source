# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/GUID.py
# Compiled at: 2008-03-17 12:58:02
"""
  A globally-unique identifier made up of time and ip and 8 digits for a counter: 
  each GUID is 40 characters wide.

  A globally unique identifier that combines ip, time, and a counter.  Since the 
  time is listed first, you can sort records by guid.  You can also extract the time 
  and ip if needed.  

  Since the counter has eight hex characters, you can create up to 
  0xffffffff (4294967295) GUIDs every millisecond.  If your processor
  is somehow fast enough to create more than that in a millisecond (looking
  toward the future, of course), the function will wait until the next
  millisecond to return.
     
  GUIDs make wonderful database keys.  They require no access to the 
  database (to get the max index number), they are extremely unique, and they sort 
  automatically by time.   GUIDs prevent key clashes when merging
  two databases together, combining data, or generating keys in distributed
  systems.
  
  GUIDs are always returned as strings.  I did not make this a "real" class because
  it just complicates things.  Since GUIDs are generally stored in databases, sockets,
  and elsewhere as strings, I prefer to just keep them always as strings.  In other
  words, I don't see much benefit in having GUID objects over regular string objects.
  
  There is an Internet Draft for UUIDs, but this module does not implement it.
  If the draft catches on, perhaps I'll conform the module to it.
"""
import math, socket, random, sys, time, threading, types
make_hexip = lambda ip: ('').join([ '%04x' % long(i) for i in ip.split('.') ])
MAX_COUNTER = max(4294967294, sys.maxint)
counter = 0
firstcounter = MAX_COUNTER
lasttime = 0
hostip = ''
lock = threading.RLock()
try:
    hostip = socket.getaddrinfo(socket.gethostname(), 0)[(-1)][(-1)][0]
    hexip = make_hexip(hostip)
except:
    hostip = '10'
    rand = random.Random()
    for i in range(3):
        hostip += '.' + str(rand.randrange(1, 255))

    hexip = make_hexip(hostip)

def generate(ip=None):
    """Generates a new guid.  This is the primary method of the module.
     A guid is unique in space and time because it combines
     the machine IP with the current time in milliseconds.  It also includes
     a counter to provide uniqueness if two GUIDs are created in a single millisecond.
     
     Be careful about sending in
     a specified IP address because the ip makes it unique in space.  You could send in
     the same IP address that is created on another machine.  You should generally leave this
     parameter at its default value of None.
     
     @param      ip  An IP address to use in the GUID.  The default is the return from socket.getaddrinfo().
     @type       ip  str, such as '127.0.0.1' or a list, such as [ 127, 0, 0, 1 ]
     @returns:   A new GUID.
     @rtype:     str
  """
    global counter
    global firstcounter
    global lasttime
    lock.acquire()
    try:
        parts = []
        now = long(time.time() * 1000)
        while lasttime == now and counter == firstcounter:
            time.sleep(0.01)
            now = long(time.time() * 1000)

        parts.append('%016x' % now)
        if lasttime != now:
            firstcounter = long(random.uniform(1, MAX_COUNTER))
            counter = firstcounter
        counter += 1
        if counter > MAX_COUNTER:
            counter = 0
        lasttime = now
        parts.append('%08x' % counter)
        parts.append(hexip)
        return ('').join(parts)
    finally:
        lock.release()


def extract_time(guid):
    """Extracts the time portion out of the guid and returns the 
     number of seconds since the epoch as a float.
  
     @param guid: The guid to extract the time from.
     @type  guid: str
     @returns:    The time this GUID was created as the number of seconds since the epoch (see the standard time module for more info).
     @rtype:      float
  """
    return float(long(guid[0:16], 16)) / 1000.0


def extract_counter(guid):
    """Extracts the counter from the guid.  Each GUID has a counter
     that ensures the GUID is unique, even if two GUIDs are created
     on the same comptuer at the same millisecond.  The counter is
     started at a random place in the range of an integer, so
     it's value is generally meaningless. :)
     
     @param guid: The guid to extract the counter from.
     @type  guid: str
     @returns:    The counter used when this GUID was created.
     @rtype:      int
  """
    return int(guid[16:24], 16)


def extract_ip(guid):
    """Extracts the ip portion out of the guid and returns it
     as a string like 10.10.10.10.  This generally provides 
     the machine IP where the GUID was created (unless the IP
     could not be determined at creation time).
     
     @param guid: The guid to extract the counter from.
     @type  guid: str
     @returns:    The IP address as something like "10.10.10.10".
     @rtype:      str
  """
    thisip = []
    for index in range(24, 40, 4):
        thisip.append(str(int(guid[index:index + 4], 16)))

    return ('.').join(thisip)


def decode(guid):
    """Extracts all parts of the guid and returns a tuple of three 
     items: time, counter, and ip.
     
     @param guid: The guid to extract the counter from.
     @type  guid: str
     @returns:    A tuple containing the (time, counter, and ip address)
     @rtype:      tuple
  """
    return (
     extract_time(guid), extract_counter(guid), extract_ip(guid))


def is_valid(guid):
    """Returns whether the given guid seems to be a valid GUID or not.
     Since the guid is in string format, it can only check for appropriate
     length and valid characters in the GUID.
     
     @param guid: The guid to check.
     @type  guid: str
     @returns:    Whether it's a valid GUID or not
     @rtype:      bool
  """
    if not isinstance(guid, types.StringTypes):
        return False
    if len(guid) != 40:
        return False
    for ch in guid.upper():
        if ch not in '0123456789ABCDEF':
            return False

    return True


if __name__ == '__main__':
    num_to_create = int(raw_input('How many GUIDs shall I create? (default is 10)  ') or 10)
    guids = []
    for i in range(num_to_create):
        guid = generate()
        guids.append(guid)

    for guid in guids:
        print 'GUID:', guid
        guidtime = extract_time(guid)
        print '\tTime:   ', time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime(guidtime)), '(millis: ' + str(round(guidtime - long(guidtime), 3)) + ')'
        print '\tIP:     ', extract_ip(guid)
        print '\tCounter:', extract_counter(guid)