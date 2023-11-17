package tiktokers;

import java.util.Iterator;

/**
   An MyTikTokManager book for looking up information about TikTokers.
*/
public interface MyTikTokManager {

   /** 
       Load the dictionary from a source.
       @param sourceName the name of the source
   */
   void load(String sourceName);

   /** 
       Look up an item.
       @param username the username of the tiktoker to look up
       @param key the name of the item to look up (e.g., Followers)
       @return the item value or null if not found
   */
   String get(String username, String key);

   /** 
       Add or change an item
       @param username the username of the tiktoker to look up
       @param key the name of the item to look up (e.g., Followers)
       @param value the value for the item
       @return the old item value or null if not found
   */
   String put(String username, String key, String value);

   /** 
       Remove an item.
       @param username the username of the tiktoker to look up
       @param key the name of the item to look up (e.g., Followers)
       @return the old item value or null if not found
   */
   String remove(String username, String key);
   
   /**
      Save the address book.
   */
   void save();
}
