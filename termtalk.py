#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SleekXMPP: The Sleek XMPP Library
Copyright (C) 2010 Nathanael C. Fritz
This file is part of SleekXMPP.

See the file LICENSE for copying permission.
"""

import sys
import logging
import getpass
from optparse import OptionParser

import sleekxmpp


# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

roster = None
live_message_dict = {}



class TermTalk(sleekxmpp.ClientXMPP):

    """
    A simple SleekXMPP bot that will echo messages it
    receives, along with a short thank you message.
    """

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        self.add_event_handler("print_roster", self.print_roster)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)

    def start(self, event):
        """
Process the session_start event.

Typical actions for the session_start event are
requesting the roster and broadcasting an initial
presence stanza.

Arguments:
event -- An empty dictionary. The session_start
event does not provide any additional
data.
"""
        print("session_start was received; self.start was called")
        self.send_presence()
        self.get_roster()
        self.send_msg()
        """ self.get_roster(callback=self.print_roster)
        print("CLIENT ROSTER:")
        print(self.client_roster) """

    def print_roster(a, b):
        print("OUR ROSTER: ")
        print(roster)
"""        for x in roster._jids:
            if x not in live_message_dict:
                live_message_dict[x] = []
        for x in live_message_dict:
            if x not in roster._jids:
                del live_message_dict[x] """

    def roster_search_name(self, msg):
        if roster.has_jid(msg["from"].bare):
           return str(roster._jids[msg["from"].bare]["name"])
        return msg["from"]

    def send_msg(self):
        user = raw_input("enter email: ")
        message = raw_input("enter msg: ")
        self.send_the_message(user, message)
        self.send_msg()

    def send_the_message(self, user, message):
        user = user.encode("utf-8")
        message = message.encode("utf-8")
        self.insert_msg(self, user.decode("utf-8"), message, 0)
        self.send_message(mto=user, mbody=message, mtype = "chat")

    def insert_msg(self, name, msg, isFromFriend):
        name = name.decode("utf-8")
        msg = msg.encode("utf-8")
        if name not in live_message_dict:
            live_message_dict[name] = []
        msglist = live_message_dict[name]
        if (len(msglist) >= 50):
            msglist.pop(0)
        msglist.append((isFromFriend, msg))


    def message(self, msg):
        """
Process incoming message stanzas. Be aware that this also
includes MUC messages and error messages. It is usually
a good idea to check the messages's type before processing
or sending replies.

Arguments:
msg -- The received message stanza. See the documentation
for stanza objects and the Message stanza to see
how it may be used.
"""
        print("General received stanza")
        print(msg)
        if msg['type'] in ('chat', 'normal'):
            print(self.roster_search_name(msg) + ":  " + msg["body"])
            print(type(msg["from"].bare))
            print(type(msg["body"]))
            self.insert_msg(msg["from"].bare, msg["body"], 1)
            reply = raw_input("enter reply: ")
            msg.reply(reply).send()
            #self.print_roster(False, False)
            #print("ROSTER : ")
            #print(roster)
            print(live_message_dict)




if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Email: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")

    # Setup the EchoBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = TermTalk(opts.jid, opts.password)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # If you are connecting to Facebook and wish to use the
    # X-FACEBOOK-PLATFORM authentication mechanism, you will need
    # your API key and an access token. Then you'll set:
    # xmpp.credentials['api_key'] = 'THE_API_KEY'
    # xmpp.credentials['access_token'] = 'THE_ACCESS_TOKEN'

    # If you are connecting to MSN, then you will need an
    # access token, and it does not matter what JID you
    # specify other than that the domain is 'messenger.live.com',
    # so '_@messenger.live.com' will work. You can specify
    # the access token as so:
    # xmpp.credentials['access_token'] = 'THE_ACCESS_TOKEN'

    # If you are working with an OpenFire server, you may need
    # to adjust the SSL version used:
    # xmpp.ssl_version = ssl.PROTOCOL_SSLv3

    # If you want to verify the SSL certificates offered by a server:
    # xmpp.ca_certs = "path/to/ca/cert"

    # Connect to the XMPP server and start processing XMPP stanzas.

    print("attempting connection")
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        # ...
        roster = xmpp.client_roster
        # xmpp.send_msg()
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")


