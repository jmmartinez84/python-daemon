#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time, ConfigParser
import logging
import logging.handlers
from datetime import datetime, date
from DjangoRestClient import DjangoRestClient

from daemon import Daemon


class MyDaemon(Daemon):


	@property
	def get_config(self):
		output =  {}
		config = ConfigParser.RawConfigParser()
		config.read('settings.cfg')

		output['Django_url'] = config.get('DjangoREST','url')
		output['Django_user'] = config.get('DjangoREST','user')
		output['Django_pwd'] = config.get('DjangoREST','pwd')

		output['Yowsup_phone'] = config.get('Yowsup','phone')
		output['Yowsup_pwd'] = config.get('Yowsup','pwd')
		return output
	def run(self):
		settings = self.get_config
		drc = DjangoRestClient(settings['Django_url'],settings['Django_user'],settings['Django_pwd'])
		while True:
			alerts = drc.get_alerts_not_sent()
			time.sleep(15)

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
