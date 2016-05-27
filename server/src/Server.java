import chat.Chatroom;
import chat.ChatroomHelper;
import org.omg.CORBA.ORB;
import org.omg.CosNaming.NameComponent;
import org.omg.CosNaming.NamingContext;
import org.omg.CosNaming.NamingContextHelper;
import org.omg.PortableServer.POA;
import org.omg.PortableServer.POAHelper;

/**
 * Simple {@link Chatroom} server implementation.
 */
public class Server {
    public static void main(String[] args)  {
        try {
            // Initialize the ORB
            ORB orb = ORB.init(args, null);
            System.out.println("Initialized ORB");

            //Instantiate Servant and create reference
            POA rootPOA = POAHelper.narrow(orb.resolve_initial_references("RootPOA"));
            ChatroomImpl chImpl = new ChatroomImpl();
            rootPOA.activate_object(chImpl);
            Chatroom chRef = ChatroomHelper.narrow(rootPOA.servant_to_reference(chImpl));

            //Bind reference with NameService
            NamingContext namingContext = NamingContextHelper.narrow(orb.resolve_initial_references("NameService"));
            System.out.println("Resolved NameService");
            NameComponent[] nc = { new NameComponent("Chatroom", "") };
            namingContext.rebind(nc, chRef);

            //Activate rootpoa
            rootPOA.the_POAManager().activate();

            //Start readthread and wait for incoming requests
            System.out.println("Server ready and running ....");

            orb.run();

        }	catch (Exception e)	{
            System.err.println("Es ist ein Fehler aufgetreten: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
