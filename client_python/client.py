#!/usr/bin/env python

import sys
import os
from threading import Thread

# Import the CORBA module
from omniORB import CORBA

# Import the stubs for the CosNaming and Example modules
import CosNaming
import chat__POA, chat

# listener implementation
class Listener_I(chat__POA.Listener):
    def receive(self, msg):
        print(msg)


# sender thread
def send_thread(chatroom, id):
    while(1):
        msg = raw_input("> ")
        chatroom.send(id, msg)

# Initialise the ORB
orb = CORBA.ORB_init(sys.argv[2:])

# Obtain a reference to the root naming context
obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)

poa = orb.resolve_initial_references("RootPOA")

if rootContext is None:
    print "Failed to narrow the root naming context"
    sys.exit(1)

# Resolve the name "test.my_context/ExampleEcho.Object"
name = [CosNaming.NameComponent("Chatroom", "")]

try:
    obj = rootContext.resolve(name)

except CosNaming.NamingContext.NotFound, ex:
    print "Name not found"
    sys.exit(1)

# Narrow the object to an Example::Echo
chatroom = obj._narrow(chat.Chatroom)
if chatroom is None:
    print "Object reference is not an Example::Echo"
    sys.exit(1)

# create and aquire an reference of listener
listener = Listener_I()
listenerRef = listener._this()

# register the listener
id = chatroom.register(listenerRef, sys.argv[1])

Thread(target=send_thread, args=(chatroom, id,)).start()

# run t=flg
poaManager = poa._get_the_POAManager()
poaManager.activate()

try:
    orb.run()
except KeyboardInterrupt:
    # unregister the listener and close down the program
    chatroom.unregister(id)
    orb.shutdown(True)
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
