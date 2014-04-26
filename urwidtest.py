import urwid

def show_or_exit(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        self.original_widget = urwid.Text(
            u"Nice to meet you, \n %s. \n\n Press Q to exit." %edit.edit_text)

edit = urwid.Edit(u"what is your name")
fill = QuestionBox(edit)
loop = urwid.MainLoop(fill, unhandled_input=show_or_exit)
loop.run()

