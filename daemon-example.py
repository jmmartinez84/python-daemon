#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time
import logging
import logging.handlers
from datetime import datetime, date
from DjangoRestClient import DjangoRestClient

from daemon import Daemon


class MyDaemon(Daemon):


	def run(self):
		while True:
			print datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')
			time.sleep(5)

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
