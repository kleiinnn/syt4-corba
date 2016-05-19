#!/usr/bin/env python

import sys

# Import the CORBA module
from omniORB import CORBA

# Import the stubs for the CosNaming and Example modules
import CosNaming

import chat__POA, chat

class Listener_I(chat__POA.Listener):
    def receive(self, msg):
        print(msg)

# Initialise the ORB
orb = CORBA.ORB_init(sys.argv)

# Obtain a reference to the root naming context
obj         = orb.resolve_initial_references("NameService")
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

listener = Listener_I()
listenerRef = listener._this()

chatroom.register(listenerRef, "foo")


poaManager = poa._get_the_POAManager()
poaManager.activate()
orb.run()
