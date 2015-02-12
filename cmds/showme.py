def run(query):
    import requests
    import random
    import socket
    rsz = 8
    starts = [i * rsz for i in range(4)]
    start = random.choice(starts)
    ipaddr = socket.gethostname()
    baseurl = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&rsz=%d&start=%d&userip=%s&q=' % (rsz, start, ipaddr)
    url = baseurl + query.replace(' ', '%20')
    try:
        r = requests.get(url)
        if r.json()['responseStatus'] != 200:
            message = r.json()['responseDetails']
        else:
            images = [result['url'] for result in r.json()['responseData']['results'] if result['url'][-4:].lower() in ['.jpg', '.gif', '.png']]
            message = random.choice(images)
    except:
        message = "I BLEW UP TRYING TO GET YOU AN IMAGE!!! :("
    return message
