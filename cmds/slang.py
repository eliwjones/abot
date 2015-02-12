def run(query):
    import requests
    baseurl = 'http://urbanscraper.herokuapp.com/define/'
    url = baseurl + query.replace(' ', '%20')
    message = ''
    try:
        r = requests.get(url)
        data = r.json()
        if 'example' in data:
            if len(data['definition']) > 1:
                message += query + ' means: \n' + data['definition']
            if len(data['example']) > 1:
                message += ' Here is an example: \n' + data['example']
    except:
        message = '???'
    return message
