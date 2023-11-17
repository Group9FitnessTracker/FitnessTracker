package stacklab;

import java.io.*;
import java.util.Stack;


public class Lister {
	
	private File file;
	private boolean showHidden;
	
	public Lister(File f, boolean showH) {
		file = f;
		showHidden = showH;
	}
	
	public void list() {
		listFilesRecurse(file);
		//listFilesStack(file);
	}
    
	private void listFilesRecurse(File f) {
		if(f.isDirectory()) {
			File[] files = f.listFiles();
			for(File file:files) {
				listFilesRecurse(file);	
			}
		}
		else {
			if(showHidden || !f.isHidden()) {
				System.out.println(f.getName());
			}
		}
			
	}
    
    //fill this in
    private void listFilesStack(File f) {
        
    }
	
	public static void main(String[] args) {
        //replace with a directory of your own
        String directory = "/Users/agc/eclipse-workspace/homework5";
		File dir = new File(directory);
		Lister l = new Lister(dir,true);
		l.list();
	}

}
