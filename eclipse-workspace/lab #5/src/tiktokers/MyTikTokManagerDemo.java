package tiktokers;

import javax.swing.JFileChooser;

public class MyTikTokManagerDemo
{
   public static void main(String[] args)
   {
      String filename = null;
      InOut in;
      if (args.length > 0) 
      {
         filename = args[0];
         in = new ConsoleInOut();
      }
      else
      {
         JFileChooser chooser = new JFileChooser();
         if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION)
            filename = chooser.getSelectedFile().getPath();
         in = new WindowInOut();
      }
      if (filename == null) return;
      MyTikTokManager myTiktokers = new ArrayListMyTikTokManager();
      myTiktokers.load(filename);
      processCommands(in, myTiktokers);
   }

   private static void processCommands(InOut in, MyTikTokManager myTiktokers)
   {
      String commands = "1: Add/Change TikToker\n" 
         + "2: Look Up TikToker\n"
         + "3: Remove TikToker\n"
         + "4: Save My TikTokers\n"
         + "5: Exit\n"
	 + "Enter Command: ";
      boolean done = false;
      while (!done)
      {
         String choice = in.nextLine(commands);
         if (choice.equals("1")) addChangeEntry(in, myTiktokers);
         else if (choice.equals("2")) lookupEntry(in, myTiktokers);
         else if (choice.equals("3")) removeEntry(in, myTiktokers);
         else if (choice.equals("4")) myTiktokers.save();
         else if (choice.equals("5")) done = true;
         else System.out.println("Not a valid option:" + choice);
      }
   }

   private static void addChangeEntry(InOut in, MyTikTokManager myTiktokers)
   {
      String username = in.nextLine("Enter username: ");
      String key = in.nextLine("Enter key: ");
      String value = in.nextLine("Enter value: ");
      String oldValue = myTiktokers.put(username, key, value);
      if (oldValue == null)
         in.message("TikToker added");
      else
         in.message("TikToker updated");
   }

   private static void lookupEntry(InOut in, MyTikTokManager myTiktokers)
   {
      String username = in.nextLine("Enter username: ");
      String key = in.nextLine("Enter key: ");
      String value = myTiktokers.get(username, key);
      if (value == null)
         in.message("No TikToker");
      else
         in.message("Value: " + value);
   }

   private static void removeEntry(InOut in, MyTikTokManager myTiktokers)
   {   
   }
}
