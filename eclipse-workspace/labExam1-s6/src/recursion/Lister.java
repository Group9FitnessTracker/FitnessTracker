package recursion;

import java.io.File;

public class Lister {
	private File file;
	private boolean showHidden;
	public Lister(File file, boolean showHidden) { //constructor
		this.file = file;
		this.showHidden = showHidden;
	}
	public void list() { //call to listRecurse
		listRecurse(file,"");
	}
	private void listRecurse(File file, String indent) { //should print the indented file names
		
		System.out.println(indent + file.getName() + ":");
		if(file.isDirectory()) {
			File[] contents = file.listFiles();
			if(contents != null) {
				
				for(File content: contents) {
					if(showHidden || !content.isHidden()) {
						
						listRecurse(content,indent + "   ");
					}
				}
			}
		}
	}
	public static void main(String[] arg) {
		//insert your file
		File directoryToList = new File("\"C:\\Users\\Beaumont\\Downloads\\lab8.singly.linkedlist\"");
		Lister lister = new Lister(directoryToList,true);
		lister.list();
		
	}

}
