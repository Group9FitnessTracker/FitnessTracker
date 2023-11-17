package tiktokers;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.NoSuchElementException;
import java.util.Scanner;

/**
 * An implementation of the AddressBook interface that uses an array list to
 * store the data.
 */
public class ArrayListMyTikTokManager implements MyTikTokManager
{

   private ArrayList<Item> items = new ArrayList<Item>();
   private String source;
   private boolean modified;

   public void load(String sourceName)
   {
      source = sourceName;
      try
      {
         Scanner in = new Scanner(new File(source));
         items = new ArrayList<Item>();
         while (in.hasNextLine())
         {
            items.add(new Item(in.nextLine(), in.nextLine(), in.nextLine()));
         }
      }
      catch (IOException ex)
      {
         ex.printStackTrace();
         source = null;
         items = new ArrayList<Item>();
      }
   }

   public String get(String username, String key)
   {
      for (Item it : items)
      {
         if (username.equals(it.getUserName()) && key.equals(it.getKey()))
         {
            return it.getValue();
         }
      }
      return null;
   }

   public String put(String username, String key, String value)
   {
      modified = true;
      for (Item it : items)
      {
         if (username.equals(it.getUserName()) && key.equals(it.getKey()))
         {
            String oldValue = it.getValue();
            it.setValue(value);
            return oldValue;
         }
      }
      items.add(new Item(username, key, value));
      return null;
   }

   public void save()
   {
      if (!modified)
      {
         return;
      }
      try
      {
         PrintWriter out = new PrintWriter(source);
         for (Item it : items)
         {
            out.println(it.getUserName());
            out.println(it.getKey());
            out.println(it.getValue());
         }
         out.close();
         modified = false;
      }
      catch (Exception ex)
      {
         ex.printStackTrace();
      }
   }

   @Override
   public String remove(String username, String key)
   {
	   //iterate through the array list and remove user name and key... Array list tiktok manager 
	   
	   for(Iterator<Item> it = items.iterator();it.hasNext();) {
		   Item one = it.next();
		   
		   if(one.getUserName().equals(username) && one.getKey().equals(key)) {
			   it.remove();
			   
			   return one.getValue();
		   }
		   
	   }
	   
	  
       return null;
       
   }  
}
