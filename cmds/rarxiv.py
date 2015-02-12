def run(query):
    import feedparser
    import random
    url = 'http://export.arxiv.org/api/query?search_query=all:%s&start=0&max_results=100' % (query)
    url = url.replace(' ', '%20')
    results = feedparser.parse(url)
    """ If want verbose.. guess could add in results['entries'][index]['summary'] """
    index = random.randrange(len(results['entries']))
    message = "'%s' - %s" % (results['entries'][index]['title'], results['entries'][index]['id'])
    return message
