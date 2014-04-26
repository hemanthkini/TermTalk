import sleekxmpp
import urwid

class uiThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):


class xmppThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        xmpplock.acquire()

        xmpplock.release()

# Create new threads
thread1 = uiThread(1, "UI")
thread2 = xmppThread(2, "xmpp")

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
