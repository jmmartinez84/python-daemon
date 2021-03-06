#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading, time
from settings import settings
from DjangoRestClient import DjangoRestClient
from yowsup.common.tools import Jid
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from yowsup.layers.protocol_iq.protocolentities        import *



class HomeLayer(YowInterfaceLayer):
    def __init__(self):
        super(HomeLayer, self).__init__()
        self.threads = []
        self.ackQueue = []
        self.alertQueue = []
        self.sentDict = {} 
        self.lock = threading.Condition()
        self.credentials = settings.get('DjangoREST')
        self.config = settings.get('YowsupHome')
        self.worker_sleep_time = int(settings.get('YowsupHome')['messagessleep'])*2
        self.messages_sleep_time = int(settings.get('YowsupHome')['messagessleep'])
        self.admin_phone = settings.get('YowsupHome')['adminphone']
        t1 = threading.Thread(target=self.GetAlerts, name='AlertsIn')
        self.threads.append(t1)
        t2 = threading.Thread(target=self.SetAlerts, name='AlertsOut')
        self.threads.append(t2)
        t1.start()
        t2.start()

    def GetAlerts(self):
        """thread worker function"""
        name = threading.current_thread().getName()
        drc = DjangoRestClient(self.credentials['url'], self.credentials['user'], self.credentials['pwd'])
        while True:
            alerts = drc.get_alerts_not_sent()
            self.lock.acquire()
            for alert in alerts:
                 self.alertQueue.append(alert)
            self.lock.release()
            time.sleep(self.worker_sleep_time)
    def SetAlerts(self):
        drc = DjangoRestClient(self.credentials['url'], self.credentials['user'], self.credentials['pwd'])
        while True:
            alerts = drc.get_alerts_not_sent()
            self.lock.acquire()
            for alert in self.sentDict:
                if(alert['sent'] == True):
                    drc.update_alert(alert)
            self.lock.release()
            time.sleep(self.worker_sleep_time)
    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lock.acquire()
        #if the id match the id in ackQueue, then pop the id of the message out
        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))
            alert = self.sentDict[entity.getId()]
            alert['sent'] = True
        self.lock.release()
        
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))


    @ProtocolEntityCallback("iq")
    def onIq(self, entity):
        self.lock.acquire()
        for alert in self.alertQueue:
            message = alert['alert_text']
            messageEntity = TextMessageProtocolEntity(message, to = Jid.normalize(self.admin_phone))
            ack_id = messageEntity.getId()
            self.ackQueue.append(ack_id)
            self.sentQueue[ack_id] = alert;
            print(alert)
        self.lock.release()

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        # just print info
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))