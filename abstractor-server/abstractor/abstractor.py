import shelve
import re
import string
import collections
import ner
from flask import Flask, jsonify, request, render_template
from os import path
from cPickle import HIGHEST_PROTOCOL
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag.stanford import POSTagger
from onetfreq import top10k, top5k, top1k
import random
import code

SHELVE_DB = 'shelve.db'

app = Flask(__name__)
app.config.from_object(__name__)

db = shelve.open(path.join(app.root_path, app.config['SHELVE_DB']),
                 protocol=HIGHEST_PROTOCOL, writeback=True)

nerify = ner.SocketNER(host='localhost', port=9000)

st = POSTagger('../stanford-postagger-2013-06-20/models/english-bidirectional-distsim.tagger',
               '../stanford-postagger-2013-06-20/stanford-postagger-3.2.0.jar')
punct = re.compile('[%s]' % re.escape(string.punctuation))
# note these are in reverse order of use for pop() later
altperson = collections.deque(['somebody else still', 'an individual', \
'another person', 'somebody else', 'someone else', 'someone', 'this person'])
altloc = collections.deque(['that spot', 'that site', 'that location', \
'there', 'that place'])
altorg = collections.deque(['the organization'])
altnoun = collections.deque(['that thing'])
altnoun_plural = collections.deque(['those things'])
altverb = collections.deque(['doing something'])
altverb_past = collections.deque(['were doing something'])

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/get_progress")
def get_progress():
    return jsonify({"progress":db["progress"]})

@app.route("/named_entities", methods=['POST'])
def ner_process():
    text = request.form["text"].encode("utf-8")
    return jsonify(stanfordner(text))

def stanfordner(text):
    return nerify.get_entities(text)

@app.route("/abstractify",  methods=['POST'])
def abstractify():
    text = request.form["text"].encode("utf-8")
    return abstract(text)

def abstract(text):
    db.setdefault('progress', 0) # Default progress is 0
    count = 0 # Just starting
    db['progress'] = count # Set current progress

    ne = stanfordner(text)
    transformations = {}

    if 'PERSON' in ne:
        people = ne['PERSON']
        for p in people:
            print p
            print "person"
            transformations[p] = get_replacement(p, altperson)


    if 'LOCATION' in ne:
        places = ne['LOCATION']
        for l in places:
            print l
            print "location"
            transformations[l] = get_replacement(l, altloc)


    if 'ORGANIZATION' in ne:
        orgs = ne['ORGANIZATION']
        for o in orgs:
            print o
            print "object"
            transformations[o] = get_replacement(o, altorg)

    count = 50 # Half way done
    wordlists = [word_tokenize(s) for s in sent_tokenize(text)]
    increment = 50.0/len(wordlists) # Calculate increment for progress bar

    # Randomly reduce wordlists, we want to make this faster
    wordlists = random.sample(wordlists, len(wordlists)/3)

    print transformations

    for wordlist in wordlists:
        ascii_word_list = []
        for word in wordlist:
            try:
                word.decode('ascii')
                ascii_word_list.append(word)
            except UnicodeDecodeError:
                print "it was not a ascii-encoded unicode string"
                print word

        pos = st.tag(ascii_word_list)
        count += increment
        db['progress'] = count # Update value for progress bar
        #code.interact(local = locals())
        for pair in pos:
            word = pair[0]
            postag = pair[1]
            if not re.match(punct, word) and word.lower() not in top1k:
                if word not in transformations:
                    if postag.startswith('NNP'):
                        print word
                        print 'NNP'
                        transformations[word] = get_replacement(word, altnoun)
                    elif postag.startswith('NNPS'):
                        print word
                        print 'NNPS'
                        transformations[word] = get_replacement(word, altnoun_plural)
                    # elif postag.startswith('VB'):
                    #     print word
                    #     print 'NNPS'
                    #     transformations[word] = get_replacement(word, altverb)
                    # elif postag.startswith('VBD'):
                    #     print word
                    #     print 'VBD'
                    #     transformations[word] = get_replacement(word, altverb_past)

    db['progress'] = 0 # Reset vale for next run

    return jsonify(transformations)

def proper_case(original, replacement):
    if original[0].isupper():
        return  replacement[0].upper() + replacement[1:]
    else:
        return replacement

def get_next_alt(alt_list):
    element = alt_list.pop()
    alt_list.appendleft(element)

    return element

def get_replacement(original, alt_list):
    alt = get_next_alt(alt_list)
    replacement = proper_case(original, alt)

    return replacement

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
