package recursion;

public class FactorialGenerator {
	public double nthFactorial(int n) {
		return computeFactorialRecurse(n);
	}
	private double computeFactorialRecurse(int n) {
		assert n >= 0;
		if(n==0)return 1;
		return n*computeFactorialRecurse(n-1);
	}
	public static void main(String args[]) {
		FactorialGenerator x = new FactorialGenerator();
		
		for(int i = 1;i<30;i++) {
			System.out.println(i);
			System.out.println(x.nthFactorial(i));
		}
		System.out.println(Long.MAX_VALUE);
	}

}
