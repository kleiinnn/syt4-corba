package helloworld;

import org.omg.CosNaming.*;
import org.omg.CORBA.*;
import org.omg.CORBA.Object;

/**
 * @author Hagen Aad Fock <hagen.fock@gmail.com>
 * @version 13.03.2015
 * 
 * Ruft die Echo Methode des C++ Servers auf und gibt einen String auf der Konsole aus.
 * Sollte ein Fehler aufgetreten sein, so wird eine Exception geworfen und eine Fehlermeldung zusammen mit dem Stracktrace auf der Konsole ausgegeben.
 */
public class Client {
	public static void main(String[] args)  {
		Echo echo;
		try {
			
			/* Erstellen und intialisieren des ORB */
			ORB orb = ORB.init(args, null);
			
			/* Erhalten des RootContext des angegebenen Namingservices */
			Object o = orb.resolve_initial_references("NameService");
			
			/* Verwenden von NamingContextExt */
			NamingContextExt rootContext = NamingContextExtHelper.narrow(o);
			
			/* Angeben des Pfades zum Echo Objekt */
			NameComponent[] name = new NameComponent[2];
			name[0] = new NameComponent("test","my_context");
			name[1] = new NameComponent("Echo", "Object");
			
			/* Aufloesen der Objektreferenzen  */
			echo = EchoHelper.narrow(rootContext.resolve(name));

			System.out.println("Der Server sagt: " + echo.echoString("Hallo Welt!"));

		}	catch (Exception e)	{
			System.err.println("Es ist ein Fehler aufgetreten: " + e.getMessage());
			e.printStackTrace();
		}
	}
}
