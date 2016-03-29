#!/usr/bin/env python

import sys, time
import logging
import logging.handlers

from daemon import Daemon


class MyDaemon(Daemon):
	my_logger = logging.getLogger('MyLogger')
	my_logger.setLevel(logging.DEBUG)
	handler = logging.handlers.SysLogHandler(address = '/var/log')
	my_logger.addHandler(handler)
	my_logger.debug('this is debug')
	my_logger.critical('this is critical')

	def run(self):
		while True:
			time.sleep(1)

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon-example.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
