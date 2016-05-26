#!/usr/bin/env python
import sys
import os
from threading import Thread

# Import the CORBA module
from omniORB import CORBA

# Import the stubs for the CosNaming and Example modules
import CosNaming
import chat__POA, chat


class ChatroomClient:
    def __init__(self, orb_args):
        """
        Create a new Chatroom client instance
        Connects to the ORB and retrieves the Chatroom remote object.

        :param orb_args: ORB connection arguments
        """
        # Initialise the ORB
        self.orb = CORBA.ORB_init(orb_args)

        # Obtain a reference to the root naming context
        obj = self.orb.resolve_initial_references("NameService")
        rootContext = obj._narrow(CosNaming.NamingContext)

        self.poa = self.orb.resolve_initial_references("RootPOA")

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

        # Narrow the object
        self.chatroom = obj._narrow(chat.Chatroom)
        if self.chatroom is None:
            print "Object reference is not an chat.Chatroom"
            sys.exit(1)

    def register(self, listener, listener_name):
        """
        Register a listener to the chatroom.

        :param listener: listener that should be registered
        :param listener_name: client listener name; this will be prepended to every message by the server
        :return: listener id
        """
        # get a remote object reference to the listener
        listener_ref = listener._this()
        # register the listener
        return self.chatroom.register(listener_ref, listener_name)

    def send(self, listener_id, msg):
        """
        Send a message to the chatroom.

        :param listener_id: listener id
        :param msg: message to send
        """
        self.chatroom.send(listener_id, msg)

    def run(self):
        """
        Run the ORB thread
        """
        poa_manager = self.poa._get_the_POAManager()
        poa_manager.activate()
        self.orb.run()

    def shutdown(self, listener_ids):
        """
        Unregister the listener and shutdown the ORB thread.

        :param listener_ids: list of listener id's which be unregistered
        """
        for id in listener_ids:
            self.chatroom.unregister(id)
        self.orb.shutdown(True)


if __name__ == '__main__':
    # listener implementation
    class ChatroomListener(chat__POA.Listener):
        def receive(self, msg):
            print(msg)


    # sender
    def send_thread(chatroom, id):
        while(1):
            msg = raw_input("> ")
            chatroom.send(id, msg)

    chatroom = ChatroomClient(sys.argv[2:])
    listener = ChatroomListener()
    id = chatroom.register(listener, sys.argv[1])

    Thread(target=send_thread, args=(chatroom, id,)).start()

    try:
        chatroom.run()
    except KeyboardInterrupt:
        # unregister the listener and close down the program
        chatroom.shutdown((id,))
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
