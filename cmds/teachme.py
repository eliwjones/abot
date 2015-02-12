def run(tag):
    import teachabot
    import random
    cache = teachabot.get_cache()
    if not tag.strip():
        tag = random.choice(list(teachabot.get_kosher_tags()))
    try:
        tag = tag.lower()
        knowledge_hash = random.choice(list(cache['tags'][tag]))
        if knowledge_hash in cache['knowledge']:
            return cache['knowledge'][knowledge_hash]
    except:
        pass
    return "Don't know nothing about '%s'" % (tag)
