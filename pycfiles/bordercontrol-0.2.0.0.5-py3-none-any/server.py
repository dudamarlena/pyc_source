# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/borda/server.py
# Compiled at: 2013-08-05 13:27:40
__doc__ = 'This module serves responses to requests on the Borda voting system. The\nrequests typically create a new election, register new candidates and voters,\nissue votes for the election, and also retrieve the resulting winner.'
import json, os.path, shelve
from contextlib import closing
import bottle, borda.count
DEFAULT_PORT = 1031
ELECTION = None
VOTERS = []
app = bottle.Bottle()
db = shelve.open(os.path.join(app.resources.base, 'shelve.db'), writeback=True)

@app.route('/election', method='GET')
def get_election_result():
    """Get election result"""
    if db['election'] is None:
        return 'Sorry, no election defined'
    else:
        return db['election'].get_winner().name


@app.route('/election', method='POST')
def create_election():
    """Create a new election"""
    election = borda.count.Election()
    election.set_candidates([])
    db['election'] = election


@app.route('/election', method='PUT')
def add_candidate():
    """Add a candidate to the open election"""
    name = bottle.request.POST.get('name')
    candidate = borda.count.Candidate(name)
    db['election'].add_candidate(candidate)


@app.route('/vote', method='GET')
def list_candidates():
    """List all candidates"""
    return json.dumps([ c.name for c in db['election'].candidates ])


@app.route('/vote', method='POST')
def add_voter():
    """Add a voter to the open election"""
    name = bottle.request.POST.get('name')
    voter = borda.count.Voter(db['election'], name)
    db['voters'].append(voter)


@app.route('/vote', method='PUT')
def vote():
    """Issue votes from a voter in the election"""
    name = bottle.request.POST.get('name')
    for voter in db['voters']:
        if voter.name == name:
            posted_votes = bottle.request.POST.getlist('votes')
            votes = []
            for posted_vote in posted_votes:
                votes.append(borda.count.Candidate(posted_vote))

            voter.votes(votes)


def main_debug():
    """Test entry point"""
    run_app(True)


def main():
    """Main entry point"""
    run_app(False)


def run_app(do_debug=False):
    """Run the web app, wheter with or without debugging"""
    db.setdefault('election', None)
    db.setdefault('voters', [])
    with closing(db):
        app.run(host='localhost', port=DEFAULT_PORT, debug=do_debug)
    return