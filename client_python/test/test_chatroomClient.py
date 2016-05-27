from client import ChatroomClient
from threading import Thread
import unittest
import chat__POA, chat

class TestChatroomClient(unittest.TestCase):
    class ChatroomListener(chat__POA.Listener):
        def __init__(self):
            self.message = None

        def receive(self, msg):
            self.messages = msg
            #self.chatroom.shutdown((self.listener_id,))


    @classmethod
    def setUpClass(cls):
        TestChatroomClient.chatroom = ChatroomClient(['-ORBInitRef', 'NameService=corbaloc::127.0.0.1:2809/NameService'])

    def test_register(self):
        listener = TestChatroomClient.ChatroomListener()
        id = TestChatroomClient.chatroom.register(listener, "test")

        TestChatroomClient.chatroom.send(id, 'msg')
        TestChatroomClient.chatroom.unregister(id)

        self.assertIn('[test] msg', listener.messages)

    def test_send_invalid_id(self):
        with self.assertRaises(chat.InvalidConnectionIdException):
            TestChatroomClient.chatroom.send(1234, 'msg')

    def test_unregister_invalid_id(self):
        with self.assertRaises(chat.InvalidConnectionIdException):
            TestChatroomClient.chatroom.unregister(1234)


if __name__ == "__main__":
    unittest.main()
