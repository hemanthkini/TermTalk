import threading
import time

import sys
import logging
import getpass
import threading
from optparse import OptionParser

import sleekxmpp
import urwid
import urwid.raw_display
import urwid.web_display

global xmpp

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
name_jid_map = []

xmpplock = threading.Lock()

currName = ""

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

        urwid.register_signal(self, ['new chats', 'new roster'])

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)
        xmpplock.release()

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
        """ self.get_roster(callback=self.print_roster)
        print("CLIENT ROSTER:")
        print(self.client_roster) """

    def print_roster(self, b):
        global roster
        for x in roster._jids:
            newmapping = []
            newmapping.append(x)
            newmapping.append(str(self.get_name_or_jid(x)))
            name_jid_map.append(newmapping)
        urwid.emit_signal(self, "new roster")
        return

    """ for x in roster._jids:
    if x not in live_message_dict:
    live_message_dict[x] = []
    for x in live_message_dict:
    if x not in roster._jids:
    del live_message_dict[x] """

    def get_names_list(self):
        xmpplock.acquire()
        nameslist = []
        for i in name_jid_map:
            nameslist.append(i[1])
        xmpplock.release()
        return nameslist

    def get_live_names_list(self):
        xmpplock.acquire()
        nameslist = []
        for i in name_jid_map:
            if i in live_message_dict:
                nameslist.append(i[1])
        xmpplock.release()
        return nameslist

    def add_name_live(self, name):
        name = name.decode("utf-8")
        if name not in roster._jids:
            name = self.get_jid_for_name(name.encode("utf-8"))
        if name not in live_message_dict:
            live_message_dict[name] = []

    def get_jid_for_name(self, name):
        for i in name_jid_map:
            if i[1] == name:
                return i[0]
        return None

    def get_name_for_jid(self, jid):
        for i in name_jid_map:
            if i[0] == jid:
                return i[1]
        return None

    def get_name_or_jid(self, name):
        name = name.decode("utf-8")
        if roster.has_jid(name):
            return str(roster._jids[name]["name"])
        return name

    def roster_search_name(self, msg):
        if roster.has_jid(msg["from"].bare):
           return str(roster._jids[msg["from"].bare]["name"])
        return msg["from"]

    def return_msg_history(self, name):
        xmpplock.acquire()
        name = name.decode("utf-8")
        newlist = []
        if name in live_message_dict:
            msglist = live_message_dict[name]
            newname = self.get_name_or_jid(name)
            for (isFromFriend, msg) in msglist:
                if isFromFriend == 0:
                    currName = "Me"
                else:
                    currName = newname
                currName = currName.encode("utf-8")
                currmsg = currName + ": " + msg
                newlist.append(currmsg)
        xmpplock.release()
        return newlist

    def send_curr_message(self, message):
        xmpplock.acquire()
        send_the_message(self.get_jid_for_name(name.encode("utf-8")), message)
        xmpplock.release()


    def send_the_message(self, user, message):
        user = user.encode("utf-8")
        message = message.encode("utf-8")
        self.insert_msg(user.decode("utf-8"), message, 0)
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
            urwid.emit_signal(self, "new chats")

            #reply = raw_input("enter reply: ")
            #msg.reply(reply).send()
            #self.print_roster(False, False)
            #print("ROSTER : ")
            #print(roster)
            #print(live_message_dict)

def mainUI(friendsList, chateesList, chatHist):
    xmpplock.acquire()
    xmpplock.release()
    print("entered mainUI")
    div = urwid.Divider(".")
    global xmpp
    print("What is xmpp?")
    print(type(globals()['xmpp']))
    print(globals()['xmpp'])

    xmpp = globals()['xmpp']

    chatObj = urwid.Padding(urwid.Text(chatHist), left=2, right=10)

    friendsText = urwid.Padding(urwid.Text("Your friends"), left=2, right=10)
    chateeText = urwid.Padding(urwid.Text("Open chats"), left=2, right=10)

    friendButtons = urwid.Pile([])
    print("friendbuttons contents:")
    print(friendButtons.contents)
    chateeButtons = urwid.Pile(([]))

    def redraw_chat_text():
        for z in xmpp.get_live_names_list():
            alreadyInList = False
            for y in chateeButtons.contents:
                if y.original_widget.original_widget.get_label() == z:
                    alreadyInList = True
            if (alreadyInList == False):
                chateeButtons.contents.append((urwid.Padding(urwid.AttrWrap(urwid.Button(z, chateeButtonPress), 'buttn', 'buttnf'), left=5, right =10), ('weight', 1)))

        chatHist = xmpp.return_msg_history(xmpp.get_jid_for_name(currName))
        parsedHistory = chatHistParse(chatHist)
        chatObj.original_widget.set_text = parsedHistory

    def chateeButtonPress(button):
        frame.header = urwid.AttrWrap(urwid.Text(
                [u"Pressed: ", button.get_label()]), 'header')
        currName = button.get_label()
        chatHist = xmpp.return_msg_history(xmpp.get_jid_for_name(currName))
        parsedHistory = chatHistParse(chatHist)
        chatObj.original_widget.set_text = parsedHistory


    def friendButtonPress(button):
        frame.header = urwid.AttrWrap(urwid.Text(
                [u"Pressed: ", button.get_label()]), 'header')
        for x in chateeButtons.contents:
            if x.original_widget.original_widget.get_label() == button.get_label():
                return
        chateeButtons.contents.append((urwid.Padding(urwid.AttrWrap(urwid.Button(button.get_label(), chateeButtonPress), 'buttn', 'buttnf'), left=5, right =10), ('weight', 1)))
        xmpp.add_name_live(button.get_label())

    def rosterRefresh():
        friendButtons.contents.extend(
            [(urwid.Padding(urwid.AttrWrap(urwid.Button(txt, friendButtonPress),
                            'buttn', 'buttnf'),
            left=5, right =10), ('weight', 1))
             for txt in roster])

    urwid.register_signal(TermTalk, ['new chats', 'new roster'])

    urwid.connect_signal(xmpp, 'new chats', redraw_chat_text)
    urwid.connect_signal(xmpp, 'new roster', rosterRefresh)

    friend = urwid.Pile([friendsText, friendButtons])
    chatee = urwid.Pile([chateeText, chateeButtons])

    text_edit_padding = ('editcp', u"Type: ")
    editObj = urwid.Edit(text_edit_padding, "")
    textEntry = urwid.Padding(urwid.AttrWrap(editObj,
                             'editbx,', 'editfc'), left = 2,  width = 50)

    foot = urwid.Pile([div, textEntry])
    allFriendsList = urwid.Columns([friend,  chatee])

    listbox_content = [
        div,
        allFriendsList,
        div,
        chatObj]

    listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

    frame = urwid.Frame(urwid.AttrWrap(listbox,'body'), footer=foot)

    if urwid.web_display.is_web_request():
        screen = urwid.web_display.Screen()
    else:
        screen = urwid.raw_display.Screen()




    def unhandled(key):
        if key == "enter":
            frame.header = urwid.AttrWrap(urwid.Text(
                [u"Typed: ", editObj.text[6:]]), 'header')
            #####instead call that function do that thing
            #xmpp.send_curr_message(editObj.text[6:])


    palette = [
        ('buttnf', 'dark blue', "white", "bold"),
        ('buttn', 'white', 'dark blue'),
        ('header', 'white', 'dark cyan', 'bold')
        ]

    print("about to exit mainUI")
    urwid.MainLoop(frame, palette, unhandled_input=unhandled).run()


friends = ["Jack", "Aashish", "niki", "hemanth"]
chatees = ["jack", "aashish"]
#chatHist = "wowwwww\n now way\n how are you so cool?\n"
chatHist = ["You: wowww", "Me: fjsdklf", "You: niki is so cool"]

def chatHistParse(chatH):
    s = ""
    for x in xrange(len(chatH)):
        s += chatH[x]
        s+= "\n"
    return s


class uiThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        print("called init in uiThread!")
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        urwid.web_display.set_preferences("UI")
        if urwid.web_display.handle_short_request():
            return
        mainUI(friends, chatees, chatHistParse(chatHist))


class xmppThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        print("called init in xmppThread!")
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        # Setup the command line arguments.
        xmpplock.acquire()
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

        global xmpp
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
            global roster
            roster = xmpp.client_roster
            # xmpp.send_msg()
            xmpp.process(block=True)
            print("Done")
        else:
            print("Unable to connect.")

threads = []

# Create new threads
thread2 = xmppThread(2, "xmpp", 2)
thread1 = uiThread(1, "UI", 1)

# Start new Threads
thread2.start()
thread1.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"
