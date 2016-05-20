import chat.ChatroomPOA;
import chat.InvalidConnectionIdException;
import chat.Listener;

import java.util.HashMap;
import java.util.Map;

/**
 * Implementation of Chatroom.
 * Class serves a simple chatroom server client can listen and send messages to.
 */
public class ChatroomImpl extends ChatroomPOA {
    private Map<Integer, Listener> listeners = new HashMap<>();
    private Map<Integer, String> listenerNames = new HashMap<>();
    private int messageIdCounter = 0;

    /**
     * Register a listener to this chatroom.
     * @param client Listener instance which should be supplied with messages
     * @param listenerName Name of the listener; this will be supplied we the message
     * @return connection id
     */
    @Override
    public int register(Listener client, String listenerName) {
        int messageId = messageIdCounter;
        messageIdCounter++;

        listeners.put(messageId, client);
        listenerNames.put(messageId, listenerName);
        return messageId;
    }

    /**
     * Send a message.
     * @param connectionId Client's connection id
     * @param message message string
     * @throws InvalidConnectionIdException
     */
    @Override
    public void send(int connectionId, String message) throws InvalidConnectionIdException {
        if(!listeners.containsKey(connectionId))
            throw new InvalidConnectionIdException(connectionId);

        for (Map.Entry<Integer, Listener> pair : listeners.entrySet()) {
            pair.getValue().receive("[" + listenerNames.get(connectionId) + "] " + message);
        }
    }

    /**
     * Unregister a listener.
     * @param connectionId Connection id of the listener
     * @throws InvalidConnectionIdException
     */
    @Override
    public void unregister(int connectionId) throws InvalidConnectionIdException {
        if(!listeners.containsKey(connectionId))
            throw new InvalidConnectionIdException(connectionId);

        listeners.remove(connectionId);
    }
}
