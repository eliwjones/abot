import sleekxmpp
import json
import sys
import time
from xml.dom import minidom
from conf import *


last_message = None


class ABot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, rooms, nick, cache_file):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.password = password
        self.nick = nick
        self.rooms = rooms
        self.cache_file = cache_file
        try:
            with open(self.cache_file, 'r') as f:
                self.seen = json.loads(f.read())
        except:
            self.seen = {}

        print "[__init__] adding event handlers."
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        for room in self.rooms:
            self.add_event_handler("muc::%s::got_online" % (room), self.muc_online)

    def muc_online(self, presence):
        _nick = presence['muc']['nick']
        print "[muc_online] " + _nick
        seen_recently = True
        if _nick not in self.seen:
            seen_recently = False
        elif int(time.time()) - self.seen[_nick] > 60 * 60:
            seen_recently = False
        if _nick != self.nick and not seen_recently:
            self.seen[_nick] = int(time.time())
#            self.send_message(mto=presence['from'].bare, mbody=_nick + "!!!! wazzup,brother..", mtype='groupchat')

    def start(self, event):
        print "[start] Session Started"
        print "[start] get_roster()"
        self.get_roster()
        print "[start] send_presence()"
        self.send_presence()
        print "[start] join rooms"
        for room in self.rooms:
            print "[start] Joining: " + room
            self.plugin['xep_0045'].joinMUC(room, nick, wait=True)
            print "[start] Joined: " + room

    def muc_message(self, msg):
        self.last_message = msg
        # Too lazy to figure out what esoteric way is used to get 'id'/'mid', so just yanking it from __repr__ xml.
        message = minidom.parseString(str(msg)).getElementsByTagName('message')
        print str(msg)
        mid = None
        try:
            # hipchat uses 'mid'
            mid = message[0].attributes['mid'].value
        except:
            # slack uses 'id'
            mid = message[0].attributes['id'].value

        if mid is None:
            print "Could not find 'mid' in attributes"
            return
        else:
            print "[muc_message] %s" % (mid)

        if mid in self.seen:
            print "Already seen this message! mid: %s" % (mid)
            return
        elif msg['mucnick'] == self.nick:
            print "I do not respond to myself!"
            return
        """ Now that I'm ready, mark as seen, and process. """
        if msg['body'].startswith('?'):
            self.seen[mid] = True
            body_parse = msg['body'].split(' ')
            cmd = body_parse[0][1:].lower()
            query = ' '.join(body_parse[1:])
            print "Command! cmd: %s, query: %s" % (cmd, query)
            try:
                if query == '!reload':
                    if "cmds.%s" % (cmd) in sys.modules:
                        del(sys.modules["cmds.%s" % (cmd)])
                        reply = "Reloaded %s" % (cmd)
                    else:
                        reply = "cmds.%s not found in sys.modules!" % (cmd)
                else:
                    cmd = __import__("cmds.%s" % (cmd), fromlist=[''])
                    reply = cmd.run(query)
            except Exception as e:
                reply = "Exception: %s" % (e)
            self.send_message(mto=msg['from'].bare, mbody=reply, mtype='groupchat')
        elif self.nick.lower() in msg['body'].lower():
            self.seen[mid] = True
            print "Think I'll respond to this one."
            self.send_message(mto=msg['from'].bare, mbody="Beep Boop Bop! To you, %s" % (msg['mucnick']), mtype='groupchat')
        else:
            # Don't wish to track all mids.. just ones I might respond to.
            print "Not sure what to do.."
            print msg
        with open(self.cache_file, 'w') as f:
            f.write(json.dumps(self.seen))


abot = ABot(jid, password, rooms, nick, cache_file)

abot.register_plugin('xep_0030')  # Service Discovery
abot.register_plugin('xep_0045')  # Multi-User Chat
abot.register_plugin('xep_0199')  # XMPP Ping

abot.connect()
abot.process(block=True)
