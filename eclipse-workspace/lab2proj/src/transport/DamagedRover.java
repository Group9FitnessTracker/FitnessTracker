package transport;

public class DamagedRover extends MarsRover{
	private final static int MAX_TRAVEL_METERS_BEFORE_EMPTY_BATTERY = 10000;
	private final static int METERS_FROM_START_TO_CLIFF = 1000;
	private final static int N_SIMULATIONS = 500;
	private double position;
	private double metersTraveled;
	private boolean fell;
	
	public void simulateStormDamageTravel() {
		position = metersTraveled = 0;
		fell = false;
		while(metersTraveled<MAX_TRAVEL_METERS_BEFORE_EMPTY_BATTERY) {
			double distanceNextTurn = (int)(1+4*Math.random());
			
			boolean forwardNotBack = (Math.random()>0.5);
			if(forwardNotBack) {
				position+=distanceNextTurn;
			}
			else {
				position-=distanceNextTurn;
			}
			metersTraveled = metersTraveled + distanceNextTurn;
			
			if((position>1000) || (position<-1000)) {
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
		DamagedRover x = new DamagedRover();
		int a = N_SIMULATIONS;
		int count = 0;
		while(a>0) {
			
		
		x.simulateStormDamageTravel();
		if(x.getFell()) {
			System.out.println("Fell");
			System.out.println(x.getMetersTraveled());
			count++;
		}
		else {
			System.out.println("No more Power");
		}
		a--;
		}
		System.out.println("Number of times rover falls off the cliff:"+count);
		
	}
	
}