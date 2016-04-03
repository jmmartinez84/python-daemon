#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, sys
import logging.handlers
from datetime import datetime, date
from DjangoRestClient import DjangoRestClient

from layer import HomeLayer
from settings import settings
from yowsup.layers                             import YowParallelLayer
from yowsup.layers.auth                        import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.stacks import YowStack
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup.layers.axolotl                     import YowAxolotlLayer
from yowsup.env.env                            import YowsupEnv

from daemon import Daemon


class YowsupDaemon(Daemon):

    def run(self):
		credentials = settings.get('Yowsup')
        phone = credentials['phone']
        password = credentials['pwd']
        CREDENTIALS = (phone, password) # replace with your phone and password
        logging.basicConfig(level = logging.DEBUG)
        layers = (
        HomeLayer,
        YowParallelLayer([YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer]),YowAxolotlLayer
        ) + YOWSUP_CORE_LAYERS

        stack = YowStack(layers)
        stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)         #setting credentials
        stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])    #whatsapp server address
        stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
        stack.setProp(YowCoderLayer.PROP_RESOURCE, YowsupEnv.getCurrent().getResource())          #info about us as WhatsApp client

        stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal
        stack.loop() #this is the program mainloop

    if __name__ == "__main__":
	daemon = YowsupDaemon('/tmp/yowsup-daemon.pid')
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
