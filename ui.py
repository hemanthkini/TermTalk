import urwid
import urwid.raw_display
import urwid.web_display

def main(friendsList):
    div = urwid.Divider(".")

    for x in xrange(len(friendsList)):
        friendButtonList =

    friendListText = "all my friends here"
    friendListObj = urwid.Padding(urwid.Text(friendListText),
                             left =2, right =2, min_width=20)

    chateesText = u"friend im chatting with"
    chateesListObj = urwid.Padding(urwid.Text(chateesText),
                             left =2, right =2, min_width=20)

    chatText = u"all the chats in the world"
    chatObj =  urwid.Padding(urwid.Text(chatText),
                             left =2, right =2, min_width=20)

    text_edit_padding = ('editcp', u"Type: ")
    editObj = urwid.Edit(text_edit_padding, "")
    textEntry = urwid.Padding(urwid.AttrWrap(editObj,
                             'editbx,', 'editfc'), left = 2,  width = 50)


    allFriendsList = urwid.Columns([friendListObj, chateesListObj])

    listbox_content = [
        div,
        allFriendsList,
        div,
        chatObj]

    listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

    frame = urwid.Frame(urwid.AttrWrap(listbox,'body'), footer=textEntry)

    if urwid.web_display.is_web_request():
        screen = urwid.web_display.Screen()
    else:
        screen = urwid.raw_display.Screen()


    urwid.MainLoop(frame).run()

    pass

friends = ["Jack", "Aashish", "niki", "hemanth"]


def setup():
    urwid.web_display.set_preferences("UI")
    if urwid.web_display.handle_short_request():
        return
    main(friends)

if '__main__' == __name__ or urwid.web_display.is_web_request():
    setup()
