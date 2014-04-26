import urwid
import urwid.raw_display
import urwid.web_display

currName = ""

def mainUI(friendsList, chateesList, chatHist, xmpp):
    div = urwid.Divider(".")

    chatObj = urwid.Padding(urwid.Text(chatHist), left=2, right=10)

    friendsText = urwid.Padding(urwid.Text("Your friends"), left=2, right=10)
    chateeText = urwid.Padding(urwid.Text("Open chats"), left=2, right=10)

    friendButtons = urwid.Pile([])
    print("friendbuttons contents:")
    print(friendButtons.contents)
    chateeButtons = urwid.Pile(([]))

    def redraw_chat_text():
        #for z in xmpp.get_live_names_list():
            #alreadyInList = False
            #for y in chateeButtons.contents:
                #if y.original_widget.original_widget.get_label() == z:
                    #alreadyInList = True
            #if (alreadyInList == False):
                #chateeButtons.contents.append((urwid.Padding(urwid.AttrWrap(urwid.Button(z, chateeButtonPress), 'buttn', 'buttnf'), left=5, right =10), ('weight', 1)))

        #chatHist = xmpp.return_msg_history(xmpp.get_jid_for_name(currName))
        #parsedHistory = chatHistParse(chatHist)
        #chatObj.original_widget.set_text = parsedHistory

    def chateeButtonPress(button):
        frame.header = urwid.AttrWrap(urwid.Text(
                [u"Pressed: ", button.get_label()]), 'header')
        currName = button.get_label()
        #chatHist = chatHistParse(["lol", "LOL"]) #make call here to get history
        #chatObj.original_widget.set_text(chatHist)


    def friendButtonPress(button):
        frame.header = urwid.AttrWrap(urwid.Text(
                [u"Pressed: ", button.get_label()]), 'header')
        for x in chateeButtons.contents:
            if x.original_widget.original_widget.get_label() == button.get_label():
                return
        chateeButtons.contents.append((urwid.Padding(urwid.AttrWrap(urwid.Button(button.get_label(), chateeButtonPress), 'buttn', 'buttnf'), left=5, right =10), ('weight', 1)))
        #xmpp.add

    friendButtons.contents.extend(
            [(urwid.Padding(urwid.AttrWrap(urwid.Button(txt, friendButtonPress),
                            'buttn', 'buttnf'),
            left=5, right =10), ('weight', 1))
             for txt in friendsList])

    urwid.register_signal(self, ['new chats'])
    urwid.connect_signal(obj, 'new chats', redraw_chat_text)

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

def setup(xmpp):
    urwid.web_display.set_preferences("UI")
    if urwid.web_display.handle_short_request():
        return
    mainUI(friends, chatees, chatHistParse(chatHist), xmpp)

if '__main__' == __name__ or urwid.web_display.is_web_request():
    setup(xmpp)
