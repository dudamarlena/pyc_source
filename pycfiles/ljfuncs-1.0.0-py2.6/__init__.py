# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/ljfuncs/__init__.py
# Compiled at: 2010-01-18 01:45:48
"""ljfuncs.py

A set of functions to query LiveJournal, primarily regarding friends, and to
make recommendations for new friends based on existing ones.

NOTE: This package is intended more to perform analysis on a user's friends and
on other LJ users; it is not intended for basic functionality like making posts
to LiveJournal, editing entries, etc.

This package offers the following:

* User class
  A class representing a LiveJournal user, with the ability to retrieve
  interests lists, friends lists, FOAF lists, determine friends list
  discrepancies (i.e. one sided friendships), and calculate compatibility with
  other users based on interest list comparisons.

* Interest class
  A simple class to represent a LiveJournal interest.

* getUsersInterests function
  Given a list of users, return a dictionary indexed by user containing a list
  of the user's interests.

* findCompatibleUsers function
  Given a list of interests, an optional weighting on the interests, and a list
  of users, calculate a compatibility score for each user based on the interests
  they have in common with those specified.

* convertScoreDictToList function
  A convenience routine to convert the output from findCompatibleUsers to a list
  of users and compatibility values sorted by compatibility.

By Sebastian Raaphorst, 2007."""
import sys, random, re, string, threading, time, urllib2

class User:
    """Class representing a LiveJournal / LiveJournal-clone service user.

    * FIELDS *
    - username: name of the user on the server
    - server: server on which user account exists."""

    def __init__(self, username, server='http://www.livejournal.com'):
        """__init__(username, server='http://www.livejournal.com')

        Create a new instance representing the specified user on the specified server."""
        self.username = username
        self.server = server.rstrip('/')

    def __str__(self):
        """Display the username."""
        return self.username

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        """Default is to use the username to hash."""
        return self.username.__hash__()

    def __cmp__(self, other):
        """Compare first by server, then by username so as not to intermingle
        users different servers."""
        if self.server < other.server:
            return -1
        else:
            if self.server > other.server:
                return 1
            if self.username < other.username:
                return -1
            if self.username > other.username:
                return 1
            return 0

    def getFriends(self):
        """getFriends

        For this user, query the server and return a tuple consisting of two
        lists, namely:
        0. A list of User objects representing the friends for this user.
        1. A list of User objects representing the people that list this user
           as a friend."""
        url = self.server + '/misc/fdata.bml?user=' + self.username
        unsortedFriends = [ f.rstrip() for f in urllib2.urlopen(url) if not f.startswith('#') ]
        friends = [ User(friend.replace('> ', ''), self.server) for friend in unsortedFriends if friend.find('> ') != -1
                  ]
        friendsof = [ User(friend.replace('< ', ''), self.server) for friend in unsortedFriends if friend.find('< ') != -1
                    ]
        return (friends, friendsof)

    def determineFriendsDiscrepancies(self):
        """determineFriendsDiscrepancies

        Determine who is listed as a friend who does not list back, and
        vice-versa. Return a tuple consisting of:
        0. A list of User objects representing people who this user lists as a
           friend, but do not list him or her back.
        1. A list of User objects representing people who list this user as a
           friend, but who this user does not list back."""
        (friends, friendsof) = self.getFriends()
        notfriendof = [ friend for friend in friends if friend not in friendsof ]
        notfriend = [ friendof for friendof in friendsof if friendof not in friends ]
        return (notfriendof, notfriend)

    def getFOAFs(self, cutoff=1000):
        """getFOAFs(cutoff=1000)

        Given a user, query the server to determine the friend of a friend
        list for the user. An optional cutoff is specified so as to not perform
        too many calculations, e.g. if a cutoff of 10 was specified, only 10
        friends of the specified user would be queried for their friends list."""
        foaf = set()
        friends = self.getFriends()[0]
        random.shuffle(friends)
        for friend in [ f for f in friends if f.username != self.username ][0:cutoff]:
            friends2 = friend.getFriends()[0]
            for friend2 in [ f for f in friends2 if f not in friends if f != self ]:
                foaf.add(friend2)

        return list(foaf)

    def getInterests(self):
        """getInterests

        Retrieve the interests list of a user and return as a list of Interest
        objects. As the LiveJournal response is identical for a nonexistent user
        and a user with no interests, an empty list is returned if an error is
        encountered."""
        url = self.server + '/misc/interestdata.bml?user=' + self.username
        rawInterests = [ i.rstrip() for i in urllib2.urlopen(url) if i.rstrip() if not i.startswith('#') ]
        if rawInterests[0].startswith('!'):
            return []
        return [ Interest(int(id), int(freq), name) for (id, freq, name) in [ j.split(' ', 2) for j in rawInterests ] ]

    def findCompatibleUsers(self, users, interestWeightings={}):
        """findCompatibleUsers(users, interestWeightings={})

        Find this user's most compatible matches from the list of users provided
        in the users list. Every user in the list is assigned a compatibility
        rating based on common interests. Interests may be weighted optionally
        through the interestWeightings dictionary; by default, all interests
        receive an equal weight of 1.

        The method returns a list of tuples of the form (score, user).

        Here are some examples of how this method can be useful:

        1. If u is a User object, to find u's most compatible friends, execute:
            u.findCompatibleUsers(u.getFriends()[0])

        2. To find the most compatible FOAFs using a maximum of x friends and y
        FOAFs:
           u.findCompatibleUsers(u.getFOAFs(x)[0:y])"""
        interests = self.getInterests()
        userInterests = getUsersInterests(users)
        compatibleUsers = findCompatibleUsers(interests, userInterests, interestWeightings)
        return compatibleUsers


class Interest:
    """A class representing a user interest.

    * FIELDS *
    - id: ID for the interest in LiveJournal.
    - freq: Number of users who list the interest.
    - name: Name of the interest."""

    def __init__(self, id, freq, name):
        """__init__(id, freq, name)

        Define a new interest with the specified fields."""
        self.id = id
        self.freq = freq
        self.name = name

    def __str__(self):
        """Return the interest's name."""
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        """Default is to use the name to hash."""
        return self.name.__hash__()

    def __cmp__(self, other):
        """Default is to compare by name."""
        if self.name < other.name:
            return -1
        else:
            if self.name > other.name:
                return 1
            return 0

    def compareByID(self, other):
        """Comparison by ID number."""
        return self.id - other.id

    def compareByFreq(self, other):
        """Comparison by freq."""
        return self.freq - other.freq


def getUsersInterests(users):
    """getUsersInterests(users)

    A convenience function: given a list of User objects, create a dictionary of
    their Interests, indexed by user."""
    interestsDict = {}

    class UserInterests(threading.Thread):

        def __init__(self, user):
            self.user = user
            self.interests = None
            threading.Thread.__init__(self)
            return

        def run(self):
            self.interests = self.user.getInterests()

    for user in users:
        sys.stderr.write('Trying: %s\n' % user)
        for i in range(3):
            try:
                t = UserInterests(user)
                t.start()
                t.join(5)
                if not t.isAlive():
                    interestsDict[user] = t.interests
                    break
            except:
                sys.stderr.write('Failed to get interests for ' + user.username + ', retrying...\n')
                time.sleep(1)

    return interestsDict


def findCompatibleUsers(interests, userInterests, interestWeightings={}):
    """findCompatibleUsers(interests, userInterests, interestWeightings={})

    NOTE: It is best to not invoke this function directly, but instead call
    it through the findCompatibleUsers method of the User class.

    Given a list of Interest objects and possible weightings on them, determine
    from a collection of Users which ones are most compatible based on interests.

    The userInterests should be a dictionary mapping Users to lists of their
    Interests, as would be returned by getUsersInterests.

    The interestWeightings should be a dictionary mapping Interests in the
    interests list to weights assigned to the interests based on their priority
    (higher means higher priority, and 0 would indicate that the interest is
    entirely unimportant). For a given interest, if it has no weighting in the
    dictionary, then it is assumed to have a weight of 1.

    The function returns a dictionary indexed by user with value being a number
    in the range [0,1], where 0 indicates that the user has nothing in common
    with the interests specified, and 1 indicates that the user is fully
    compatible with the interests specified.

    In order to convert to a list, sorted by value, invoke:
        convertScoreDictToList(userScores)"""
    interestScores = dict([ (interest, interestWeightings[interest] if interest in interestWeightings else 1.0) for interest in interests ])
    print interestScores
    maxScore = float(sum(interestScores.values()))
    userScores = {}
    for user in userInterests:
        if maxScore == 0.0:
            userScores[user] = 0.0
            continue
        commonInterests = [ interest for interest in interests if interest in userInterests[user] ]
        userScores[user] = sum([ interestScores[interest] for interest in commonInterests ]) / maxScore

    return userScores


def convertScoreDictToList(userScores):
    """convertScoreDictToList(userScores)

    Given a dictionary mapping users to compatibility scores as created by
    findCompatibleUsers, this function returns a list of tuples of the form
    (User, score), sorted in nondecreasing order according to score."""
    return sorted(userScores.items(), key=lambda x: x[1], reverse=True)