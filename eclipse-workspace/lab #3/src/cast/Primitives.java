package cast;

public class Primitives {
	public static void dumpMaxValues() {
		
		long l = Long.MAX_VALUE;
		int i = Integer.MAX_VALUE;
		short s = Short.MAX_VALUE;
		float f = Float.MAX_VALUE;
		double d = Double.MAX_VALUE;
		byte b = Byte.MAX_VALUE;
		System.out.println(b); //byte
		System.out.println(l);
		System.out.println(i);
		System.out.println(s);
		System.out.println(f);
		System.out.println(d);
		
	}
	public static void main(String []args) {
		dumpMaxValues();
	}
	

}
