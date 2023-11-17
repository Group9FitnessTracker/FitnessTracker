package transport;

public class Vehicle {
	private int nWheels;
	public Vehicle(int n) {
		nWheels = n;
		System.out.println("Vehicle constructor");
	}
	public Vehicle() {}
	
	public static void main(String[] args) {
		Vehicle v = new Vehicle();
	}
	

}
