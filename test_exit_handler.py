import signal, time
def set_exit_handler(func):
	print "set_exit_handler"
	signal.signal(signal.SIGTERM, func)
if __name__ == "__main__":
    def on_exit(sig, func=None):
        print "exit handler triggered"
        time.sleep(5)
    set_exit_handler(on_exit)
    print "Press  to quit"
    raw_input()
    print "quit!"