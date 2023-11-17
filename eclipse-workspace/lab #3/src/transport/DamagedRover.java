package transport;

public class DamagedRover extends MarsRover{
	private final static int MAX_TRAVEL_METERS_BEFORE_EMPTY_BATTERY = 10000;
	private final static int METERS_FROM_START_TO_CLIFF = 1000;
	private final static int N_SIMULATIONS = 500;
//	private double position; old instance variable
	private double xPosition;
	private double yPosition;
	private double metersTraveled;
	private boolean fell;
	
	private void move(double distance, boolean forward) {
		if(forward)changePositionBy(distance,0);
		else changePositionBy(distance,0);
	}
	
	public void simulateStormDamageTravel() {
		setPosition(0.0,0.0);
		metersTraveled = 0;
		fell = false;
		while(metersTraveled<MAX_TRAVEL_METERS_BEFORE_EMPTY_BATTERY) {
			double distanceNextTurn = (int)(1+4*Math.random());
			
			boolean forwardNotBack = (Math.random()>0.5);
			if(forwardNotBack) {
				changePositionBy(distanceNextTurn,0);
			}
			else {
				changePositionBy(-distanceNextTurn,0);
			}
			metersTraveled = metersTraveled + distanceNextTurn;
			
			if((getXPosition()>1000) || (getXPosition()<(-1000))) {
				fell = true;
				break;
			}
			
		}
	}
	
	public double getMetersTraveled() {
		return metersTraveled;
	}
	
	public boolean getFell() {
		return fell;
	}
	
	public static void main(String []args) {
		System.out.println("STARTING");
		
		DamagedRover rover = new DamagedRover();
		int nFalls = 0;
		for (int i=0; i<N_SIMULATIONS; i++)
		{
		rover.simulateStormDamageTravel();
		if (rover.getFell())
		nFalls++;
		}
		System.out.println(nFalls + " falls in " + N_SIMULATIONS);
		System.out.println("DONE");
	}
	
}