Abot
====

Prerequisites:

    $ cd abot
    $ virtualenv venv --distribute
    $ pip install -r requirements.txt

Sample conf.py:

    import os
    jid = "BOTJID@chat.hipchat.com"
    password = "PASSWORDHERE"
    rooms = ["room1@conf.hipchat.com", "room2@conf.hipchat.com"]
    nick = "Abot"
    cache_file = os.path.dirname(os.path.abspath(__file__)) + "/abot_cache"


