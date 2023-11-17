package transport;

public class Vehicle {
	private int nWheels;
	private double xPosition;
	private double yPosition;
	public Vehicle(int n) {
		nWheels = n;
		System.out.println("Vehicle constructor");
	}
	public Vehicle() {}
	
	public static void main(String[] args) {
		Vehicle v = new Vehicle();
	}
	public String toString() {
		return super.toString();
	}
	public double getXPosition() {
		return xPosition;
	}
	public double getYPosition() {
		return yPosition;
	}
	public void setXPosition(double a) {
		xPosition = a;
	}
	public void setYPosition(double b) {
		yPosition = b;
	}
	public void setPosition(double xPosition, double yPosition) {
		this.xPosition = xPosition;
		this.yPosition = yPosition;
	}
	public void changePositionBy(double xDelta, double yDelta) {
		xPosition += xDelta;
		yPosition += yDelta;
	}
	

}
