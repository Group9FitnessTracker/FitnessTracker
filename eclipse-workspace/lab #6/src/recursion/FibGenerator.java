package recursion;


import java.util.logging.Level;
import java.util.logging.Logger;

public class FibGenerator {
	public int nthFib(int n) {
		return computeFibRecurse(n);
	}
	private int computeFibRecurse(int n) {
		if(n == 1 || n==2) {
			return 1;
		}
		return computeFibRecurse(n-2) + computeFibRecurse(n-1);
	}
	public static void main (String args[]) {
		System.out.println("STARTING");
		FibGenerator x = new FibGenerator();
		for(int i = 1;i<20;i++) {
			System.out.println(i);
			System.out.println(x.nthFib(i));
			Logger.getGlobal().setLevel(Level.ALL);
			
		}
		
	}

}
