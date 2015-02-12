from collections import defaultdict
import pickle
import re
import os
_CACHE_FILE = os.path.dirname(os.path.abspath(__file__)) + "/data/teachabot_cache"
_CACHE = None
_KOSHER_TAGS_FILE = os.path.dirname(os.path.abspath(__file__)) + "/data/teachabot_kosher_tags"
_KOSHER_TAGS = None


def run(query):
    _KOSHER_TAGS = get_kosher_tags()
    if query.startswith('kosher: '):
        tag = query.split()[1].lower()
        _KOSHER_TAGS.add(tag)
        sync_tags()
        return "Added tag: %s to kosher tags!" % (tag)

    """ query should contain <tag1,tag2> <knowledge> """
    tags = None
    knowledge = None
    try:
        tags = query.split()[0].split(',')
        tags = [tag.lower() for tag in tags]
        knowledge = ' '.join(query.split(' ')[1:])
    except:
        pass
    if not knowledge or not knowledge.strip():
        return "Try: ?teachabot <tag1,tag2> <knowledge>.  I got tags: %s knowledge: %s." % (tags, knowledge)

    _CACHE = get_cache()

    bad_tags = [tag for tag in tags if tag not in _KOSHER_TAGS]
    if bad_tags:
        return "Non-kosher tags: %s, choose tags from %s, or add kosher tag with command: ?teachabot kosher: <tagname>" % (bad_tags, _KOSHER_TAGS)

    knowledge_hash = get_hash(knowledge)
    _CACHE['knowledge'][knowledge_hash] = knowledge
    for tag in tags:
        _CACHE['tags'][tag].add(knowledge_hash)
    """ If wish to be fancy, guess could randomly decide when to sync.. or keep track of time. """
    sync_cache()

    return "Thanks for teaching me! I now associate '%s' with %s" % (knowledge, tags)


def get_hash(item):
    return str(hash(re.sub('\s+', ' ', item.lower())))


def sync_cache():
    global _CACHE, _CACHE_FILE
    with open(_CACHE_FILE, 'w') as f:
        f.write(pickle.dumps(_CACHE))


def sync_tags():
    global _KOSHER_TAGS, _KOSHER_TAGS_FILE
    with open(_KOSHER_TAGS_FILE, 'w') as f:
        f.write(pickle.dumps(_KOSHER_TAGS))


def get_cache():
    global _CACHE, _CACHE_FILE
    if _CACHE is None:
        try:
            with open(_CACHE_FILE, 'r') as f:
                _CACHE = pickle.loads(f.read())
        except:
            _CACHE = {'knowledge': {}}
            _CACHE['tags'] = defaultdict(set)
    return _CACHE


def get_kosher_tags():
    global _KOSHER_TAGS, _KOSHER_TAGS_FILE
    if _KOSHER_TAGS is None:
        try:
            with open(_KOSHER_TAGS_FILE, 'r') as f:
                _KOSHER_TAGS = pickle.loads(f.read())
        except:
            _KOSHER_TAGS = set([])
    return _KOSHER_TAGS
