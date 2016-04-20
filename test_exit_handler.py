import os, sys
import signal
def set_exit_handler(func):
	signal.signal(signal.SIGTERM, func)
if __name__ == "__main__":
    def on_exit(sig, func=None):
        print "exit handler triggered"
        import time
        time.sleep(5)
    set_exit_handler(on_exit)
    print "Press  to quit"
    raw_input()
    print "quit!"