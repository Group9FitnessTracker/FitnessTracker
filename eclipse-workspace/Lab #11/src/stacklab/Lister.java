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
	public void list1() {
		listFilesStack(file);
	}
    
	private void listFilesRecurse(File f) {
		if(f.isDirectory()) { //check if path name is directory
			File[] files = f.listFiles(); //create a list of type File and store each file in directory
			for(File file:files) { //for each file call listFilesRecurse
				listFilesRecurse(file);	
			}
		}
		else {
			if(showHidden || !f.isHidden()) { //print each file name
				System.out.println(f.getName());
			}
		}
			
	}
    
    //fill this in
    private void listFilesStack(File f) {
    	Stack<File> stack = new Stack<>();
    	stack.push(f);
        while(!stack.isEmpty()) {
        	File curr = stack.pop();
        	if(curr.isDirectory()) {
        		File[] files = curr.listFiles();
        		if(files!=null) {
        			for(File file:files) {
        				stack.push(file);
        			}
        		}
        	}
        	else {
        		if(showHidden || !curr.isHidden()) {
        			System.out.println(curr.getName());
        		}
        	}
        }
    }
	
	public static void main(String[] args) {
        //replace with a directory of your own
        String directory = "/Users/agc/eclipse-workspace/homework5";
		File dir = new File(directory);
		Lister l = new Lister(dir,true);
		l.list();
		l.list1();
	}

}
