from client import ChatroomClient
from threading import Thread
import unittest
import chat__POA

class TestChatroomClient(unittest.TestCase):
    class ChatroomListener(chat__POA.Listener):
        def __init__(self):
            self.message = None

        def receive(self, msg):
            self.messages = msg
            #self.chatroom.shutdown((self.listener_id,))


    def test_register(self):
        chatroom = ChatroomClient(['-ORBInitRef', 'NameService=corbaloc::127.0.0.1:2809/NameService'])
        listener = TestChatroomClient.ChatroomListener()
        id = chatroom.register(listener, "test")

        def send_thread(chatroom, id):
            chatroom.send(id, 'msg')
            chatroom.shutdown((id,))

        Thread(target=send_thread, args=(chatroom, id,)).start()
        chatroom.run()

        self.assertIn('[test] msg', listener.messages)


if __name__ == "__main__":
    unittest.main()
