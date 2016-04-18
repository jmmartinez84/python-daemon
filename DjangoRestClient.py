#!/usr/bin/python

import os
import json
import urllib, urllib2
import base64

class DjangoRestClient:
    my_opener = None
    baseUrl = None
    def __init__(self, url, username, password, debug=False, proxy=None ):
        if url.endswith('/'):
            self.baseUrl = url
        else:
            self.baseUrl = url+'/'
        if proxy != None:
            proxyHandler = urllib2.ProxyHandler({'http': proxy})
        else:
            proxyHandler = None
        if debug:
            debugHandler=urllib2.HTTPHandler(debuglevel=1)
        else:
            debugHandler = None
            
        if debugHandler != None and proxyHandler != None:
            opener = urllib2.build_opener(proxyHandler, debugHandler)
        elif debugHandler != None:
            opener = urllib2.build_opener(debugHandler)
        elif proxyHandler != None:
            opener = urllib2.build_opener(proxyHandler)
        else:
            opener = urllib2.build_opener()
        self.auth_api(opener, username,password)
    def auth_api(self, opener, username, password):
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        opener.addheaders = [("Authorization", "Basic %s" % base64string)]
        self.my_opener = opener
        urllib2.install_opener(opener)
    def add_invitado(self, telefono, nombre, activo):
        invitado_url = u'invitado/'
        url = self.baseUrl + invitado_url
        data = urllib.urlencode({'telefono' : telefono,
                                 'nombre' : nombre,
                                 'activo': True})
        content = urllib2.urlopen(url=url, data=data).read()
        invitado = json.loads(content)
        return invitado

    def get_invitado(self, telefono):
        invitado_url = u'invitado/'
        url = self.baseUrl+invitado_url+str(telefono)+u'/'
        content = urllib2.urlopen(url).read()
        invitado = json.loads(content)
        return invitado

    def exists_invitado(self, telefono):
        invitado_url =u'invitado/'
        query_string = u'?telefono='
        url = self.baseUrl+invitado_url+query_string+str(telefono)
        content = urllib2.urlopen(url).read()
        invitados = json.loads(content)
        invitadosCount = len(invitados)
        return invitadosCount > 0

    def add_image(self, img_from, img_url, img_caption, img_file_name, img_width, img_height):
        image_url = u'add_image/'
        url = self.baseUrl + image_url
        if img_caption is None:
            img_caption = ""
        data = urllib.urlencode({
            'img_from':img_from,
            'img_azure_url':'',
            'img_url':img_url,
            'img_caption':img_caption,
            'img_file_name':img_file_name,
            'img_width':img_width,
            'img_height':img_height
            })
        content = urllib2.urlopen(url=url, data=data).read()
        image = json.loads(content)
        return image
        
    def get_invitados_activos(self):
        invitado_url =u'invitado/?activo=True'
        url = self.baseUrl+invitado_url
        content = urllib2.urlopen(url).read()
        invitados = json.loads(content)
        return invitados

    def update_invitado(self, invitado):
        invitado_url =u'invitado/'
        url = self.baseUrl+invitado_url+str(invitado["telefono"])+"/"
        request = urllib2.Request(url, data=json.dumps(invitado))
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda: 'PUT'
        response = self.my_opener.open(request)
        response.close()
        return response

    def set_invitado_activo_inactivo(self, telefono, activo):
        invitado_exists = self.exists_invitado(telefono)
        if(invitado_exists):
            invitado = self.get_invitado(telefono)
            invitado["activo"]=activo
            new_invitado = self.update_invitado(invitado)
            return new_invitado
    def set_invitado_activo(self, telefono):
        self.set_invitado_activo_inactivo(telefono,True)

    def set_invitado_inactivo(self,telefono):
        self.set_invitado_activo_inactivo(telefono,False)

    def get_mensaje(self, code):
        mensaje_url = u'mensaje/'
        url = self.baseUrl+mensaje_url+urllib.quote_plus(code)+u'/'
        content = urllib2.urlopen(url).read()
        mensaje = json.loads(content)
        return mensaje

    def exists_mensaje(self, code):
        mensaje_url = u'mensaje/'
        query_string = u'?code='
        url = self.baseUrl+mensaje_url+query_string + urllib.quote_plus(code)
        content = urllib2.urlopen(url).read()
        mensajes = json.loads(content)
        mensajesCount = len(mensajes)
        return mensajesCount > 0

    def get_mensajes_activos(self):
        mensaje_url = u'mensaje/?activo=True'
        url = self.baseUrl+mensaje_url
        content = urllib2.urlopen(url).read()
        mensajes = json.loads(content)
        return mensajes

    def update_mensaje(self, mensaje):
        mensaje_url=u'mensaje/'
        url = self.baseUrl+mensaje_url+urllib.quote_plus(mensaje['code'])+u'/'
        request = urllib2.Request(url, data=mensaje)
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda: 'PUT'
        response = self.my_opener.open(url, request)
        response.close()
        return response

    def set_mensaje_activo(self,code):
        msj_exists=mesaje_exists(code)
        if(msj_exists):
            mensaje = self.get_invitado(code)
            mensaje["activo"]=True
            new_mensaje = self.update_mensaje(mensaje)
            return new_mensaje


    def create_mensajeinvitado(self, telefono, code):
        mensajeinvitado_url = u'mensajeinvitado/'
        url = self.baseUrl+mensajeinvitado_url
        data = urllib.urlencode({ "invitado":telefono,
                                  "mensaje":code,
                                  "sent":False})
        content = urllib2.urlopen(url=url, data=data).read()
        mensajeinvitado = json.loads(content)
        return mensajeinvitado

    def get_mensajeinvitado(self,pk):
        mensaje_url = u'mensajeinvitado/'
        url = self.baseUrl+mensaje_url+str(pk)+u'/'
        content = urllib2.urlopen(url).read()
        mensajeinvitado = json.loads(content)
        return mensajeinvitado

    def mensajeinvitado_exists(self, pk):
        mensajeinvitado_url = u'mensajeinvitado/'
        query_string = u'?pk='
        url = self.baseUrl+mensajeinvitado_url+query_string + str(pk)
        content = urllib2.urlopen(url).read()
        mensajesinvitado = json.loads(content)
        mensajesinvitadoCount = len(mensajesinvitado)
        return mensajesinvitadoCount > 0

    def update_mensajeinvitado(self,mensajeinvitado):
        mensajeinvitado_url = u'mensajeinvitado/'
        url = self.baseUrl+mensajeinvitado_url+str(mensajeinvitado['pk'])+u'/'
        request = urllib2.Request(url, data=json.dumps(mensajeinvitado))
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda: 'PUT'
        response = self.my_opener.open(request)
        response.close()
        return response

    def set_mensajeinvitado_as_sent(self, pk):
        msjinvitado_exists=self.mensajeinvitado_exists(pk)
        if(msjinvitado_exists):
            mensajeinvitado = self.get_mensajeinvitado(pk)
            mensajeinvitado["sent"]=True
            new_mensajeinvitado = self.update_mensajeinvitado(mensajeinvitado)
            return new_mensajeinvitado

    def get_mensajeinvitados_by_invitado_not_sent(self, telefono):
          mensajeinvitado_url = u'mensajeinvitado/'
          query_string = u'?invitado=%s&sent=False' % telefono
          url = self.baseUrl+mensajeinvitado_url+query_string
          content = urllib2.urlopen(url).read()
          mensajesinvitado = json.loads(content)
          return mensajesinvitado

    def mensajeinvitado_exists_by_telefono_code(self, telefono, code):
        mensajeinvitado_url = u'mensajeinvitado/'
        query_string = u'?invitado=%s&mensaje=%s' % (telefono, urllib.quote_plus(code))
        url = self.baseUrl+mensajeinvitado_url+query_string
        content = urllib2.urlopen(url).read()
        mensajesinvitado = json.loads(content)
        mensajesinvitadoCount = len(mensajesinvitado)
        return mensajesinvitadoCount > 0

    def create_mensajesinvitado_by_invitado(self,invitado):
        mensajes_activos = self.get_mensajes_activos()
        for mensaje in mensajes_activos:
            telefono = invitado['telefono']
            code = mensaje['code']
            already_exists = self.mensajeinvitado_exists_by_telefono_code(telefono, code)
            if not already_exists:
                self.create_mensajeinvitado(telefono, code)
                
    def get_mensajeinvitados_by_invitado(self, telefono):
          mensajeinvitado_url = u'mensajeinvitado/'
          query_string = u'?invitado=%s' % telefono
          url = self.baseUrl+mensajeinvitado_url+query_string
          content = urllib2.urlopen(url).read()
          mensajesinvitado = json.loads(content.decode('utf-8'))
          return mensajesinvitado
    def create_mensajesactivos_invitado_by_invitado(self,invitado, mensajes_activos):
        telefono = invitado['telefono']
        mensajes_invitado = self.get_mensajeinvitados_by_invitado(telefono)
        for mensaje in mensajes_activos:
            code = mensaje['code']
            exists = False
            for mensajeinvitado in mensajes_invitado:
                if mensajeinvitado['mensaje'] == code:
                    exists = True
                    break
            if not exists:
                self.create_mensajeinvitado(telefono, code)
    def start_invitado(self, telefono, nombre):
        already_exists = self.exists_invitado(telefono)
        if not already_exists:
            invitado = self.add_invitado(telefono,nombre,True)          
        else:
            invitado = self.get_invitado(telefono)
        mensajes_activos = self.get_mensajes_activos()
        self.create_mensajesactivos_invitado_by_invitado(invitado, mensajes_activos)

    def get_mensajes_pendients_by_invitado(self,invitado):
        mensajesinvitado = self.get_mensajeinvitados_by_invitado_not_sent(invitado['telefono'])
        mensajes_result = []
        for mensajeinvitado in mensajesinvitado:
            mensaje = self.get_mensaje(mensajeinvitado['mensaje'])
            mensaje['pk'] = mensajeinvitado['pk']
            mensajes_result.append(mensaje)
        return mensajes_result

    def exists_ubicacion_by_code(self, code):
        ubicacion_url = u'ubicacion/'
        query_string = u'?code=%s' % code.encode('utf-8')
        url = self.baseUrl+mensajeinvitado_url+query_string
        content = urllib2.urlopen(url).read()
        ubicacion = json.loads(content)
        ubicacion_count = len(mensajesinvitado)
        return ubicacion_count > 0
    def get_ubicacion_by_code(self,code):
        invitado_url = u'ubicacion/'
        url = self.baseUrl+invitado_url+code.encode('utf-8')+u'/'
        content = urllib2.urlopen(url).read()
        ubicacion = json.loads(content)
        return ubicacion

    def get_alerts_not_sent(self):
        alert_url = u'alert/'
        url = self.baseUrl+alert_url+u'?sent=False'
        content = urllib2.urlopen(url).read()
        alerts_to_send = json.loads(content)
        return alerts_to_send

    def add_alert(self, text):
        alert_url = u'alert/'
        url = self.baseUrl+alert_url
        data = urllib.urlencode({'alert_text' : text,
                                 'sent': False})
        content = urllib2.urlopen(url=url, data=data).read()
        alert = json.loads(content)
        return alert
    def update_alert(self, alert):
        alert_url = u'alert/'
        url = self.baseUrl+alert_url+str(alert['pk'])+u'/'
        request = urllib2.Request(url, data=json.dumps(alert))
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda: 'PUT'
        response = self.my_opener.open(request)
        response.close()
        return response
        
    def set_alert_as_sent(self, alert):
       alert["sent"]=True
       new_alert = self.update_alert(alert)
       return new_alert

    def add_temperature(self, serial, temperature, humidity):
        temperature_url = u'temperature/'
        url = self.baseUrl+temperature_url
        data = urllib.urlencode({'serial':serial,
                                'temperature':temperature,
                                'humidity':humidity})
        content = urllib2.urlopen(url=url, data=data).read()
        temperature = json.loads(content)
        return temperature

