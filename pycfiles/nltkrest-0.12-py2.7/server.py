# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/nltkrest/server.py
# Compiled at: 2016-03-15 00:26:39
from flask import Flask, request
import nltk, json
from nltk_contrib import timex
import time, sys, getopt
USAGE = '\nnltk-rest --port -p <port> -v [--help -h]\n\nExpose NLTK over REST as a server using Python Flask. Submit content to the\n`/nltk` endpoint in the REST body request. \n\n-h, --help Prints this message.\n-p, --port Sets the port for the REST server, default is 8881.\n'
Verbose = 0
Port = 8881

def echo2(*s):
    sys.stderr.write('server.py [NLTK]: ' + (' ').join(map(str, s)) + '\n')


app = Flask(__name__)

@app.route('/')
def status():
    msg = '\n       <html><head><title>NLTK REST Server</title></head><body><h3>NLTK REST server</h3>\n       <p>This app exposes the Python <a href="http://nltk.org/">Natural Language Toolkit (NLTK)</a>\n       as a REST server.</p>\n       <h2>Status: Running</h2>\n       <p>More apps from the <a href="//irds.usc.edu/">USC Information Retrieval & Data Science Group</a>.</p>\n    '
    return msg


@app.route('/nltk', methods=['PUT', 'POST'])
def namedEntityRecognizer():
    global Verbose
    echo2('Performing NER on incoming stream')
    content = request.stream.read()
    if Verbose:
        echo2('Incoming content is ' + content)
    start = time.time()
    date_time = timex.tag(content)
    tokenized = nltk.word_tokenize(content)
    tagged = nltk.pos_tag(tokenized)
    namedEnt = nltk.ne_chunk(tagged, binary=True)
    names = extract_entity_names(namedEnt)
    names.extend(date_time)
    result = {'result': 'success', 'names': names}
    jsonDoc = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
    end = time.time()
    print 'NER took ' + str(end - start) + ' seconds'
    return jsonDoc


def extract_entity_names(t):
    entity_names = []
    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append((' ').join([ child[0] for child in t ]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names


def main(argv=None):
    """Run NLTK REST server from command line according to USAGE."""
    global Verbose
    if argv is None:
        argv = sys.argv
    try:
        opts, argv = getopt.getopt(argv[1:], 'hp:v', [
         'help', 'port=', 'verbose'])
    except getopt.GetoptError as (msg, bad_opt):
        die('%s error: Bad option: %s, %s' % (argv[0], bad_opt, msg))

    port = Port
    for opt, val in opts:
        if opt in ('-h', '--help'):
            echo2(USAGE)
            sys.exit()
        elif opt in '--port':
            port = int(val)
        elif opt in ('-v', '--verbose'):
            Verbose = 1
        else:
            die(USAGE)

    app.run(debug=Verbose, port=port)
    return


if __name__ == '__main__':
    main(sys.argv)