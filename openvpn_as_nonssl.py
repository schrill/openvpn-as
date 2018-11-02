#!/usr/bin/env python3
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from os import urandom
from base64 import b64encode,b64decode
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
    def do_POST(self):
        RequestHandler.host = self.headers["host"]
        RequestHandler.address = self.headers["x-forwarded-for"]
        RequestHandler.auth = self.headers["authorization"]
        SimpleXMLRPCRequestHandler.do_POST(self)

server = SimpleXMLRPCServer(("localhost", 15000),
                            requestHandler=RequestHandler)

def GetSession():
    random_bytes = urandom(16)
    token = b64encode(random_bytes).decode('utf-8')
    GetSession = {'status': 0, 'session_id': token}
    address = RequestHandler.address
    r.setex (address,token,9)
    return GetSession
server.register_function(GetSession)

def EnumConfigTypes():
    address = RequestHandler.address
    auth = b64decode(RequestHandler.auth.split(" ")[-1]).decode('utf-8').split(":")[-1]
    check = r.get(address).decode('utf-8')
    if auth == check:
      EnumConfigTypes = {'generic': True, 'userlogin': True, 'userlocked': True, 'autologin': True,
                         'cws_ui_offer': True, 'user_locked': True, 'win': True, 'ios': True,
                         'autologin': True, 'mac': True, 'linux': True, 'android': True, 'server_locked': False}
      return EnumConfigTypes
    return True
server.register_function(EnumConfigTypes)

def GetAutologin():
    address = RequestHandler.address
    auth = b64decode(RequestHandler.auth.split(" ")[-1]).decode('utf-8').split(":")[-1]
    check = r.get(address).decode('utf-8')
    if auth == check:
      host = RequestHandler.host.split(".")[0]
      with open('/etc/openvpn_conf/vpn_'+str(host)+'.ovpn', 'r') as conf:
           GetAutologin=conf.read()
      return GetAutologin
    r.delete(address)
    return True
server.register_function(GetAutologin)

server.serve_forever()

