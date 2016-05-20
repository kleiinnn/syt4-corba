import chat.ChatroomPOA;
import chat.InvalidConnectionIdException;
import chat.Listener;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by markus on 19/05/16.
 */
public class ChatroomImpl extends ChatroomPOA {
    private Map<Integer, Listener> listeners = new HashMap<>();
    private int messageIdCounter = 0;

    @Override
    public int register(Listener client, String listenerName) {
        int messageId = messageIdCounter;
        messageIdCounter++;

        listeners.put(messageId, client);
        return messageId;
    }

    @Override
    public void send(int connectionId, String message) throws InvalidConnectionIdException {
        System.out.println(message);
        for (Map.Entry<Integer, Listener> pair : listeners.entrySet()) {
            pair.getValue().receive(message);
        }
    }

    @Override
    public void unregister(int connectionId) throws InvalidConnectionIdException {
        listeners.remove(connectionId);
    }
}
