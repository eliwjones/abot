def get_definitions(xml):
    import xmltodict
    from collections import OrderedDict
    definitions = xmltodict.parse(xml)
    defs = []
    if 'entry' not in definitions['entry_list']:
        return []
    if type(definitions['entry_list']['entry']) != list:
        definitions['entry_list']['entry'] = [definitions['entry_list']['entry']]
    for section in definitions['entry_list']['entry']:
        if type(section) != OrderedDict:
            continue
        if not 'def' in section:
            continue
        if not 'dt' in section['def']:
            continue
        if type(section['def']['dt']) == unicode:
            defs.append(section['def']['dt'])
            continue
        for entry in section['def']['dt']:
            if type(entry) != unicode:
                continue
            if not entry.startswith(':'):
                continue
            defs.append(entry)
    return defs


def run(word):
    import requests
    url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/%s?key=fae166f8-39f6-4de9-a16d-8d2c25353d34" % (word)
    message = ''
    r = requests.get(url)
    xml = r.text
    defs = get_definitions(xml)
    if len(defs) > 0:
        message = "\n".join(defs)
    else:
        message = 'Not found.'
    return message

if __name__ == "__main__":
    message = run("html")
    print message
