import chat.Chatroom;
import chat.ChatroomHelper;
import chat.InvalidConnectionIdException;
import chat.Listener;
import chat.ListenerHelper;
import chat.ListenerPOA;
import org.omg.CORBA.ORB;
import org.omg.CosNaming.NameComponent;
import org.omg.CosNaming.NamingContextExt;
import org.omg.CosNaming.NamingContextExtHelper;
import org.omg.PortableServer.POA;
import org.omg.PortableServer.POAHelper;

/**
 * Created by markus on 19/05/16.
 */
public class Client {
    public static void main(String[] args) {
        try {
            /* Erstellen und intialisieren des ORB */
            ORB orb = ORB.init(args, null);

            POA rootPOA = POAHelper.narrow(orb.resolve_initial_references("RootPOA"));

			/* Erhalten des RootContext des angegebenen Namingservices */
            Object o = orb.resolve_initial_references("NameService");

			/* Verwenden von NamingContextExt */
            NamingContextExt rootContext = NamingContextExtHelper.narrow((org.omg.CORBA.Object) o);

			/* Angeben des Pfades zum Echo Objekt */
            NameComponent[] name = new NameComponent[1];
            name[0] = new NameComponent("Chatroom", "");

			/* Aufloesen der Objektreferenzen  */
            Chatroom chatroom = ChatroomHelper.narrow(rootContext.resolve(name));

            ListenerImpl listenerImpl = new ListenerImpl();
            rootPOA.activate_object(listenerImpl);
            Listener chRef = ListenerHelper.narrow(rootPOA.servant_to_reference(listenerImpl));
            int id = chatroom.register(chRef, "foo");
            System.out.println("Listener registered with MessageServer");

            new Thread(() -> {
                try {
                    chatroom.send(id, "Foobar!");
                } catch (InvalidConnectionIdException e) {
                    e.printStackTrace();
                }
            }).start();


            rootPOA.the_POAManager().activate();
            System.out.println("Wait for incoming messages");
            orb.run();
            orb.shutdown(false);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    private static class ListenerImpl extends ListenerPOA {

        @Override
        public void receive(String message) {
            System.out.println(message);

        }
    }
}
